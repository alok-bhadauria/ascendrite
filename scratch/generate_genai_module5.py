import os
import json

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    genai_dir = os.path.join(base_dir, "knowledge-base", "ai", "genai")

    m5_data = {
        "genai-m5-t1": {
            "title": "Continuous Batching & Speculative Decoding",
            "notes": {
                "learning_outcomes": [
                    "Explain Continuous Batching iteration-level scheduling.",
                    "Formulate Speculative Decoding draft-target verification steps."
                ],
                "sections": [
                    {
                        "title": "Continuous Batching (Iteration-Level Scheduling)",
                        "content": "Static batching requires all sequences in a batch to finish generation before processing a new batch, causing compute idle time due to sequence length variance. \n\n**Continuous Batching** schedules tasks at the iteration level, inserting new requests as soon as a sequence completes. This minimizes idle resources and maximizes GPU utilization.",
                        "callouts": []
                    },
                    {
                        "title": "Speculative Decoding Mathematics",
                        "content": "**Speculative Decoding** accelerates generation without losing accuracy by using a small draft model to speculate $K$ future tokens. The target model validates them in parallel in a single forward pass.\n\nA speculated token $x$ is accepted with probability:\n\n$$P_{accept} = \\min\\left(1.0, \\frac{P_{target}(x \\mid context)}{P_{draft}(x \\mid context)}\\right)$$\n\nIf the token is rejected, we sample a replacement token from the normalized difference distribution: $\\text{softmax}(\\max(0, P_{target}(x) - P_{draft}(x)))$, guaranteeing that outputs are mathematically identical to the target model.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Speculative Decoding\n\n*   **Core Principle:** Draft model generates candidate tokens; target model validates them in a single batch forward pass.\n*   **Acceptance Probability:** \n    \n    $$\\alpha = \\min\\left(1.0, \\frac{P_{\\text{target}}(x)}{P_{\\text{draft}}(x)}\\right)$$\n",
            "interview": "# Interview Prep: Serving Optimizations\n\n## Q1: How does Speculative Decoding accelerate inference without altering output distributions?\n\n### Standard Answer\nThe acceptance probability step guarantees that the output distribution matches the target model exactly. If a draft token is rejected, we sample a new token from the normalized difference distribution, ensuring no loss in quality.\n",
            "example_code": "import numpy as np\n\ndef verify_speculative_token(p_target, p_draft):\n    ratio = p_target / p_draft if p_draft > 0 else 0.0\n    return float(np.minimum(1.0, ratio))\n\nif __name__ == '__main__':\n    print('Speculative decoding modules loaded.')\n",
            "practice_code": "import numpy as np\n\ndef verify_speculative_token(p_target, p_draft):\n    ratio = p_target / p_draft if p_draft > 0 else 0.0\n    return float(np.minimum(1.0, ratio))\n\ndef run_practice():\n    assert verify_speculative_token(0.8, 0.4) == 1.0\n    assert verify_speculative_token(0.2, 0.4) == 0.5\n    print('[PASS] Speculative decoding verification scores checked.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m5-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary constraint governing continuous batching schedules?",
                        "options": ["Iteration-level (token-level) job insertion and deletion, preventing idle resource waits.", "Static padding rules.", "Removing positional embeddings.", "The learning rate shape."],
                        "correct_answer": "Iteration-level (token-level) job insertion and deletion, preventing idle resource waits.",
                        "explanation": "Continuous batching schedules execution steps dynamically at each token step, bypassing block boundaries."
                    }
                ]
            }
        },
        "genai-m5-t2": {
            "title": "PagedAttention & vLLM",
            "notes": {
                "learning_outcomes": [
                    "Explain PagedAttention virtual memory block maps.",
                    "Formulate KV Cache block allocation equations."
                ],
                "sections": [
                    {
                        "title": "KV Cache Fragmentation and PagedAttention",
                        "content": "Traditional KV Cache allocation requires continuous memory blocks allocated for the maximum sequence length. This leads to severe memory fragmentation (wasting up to 60-80% of RAM). \n\n**PagedAttention** solves this by partitioning the KV Cache into fixed-size physical blocks, mapping them to virtual blocks using a page table. This eliminates fragmentation and allows KV caches to be shared across requests.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# PagedAttention\n\n*   **Virtual Block Table:** Translates logical sequence positions to physical GPU memory addresses.\n*   **Benefit:** Reduces memory fragmentation to under 4%, increasing maximum batch sizes.\n",
            "interview": "# Interview Prep: PagedAttention\n\n## Q1: Explain how PagedAttention enables memory sharing during parallel generation tasks (like beam search).\n\n### Standard Answer\nDuring beam search, different candidate paths share a common prefix. PagedAttention maps the logical blocks of these paths to the same physical memory block. The block is duplicated only when a write operation occurs (Copy-on-Write), saving memory.\n",
            "example_code": "class VirtualBlockTable:\n    def __init__(self):\n        self.table = {}\n    def allocate_page(self, logical_idx, physical_idx):\n        self.table[logical_idx] = physical_idx\n    def get_physical(self, logical_idx):\n        return self.table.get(logical_idx, -1)\n\nif __name__ == '__main__':\n    print('Virtual page table initialized.')\n",
            "practice_code": "class VirtualBlockTable:\n    def __init__(self):\n        self.table = {}\n    def allocate_page(self, logical_idx, physical_idx):\n        self.table[logical_idx] = physical_idx\n    def get_physical(self, logical_idx):\n        return self.table.get(logical_idx, -1)\n\ndef run_practice():\n    pt = VirtualBlockTable()\n    pt.allocate_page(10, 1024)\n    assert pt.get_physical(10) == 1024\n    assert pt.get_physical(20) == -1\n    print('[PASS] PagedAttention virtual translations validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m5-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary memory waste category resolved by PagedAttention?",
                        "options": ["Internal and external physical block memory fragmentation.", "Embedding matrix footprint size.", "The gradient scaling factor.", "Causal masking matrices."],
                        "correct_answer": "Internal and external physical block memory fragmentation.",
                        "explanation": "By breaking cache allocation into small, non-contiguous blocks, PagedAttention eliminates the need for continuous allocation."
                    }
                ]
            }
        },
        "genai-m5-t3": {
            "title": "Post-Training Quantization",
            "notes": {
                "learning_outcomes": [
                    "Explain GPTQ second-order Taylor expansion math.",
                    "Formulate Activation-aware Weight Quantization (AWQ) channels."
                ],
                "sections": [
                    {
                        "title": "Quantization Error Minimization and GPTQ",
                        "content": "Post-Training Quantization (PTQ) compresses model parameters without requiring retraining. **GPTQ** models quantization as a quadratic error minimization problem. It uses the inverse Hessian matrix $\\mathbf{H}^{-1}$ to adjust remaining weights to compensate for quantization errors:\n\n$$\\Delta \\mathbf{w} = -\\frac{w_i - \\text{quant}(w_i)}{[\\mathbf{H}^{-1}]_{ii}} \\mathbf{H}^{-1}_{:, i}$$\n\nThis updates weight matrices column by column, preserving model capacity even at 4-bit configurations.",
                        "callouts": []
                    },
                    {
                        "title": "Activation-aware Weight Quantization (AWQ)",
                        "content": "**AWQ (Activation-aware Weight Quantization)** protects the top 1% of salient channels (which carry the most information during inference) from heavy quantization. Instead of quantizing them directly, AWQ scales these channels up before quantization, protecting them from rounding errors and preserving model performance.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Post-Training Quantization\n\n*   **GPTQ:** Minimizes quadratic quantization error using inverse Hessians.\n*   **AWQ:** Protects the top 1% of salient channels by scaling, quantizing the remaining channels to 4 bits.\n",
            "interview": "# Interview Prep: Quantization\n\n## Q1: Why do outliers in activation distributions cause high quantization loss in simple integer quantization (e.g. INT8)?\n\n### Standard Answer\nSimple quantization maps the maximum absolute activation to the maximum integer range. If outliers are present, the scaling factor is distorted, forcing the bulk of standard activations to compress into a few bins, destroying representation detail.\n",
            "example_code": "import numpy as np\n\ndef compute_awq_scale(weights, activation_magnitudes, alpha=0.5):\n    return weights * (activation_magnitudes ** alpha)\n\nif __name__ == '__main__':\n    print('AWQ scale shifting functions active.')\n",
            "practice_code": "import numpy as np\n\ndef compute_awq_scale(weights, activation_magnitudes, alpha=0.5):\n    return weights * (activation_magnitudes ** alpha)\n\ndef run_practice():\n    w = np.array([1.0, 1.0])\n    m = np.array([4.0, 1.0])\n    scale = compute_awq_scale(w, m, 0.5)\n    assert np.allclose(scale, np.array([2.0, 1.0]))\n    print('[PASS] AWQ scaling calculations verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m5-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the core mathematical mechanism behind GPTQ updates?",
                        "options": ["Using the inverse Hessian matrix to adjust remaining weights to compensate for quantization error.", "Replacing weights with random values.", "Converting models to ASCII format.", "Dropping attention layers."],
                        "correct_answer": "Using the inverse Hessian matrix to adjust remaining weights to compensate for quantization error.",
                        "explanation": "GPTQ solves the quadratic error minimization task using the inverse Hessian matrix, updating parameter matrices row by row."
                    }
                ]
            }
        },
        "genai-m5-t4": {
            "title": "Triton Inference Server",
            "notes": {
                "learning_outcomes": [
                    "Explain Triton concurrency and dynamic batching.",
                    "Formulate dynamic batch queue schedulers."
                ],
                "sections": [
                    {
                        "title": "Enterprise Serving with Triton",
                        "content": "Triton Inference Server optimizes GPU utilization by running multiple model instances in parallel. It implements a dynamic batch scheduler that queues incoming inference requests and groups them into batches dynamically, maximizing throughput while respecting SLA latency bounds.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Triton Inference Server\n\n*   **Dynamic Batching:** Groups independent requests into a single batch to maximize GPU memory bandwidth.\n*   **Concurrent Execution:** Runs multiple models (or model instances) in parallel on the same GPU.\n",
            "interview": "# Interview Prep: Triton Serving\n\n## Q1: How does Triton's dynamic batching scheduler balance throughput and latency SLAs?\n\n### Standard Answer\nTriton uses two parameters: `max_queue_delay_microseconds` and `max_batch_size`. The scheduler waits for incoming requests until either the maximum batch size is reached or the queue delay threshold is exceeded, guaranteeing latency bounds.\n",
            "example_code": "class TritonScheduler:\n    def __init__(self, max_batch=4):\n        self.queue = []\n        self.max_batch = max_batch\n    def add_request(self, req):\n        self.queue.append(req)\n    def get_batch(self):\n        batch = self.queue[:self.max_batch]\n        self.queue = self.queue[self.max_batch:]\n        return batch\n\nif __name__ == '__main__':\n    print('Triton simulation scheduler configured.')\n",
            "practice_code": "class TritonScheduler:\n    def __init__(self, max_batch=4):\n        self.queue = []\n        self.max_batch = max_batch\n    def add_request(self, req):\n        self.queue.append(req)\n    def get_batch(self):\n        batch = self.queue[:self.max_batch]\n        self.queue = self.queue[self.max_batch:]\n        return batch\n\ndef run_practice():\n    sc = TritonScheduler(2)\n    sc.add_request('r1')\n    sc.add_request('r2')\n    sc.add_request('r3')\n    b1 = sc.get_batch()\n    assert len(b1) == 2\n    assert sc.queue == ['r3']\n    print('[PASS] Triton queue scheduler simulations checked.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m5-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What does a high 'max_queue_delay_microseconds' setting indicate for Triton throughput?",
                        "options": ["It increases GPU utilization and batch sizes but increases latency for individual requests.", "It disables execution queues.", "It reduces throughput to zero.", "It replaces the model scheduler."],
                        "correct_answer": "It increases GPU utilization and batch sizes but increases latency for individual requests.",
                        "explanation": "Allowing the queue to wait longer increases the probability of forming large batches, maximizing GPU compute density."
                    }
                ]
            }
        },
        "genai-m5-t5": {
            "title": "Guardrails & Safety Serving",
            "notes": {
                "learning_outcomes": [
                    "Explain toxicity logit check alignments.",
                    "Formulate LlamaGuard classification templates."
                ],
                "sections": [
                    {
                        "title": "Model Guardrails",
                        "content": "To prevent models from generating toxic, illegal, or harmful content, serving architectures implement guardrails. LlamaGuard is a fine-tuned model trained to classify user queries and generated outputs. If the guardrail classifies the output as unsafe, the serving API overrides the response with a pre-configured refusal message.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Guardrails & Safety Serving\n\n*   **LlamaGuard:** Evaluates prompts/responses against safety policies.\n*   **Input Guardrail:** Intercepts malicious prompts before model execution.\n*   **Output Guardrail:** Validates generated text before returning it to the user.\n",
            "interview": "# Interview Prep: Guardrails\n\n## Q1: Why are guardrail models preferred over simple string regex filters for safety validation?\n\n### Standard Answer\nRegex filters check for exact substring matches, which are easily bypassed by character modifications or subtle phrasing. Guardrail models leverage semantic representation capabilities to detect implicit toxicity and adversarial prompts.\n",
            "example_code": "def evaluate_safety_logits(logits, toxic_indices, threshold=0.5):\n    toxic_activation = logits[toxic_indices]\n    return 'unsafe' if np.any(toxic_activation > threshold) else 'safe'\n\nif __name__ == '__main__':\n    print('Safety logit checks configured.')\n",
            "practice_code": "import numpy as np\n\ndef evaluate_safety_logits(logits, toxic_indices, threshold=0.5):\n    toxic_activation = logits[toxic_indices]\n    return 'unsafe' if np.any(toxic_activation > threshold) else 'safe'\n\ndef run_practice():\n    logits = np.array([0.1, 0.9])\n    res = evaluate_safety_logits(logits, [1], 0.5)\n    assert res == 'unsafe'\n    print('[PASS] Safety logits validation checks completed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m5-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Where are output guardrail checks executed in a production API serving pipeline?",
                        "options": ["After token generation is complete but before the text is returned to the user.", "Before the token embedding projection step.", "During the weight quantization pass.", "Only in the training loop."],
                        "correct_answer": "After token generation is complete but before the text is returned to the user.",
                        "explanation": "Output guardrails intercept generated tokens, evaluating them against safety policies before serving them to the client."
                    }
                ]
            }
        }
    }

    # Write files
    for topic_id, data in m5_data.items():
        module_num = topic_id.split("-")[1]
        
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
        write_file(os.path.join(genai_dir, "notes", f"{topic_id}.json"), json.dumps(notes_content, indent=2))
        write_file(os.path.join(genai_dir, "revision", f"{topic_id}.md"), data["revision"])
        write_file(os.path.join(genai_dir, "interview", f"{topic_id}.md"), data["interview"])
        write_file(os.path.join(genai_dir, "examples", f"{topic_id}-ex1.py"), data["example_code"])
        write_file(os.path.join(genai_dir, "practice", f"{topic_id}-prac1.py"), data["practice_code"])
        write_file(os.path.join(genai_dir, "quiz", f"{topic_id}-quiz.json"), json.dumps(data["quiz"], indent=2))

    print("\nSuccessfully generated enriched GenAI Module 5 files!")

if __name__ == "__main__":
    main()
