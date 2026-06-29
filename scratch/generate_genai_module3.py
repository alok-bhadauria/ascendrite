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

    m3_data = {
        "genai-m3-t1": {
            "title": "LoRA Mathematics",
            "notes": {
                "learning_outcomes": [
                    "Derive Low-Rank Adaptation weight decompositions.",
                    "Formulate scaling multiplier metrics."
                ],
                "sections": [
                    {
                        "title": "LoRA Matrix Decomposition",
                        "content": "To avoid updating billions of parameters during fine-tuning, **Low-Rank Adaptation (LoRA)** freezes the pre-trained weight matrix $\\mathbf{W}_0 \\in \\mathbb{R}^{d \\times k}$ and parameterizes the update using two low-rank matrices $\\mathbf{A} \\in \\mathbb{R}^{r \\times k}$ and $\\mathbf{B} \\in \\mathbb{R}^{d \\times r}$ where rank $r \\ll \\min(d, k)$.\n\nThe forward pass is modified to add this low-rank update scaled by a constant factor:\n\n$$\\mathbf{h} = \\mathbf{W}_0\\mathbf{x} + \\Delta\\mathbf{W}\\mathbf{x} = \\mathbf{W}_0\\mathbf{x} + \\frac{\\alpha}{r} \\mathbf{B}\\mathbf{A}\\mathbf{x}$$\n\nwhere $\\alpha$ is a scaling hyperparameter that controls the magnitude of the adapter's influence. Matrix $\\mathbf{A}$ is initialized using a Gaussian distribution, while $\\mathbf{B}$ is initialized to zero, ensuring $\\Delta\\mathbf{W} = 0$ at the start of training.",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Zero Inference Latency",
                                "content": "During deployment, the low-rank updates can be merged back into the base weights: $\\mathbf{W}_{merged} = \\mathbf{W}_0 + \\frac{\\alpha}{r} \\mathbf{B}\\mathbf{A}$. This folds the adapter weights directly into the base matrices, yielding zero additional inference latency."
                            }
                        ]
                    }
                ]
            },
            "revision": "# LoRA Mathematics\n\n$$\\mathbf{h} = \\mathbf{W}_0\\mathbf{x} + \\frac{\\alpha}{r} \\mathbf{B}\\mathbf{A}\\mathbf{x}$$\n$$\\mathbf{W}_{merged} = \\mathbf{W}_0 + \\frac{\\alpha}{r} \\mathbf{B}\\mathbf{A}$$\n",
            "interview": "# Interview Prep: LoRA Math\n\n## Q1: Prove mathematically how LoRA reduces parameter storage during training for a layer of size d x d with rank r.\n\n### Standard Answer\nFor a matrix of size $d \\times d$, the number of parameters is $d^2$. Under LoRA, the low-rank decomposition matrices $\\mathbf{A}$ and $\\mathbf{B}$ have dimensions $r \\times d$ and $d \\times r$ respectively, requiring $2 r d$ parameters. If $d = 4096$ and $r = 8$, standard tuning requires $16.7 \\times 10^6$ parameters, while LoRA requires only $2 \\times 8 \\times 4096 = 65,536$ parameters, a $99.6\\%$ reduction in parameter updates.\n",
            "example_code": "import numpy as np\n\ndef lora_forward(x, W0, A, B, alpha=16, r=8):\n    h0 = np.dot(x, W0)\n    h_lora = np.dot(np.dot(x, A), B) * (alpha / r)\n    return h0 + h_lora\n\nif __name__ == '__main__':\n    print('LoRA equations configured.')\n",
            "practice_code": "import numpy as np\n\ndef lora_forward(x, W0, A, B, alpha=16, r=8):\n    h0 = np.dot(x, W0)\n    h_lora = np.dot(np.dot(x, A), B) * (alpha / r)\n    return h0 + h_lora\n\ndef run_practice():\n    x = np.array([1.0, 1.0])\n    W0 = np.zeros((2, 2))\n    A = np.array([[1.0, 0.0], [0.0, 1.0]])\n    B = np.array([[1.0, 0.0], [0.0, 1.0]])\n    out = lora_forward(x, W0, A, B, 8, 8)\n    assert np.allclose(out, x)\n    print('[PASS] LoRA forward calculations verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m3-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the key benefit of LoRA's parameterization structure during model serving?",
                        "options": ["The adapter weights can be pre-merged with the base weights, yielding zero additional inference latency.", "It makes the model immune to quantization loss.", "It increases context window sizes.", "It bypasses tokenization steps."],
                        "correct_answer": "The adapter weights can be pre-merged with the base weights, yielding zero additional inference latency.",
                        "explanation": "Because the update is linear, W_merged = W0 + (alpha/r)*B*A can be pre-computed, eliminating runtime overhead."
                    }
                ]
            }
        },
        "genai-m3-t2": {
            "title": "QLoRA & Double Quantization",
            "notes": {
                "learning_outcomes": [
                    "Explain NormalFloat4 (NF4) quantization formats.",
                    "Formulate Double Quantization memory savings calculations."
                ],
                "sections": [
                    {
                        "title": "NormalFloat4 (NF4) Quantization",
                        "content": "QLoRA reduces the memory footprint of fine-tuning by quantizing the base model weights to 4-bit representation while training 16-bit LoRA adapter parameters. It introduces **NormalFloat4 (NF4)**, an information-theoretically optimal quantization scheme for normally distributed data.\n\nNF4 maps base weights to 16 quantization bins containing equal probability areas under a standard normal distribution $\\mathcal{N}(0, 1)$. This preserves model capacity better than standard 4-bit integer formats.",
                        "callouts": []
                    },
                    {
                        "title": "Double Quantization Mechanics",
                        "content": "To compress memory usage further, QLoRA implements **Double Quantization (DQ)**. Quantization scale factors are typically stored as 32-bit floats for each block of 64 weights. Double Quantization treats these scale factors as inputs to a second 8-bit quantization pass, reducing scale storage overhead from 32 bits to 8 bits, saving an additional 0.37 bits per parameter.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# QLoRA & NF4\n\n*   **NF4:** Quantization bins designed to carry equal information density for normally distributed weights.\n*   **Double Quantization (DQ):** Quantizes the scales of the base quantization block, compressing storage requirements.\n",
            "interview": "# Interview Prep: QLoRA\n\n## Q1: Explain how NormalFloat4 (NF4) achieves higher accuracy than standard FP4 quantization.\n\n### Standard Answer\nBase model weights are normally distributed. Standard FP4 has fixed intervals, which allocates too many bits to low-probability values in the tails and saturates values near the mean. NF4 creates quantiles with equal probability density, ensuring that each bin carries equal information.\n",
            "example_code": "import numpy as np\n\ndef quantize_nf4(w, scale):\n    return w / scale\n\nif __name__ == '__main__':\n    print('QLoRA helpers active.')\n",
            "practice_code": "import numpy as np\n\ndef quantize_nf4(w, scale):\n    return w / scale\n\ndef run_practice():\n    assert quantize_nf4(10.0, 5.0) == 2.0\n    print('[PASS] NF4 scaling checks completed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m3-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary role of Double Quantization in QLoRA?",
                        "options": ["To quantize the quantization constants (scales) of the first quantization pass, further reducing memory usage.", "To compile model matrices twice.", "To double the learning rate.", "To split attention heads."],
                        "correct_answer": "To quantize the quantization constants (scales) of the first quantization pass, further reducing memory usage.",
                        "explanation": "Double Quantization treats the scale factors as inputs to a second quantization pass, reducing the footprint of scaling factors from 32-bit floats to 8-bit integers."
                    }
                ]
            }
        },
        "genai-m3-t3": {
            "title": "Prompt & Prefix Tuning",
            "notes": {
                "learning_outcomes": [
                    "Compare virtual token prefix insertion with LoRA.",
                    "Formulate attention matrix modifications."
                ],
                "sections": [
                    {
                        "title": "Prompt Tuning and Prefix Tuning",
                        "content": "Prompt Tuning and Prefix Tuning are early parameter-efficient fine-tuning architectures:\n\n*   **Prompt Tuning:** Prepends $K$ trainable continuous embedding vectors ('virtual tokens') directly to the input sequence embeddings: $\\mathbf{X}_{tuned} = [\\mathbf{P}_{embed}; \\mathbf{X}]$. Only these prefix tokens are updated during training. While simple, prompt tuning struggles to converge for models under 10 billion parameters.\n*   **Prefix Tuning:** Prepends trainable key ($\\mathbf{P}_K$) and value ($\\mathbf{P}_V$) activations to the attention matrices at every transformer layer, modifying the attention calculation directly:\n\n$$\\text{Attention}(\\mathbf{Q}, [\\mathbf{P}_K; \\mathbf{K}], [\\mathbf{P}_V; \\mathbf{V}])$$\n\nThis provides more stable training convergence across various model scales.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Prompt & Prefix Tuning\n\n*   **Prompt Tuning:** Adds virtual tokens to sequence inputs: $\\mathbf{X}_{tuned} = [\\mathbf{P}_{embed}; \\mathbf{X}]$.\n*   **Prefix Tuning:** Prepend continuous key-value states to attention computation steps: $\\mathbf{K}_{new} = [\\mathbf{P}_K; \\mathbf{K}]$.\n",
            "interview": "# Interview Prep: Prefix Tuning\n\n## Q1: How does Prefix Tuning bypass context window limits compared to standard prompting?\n\n### Standard Answer\nIn standard prompting, virtual tokens are passed as inputs, consuming space in the context window. In prefix tuning, the prefixes are injected directly into the attention layers, bypassing the context window constraint.\n",
            "example_code": "import numpy as np\n\ndef prefix_tune_attention_keys(keys, prefix_keys):\n    return np.concatenate([prefix_keys, keys], axis=0)\n\nif __name__ == '__main__':\n    print('Prefix tuning vectors configured.')\n",
            "practice_code": "import numpy as np\n\ndef prefix_tune_attention_keys(keys, prefix_keys):\n    return np.concatenate([prefix_keys, keys], axis=0)\n\ndef run_practice():\n    k = np.array([[1.0]])\n    pk = np.array([[2.0]])\n    merged = prefix_tune_attention_keys(k, pk)\n    assert np.allclose(merged, np.array([[2.0], [1.0]]))\n    print('[PASS] Prefix tuning key injection validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m3-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Which vectors are modified in Prefix Tuning?",
                        "options": ["Key and Value vectors in the attention computation.", "Query vectors only.", "Vocabulary indices.", "Loss function scale factors."],
                        "correct_answer": "Key and Value vectors in the attention computation.",
                        "explanation": "Prefix tuning prepends learnable prefix vectors to the key (K) and value (V) matrices at every layer of the network."
                    }
                ]
            }
        },
        "genai-m3-t4": {
            "title": "Bottleneck Adapters",
            "notes": {
                "learning_outcomes": [
                    "Explain residual bottleneck adapter configurations.",
                    "Formulate latency scaling equations."
                ],
                "sections": [
                    {
                        "title": "Bottleneck Projection Layers",
                        "content": "Bottleneck adapters are small feedforward networks inserted after multi-head self-attention and MLP blocks. They project activations $\\mathbf{h}$ to a low-dimensional bottleneck space using down-projection weights $\\mathbf{W}_D \\in \\mathbb{R}^{d \\times m}$ (where $m \\ll d$), apply a non-linear activation, and project them back using up-projection weights $\\mathbf{W}_U \\in \\mathbb{R}^{m \\times d}$, adding a residual connection:\n\n$$\\mathbf{h}_{new} = \\mathbf{h} + f(\\mathbf{h}\\mathbf{W}_D)\\mathbf{W}_U$$",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Bottleneck Adapters\n\n$$\\mathbf{h}_{new} = \\mathbf{h} + f(\\mathbf{h}\\mathbf{W}_{down})\\mathbf{W}_{up}$$\n",
            "interview": "# Interview Prep: Bottleneck Adapters\n\n## Q1: Why do sequential adapters introduce higher inference latency compared to LoRA adapters?\n\n### Standard Answer\nLoRA updates can be folded back into the base weights during compilation, resulting in zero latency overhead. Sequential adapters add feedforward layers to the execution graph, preventing weight folding and adding compute overhead at each layer.\n",
            "example_code": "import numpy as np\n\ndef bottleneck_adapter(h, W_down, W_up):\n    down = np.dot(h, W_down)\n    activated = np.maximum(0.0, down)\n    return h + np.dot(activated, W_up)\n\nif __name__ == '__main__':\n    print('Bottleneck adapter module ready.')\n",
            "practice_code": "import numpy as np\n\ndef bottleneck_adapter(h, W_down, W_up):\n    down = np.dot(h, W_down)\n    activated = np.maximum(0.0, down)\n    return h + np.dot(activated, W_up)\n\ndef run_practice():\n    h = np.array([1.0, 1.0])\n    W_down = np.zeros((2, 1))\n    W_up = np.zeros((1, 2))\n    out = bottleneck_adapter(h, W_down, W_up)\n    assert np.allclose(out, h)\n    print('[PASS] Bottleneck zero projection verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m3-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the role of the down-projection layer W_down in a bottleneck adapter?",
                        "options": ["To project activations into a low-dimensional bottleneck space, reducing parameter counts.", "To double the output dimensions.", "To replace self-attention blocks.", "To initialize weights."],
                        "correct_answer": "To project activations into a low-dimensional bottleneck space, reducing parameter counts.",
                        "explanation": "W_down projects the model activations (dimension d) to a smaller bottleneck size (m), minimizing parameter counts."
                    }
                ]
            }
        },
        "genai-m3-t5": {
            "title": "Memory Optimization in Fine-Tuning",
            "notes": {
                "learning_outcomes": [
                    "Explain Gradient Checkpointing memory trade-offs.",
                    "Formulate activation storage size boundaries."
                ],
                "sections": [
                    {
                        "title": "The Backpropagation Memory Bottleneck",
                        "content": "Standard backpropagation requires storing activation states computed during the forward pass in RAM. In deep networks, this creates a memory bottleneck, as storing activation matrices scales linearly with layer count $L$.",
                        "callouts": []
                    },
                    {
                        "title": "Gradient Checkpointing Mechanics",
                        "content": "**Gradient Checkpointing** optimizes this memory footprint by storing activations at only a subset of layers ('checkpoints'). During the backward pass, missing activations are re-computed dynamically from the nearest preceding checkpoint. \n\nBy placing checkpoints at every $\\sqrt{L}$ layers, the model stores exactly $\\sqrt{L}$ activations. During the backward pass, computing gradients for a segment requires storing an additional $\\sqrt{L}$ temporary activations. This reduces peak memory usage from $\\mathcal{O}(L)$ to $\\mathcal{O}(\\sqrt{L})$, trading a 30% increase in compute cost for up to a 70% decrease in peak GPU memory usage.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Memory Optimization\n\n*   **Standard Backprop:** Stores all activation matrices: memory $\\mathcal{O}(L)$.\n*   **Gradient Checkpointing:** Stores $\\sqrt{L}$ activations, re-computing intermediate steps: memory $\\mathcal{O}(\\sqrt{L})$.\n",
            "interview": "# Interview Prep: Memory Optimizations\n\n## Q1: Prove how storing activations at the boundary of every N layers reduces memory scaling to square root boundaries.\n\n### Standard Answer\nLet $L$ be the number of layers. By setting checkpoints at every $\\sqrt{L}$ layers, the model stores exactly $\\sqrt{L}$ checkpoint activations. During backpropagation, we compute gradients for a segment of size $\\sqrt{L}$ layers, requiring an additional $\\sqrt{L}$ temporary activation stores. The maximum memory footprint scales as $2\\sqrt{L} = \\mathcal{O}(\\sqrt{L})$ rather than $\\mathcal{O}(L)$.\n",
            "example_code": "def compute_checkpoint_mem(n_layers, acts_per_layer):\n    std_mem = n_layers * acts_per_layer\n    check_mem = 2 * int(n_layers ** 0.5) * acts_per_layer\n    return std_mem, check_mem\n\nif __name__ == '__main__':\n    print('Checkpoint memory estimation loaded.')\n",
            "practice_code": "def compute_checkpoint_mem(n_layers, acts_per_layer):\n    std_mem = n_layers * acts_per_layer\n    check_mem = 2 * int(n_layers ** 0.5) * acts_per_layer\n    return std_mem, check_mem\n\ndef run_practice():\n    std, check = compute_checkpoint_mem(100, 10)\n    assert std == 1000\n    assert check == 200\n    print('[PASS] Checkpoint memory scale calculation verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m3-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary trade-off when enabling Gradient Checkpointing during fine-tuning?",
                        "options": ["It reduces peak memory usage but increases total compute time by approximately 30%.", "It increases memory footprint.", "It restricts the model to 2 heads.", "It requires retraining the base tokenizer."],
                        "correct_answer": "It reduces peak memory usage but increases total compute time by approximately 30%.",
                        "explanation": "Because missing activations must be re-computed during the backward pass, the compute overhead increases by roughly 30%."
                    }
                ]
            }
        }
    }

    # Write files
    for topic_id, data in m3_data.items():
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

    print("\nSuccessfully generated enriched GenAI Module 3 files!")

if __name__ == "__main__":
    main()
