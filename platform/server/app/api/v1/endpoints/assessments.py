import logging
from typing import List
from app.core.routing import APIRouter
from fastapi import Depends, HTTPException, status
from app.modules.users.models.user import UserModel
from app.modules.assessments.models.quiz_submission import QuizSubmissionModel, AnswerDetail
from app.modules.assessments.schemas.quiz_submission import QuizSubmitRequest, QuizSubmissionResponse
from app.modules.learning.schemas.progress import TopicProgressLog
from app.modules.knowledge.services.curriculum import curriculum_service
from app.modules.learning.services.progress import ProgressService
from app.api.v1.dependencies import (
    get_quiz_submission_repository,
    get_progress_repository,
    get_current_user
)
from app.modules.assessments.repositories.quiz_submission import QuizSubmissionRepository
from app.modules.learning.repositories.progress import ProgressRepository

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/{subject_id}/{topic_id}/submit", response_model=QuizSubmissionResponse, tags=["Assessments"])
async def submit_quiz(
    subject_id: str,
    topic_id: str,
    payload: QuizSubmitRequest,
    current_user: UserModel = Depends(get_current_user),
    quiz_repo: QuizSubmissionRepository = Depends(get_quiz_submission_repository),
    progress_repo: ProgressRepository = Depends(get_progress_repository)
):
    """Submit student answers for a topic quiz, evaluate correctness, and log progress"""
    # 1. Fetch original quiz questions from curriculum cache
    quiz_data = curriculum_service.get_topic_asset(subject_id, "quiz", topic_id)
    if not quiz_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz for topic '{topic_id}' not found."
        )

    # 2. Grade the answers
    correct_count = 0
    total_questions = len(quiz_data.get("questions", []))
    answer_details: List[AnswerDetail] = []

    for user_ans in payload.answers:
        # Match question keys
        db_question = next(
            (q for q in quiz_data["questions"] if q["question_id"] == user_ans.question_id),
            None
        )
        if not db_question:
            continue

        is_correct = False
        try:
            # Check string equivalence against option array index
            selected_text = db_question["options"][user_ans.selected_option]
            if selected_text == db_question["correct_answer"]:
                is_correct = True
                correct_count += 1
        except IndexError:
            logger.warning(f"Submitted invalid option index {user_ans.selected_option} for question '{user_ans.question_id}'")
            pass

        answer_details.append(
            AnswerDetail(
                question_id=user_ans.question_id,
                selected_option=user_ans.selected_option,
                is_correct=is_correct
            )
        )

    # 3. Log detailed submission record
    submission = QuizSubmissionModel(
        user_id=current_user.id,
        topic_id=topic_id,
        score=correct_count,
        total_questions=total_questions,
        answers=answer_details
    )
    saved_submission = await quiz_repo.create(submission)

    # 4. Propagate score back to Progress logs (percentage format)
    score_pct = 0.0
    if total_questions > 0:
        score_pct = (correct_count / total_questions) * 100.0

    progress_service = ProgressService(progress_repo)
    progress_log = TopicProgressLog(
        topic_id=topic_id,
        duration_seconds=0, # Duration logged separately, or default 0 on submits
        quiz_score=round(score_pct, 2)
    )
    await progress_service.log_topic_progress(current_user.id, subject_id, progress_log)

    return saved_submission

@router.get("/history", response_model=List[QuizSubmissionResponse], tags=["Assessments"])
async def get_quiz_history(
    current_user: UserModel = Depends(get_current_user),
    quiz_repo: QuizSubmissionRepository = Depends(get_quiz_submission_repository)
):
    """Retrieve history logs of all quiz attempts by the active user"""
    return await quiz_repo.get_by_user(current_user.id)
