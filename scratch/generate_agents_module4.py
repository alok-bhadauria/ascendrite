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

    m4_data = {
        "ai-agents-m4-t1": {
            "title": "Multi-Agent Topologies",
            "notes": {
                "learning_outcomes": [
                    "Compare hierarchical topologies with peer-to-peer message buses.",
                    "Explain supervisor routing strategies."
                ],
                "sections": [
                    {
                        "title": "Multi-Agent Topologies",
                        "content": "For complex tasks, a single agent can suffer from context-window clutter and reasoning dilution. **Multi-agent systems** solve this by distributing tasks across multiple specialized agents. \n\n*   **Hierarchical Topology:** A 'supervisor' agent acts as a manager, taking user queries, delegating tasks to specialist worker agents, and aggregating results. Workers communicate only with the supervisor.\n*   **Peer-to-Peer (P2P) Topology:** Agents communicate directly with each other via a shared message bus, passing tasks and feedback dynamically. This is highly flexible but harder to coordinate.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Multi-Agent Topologies\n\n*   **Hierarchical:** Coordinator supervisor delegates tasks to workers, maintaining centralized control.\n*   **Peer-to-Peer:** Collaborative agents route tasks and share updates directly over a common message bus.\n",
            "interview": "# Interview Prep: Multi-Agent Topologies\n\n## Q1: Why do hierarchical topologies scale better than peer-to-peer message buses for complex software development tasks?\n\n### Standard Answer\nIn P2P systems, every agent can message any other agent, creating high communication overhead and prompt context clutter (chattering). Hierarchical topologies restrict communication paths: workers report results back to the supervisor, who acts as a filter, reducing context bloat and coordinating execution steps.\n",
            "example_code": "def route_to_agent(state):\n    task = state.get('next_task')\n    if 'code' in task:\n        return 'coder_agent'\n    return 'tester_agent'\n\nif __name__ == '__main__':\n    print('Supervisor routing matrix loaded.')\n",
            "practice_code": "def route_to_agent(state):\n    task = state.get('next_task')\n    if 'code' in task:\n        return 'coder_agent'\n    return 'tester_agent'\n\ndef run_practice():\n    state = {'next_task': 'write code for search'}\n    assert route_to_agent(state) == 'coder_agent'\n    print('[PASS] Multi-agent supervisor routing verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m4-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary role of the supervisor agent in a hierarchical multi-agent topology?",
                        "options": ["To coordinate workers, routing sub-tasks dynamically and aggregating results.", "To compile python code.", "To write database schemas.", "To replace tokenizers."],
                        "correct_answer": "To coordinate workers, routing sub-tasks dynamically and aggregating results.",
                        "explanation": "In hierarchical setups, the supervisor acts as a manager, coordinating tasks among worker agents and organizing outputs."
                    }
                ]
            }
        },
        "ai-agents-m4-t2": {
            "title": "State Sharing & Message Formats",
            "notes": {
                "learning_outcomes": [
                    "Explain inter-agent JSON message schemas.",
                    "Formulate joint state resolution logic."
                ],
                "sections": [
                    {
                        "title": "Shared State and Message Envelopes",
                        "content": "To collaborate, agents must exchange state. In shared-state graphs (like LangGraph), agents read and write to the same global state object. In message-passing systems, agents exchange structured JSON envelopes containing the sender ID, receiver ID, payload parameters, and conversation context. A common protocol (e.g. Agent Communication Language) parses these envelopes to maintain sync.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# State Sharing & Messages\n\n*   **Global Shared State:** All agents read and write to a centralized state database.\n*   **Message-Passing Envelopes:** Agents communicate by exchanging structured JSON objects containing message parameters.\n",
            "interview": "# Interview Prep: State Sharing\n\n## Q1: How do you handle merge conflicts when two agents write to the same state field simultaneously?\n\n### Standard Answer\nWe implement optimistic locking or assign a master state reducer. If two updates conflict, the reducer merges them sequentially based on timestamps or field-specific rules (e.g. appending messages to a thread list).",
            "example_code": "def parse_envelope(envelope_json):\n    # Simple parser\n    import json\n    return json.loads(envelope_json)\n\nif __name__ == '__main__':\n    print('Envelope parsing helper initialized.')\n",
            "practice_code": "import json\n\ndef parse_envelope(envelope_json):\n    return json.loads(envelope_json)\n\ndef run_practice():\n    env = '{\"sender\": \"agent_1\", \"body\": \"hello\"}'\n    parsed = parse_envelope(env)\n    assert parsed['sender'] == 'agent_1'\n    print('[PASS] Envelope parser checks passed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m4-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "How do agents exchange information in a message-passing multi-agent system?",
                        "options": ["By exchanging structured JSON messages containing sender, recipient, and payload parameters.", "By modifying the model weights.", "By printing values to stdout.", "By running PPO loops."],
                        "correct_answer": "By exchanging structured JSON messages containing sender, recipient, and payload parameters.",
                        "explanation": "In message-passing architectures, agents collaborate by sending structured JSON message envelopes to each other."
                    }
                ]
            }
        },
        "ai-agents-m4-t3": {
            "title": "Agent Specialists & Segregation",
            "notes": {
                "learning_outcomes": [
                    "Explain specialist profiles and role configuration rules.",
                    "Formulate prompt-based boundary segregation."
                ],
                "sections": [
                    {
                        "title": "Specialist Roles and Boundaries",
                        "content": "Specialization reduces task complexity. By configuring distinct prompts, we define agent roles (e.g. Coder, Tester, Analyst). The **Coder** prompt directs the model to focus strictly on code implementation, while the **Tester** prompt instructs it to design test cases. Prompt boundaries prevent agents from executing actions outside their scope, ensuring clean separation of concerns.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Specialists & Segregation\n\n*   **Role Specialization:** Configuring agents with specific prompt templates (e.g. Coder, Tester).\n*   **Boundaries Segregation:** Restricting the tools and actions available to each agent based on its role.\n",
            "interview": "# Interview Prep: Specialist Agents\n\n## Q1: Why is it better to have separate Coder and Tester agents than a single agent that writes and tests code?\n\n### Standard Answer\nA single agent suffers from confirmation bias: it will write test cases that fit its code implementation, failing to spot edge cases. Splitting the roles forces the Tester agent to evaluate the code independently, increasing the likelihood of identifying bugs.\n",
            "example_code": "def configure_specialist(role, system_prompt):\n    return {\"role\": role, \"prompt\": system_prompt}\n\nif __name__ == '__main__':\n    print('Specialist factories active.')\n",
            "practice_code": "def configure_specialist(role, system_prompt):\n    return {\"role\": role, \"prompt\": system_prompt}\n\ndef run_practice():\n    coder = configure_specialist('coder', 'Write clean code')\n    assert coder['role'] == 'coder'\n    assert 'clean' in coder['prompt']\n    print('[PASS] Specialist profiles configured successfully.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m4-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary objective of prompt-based role segregation in multi-agent systems?",
                        "options": ["To define clear behavioral boundaries and prevent confirmation bias during complex tasks.", "To speed up token generation rates.", "To compress context databases.", "To replace long-term memory databases."],
                        "correct_answer": "To define clear behavioral boundaries and prevent confirmation bias during complex tasks.",
                        "explanation": "Segregating roles ensures agents focus on their specific tasks (e.g. coding vs testing), mitigating bias and improving quality."
                    }
                ]
            }
        },
        "ai-agents-m4-t4": {
            "title": "Conflict Resolution & Consensus",
            "notes": {
                "learning_outcomes": [
                    "Explain multi-agent debate structures and consensus rules.",
                    "Formulate task handoff protocols."
                ],
                "sections": [
                    {
                        "title": "Multi-Agent Debate and Consensus",
                        "content": "When agents output conflicting results (e.g. two analysts draw different conclusions from a dataset), the system applies **consensus rules**:\n\n1.  **Voting Consensus:** Multiple agents evaluate the proposals, and the option with the most votes is selected.\n2.  **Debate Structures:** Agents exchange arguments in a multi-turn conversation, modifying their positions until a consensus is reached or a maximum number of turns is exceeded.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Conflict Resolution & Consensus\n\n*   **Consensus Rules:** Mathematical voting or ranking schemes to select options.\n*   **Multi-Agent Debate:** Dynamic exchanges where agents critique and update proposals to reach agreement.\n",
            "interview": "# Interview Prep: Consensus Loops\n\n## Q1: How does a multi-agent debate loop prevent reasoning deadlock?\n\n### Standard Answer\nWe implement a turn limit (e.g., max 3 debate rounds). If consensus is not reached by the limit, control is passed to a tie-breaker coordinator or a human operator to resolve the deadlock.\n",
            "example_code": "def tally_votes(votes):\n    counts = {}\n    for v in votes:\n        counts[v] = counts.get(v, 0) + 1\n    return max(counts, key=counts.get)\n\nif __name__ == '__main__':\n    print('Voting modules initialized.')\n",
            "practice_code": "def tally_votes(votes):\n    counts = {}\n    for v in votes:\n        counts[v] = counts.get(v, 0) + 1\n    return max(counts, key=counts.get)\n\ndef run_practice():\n    votes = ['option_A', 'option_B', 'option_A']\n    assert tally_votes(votes) == 'option_A'\n    print('[PASS] Consensus voting tally checks completed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m4-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Which mechanism is commonly used to resolve conflicting outputs between specialist agents?",
                        "options": ["Tallying votes using consensus rules or executing multi-turn debate loops.", "Halting the program.", "Applying absolute positional encodings.", "Running negative sampling checks."],
                        "correct_answer": "Tallying votes using consensus rules or executing multi-turn debate loops.",
                        "explanation": "Consensus rules (like majority voting) and debate loops resolve conflicting opinions, finding a common solution."
                    }
                ]
            }
        },
        "ai-agents-m4-t5": {
            "title": "Scalability & Parallel Execution",
            "notes": {
                "learning_outcomes": [
                    "Explain asynchronous multi-agent worker scheduling.",
                    "Formulate concurrent state consolidation."
                ],
                "sections": [
                    {
                        "title": "Asynchronous Workers and Concurrency Limits",
                        "content": "To scale multi-agent systems, agents must execute tasks in parallel. An asynchronous scheduler manages worker pools, distributing independent sub-tasks across threads. Once workers complete, their updates are merged into the global state using thread-safe consolidation reducers.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Scalability & Parallel Execution\n\n*   **Asynchronous Scheduling:** Dispatching independent tasks to parallel workers to maximize throughput.\n*   **State Merging:** Thread-safe operations that consolidate updates from multiple parallel workers.\n",
            "interview": "# Interview Prep: Parallel Execution\n\n## Q1: How do you handle dependency resolution when scheduling parallel agent tasks?\n\n### Standard Answer\nWe construct a Directed Acyclic Graph (DAG) of task dependencies. The scheduler executes tasks in topological order, starting tasks only after all their prerequisite parent tasks have completed successfully.\n",
            "example_code": "import time\n\ndef run_async_mock(worker_id):\n    # Simulate a task\n    return f\"Result {worker_id}\"\n\nif __name__ == '__main__':\n    print('Parallel scheduler tools active.')\n",
            "practice_code": "def run_async_mock(worker_id):\n    return f\"Result {worker_id}\"\n\ndef run_practice():\n    res = run_async_mock(1)\n    assert res == 'Result 1'\n    print('[PASS] Parallel worker simulation verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m4-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary constraint when merging concurrent state updates from parallel workers?",
                        "options": ["Ensuring thread-safe state consolidation via master reducers to prevent race conditions.", "Double quantization.", "Using the Viterbi algorithm.", "Updating base model weights."],
                        "correct_answer": "Ensuring thread-safe state consolidation via master reducers to prevent race conditions.",
                        "explanation": "Parallel execution requires thread-safe state consolidation to merge updates without corrupting data."
                    }
                ]
            }
        }
    }

    # Write Module 4 files
    for topic_id, data in m4_data.items():
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

    print("\nSuccessfully generated AI Agents Module 4 files!")

if __name__ == "__main__":
    main()
