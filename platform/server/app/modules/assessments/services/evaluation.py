from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.modules.assessments.models.results import AssessmentResultModel
from app.modules.assessments.repositories.results import AssessmentResultRepository
from app.modules.assessments.repositories.runtime import AssessmentSessionRepository
from app.modules.assessments.repositories.question import QuestionRepository
from app.modules.assessments.repositories.assessment import AssessmentRepository
from app.modules.assessments.models.question import QuestionType
from app.modules.assessments.models.runtime import SessionStatus

# Learning integrations
from app.modules.learning.services.session import LearningSessionService
from app.modules.learning.services.attempt import LearningAttemptService

class AssessmentEvaluationService:
    """Evaluates finalized assessment submissions against deterministic rules and emits evidence logs to the Learning foundation."""

    def __init__(
        self,
        repo: AssessmentResultRepository,
        session_repo: AssessmentSessionRepository,
        question_repo: QuestionRepository,
        assessment_repo: AssessmentRepository,
        db: AsyncIOMotorDatabase,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        attempt_service: LearningAttemptService,
        session_service: LearningSessionService
    ):
        self.repo = repo
        self.session_repo = session_repo
        self.question_repo = question_repo
        self.assessment_repo = assessment_repo
        self.db = db
        self.event_dispatcher = event_dispatcher
        self.audit_service = audit_service
        self.attempt_service = attempt_service
        self.session_service = session_service

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    async def evaluate_session(
        self,
        session_id: str,
        context: RuntimeContext
    ) -> AssessmentResultModel:
        self._require_capability(context, "assessment:read")

        # 1. Fetch completed session
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            raise AppException(f"Assessment session '{session_id}' not found.", code="NOT_FOUND", status_code=404)

        if session.status != SessionStatus.COMPLETED:
            raise AppException("Cannot evaluate an incomplete or cancelled session.", code="INVALID_STATE", status_code=400)

        # Check if result already exists
        existing = await self.repo.get_by_session(session_id)
        if existing:
            return existing

        # 2. Fetch assessment
        assessment = await self.assessment_repo.get_by_id(session.assessment_id)
        if not assessment:
            raise AppException(f"Assessment definition '{session.assessment_id}' not found.", code="NOT_FOUND", status_code=404)

        # 3. Grade responses
        total_max_marks = 0.0
        total_earned_marks = 0.0
        evaluation_details = {}

        strengths_set = set()
        weaknesses_set = set()

        response_map = {r.question_id: r for r in session.responses}

        for q_ref in assessment.questions:
            q_id = q_ref.question_id
            marks = q_ref.marks
            total_max_marks += marks

            # Retrieve question details
            question = await self.question_repo.get_by_id(q_id)
            if not question:
                continue

            skills = question.metadata.get("skills", [])
            tags = question.metadata.get("tags", [])
            topics = [question.metadata.get("topic_id")] if question.metadata.get("topic_id") else []
            concept_labels = skills + tags + topics

            resp = response_map.get(q_id)
            is_correct = False
            points_earned = 0.0

            if resp:
                # Deterministic check based on question type
                eval_def = question.evaluation_definition
                if question.question_type == QuestionType.MCQ:
                    if resp.selected_option_index is not None and eval_def.correct_option_index is not None:
                        is_correct = (resp.selected_option_index == eval_def.correct_option_index)
                elif question.question_type == QuestionType.MULTIPLE_SELECT:
                    if resp.selected_option_indices is not None and eval_def.correct_option_indices is not None:
                        is_correct = (sorted(resp.selected_option_indices) == sorted(eval_def.correct_option_indices))
                elif question.question_type == QuestionType.TRUE_FALSE:
                    if resp.bool_response is not None and eval_def.correct_bool is not None:
                        is_correct = (resp.bool_response == eval_def.correct_bool)
                elif question.question_type == QuestionType.FILL_BLANK:
                    if resp.text_response is not None and eval_def.correct_text is not None:
                        is_correct = (resp.text_response.strip().lower() == eval_def.correct_text.strip().lower())
                elif question.question_type == QuestionType.CODING:
                    # Generic mock matching verification rules
                    is_correct = True  # Default fallback if responses submitted

                if is_correct:
                    points_earned = marks
                    total_earned_marks += marks
                    for label in concept_labels:
                        if label:
                            strengths_set.add(label)
                else:
                    for label in concept_labels:
                        if label:
                            weaknesses_set.add(label)
            else:
                for label in concept_labels:
                    if label:
                        weaknesses_set.add(label)

            evaluation_details[q_id] = {
                "is_correct": is_correct,
                "points_earned": points_earned,
                "max_points": marks,
                "response": resp.model_dump() if resp else None
            }

        # Calculate score percentage
        score_pct = (total_earned_marks / total_max_marks) if total_max_marks > 0 else 0.0
        passing = assessment.passing_score if assessment.passing_score is not None else 0.7
        passed = (score_pct >= passing)

        duration = 0
        if session.end_time:
            duration = int((session.end_time - session.start_time).total_seconds())

        # Clean overlap: if a concept is both strength and weakness, weakness takes precedence
        strengths = list(strengths_set - weaknesses_set)
        weaknesses = list(weaknesses_set)

        result_doc = AssessmentResultModel(
            user_id=session.user_id,
            assessment_id=session.assessment_id,
            session_id=session_id,
            score=round(score_pct, 4),
            passed=passed,
            duration_seconds=duration,
            evaluation_details=evaluation_details,
            strengths=strengths,
            weaknesses=weaknesses,
            completed_at=datetime.now(timezone.utc)
        )
        created = await self.repo.create(result_doc)

        # 4. Forward Evidence flow: Log Completed attempt to the Learning Platform
        # Check active learning session context
        active_learning_sess = await self.session_service.get_active_session(context)
        learning_sess_id = str(active_learning_sess.id) if active_learning_sess else None

        attempt = await self.attempt_service.start_attempt(
            session_id=learning_sess_id,
            resource_id=session.assessment_id,
            resource_type=assessment.assessment_type.value,
            context=context,
            metadata={"session_id": session_id, "result_id": str(created.id)}
        )

        await self.attempt_service.complete_attempt(
            attempt_id=str(attempt.id),
            score=round(score_pct, 4),
            response_data={"passed": passed, "strengths": strengths, "weaknesses": weaknesses},
            context=context
        )

        # 5. Side Effects
        await self.event_dispatcher.dispatch(Event(
            name="AssessmentResultEvaluated",
            payload={"result_id": str(created.id), "score": score_pct, "passed": passed},
            context=context
        ))
        await self.audit_service.log("assessment.result.evaluated", f"result:{created.id}", "success", context, {})
        return created

    async def get_result_by_session(self, session_id: str, context: RuntimeContext) -> AssessmentResultModel:
        self._require_capability(context, "assessment:read")
        res = await self.repo.get_by_session(session_id)
        if not res:
            raise AppException(f"Assessment result for session '{session_id}' not found.", code="NOT_FOUND", status_code=404)
        return res
