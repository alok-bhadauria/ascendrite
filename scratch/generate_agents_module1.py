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

    m1_data = {
        "ai-agents-m1-t1": {
            "title": "Agent Philosophy & Loops",
            "notes": {
                "learning_outcomes": [
                    "Contrast passive text generation with autonomous agent loops.",
                    "Explain environmental feedback signals and execution routing."
                ],
                "sections": [
                    {
                        "title": "Autonomous Execution Loops",
                        "content": "Traditional LLMs operate passively, taking a single input and generating a single output. **AI Agents** transition this paradigm to autonomous execution loops. An agent runs in a continuous loop: it perceives the state of an environment, updates its internal state, decides on an action, executes it via tools, and processes the feedback from the environment. This mimics the classic cybernetic feedback loop (Perceive-Plan-Act).",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Agent Philosophy & Loops\n\n*   **Passive Generation:** Single input-output pass.\n*   **Autonomous Loop:** Continuous perception-action cycle responding to environmental feedback.\n",
            "interview": "# Interview Prep: Agent Loops\n\n## Q1: How does an agent loop handle unexpected exceptions during tool execution without crashing?\n\n### Standard Answer\nAn agent loop must wrap tool execution blocks in robust try-catch handlers. Instead of crashing, the exception traceback is captured, formatted as a text string, and injected back into the LLM context as an 'Observation'. This allows the agent's reasoning layer to diagnose the error and plan a correction.\n",
            "example_code": "class SimpleAgentLoop:\n    def __init__(self, env):\n        self.env = env\n    def run_step(self, action):\n        return self.env.execute(action)\n\nif __name__ == '__main__':\n    print('Agent loop base module loaded.')\n",
            "practice_code": "class MockEnv:\n    def execute(self, action):\n        return f\"Observed outcome of {action}\"\n\ndef run_practice():\n    env = MockEnv()\n    assert env.execute('search') == 'Observed outcome of search'\n    print('[PASS] Agent environment feedback loop verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m1-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the core structural difference between an autonomous agent loop and standard prompt-response generation?",
                        "options": ["The agent loop dynamically executes actions based on feedback from the environment and continues processing iteratively.", "The agent loop runs faster.", "The agent loop does not use embeddings.", "The agent loop is immune to hallucination."],
                        "correct_answer": "The agent loop dynamically executes actions based on feedback from the environment and continues processing iteratively.",
                        "explanation": "Agent loops run in iterations, processing observations from tool executions to decide subsequent actions, rather than completing in a single turn."
                    }
                ]
            }
        },
        "ai-agents-m1-t2": {
            "title": "ReAct Reasoning Framework",
            "notes": {
                "learning_outcomes": [
                    "Explain the ReAct (Reasoning + Acting) execution sequence.",
                    "Formulate Thought-Action-Observation regex parsing boundaries.",
                    "Define loop termination parameters to prevent infinite executions."
                ],
                "sections": [
                    {
                        "title": "The ReAct Execution Loop",
                        "content": "The **ReAct (Reasoning and Acting)** framework integrates reasoning token generations and action execution steps in a tight loop. For each iteration, the agent generates a structured trace:\n\n1.  **Thought:** The model analyzes the current goal and observations, planning its next action.\n2.  **Action:** The model selects a tool and outputs formatted arguments (e.g. `Action: Search[quantum physics]`).\n3.  **Observation:** The system executes the tool and appends the result to the prompt context, letting the model process the feedback in the next iteration.",
                        "callouts": [
                            {
                                "type": "Student Trap",
                                "title": "Parsing Ambiguities",
                                "content": "If the model outputs 'Thought' and 'Action' in a single turn, the inference engine must stop generation immediately after the 'Action' token. If it continues generating the 'Observation' itself, it will hallucinate tool outputs, breaking the loop integration."
                            }
                        ]
                    },
                    {
                        "title": "Infinite Loop Mitigations",
                        "content": "To prevent runaway costs and infinite execution loops (where the agent keeps executing the same failing action), systems enforce termination parameters:\n*   `max_iterations`: Hard limit on the number of loop iterations (typically 10-15).\n*   `timeout_seconds`: Hard wall-clock execution time limit.\n*   *Stop Sequences*: Stop generation immediately on `Observation:` tags to hand control back to the parser.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# ReAct Reasoning Framework\n\n## 1. Execution Sequence\n`Thought` $\\to$ `Action` $\\to$ `Observation` $\\to$ `Thought` ...\n\n## 2. Termination Safeguards\n*   Enforce `max_iterations` limits.\n*   Register `Observation:` as a hard stop sequence during model generation.\n",
            "interview": "# Interview Prep: ReAct Framework\n\n## Q1: Why do we force the LLM to write a 'Thought' block before outputting an 'Action' block in ReAct loops?\n\n### Standard Answer\nWriting a 'Thought' block forces the model to allocate computation steps (tokens) to reasoning before selecting an action. Because LLMs are autoregressive, generating the thought tokens builds a contextual path that guides the model to select a more appropriate tool and construct valid arguments, reducing reasoning errors.\n",
            "example_code": "import re\n\ndef parse_react_action(text):\n    match = re.search(r'Action:\\s*(\\w+)\\[(.*)\\]', text)\n    if match:\n        return match.group(1), match.group(2)\n    return None, None\n\nif __name__ == '__main__':\n    print('ReAct parser configured.')\n",
            "practice_code": "import re\n\ndef parse_react_action(text):\n    match = re.search(r'Action:\\s*(\\w+)\\[(.*)\\]', text)\n    if match:\n        return match.group(1), match.group(2)\n    return None, None\n\ndef run_practice():\n    trace = \"Thought: I need to find the result. Action: Search[Llama 3 paper]\"\n    tool, arg = parse_react_action(trace)\n    assert tool == 'Search'\n    assert arg == 'Llama 3 paper'\n    print('[PASS] ReAct regex parser verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m1-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary risk of omitting stop sequences for the 'Observation:' tag in a ReAct loop?",
                        "options": ["The model will hallucinate the tool's observation itself instead of allowing the system to run the actual tool.", "The model will output binary codes.", "The context window will shrink.", "The learning rate will decay."],
                        "correct_answer": "The model will hallucinate the tool's observation itself instead of allowing the system to run the actual tool.",
                        "explanation": "If the model does not stop generating at the 'Observation' boundary, it will write its own imaginary observation data, bypassing the external tool."
                    }
                ]
            }
        },
        "ai-agents-m1-t3": {
            "title": "Planning & Goal Decomposition",
            "notes": {
                "learning_outcomes": [
                    "Explain task decomposition and recursive planning.",
                    "Contrast proactive task queues (BabyAGI) with Plan-and-Solve strategies."
                ],
                "sections": [
                    {
                        "title": "Recursive Goal Decomposition",
                        "content": "For complex objectives, agents must split a goal into manageable sub-tasks. **BabyAGI** structures this by maintaining a task list, prioritizing tasks dynamically, executing the top task, and creating new tasks based on the execution result. The system loops until the task list is empty.",
                        "callouts": []
                    },
                    {
                        "title": "Plan-and-Solve Strategies",
                        "content": "While recursive planning updates tasks dynamically, **Plan-and-Solve** drafts a static sequence of tasks first, executing them step-by-step. This reduces token overhead by avoiding replanning at each step, but is less adaptable to unexpected environmental feedback.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Planning & Goal Decomposition\n\n*   **Recursive Planning (BabyAGI):** Dynamic task queue creation, prioritization, and execution loops.\n*   **Plan-and-Solve:** Static multi-step task list generation followed by execution, minimizing intermediate reasoning loops.\n",
            "interview": "# Interview Prep: Goal Decomposition\n\n## Q1: How does BabyAGI prioritize tasks dynamically during execution?\n\n### Standard Answer\nAfter executing a task and receiving feedback, a dedicated 'task creation' prompt generates new sub-tasks. Then, a 'prioritization' prompt takes all unexecuted tasks along with the current context and outputs an ordered list of task IDs, re-allocating resource priority based on the latest state.\n",
            "example_code": "class TaskQueue:\n    def __init__(self):\n        self.tasks = []\n    def add_task(self, name):\n        self.tasks.append(name)\n    def pop_task(self):\n        return self.tasks.pop(0) if self.tasks else None\n\nif __name__ == '__main__':\n    print('TaskQueue module compiled.')\n",
            "practice_code": "class TaskQueue:\n    def __init__(self):\n        self.tasks = []\n    def add_task(self, name):\n        self.tasks.append(name)\n    def pop_task(self):\n        return self.tasks.pop(0) if self.tasks else None\n\ndef run_practice():\n    tq = TaskQueue()\n    tq.add_task('Task 1')\n    tq.add_task('Task 2')\n    assert tq.pop_task() == 'Task 1'\n    assert len(tq.tasks) == 1\n    print('[PASS] Task queue basic schedulers verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m1-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary advantage of the Plan-and-Solve approach over recursive task-queue planning?",
                        "options": ["It reduces intermediate replanning token costs by establishing a structured execution blueprint upfront.", "It is immune to logical errors.", "It eliminates the need for tool declarations.", "It uses less context memory."],
                        "correct_answer": "It reduces intermediate replanning token costs by establishing a structured execution blueprint upfront.",
                        "explanation": "Plan-and-Solve drafts a static list of actions first, avoiding the overhead of running planning prompts at every single loop iteration."
                    }
                ]
            }
        },
        "ai-agents-m1-t4": {
            "title": "Advanced Reasoning Paths",
            "notes": {
                "learning_outcomes": [
                    "Explain Tree of Thoughts (ToT) search heuristics.",
                    "Formulate Self-Reflection correction loops."
                ],
                "sections": [
                    {
                        "title": "Tree of Thoughts (ToT)",
                        "content": "Standard decoding (like chain-of-thought) generates linear paths. For complex search problems (e.g. math proofs, puzzles), **Tree of Thoughts (ToT)** constructs a search tree where nodes represent intermediate thoughts. The model uses search heuristics (e.g. depth-first search or breadth-first search) to explore paths, evaluating node validity and backtracking when a path is deemed invalid.",
                        "callouts": []
                    },
                    {
                        "title": "Self-Reflection Loops",
                        "content": "To correct errors autonomously, agents implement **Self-Reflection**. Before returning a final answer, a reflection prompt evaluates the generated trace for logical flaws or constraint violations. If flaws are found, the model generates corrections, continuing the loop until the output passes validation.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Advanced Reasoning Paths\n\n*   **Tree of Thoughts:** Graph-search evaluation heuristics (DFS/BFS) over branching thought nodes.\n*   **Self-Reflection:** Validation prompts checking execution outputs for logical consistency and triggering retries.\n",
            "interview": "# Interview Prep: Reasoning Paths\n\n## Q1: How does Tree of Thoughts (ToT) evaluate intermediate thought nodes during search?\n\n### Standard Answer\nToT prompts the LLM to act as a heuristic evaluator. For a given intermediate node, the model classifies it as 'sure' (highly likely to lead to a solution), 'likely' (promising), or 'impossible' (hopeless). Based on these classifications, the search algorithm guides traversal (e.g. pruning 'impossible' branches).",
            "example_code": "def dfs_backtrack_sim(node, visited):\n    visited.append(node)\n    return visited\n\nif __name__ == '__main__':\n    print('DFS backtracking trackers ready.')\n",
            "practice_code": "def dfs_backtrack_sim(node, visited):\n    visited.append(node)\n    return visited\n\ndef run_practice():\n    vis = []\n    res = dfs_backtrack_sim('root', vis)\n    assert res == ['root']\n    print('[PASS] DFS search simulation validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m1-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the role of self-reflection loops in agentic systems?",
                        "options": ["To review output quality and correct mistakes before returning the final answer.", "To compress context databases.", "To select the next token.", "To speed up token generation rates."],
                        "correct_answer": "To review output quality and correct mistakes before returning the final answer.",
                        "explanation": "Self-reflection runs checks on candidate responses, identifying flaws and rewriting sections to ensure accuracy."
                    }
                ]
            }
        },
        "ai-agents-m1-t5": {
            "title": "Structured Argument Extraction",
            "notes": {
                "learning_outcomes": [
                    "Explain JSON Schema constraints in tool calling.",
                    "Formulate logit bias modifications for argument syntax."
                ],
                "sections": [
                    {
                        "title": "JSON Schema Constraints",
                        "content": "To interface with external APIs, agents must extract structured arguments from text. This is configured by passing a JSON Schema defining parameter names, types, and constraint rules. The model output is parsed into these fields, validating argument types before execution.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Structured Argument Extraction\n\n*   **Structured Output:** Maps model outputs to structured parameter blocks (e.g. JSON schemas).\n*   **Validations:** Verifies parameter types and ranges before calling APIs.\n",
            "interview": "# Interview Prep: Argument Extraction\n\n## Q1: How do modern serving libraries guarantee that tool arguments conform exactly to JSON schemas?\n\n### Standard Answer\nServing libraries (like OpenAI's structured outputs or vLLM) compile the JSON schema into a Context-Free Grammar (CFG). During token generation, the engine masks vocabulary logits that violate the grammar constraints (e.g., forcing a closing bracket `}` or quote `\"`), guaranteeing schema compliance.\n",
            "example_code": "import json\n\ndef parse_tool_args(json_str):\n    try:\n        return json.loads(json_str), True\n    except ValueError:\n        return {}, False\n\nif __name__ == '__main__':\n    print('Schema validator ready.')\n",
            "practice_code": "import json\n\ndef parse_tool_args(json_str):\n    try:\n        return json.loads(json_str), True\n    except ValueError:\n        return {}, False\n\ndef run_practice():\n    args, ok = parse_tool_args('{\"query\": \"Llama\"}')\n    assert ok\n    assert args['query'] == 'Llama'\n    print('[PASS] JSON parser validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m1-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Which validation step is performed when converting a natural language query into tool parameters?",
                        "options": ["Parsing parameter outputs against JSON schema types and constraints.", "Replacing embeddings with tokens.", "Pruning older context files.", "Running PPO gradient calculations."],
                        "correct_answer": "Parsing parameter outputs against JSON schema types and constraints.",
                        "explanation": "The parser validates that the generated arguments conform to the types and constraints defined in the tool's JSON Schema."
                    }
                ]
            }
        }
    }

    # Write Module 1 files
    for topic_id, data in m1_data.items():
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

    print("\nSuccessfully generated AI Agents Module 1 files!")

if __name__ == "__main__":
    main()
