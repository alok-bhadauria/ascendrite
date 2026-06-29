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

    m5_data = {
        "ai-agents-m5-t1": {
            "title": "MCP Architecture",
            "notes": {
                "learning_outcomes": [
                    "Explain Model Context Protocol (MCP) client-server topology.",
                    "Formulate JSON-RPC communication primitives for stdio/HTTP bindings."
                ],
                "sections": [
                    {
                        "title": "Model Context Protocol (MCP) Architecture",
                        "content": "Integrating agents with custom tools in enterprise contexts often leads to fragmented, ad-hoc API wrappers. The **Model Context Protocol (MCP)** standardizes this integration using a client-server architecture. \n\nUnder MCP:\n1.  **MCP Client:** The agent execution engine (such as Claude Desktop or a custom runner).\n2.  **MCP Server:** A lightweight microservice exposing tools, prompts, or resources via a standardized protocol.\n\nCommunication is structured using **JSON-RPC 2.0** over communication channels (typically standard input/output `stdio` for local processes, or `SSE` HTTP connections for remote servers).",
                        "callouts": []
                    }
                ]
            },
            "revision": "# MCP Architecture\n\n*   **Client-Server Topology:** Standardized protocol connecting agent engines (clients) with tool servers.\n*   **JSON-RPC 2.0 Primitives:** Exchanging structured request/response payloads over stdio or HTTP SSE.\n",
            "interview": "# Interview Prep: MCP Architecture\n\n## Q1: Why is stdio preferred over HTTP SSE for local MCP server integrations?\n\n### Standard Answer\n`stdio` uses standard input/output streams for communication. When the client launches a local server process, it communicates directly via process pipes. This requires no network configuration, firewalls, or token authentication, simplifying deployment and reducing latency.\n",
            "example_code": "def make_jsonrpc_request(method, params, request_id):\n    return {\n        \"jsonrpc\": \"2.0\",\n        \"method\": method,\n        \"params\": params,\n        \"id\": request_id\n    }\n\nif __name__ == '__main__':\n    print('MCP request builders loaded.')\n",
            "practice_code": "def make_jsonrpc_request(method, params, request_id):\n    return {\n        \"jsonrpc\": \"2.0\",\n        \"method\": method,\n        \"params\": params,\n        \"id\": request_id\n    }\n\ndef run_practice():\n    req = make_jsonrpc_request('tools/list', {}, 1)\n    assert req['jsonrpc'] == '2.0'\n    assert req['method'] == 'tools/list'\n    assert req['id'] == 1\n    print('[PASS] JSON-RPC request structures verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m5-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the standard transport protocol used by local processes to communicate in the Model Context Protocol?",
                        "options": ["stdio (standard input/output pipes)", "gRPC only", "FTP", "WebSockets only"],
                        "correct_answer": "stdio (standard input/output pipes)",
                        "explanation": "Local MCP integrations leverage stdio pipes for inter-process communication, avoiding network overhead."
                    }
                ]
            }
        },
        "ai-agents-m5-t2": {
            "title": "MCP Tool & Resource Declarations",
            "notes": {
                "learning_outcomes": [
                    "Explain MCP tool capability and resource declarations.",
                    "Formulate dynamic client-side discovery loops."
                ],
                "sections": [
                    {
                        "title": "Dynamic Discovery, Tools, and Resources",
                        "content": "Under MCP, servers declare their capabilities dynamically during process handshakes:\n\n1.  **Tools:** Executable functions that perform actions (e.g. executing code or querying APIs). Servers return JSON schemas describing parameters.\n2.  **Resources:** Read-only data sources (e.g. database schemas, log files) exposed as URI structures (e.g. `postgres://db/table`).\n\nThe client queries these definitions using standard requests (like `tools/list` or `resources/list`), dynamically configuring the agent's tool set.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# MCP Capabilities\n\n*   **Tools:** Executable functions defined by JSON schemas.\n*   **Resources:** Read-only URIs exposing datasets or logs directly to the model context.\n",
            "interview": "# Interview Prep: MCP Tools\n\n## Q1: How does the client handle dynamic tool updates on the server side without restarting?\n\n### Standard Answer\nThe client issues a `tools/list` request during initialization and can monitor server notification events (e.g. `notifications/tools/list_changed`). If tools are added, the client updates its schema bindings dynamically.\n",
            "example_code": "def format_tool_schema(name, description, input_schema):\n    return {\n        \"name\": name,\n        \"description\": description,\n        \"inputSchema\": input_schema\n    }\n\nif __name__ == '__main__':\n    print('MCP schema formatter compiled.')\n",
            "practice_code": "def format_tool_schema(name, description, input_schema):\n    return {\n        \"name\": name,\n        \"description\": description,\n        \"inputSchema\": input_schema\n    }\n\ndef run_practice():\n    schema = format_tool_schema('run_cmd', 'Runs command', {'type': 'object'})\n    assert schema['name'] == 'run_cmd'\n    assert schema['inputSchema']['type'] == 'object'\n    print('[PASS] Dynamic tool discovery schema validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m5-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary difference between Tools and Resources under the Model Context Protocol?",
                        "options": ["Tools are executable functions, whereas Resources are read-only data sources exposed via URIs.", "Tools use gRPC and resources use FTP.", "Tools are always local and resources are remote.", "There is no difference."],
                        "correct_answer": "Tools are executable functions, whereas Resources are read-only data sources exposed via URIs.",
                        "explanation": "Tools perform actions (e.g. running code), while resources provide read-only data streams (e.g. files) to the model context."
                    }
                ]
            }
        },
        "ai-agents-m5-t3": {
            "title": "Agent Evaluation Frameworks",
            "notes": {
                "learning_outcomes": [
                    "Explain trajectory logging database structures.",
                    "Formulate success metrics and evaluation benchmarks."
                ],
                "sections": [
                    {
                        "title": "Trajectory Logging and Evaluation Metrics",
                        "content": "Evaluating agents is challenging because they generate multi-step execution traces (trajectories) rather than single outputs. **Trajectory Logging** databases record every thought, action, and observation in the loop. Evaluators (human auditors or LLM judges) analyze these logs to measure accuracy, tool usage efficiency, and recovery performance.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Agent Evaluations\n\n*   **Trajectory Log:** Database records storing every step (thought-action-observation) of the execution loop.\n*   **Metrics:** Tracking success rate, token efficiency, and error recovery rates.\n",
            "interview": "# Interview Prep: Agent Evals\n\n## Q1: Why are standard output-matching tests insufficient for evaluating autonomous agents?\n\n### Standard Answer\nAgents can arrive at the correct output via highly inefficient or risky paths (e.g. executing redundant database scans or trying to access restricted files). Trajectory evaluation audits the intermediate steps to ensure safety, efficiency, and compliance.\n",
            "example_code": "def calculate_trajectory_efficiency(n_steps, min_steps=3):\n    # Ratio of optimal steps to actual steps\n    return min_steps / n_steps if n_steps > 0 else 0.0\n\nif __name__ == '__main__':\n    print('Trajectory metrics loaded.')\n",
            "practice_code": "def calculate_trajectory_efficiency(n_steps, min_steps=3):\n    return min_steps / n_steps if n_steps > 0 else 0.0\n\ndef run_practice():\n    eff = calculate_trajectory_efficiency(6, 3)\n    assert eff == 0.5\n    print('[PASS] Trajectory efficiency calculation verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m5-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What does a trajectory log store in an agentic evaluation framework?",
                        "options": ["The complete step-by-step history of thoughts, actions, and observations generated during execution.", "Only the final output.", "The model weights.", "The compiler configuration."],
                        "correct_answer": "The complete step-by-step history of thoughts, actions, and observations generated during execution.",
                        "explanation": "Trajectory logs store the entire execution trace, allowing developers to analyze agent behaviors and diagnose failures."
                    }
                ]
            }
        },
        "ai-agents-m5-t4": {
            "title": "Production Safety Guardrails",
            "notes": {
                "learning_outcomes": [
                    "Explain prompt injection scanners and rate limit configurations.",
                    "Formulate execution approval rules."
                ],
                "sections": [
                    {
                        "title": "Safety Guardrails and Scanners",
                        "content": "Production deployment requires safety guardrails. We configure:\n\n1.  **Input Guardrails:** Scanners that inspect incoming user prompts for injections or toxic content before execution.\n2.  **Rate Limiters:** Limit the number of iterations or tokens consumed per user session to prevent API cost spikes.\n3.  **Action Approval Gates:** Rule engines that flag sensitive actions (e.g. modifying files) for human verification.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Production Safety\n\n*   **Input Guardrails:** Sanitizing user prompts to block injections.\n*   **Rate Limits:** Bounding iterations and tokens per session to control costs.\n",
            "interview": "# Interview Prep: Guardrails\n\n## Q1: How do you design a rate limiter to prevent recursive agent loops from consuming thousands of dollars in tokens?\n\n### Standard Answer\nWe implement a hard limit on both the max token count and the max iteration count per session. If the token count or iteration count exceeds the threshold, the session is terminated automatically, and an alert is logged.\n",
            "example_code": "def enforce_iteration_limit(current_iter, max_iter=10):\n    return current_iter < max_iter\n\nif __name__ == '__main__':\n    print('Iteration guardrails active.')\n",
            "practice_code": "def enforce_iteration_limit(current_iter, max_iter=10):\n    return current_iter < max_iter\n\ndef run_practice():\n    assert enforce_iteration_limit(5, 10)\n    assert not enforce_iteration_limit(10, 10)\n    print('[PASS] Iteration guardrails checks completed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m5-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary function of an action approval gate in an agentic safety pipeline?",
                        "options": ["To intercept sensitive actions (e.g. file writes) and require human verification before execution.", "To speed up token generation rates.", "To encrypt data.", "To run PPO loops."],
                        "correct_answer": "To intercept sensitive actions (e.g. file writes) and require human verification before execution.",
                        "explanation": "Approval gates intercept high-risk actions, requiring human authorization before the system executes them."
                    }
                ]
            }
        },
        "ai-agents-m5-t5": {
            "title": "Sandbox Execution Environments",
            "notes": {
                "learning_outcomes": [
                    "Explain containerized runtimes and isolated python interpreters.",
                    "Formulate file read-write boundary rules."
                ],
                "sections": [
                    {
                        "title": "Containerization and Isolated Interpreters",
                        "content": "Allowing agents to execute code on host systems creates severe security risks (e.g. data theft or system deletion). \n\nTo mitigate this, agents run code inside **sandboxed execution environments** (e.g. Docker containers or microVMs). The interpreter has no access to the host filesystem, network, or environment variables. File read-write actions are strictly bounded to a temporary sandbox directory.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Sandboxed Execution\n\n*   **Sandboxes:** Isolated runtimes (e.g. Docker containers) that execute agent-generated code without risking the host.\n*   **Path Boundaries:** Restricting file read/write operations to a specific temporary sandbox directory.\n",
            "interview": "# Interview Prep: Sandboxing\n\n## Q1: How do you prevent a malicious python script executed by an agent from consuming all host CPU resources?\n\n### Standard Answer\nWe configure container-level resource limits (e.g. Docker cgroups), restricting the sandbox process to a single CPU core and a fixed RAM allocation (e.g. 512MB), and enforce execution timeout bounds.\n",
            "example_code": "def validate_sandbox_path(path, sandbox_dir):\n    # Simple check if path is within sandbox directory\n    import os\n    abs_sandbox = os.path.abspath(sandbox_dir)\n    abs_target = os.path.abspath(path)\n    return abs_target.startswith(abs_sandbox)\n\nif __name__ == '__main__':\n    print('Path bounds validation systems loaded.')\n",
            "practice_code": "def validate_sandbox_path(path, sandbox_dir):\n    import os\n    # Use string prefix checks on absolute paths\n    abs_sandbox = os.path.abspath(sandbox_dir)\n    abs_target = os.path.abspath(path)\n    return abs_target.startswith(abs_sandbox)\n\ndef run_practice():\n    sandbox = './sandbox'\n    # target inside sandbox\n    assert validate_sandbox_path('./sandbox/file.txt', sandbox)\n    # target attempting escape\n    assert not validate_sandbox_path('./sandbox/../host_file.txt', sandbox)\n    print('[PASS] Sandbox path validation checked.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m5-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Why must code execution tools run in isolated containers rather than the host system?",
                        "options": ["To prevent agent-generated scripts from accessing the host filesystem, network, or hardware resources, protecting the system from security breaches.", "To speed up code execution.", "To avoid writing logs.", "To reduce parameter counts."],
                        "correct_answer": "To prevent agent-generated scripts from accessing the host filesystem, network, or hardware resources, protecting the system from security breaches.",
                        "explanation": "Sandboxing isolates the environment, preventing generated scripts from executing destructive commands on the host system."
                    }
                ]
            }
        }
    }

    # Write Module 5 files
    for topic_id, data in m5_data.items():
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

    print("\nSuccessfully generated AI Agents Module 5 files!")

if __name__ == "__main__":
    main()
