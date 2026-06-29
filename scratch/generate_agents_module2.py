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

    m2_data = {
        "ai-agents-m2-t1": {
            "title": "Short-Term Memory Systems",
            "notes": {
                "learning_outcomes": [
                    "Explain conversational session buffers and message tracking.",
                    "Formulate window size truncations to fit context budgets."
                ],
                "sections": [
                    {
                        "title": "Conversational Session Buffers",
                        "content": "Short-term memory manages active session state. In chat systems, this is tracked as a chronological list of messages: `SystemMessage`, `HumanMessage`, and `AIMessage`. As the conversation progresses, the prompt grows. To prevent exceeding the context window, systems apply sliding window truncation: discarding the oldest messages once token count thresholds are breached.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Short-Term Memory Systems\n\n*   **Session Buffer:** Chronological tracking of system, user, and assistant message states.\n*   **Truncation:** Discarding early messages to maintain token usage within maximum boundaries.\n",
            "interview": "# Interview Prep: Short-Term Memory\n\n## Q1: Why is simple message truncation risky for reasoning agents, and how do we mitigate it?\n\n### Standard Answer\nSimple truncation deletes the oldest messages. If the user defined critical goals or instructions early in the conversation, truncation will erase them, causing the agent to drift from its objectives. To mitigate this, system prompts and instructions are explicitly locked, ensuring only user-assistant chat history is pruned.\n",
            "example_code": "def prune_messages(messages, max_tokens, token_counter):\n    # Simple message list pruning helper\n    total_tokens = sum([token_counter(m) for m in messages])\n    while total_tokens > max_tokens and len(messages) > 1:\n        removed = messages.pop(0)\n        total_tokens -= token_counter(removed)\n    return messages\n\nif __name__ == '__main__':\n    print('Pruning utilities loaded.')\n",
            "practice_code": "def prune_messages(messages, max_tokens):\n    # Assumes each message is 10 tokens\n    while len(messages) * 10 > max_tokens and len(messages) > 1:\n        messages.pop(0)\n    return messages\n\ndef run_practice():\n    msg = ['m1', 'm2', 'm3']\n    pruned = prune_messages(msg, 20)\n    assert pruned == ['m2', 'm3']\n    print('[PASS] Message list pruning validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m2-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary objective of conversational sliding window memory?",
                        "options": ["To limit context footprint by keeping only the most recent chat messages in the active prompt.", "To speed up decoding.", "To replace long-term memory.", "To prevent model overfitting."],
                        "correct_answer": "To limit context footprint by keeping only the most recent chat messages in the active prompt.",
                        "explanation": "Sliding window memory prunes old messages to keep active token footprints within context budgets."
                    }
                ]
            }
        },
        "ai-agents-m2-t2": {
            "title": "Context Window Management",
            "notes": {
                "learning_outcomes": [
                    "Explain context historical pruning.",
                    "Formulate LLM-based summarization compression loops."
                ],
                "sections": [
                    {
                        "title": "Summarization and Context Compression",
                        "content": "To retain semantic context over long conversations, systems use **summarization compression loops**. When token count limits are reached, the system triggers a background prompt asking the model to summarize the preceding chat history. This summary replaces the pruned messages, compressing hundreds of tokens into a single paragraph.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Context Window Management\n\n*   **Summarization Loops:** Condensing historical message lists into a single summary block.\n*   **Context Budgets:** Allocating specific context spaces to system instructions, tools, and history.\n",
            "interview": "# Interview Prep: Context Management\n\n## Q1: How do we prevent token count tracking errors in production agent pipelines?\n\n### Standard Answer\nProduction systems must use exact tokenizer calculations (e.g. tiktoken for GPT models) rather than character heuristics. If token counts are underestimated, the prompt will exceed the model's hard limits, triggering API errors and crashing the loop.\n",
            "example_code": "def compress_summary(summary, new_message):\n    return f\"{summary} | Then: {new_message}\"\n\nif __name__ == '__main__':\n    print('Context compression helper initialized.')\n",
            "practice_code": "def compress_summary(summary, new_message):\n    return f\"{summary} | Then: {new_message}\"\n\ndef run_practice():\n    summary = \"User asked for research.\"\n    updated = compress_summary(summary, \"Sent search tool output.\")\n    assert \"research\" in updated\n    print('[PASS] Context compression verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m2-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the role of summarization compression loops in long conversations?",
                        "options": ["To condense historical chat messages into a single summary to save context space.", "To remove stop words.", "To convert text to embeddings.", "To retrain the base model weights."],
                        "correct_answer": "To condense historical chat messages into a single summary to save context space.",
                        "explanation": "Summarization loops compress historical messages into a brief summary, preserving context while saving token space."
                    }
                ]
            }
        },
        "ai-agents-m2-t3": {
            "title": "Episodic & Semantic Long-Term Memory",
            "notes": {
                "learning_outcomes": [
                    "Formulate vector database long-term memory integrations.",
                    "Apply memory retrieval and pruning routing rules."
                ],
                "sections": [
                    {
                        "title": "Long-Term Memory and Vector Databases",
                        "content": "To access information from past sessions, agents implement **long-term memory**. The system vectorizes observations and logs them into a vector database. At query time, the agent performs a similarity search, retrieving relevant past interactions and injecting them into the context as 'Episodic Memory'.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Long-Term Memory\n\n*   **Episodic Memory:** Storing past execution traces and observations in a vector database.\n*   **Retrieval Routing:** Performing similarity searches on active user queries to recall relevant past interactions.\n",
            "interview": "# Interview Prep: Long-Term Memory\n\n## Q1: How does long-term retrieval routing prevent irrelevant memories from polluting the context window?\n\n### Standard Answer\nWe apply distance thresholds (e.g. cosine distance < 0.35) and limit retrieval size ($K=3$). This prevents low-similarity, irrelevant memories from cluttering the context window.\n",
            "example_code": "def retrieve_long_term_memories(query, vector_db, k=3):\n    # Mock retrieval helper\n    return vector_db.get('docs', [])[:k]\n\nif __name__ == '__main__':\n    print('Long-term memory module configured.')\n",
            "practice_code": "def retrieve_long_term_memories(query, vector_db, k=3):\n    return vector_db.get('docs', [])[:k]\n\ndef run_practice():\n    db = {'docs': ['Memory 1', 'Memory 2']}\n    res = retrieve_long_term_memories('test', db, 1)\n    assert res == ['Memory 1']\n    print('[PASS] Long-term memory retrieval validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m2-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "How do agents retrieve episodic memories from long-term storage?",
                        "options": ["By performing a vector similarity search on the active query against the memory database.", "By scanning database tables sequentially.", "By reloading the base model weights.", "By applying regex matching only."],
                        "correct_answer": "By performing a vector similarity search on the active query against the memory database.",
                        "explanation": "Episodic memories are retrieved by converting the active query to an embedding and searching a vector database for similar past observations."
                    }
                ]
            }
        },
        "ai-agents-m2-t4": {
            "title": "Custom Tool Definitions",
            "notes": {
                "learning_outcomes": [
                    "Formulate function declaration schemas for tool call interfaces.",
                    "Explain return serialization mapping."
                ],
                "sections": [
                    {
                        "title": "Tool Declarations and Schema Formats",
                        "content": "To enable tool execution, agents must declare their interfaces to the model. This is structured as a list of tool declarations containing the function name, description, and parameter types formatted as JSON schemas. This schema allows the model to understand the tool's usage, inputs, and constraints.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Custom Tool Definitions\n\n*   **Function Declarations:** JSON schemas defining parameter names, types, and descriptions.\n*   **Return Mapping:** Serializing tool outputs to text strings to inject them back into the model context.\n",
            "interview": "# Interview Prep: Tool Definitions\n\n## Q1: Why are detailed parameter descriptions critical in tool definitions?\n\n### Standard Answer\nTool descriptions are injected directly into the model's system context. The model relies on these descriptions to select the correct tool and construct valid arguments. Vague descriptions lead to incorrect tool selections and invalid arguments.\n",
            "example_code": "def get_tool_schema(name, desc, params):\n    return {\n        \"name\": name,\n        \"description\": desc,\n        \"parameters\": params\n    }\n\nif __name__ == '__main__':\n    print('Tool schema builder configured.')\n",
            "practice_code": "def get_tool_schema(name, desc, params):\n    return {\n        \"name\": name,\n        \"description\": desc,\n        \"parameters\": params\n    }\n\ndef run_practice():\n    schema = get_tool_schema('Calculator', 'Math tool', {'type': 'object'})\n    assert schema['name'] == 'Calculator'\n    assert schema['parameters']['type'] == 'object'\n    print('[PASS] Tool schema extraction validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m2-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary role of the function description in a tool declaration?",
                        "options": ["It tells the LLM when and how to select the tool based on the user's intent.", "It compiles the tool to binary code.", "It encrypts the parameters.", "It specifies the execution rate limit."],
                        "correct_answer": "It tells the LLM when and how to select the tool based on the user's intent.",
                        "explanation": "Function descriptions serve as documentation for the LLM, helping it match user intents to the appropriate tool interfaces."
                    }
                ]
            }
        },
        "ai-agents-m2-t5": {
            "title": "Error Handling & Recovery Loops",
            "notes": {
                "learning_outcomes": [
                    "Explain exception capturing in tool execution loops.",
                    "Formulate feedback-guided recovery traces."
                ],
                "sections": [
                    {
                        "title": "Tool Exception Capture and Injection",
                        "content": "In autonomous pipelines, runtime errors must be handled gracefully. When a tool throws an exception, the system catches the error, formats the traceback, and returns it to the model as an 'Observation'. This provides the model with the error context, allowing it to generate a correction (e.g. correcting a syntax error in an SQL query) in the next iteration.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Error Handling & Recovery\n\n*   **Exception Capture:** Wrapping tool executions to catch errors and prevent crashes.\n*   **Recovery Loops:** Passing tracebacks back to the model as observations to guide corrections.\n",
            "interview": "# Interview Prep: Error Recovery\n\n## Q1: How do we prevent infinite loops when an agent keeps repeating a failing action?\n\n### Standard Answer\nWe implement a retry budget. If the model encounters the same exception repeatedly, the system triggers a hard stop, logs a failure message, and exits the loop to prevent runaway token costs.\n",
            "example_code": "def safe_tool_execute(tool_func, args):\n    try:\n        return tool_func(**args)\n    except Exception as e:\n        return f\"Error during execution: {str(e)}\"\n\nif __name__ == '__main__':\n    print('Safe executor module initialized.')\n",
            "practice_code": "def safe_tool_execute(tool_func, args):\n    try:\n        return tool_func(**args)\n    except Exception as e:\n        return f\"Error during execution: {str(e)}\"\n\ndef run_practice():\n    def failing_tool():\n        raise ValueError(\"Connection failed\")\n    res = safe_tool_execute(failing_tool, {})\n    assert \"ValueError\" in res or \"Connection\" in res\n    print('[PASS] Exception capture safety checks validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "ai-agents-m2-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "How does an agent recover from a tool execution exception in a ReAct loop?",
                        "options": ["By analyzing the formatted error string returned as an Observation and correcting its arguments in the next step.", "By halting execution immediately.", "By reloading the base weights.", "By calling another model."],
                        "correct_answer": "By analyzing the formatted error string returned as an Observation and correcting its arguments in the next step.",
                        "explanation": "Injecting the error message back into the model's context as an observation allows the model to analyze the failure and generate a corrected action."
                    }
                ]
            }
        }
    }

    # Write Module 2 files
    for topic_id, data in m2_data.items():
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

    print("\nSuccessfully generated AI Agents Module 2 files!")

if __name__ == "__main__":
    main()
