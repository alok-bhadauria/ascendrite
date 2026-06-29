import os
import json

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    agents_dir = os.path.join(base_dir, "knowledge-base", "ai", "ai-agents")

    m3_data = {
        "ai-agents-m3-t1": {
            "title": "LangGraph Architecture",
            "notes": {
                "learning_outcomes": [
                    "Explain stateful execution graphs and node function definitions.",
                    "Formulate state reducer operations and consolidation logic."
                ],
                "sections": [
                    {
                        "title": "Stateful Execution Graphs",
                        "content": "While simple chains execute sequentially, complex workflows require state tracking and cyclic execution paths. **LangGraph** models workflows as stateful directed graphs, where nodes represent actions (e.g. calling an LLM or a tool) and edges define execution flow. The graph shares a global state object passed between nodes during execution.",
                        "callouts": []
                    },
                    {
                        "title": "State Reducers and Consolidation",
                        "content": "To prevent concurrent nodes from overwriting the global state, LangGraph uses **reducers**. A reducer defines how node updates are merged into the state (e.g. appending new messages to a list rather than overwriting it):\n\n$$\\mathbf{S}_{t+1} = \\text{Reducer}(\\mathbf{S}_t, \\Delta \\mathbf{S})$$\n\nThis guarantees state consistency across parallel execution branches.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# LangGraph Architecture\n\n*   **Stateful Graphs:** Modeling workflows as nodes (actions) and edges (transitions) over a shared state.\n*   **Reducers:** Mathematical consolidation functions that merge node updates into the global state.\n",
            "interview": "# Interview Prep: LangGraph\n\n## Q1: How do state reducers prevent concurrent write conflicts in graph executions?\n\n### Standard Answer\nReducers define conflict resolution rules (e.g., list append, dictionary merge, or custom math overrides). When parallel nodes complete execution, their updates are processed sequentially by the reducer, maintaining state consistency.\n",
            "example_code": "def message_list_reducer(state, new_messages):\n    return state + new_messages\n\nif __name__ == '__main__':\n    print('LangGraph state reducers active.')\n",
            "practice_code": "def message_list_reducer(state, new_messages):\n    return state + new_messages\n\ndef run_practice():\n    initial = ['msg1']\n    updated = message_list_reducer(initial, ['msg2', 'msg3'])\n    assert updated == ['msg1', 'msg2', 'msg3']\n    print('[PASS] Reducer state updates validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m3-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary role of a state reducer in LangGraph?",
                        "options": ["To define how updates from nodes are merged into the shared global state.", "To prune positional embeddings.", "To compress images.", "To speed up token generation rates."],
                        "correct_answer": "To define how updates from nodes are merged into the shared global state.",
                        "explanation": "State reducers consolidate updates, preventing concurrent execution paths from overwriting the global state."
                    }
                ]
            }
        },
        "ai-agents-m3-t2": {
            "title": "Graph Routing & Conditional Edges",
            "notes": {
                "learning_outcomes": [
                    "Explain conditional routing functions and dynamic edge selection.",
                    "Formulate cycle detection and loop controls."
                ],
                "sections": [
                    {
                        "title": "Conditional Routing and Loop Controls",
                        "content": "Standard edges define static transitions. To build flexible workflows, we use **conditional edges**. A conditional routing function evaluates the current state and returns the next node to execute. This allows the graph to adapt to execution outcomes, executing cycles (loops) until a exit condition is met.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Graph Routing\n\n*   **Conditional Edges:** Dynamic routing functions that evaluate state to determine the next node transition.\n*   **Loops & Cycles:** Repeating node executions until a terminal condition is met.\n",
            "interview": "# Interview Prep: Graph Routing\n\n## Q1: How do we prevent infinite loops in stateful graph execution loops?\n\n### Standard Answer\nWe configure a maximum recursion depth limit (e.g. `recursion_limit=50`). If the execution path visits more nodes than the limit, the engine raises an exception and halts, preventing infinite loops.\n",
            "example_code": "def route_next_node(state):\n    if state.get('error'):\n        return 'error_handler'\n    return 'success_end'\n\nif __name__ == '__main__':\n    print('Graph routing module configured.')\n",
            "practice_code": "def route_next_node(state):\n    if state.get('error'):\n        return 'error_handler'\n    return 'success_end'\n\ndef run_practice():\n    state = {'error': True}\n    assert route_next_node(state) == 'error_handler'\n    print('[PASS] Conditional edge routing checks passed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m3-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What does a conditional edge evaluate to determine the next graph transition?",
                        "options": ["The current shared global state.", "The token generation speed.", "The API key validation state.", "The learning rate shape."],
                        "correct_answer": "The current shared global state.",
                        "explanation": "Conditional routing functions evaluate the shared global state to select the next node path dynamically."
                    }
                ]
            }
        },
        "ai-agents-m3-t3": {
            "title": "Persistence & State Rewinding",
            "notes": {
                "learning_outcomes": [
                    "Explain thread checkpointing state savers.",
                    "Formulate state rollbacks and time-travel debugging triggers."
                ],
                "sections": [
                    {
                        "title": "Thread Checkpointing",
                        "content": "To enable persistence, graph engines implement **thread checkpointing**. At each step, the state is serialized and stored in a database (checkpoint). This allows long-running agents to resume execution after crashes or pauses, and enables multi-user session management.",
                        "callouts": []
                    },
                    {
                        "title": "State Rewinding (Time-Travel)",
                        "content": "Checkpoint databases enable **time-travel debugging**. By loading a past checkpoint ID, developers can inspect the agent's state at that point, modify it, and fork execution along a new path. This is critical for debugging and safety auditing.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Persistence & Checkpointing\n\n*   **Thread Checkpointing:** Saving state snapshots to a database at each execution step.\n*   **Time-Travel Debugging:** Rolling back state to a past checkpoint ID to inspect or fork execution paths.\n",
            "interview": "# Interview Prep: Persistence\n\n## Q1: How does state checkpointing support human-in-the-loop interventions?\n\n### Standard Answer\nWhen an action requires human review, the engine checkpoints the state and pauses execution. Once human feedback is received, the engine loads the checkpoint, applies the update, and resumes execution from the exact point it paused.\n",
            "example_code": "class MockCheckpointSaver:\n    def __init__(self):\n        self.db = {}\n    def save(self, thread_id, state):\n        self.db[thread_id] = state.copy()\n    def load(self, thread_id):\n        return self.db.get(thread_id, {})\n\nif __name__ == '__main__':\n    print('Checkpoint modules ready.')\n",
            "practice_code": "class MockCheckpointSaver:\n    def __init__(self):\n        self.db = {}\n    def save(self, thread_id, state):\n        self.db[thread_id] = state.copy()\n    def load(self, thread_id):\n        return self.db.get(thread_id, {})\n\ndef run_practice():\n    saver = MockCheckpointSaver()\n    saver.save('thread_1', {'step': 5})\n    assert saver.load('thread_1') == {'step': 5}\n    print('[PASS] Checkpoint persistence checks validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m3-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary benefit of time-travel debugging in stateful agent graphs?",
                        "options": ["To roll back execution state to any past checkpoint step to inspect variables or fork execution paths.", "To compress context databases.", "To speed up token generation rates.", "To train the tokenizer."],
                        "correct_answer": "To roll back execution state to any past checkpoint step to inspect variables or fork execution paths.",
                        "explanation": "Time-travel debugging loads past checkpoint IDs, allowing developers to inspect or resume execution from previous states."
                    }
                ]
            }
        },
        "ai-agents-m3-t4": {
            "title": "Human-in-the-Loop Integrations",
            "notes": {
                "learning_outcomes": [
                    "Explain execution interruption mechanics and manual payload injections.",
                    "Formulate approval checkpoint handlers."
                ],
                "sections": [
                    {
                        "title": "Execution Interruption and Approval Checkpoints",
                        "content": "For safety-critical actions (e.g. sending emails or executing financial transfers), agents must not operate autonomously. We insert **human-in-the-loop checkpoints** that pause the execution thread before executing specific nodes. The system awaits manual review, resuming execution only after receiving approval or modification payloads.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Human-in-the-Loop\n\n*   **Interrupts:** Pausing execution threads before safety-critical node executions.\n*   **Approvals:** Manual payload injections (approve/reject/edit) that update the state before resuming.\n",
            "interview": "# Interview Prep: Human-in-the-Loop\n\n## Q1: How do you implement a secure approval gate for a database delete operation in an agent graph?\n\n### Standard Answer\nWe define a breakpoint on the `delete_db` node. The graph executes up to the breakpoint and pauses. An API exposes the pending payload to an admin portal. Once the admin clicks 'Approve', the system injects an approval token into the state and triggers the graph resume loop.\n",
            "example_code": "def check_approval_status(state):\n    return state.get('human_approved', False)\n\nif __name__ == '__main__':\n    print('Approval validators loaded.')\n",
            "practice_code": "def check_approval_status(state):\n    return state.get('human_approved', False)\n\ndef run_practice():\n    state = {'human_approved': True}\n    assert check_approval_status(state)\n    print('[PASS] Approval check validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m3-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What happens when an agent graph encounters a configured breakpoint?",
                        "options": ["Execution pauses, and the current state is serialized, waiting for an external resume signal.", "The program crashes.", "The context is deleted.", "The model is retrained."],
                        "correct_answer": "Execution pauses, and the current state is serialized, waiting for an external resume signal.",
                        "explanation": "Breakpoints pause execution, serializing the state to database checkpoints while waiting for external inputs or approval signals."
                    }
                ]
            }
        },
        "ai-agents-m3-t5": {
            "title": "Self-Correction Loops",
            "notes": {
                "learning_outcomes": [
                    "Explain iterative execution check validation structures.",
                    "Formulate compiler error self-correction loops."
                ],
                "sections": [
                    {
                        "title": "Compiler Feedback and Self-Correction",
                        "content": "For code generation or data transformations, agents can evaluate their outputs using validation tools (e.g. running a python interpreter or JSON linter). If compilation or validation fails, the traceback errors are passed back to the model as context. The model generates corrections, looping until the output compiles successfully.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Self-Correction Loops\n\n*   **Validation Checks:** Running compilers, linters, or test suites on agent outputs.\n*   **Feedback Loops:** Passing parser tracebacks back to the generator to correct code errors.\n",
            "interview": "# Interview Prep: Self-Correction\n\n## Q1: How does a compiler-guided self-correction loop prevent the model from repeating syntax errors?\n\n### Standard Answer\nThe linter output (or traceback) must be accompanied by instructions asking the model to explain the syntax error before correcting it. This forces the model to generate reasoning tokens, guiding it to write syntactically valid code.\n",
            "example_code": "def validate_output_length(text, min_len=5):\n    return len(text) >= min_len\n\nif __name__ == '__main__':\n    print('Linter modules ready.')\n",
            "practice_code": "def validate_output_length(text, min_len=5):\n    return len(text) >= min_len\n\ndef run_practice():\n    assert validate_output_length('Llama model')\n    assert not validate_output_length('cat')\n    print('[PASS] Output length linter checks validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m3-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary context injected back to the model during a compiler self-correction step?",
                        "options": ["The compilation error message or linter traceback.", "The system prompt.", "The dataset file path.", "The vocabulary lookup index."],
                        "correct_answer": "The compilation error message or linter traceback.",
                        "explanation": "Injecting the traceback provides the model with the error context, allowing it to diagnose and fix the syntax errors."
                    }
                ]
            }
        }
    }

    # Write Module 3 files
    for topic_id, data in m3_data.items():
        notes_content = {
            "topic_id": topic_id,
            "title": data["title"],
            "version": "1.0.0",
            "topic_metadata": {
                "difficulty": "Medium",
                "estimated_hours": 5,
                "importance": "High"
            },
            "learning_outcomes": data["notes"]["learning_outcomes"],
            "content_sections": [
                {
                    "title": sec["title"],
                    "content": sec["content"],
                    "callouts": sec.get("callouts", [])
                } for sec in data["notes"]["sections"]
            ],
            "example_refs": [f"{topic_id}-ex1"],
            "diagram_refs": [],
            "practice_refs": [f"{topic_id}-prac1"],
            "quiz_refs": [f"{topic_id}-quiz"]
        }
        write_file(os.path.join(agents_dir, "notes", f"{topic_id}.json"), json.dumps(notes_content, indent=2))
        write_file(os.path.join(agents_dir, "revision", f"{topic_id}.md"), data["revision"])
        write_file(os.path.join(agents_dir, "interview", f"{topic_id}.md"), data["interview"])
        write_file(os.path.join(agents_dir, "examples", f"{topic_id}-ex1.py"), data["example_code"])
        write_file(os.path.join(agents_dir, "practice", f"{topic_id}-prac1.py"), data["practice_code"])
        write_file(os.path.join(agents_dir, "quiz", f"{topic_id}-quiz.json"), json.dumps(data["quiz"], indent=2))

    print("\nSuccessfully generated AI Agents Module 3 files!")

if __name__ == "__main__":
    main()
