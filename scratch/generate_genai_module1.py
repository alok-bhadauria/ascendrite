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

    m1_data = {
        "genai-m1-t1": {
            "title": "Generative Model Taxonomies",
            "notes": {
                "learning_outcomes": [
                    "Compare autoregressive decoder-only architectures with encoder-decoder configurations.",
                    "Formulate RMSNorm mathematical steps and contrast them with standard LayerNorm.",
                    "Derive SwiGLU activation function formulations."
                ],
                "sections": [
                    {
                        "title": "Generative Architecture Configurations",
                        "content": "Large Language Models generally follow either a decoder-only (e.g. GPT, LLaMA) or encoder-decoder (e.g. T5, BART) configuration.\n\n*   **Decoder-only Models:** Focus strictly on left-to-right next-token probability prediction (autoregressive), utilizing causal masking to block queries from looking ahead. They are highly optimized for generative text completion tasks.\n*   **Encoder-decoder Models:** Encode the full bidirectional context first and pass it to a causal decoder via cross-attention. This is useful for sequence-to-sequence translation, summarization, and comprehension tasks where the full input context must be analyzed bidirectional before generation starts.",
                        "callouts": []
                    },
                    {
                        "title": "RMSNorm and SwiGLU Derivations",
                        "content": "To optimize inference latency, modern architectures replace standard LayerNorm with **Root Mean Square Normalization (RMSNorm)**. RMSNorm scales activation vectors by their root mean square value, bypassing mean subtraction computation steps:\n\n$$\\text{RMSNorm}(\\mathbf{a}) = \\frac{\\mathbf{a}}{\\text{RMS}(\\mathbf{a})} \\odot \\mathbf{g}$$\n\nwhere $\\text{RMS}(\\mathbf{a}) = \\sqrt{\\frac{1}{d} \\sum_{i=1}^d a_i^2 + \\epsilon}$ and $\\mathbf{g}$ is a learnable scaling vector. This reduces memory bandwidth overhead by avoiding two sequential passes over data.\n\nAdditionally, feedforward blocks replace ReLU with **SwiGLU** activation functions. SwiGLU is a Gated Linear Unit (GLU) variation:\n\n$$\\text{SwiGLU}(\\mathbf{x}) = \\left( \\mathbf{x}\\mathbf{W}_1 \\odot \\text{swish}(\\mathbf{x}\\mathbf{W}_2) \\right) \\mathbf{W}_3$$\n\nwhere $\\text{swish}(\\mathbf{z}) = \\mathbf{z} \\odot \\sigma(\\beta \\mathbf{z})$ is the Swish activation. The gate mechanism improves optimization convergence during gradient updates.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Generative Model Taxonomies\n\n## 1. RMSNorm\n$$\\text{RMSNorm}(\\mathbf{a}) = \\frac{\\mathbf{a}}{\\sqrt{\\frac{1}{d} \\sum_{i=1}^d a_i^2 + \\epsilon}} \\odot \\mathbf{g}$$\n\n## 2. SwiGLU\n$$\\text{SwiGLU}(\\mathbf{x}) = (\\mathbf{x}\\mathbf{W}_1 \\odot \\text{swish}(\\mathbf{x}\\mathbf{W}_2)) \\mathbf{W}_3$$\n",
            "interview": "# Interview Prep: Generative Taxonomies\n\n## Q1: Why does RMSNorm perform faster in training and inference loops than standard LayerNorm?\n\n### Standard Answer\nLayerNorm requires calculating both the mean and variance of activation vectors, which requires two passes over the data (mean pass and variance pass). RMSNorm assumes a mean of zero, requiring only a single pass to compute the root mean square, which saves memory bandwidth and GPU core cycles.\n",
            "example_code": "import numpy as np\n\ndef rmsnorm(x, g, eps=1e-6):\n    rms = np.sqrt(np.mean(x**2, axis=-1, keepdims=True) + eps)\n    return (x / rms) * g\n\nif __name__ == '__main__':\n    print('RMSNorm configured.')\n",
            "practice_code": "import numpy as np\n\ndef rmsnorm(x, g, eps=1e-6):\n    rms = np.sqrt(np.mean(x**2, axis=-1, keepdims=True) + eps)\n    return (x / rms) * g\n\ndef run_practice():\n    x = np.array([[1.0, 1.0]])\n    g = np.array([2.0, 2.0])\n    out = rmsnorm(x, g)\n    assert np.allclose(out, np.array([[2.0, 2.0]]))\n    print('[PASS] RMSNorm checks completed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m1-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the principal difference between RMSNorm and LayerNorm?",
                        "options": ["RMSNorm bypasses mean subtraction, computing normalized scores using root mean square scaling only.", "RMSNorm adds a soft-thresholding parameter.", "RMSNorm operates strictly in the frequency domain.", "LayerNorm is always slow and cannot be parallelized."],
                        "correct_answer": "RMSNorm bypasses mean subtraction, computing normalized scores using root mean square scaling only.",
                        "explanation": "RMSNorm simplifies normalization by scaling activations by their root mean square value, assuming a mean of 0.0, which eliminates one traversal pass over inputs."
                    }
                ]
            }
        },
        "genai-m1-t2": {
            "title": "Attention Optimizations",
            "notes": {
                "learning_outcomes": [
                    "Explain the memory bandwidth bottleneck of KV caching during decoding.",
                    "Contrast MQA and GQA configurations."
                ],
                "sections": [
                    {
                        "title": "The KV Cache Bottleneck",
                        "content": "Autoregressive generation requires storing key and value states of past tokens in RAM to avoid re-computing them at each generation iteration. This is called the **KV Cache**. While it saves compute, the KV Cache footprint is huge, scaling linearly with layer count, head count, batch size, and sequence length. \n\nAt large sequence lengths, serving models becomes bounded by memory bandwidth rather than GPU floating-point operations (FLOPs), as loading the large KV cache matrices from GPU VRAM to local SRAM limits performance.",
                        "callouts": []
                    },
                    {
                        "title": "MQA and GQA Solutions",
                        "content": "To reduce the KV cache size, modern architectures use alternative attention structures:\n\n*   **Multi-Query Attention (MQA):** Shares a single key-value head across all query heads. This drastically reduces the KV cache size (by a factor equal to the number of query heads, e.g., 32x), accelerating inference throughput, but it degrades model capacity and accuracy.\n*   **Grouped-Query Attention (GQA):** Combines MHA accuracy with MQA speed by grouping query heads into partitions. Each partition shares a key-value head. If $H$ query heads are grouped into $G$ groups, the KV cache size is reduced by $H/G$. This balances the trade-off, maintaining model accuracy close to MHA while accelerating inference speeds.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Attention Optimizations\n\n*   **Multi-Head Attention (MHA):** $H$ query heads, $H$ key-value heads.\n*   **Multi-Query Attention (MQA):** $H$ query heads, 1 key-value head.\n*   **Grouped-Query Attention (GQA):** $H$ query heads grouped into $G$ groups, sharing $G$ key-value heads.\n",
            "interview": "# Interview Prep: Attention Optimizations\n\n## Q1: How does Grouped-Query Attention (GQA) balance the trade-off between MHA accuracy and MQA inference speeds?\n\n### Standard Answer\nMQA achieves maximum throughput by reducing KV cache sizes to a single head, but it degrades model capacity and accuracy. GQA generalizes this by introducing a group parameter $G$. If $G=8$ and $H=64$, 8 query heads share a key-value head. This yields 8x memory savings over MHA while maintaining comparable generation quality.\n",
            "example_code": "import numpy as np\n\ndef repeat_kv(kv_heads, n_rep):\n    return np.repeat(kv_heads, n_rep, axis=2)\n\nif __name__ == '__main__':\n    print('GQA repeat function ready.')\n",
            "practice_code": "import numpy as np\n\ndef repeat_kv(kv_heads, n_rep):\n    return np.repeat(kv_heads, n_rep, axis=2)\n\ndef run_practice():\n    kv = np.array([[[[1.0], [2.0]]]]) # shape (1,1,2,1)\n    rep = repeat_kv(kv, 2)\n    assert rep.shape == (1, 1, 4, 1)\n    print('[PASS] GQA KV repeat dimension matches.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m1-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary memory bottleneck resolved by Multi-Query Attention (MQA)?",
                        "options": ["KV Cache storage and memory bandwidth during autoregressive decoding.", "Query matrix multiplication speeds.", "The learning rate scheduling boundaries.", "Positional embedding storage."],
                        "correct_answer": "KV Cache storage and memory bandwidth during autoregressive decoding.",
                        "explanation": "MQA uses a single key-value head, drastically reducing the KV Cache memory footprint and accelerating inference memory read-write bounds."
                    }
                ]
            }
        },
        "genai-m1-t3": {
            "title": "LLM Decoding Mathematics",
            "notes": {
                "learning_outcomes": [
                    "Compare Greedy and Beam Search decoding parameters.",
                    "Formulate Temperature-scaled softmax and Top-K/Top-P sampling equations."
                ],
                "sections": [
                    {
                        "title": "Greedy Search and Beam Search",
                        "content": "LLMs output logits representing predictions over a vocabulary. To generate text, we decode these logits:\n\n*   **Greedy Search:** Selects the token with the highest probability at each step. It is computationally cheap but often leads to repetitive or suboptimal sequences.\n*   **Beam Search:** Keeps track of the top $B$ candidate sequences (beams) at each step, evaluating their cumulative probabilities. While computationally expensive, it yields better global optimization.",
                        "callouts": []
                    },
                    {
                        "title": "Temperature Scaling, Top-K, and Top-P",
                        "content": "To introduce diversity, we sample from the probability distribution. Logits are scaled using a temperature parameter $T > 0$:\n\n$$p_i = \\frac{\\exp(z_i / T)}{\\sum_j \\exp(z_j / T)}$$\n\n*   Low temperature ($T \\to 0$) concentrates probability mass on the top token, approaching greedy search.\n*   High temperature ($T > 1$) flattens the distribution, increasing diversity but raising the risk of incoherent outputs.\n\nTo restrict sampling to safe tokens, we apply filtering:\n1.  **Top-K:** Selects only the $K$ highest-probability tokens.\n2.  **Top-P (Nucleus Sampling):** Dynamically filters candidates by selecting the smallest subset of tokens whose cumulative probability exceeds threshold $P$:\n\n$$\\sum_{i \\in \\mathcal{V}_{Top-P}} P(w_i \\mid w_{<t}) \\ge P$$",
                        "callouts": []
                    }
                ]
            },
            "revision": "# LLM Decoding Mathematics\n\n## 1. Temperature-Scaled Softmax\n$$p_i = \\frac{e^{z_i / T}}{\\sum_j e^{z_j / T}}$$\n\n## 2. Top-P Condition\n$$\\sum_{i \\in \\mathcal{V}_{Top-P}} P(w_i \\mid w_{<t}) \\ge P$$\n",
            "interview": "# Interview Prep: Decoding Mathematics\n\n## Q1: How does Top-P sampling vary the number of candidates dynamically compared to Top-K?\n\n### Standard Answer\nTop-K keeps the candidate set size constant (exactly $K$). In flat distributions, this can exclude likely candidates, whereas in peak distributions, it can include highly unlikely candidates. Top-P uses a cumulative probability threshold $P$. When the distribution is flat, many tokens are selected; when the distribution is narrow, only the top few are selected.\n",
            "example_code": "import numpy as np\n\ndef temperature_softmax(logits, temperature=0.7):\n    scaled_logits = logits / temperature\n    exp_logits = np.exp(scaled_logits - np.max(scaled_logits))\n    return exp_logits / np.sum(exp_logits)\n\nif __name__ == '__main__':\n    print('Decoding soft-max methods initialized.')\n",
            "practice_code": "import numpy as np\n\ndef temperature_softmax(logits, temperature=0.7):\n    scaled_logits = logits / temperature\n    exp_logits = np.exp(scaled_logits - np.max(scaled_logits))\n    return exp_logits / np.sum(exp_logits)\n\ndef run_practice():\n    logits = np.array([1.0, 1.0])\n    probs = temperature_softmax(logits, 1.0)\n    assert np.allclose(probs, np.array([0.5, 0.5]))\n    print('[PASS] Temperature scaled probability check passes.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m1-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the effect of setting temperature parameter T very close to 0 (e.g., T = 0.01)?",
                        "options": ["The generation becomes highly deterministic, approaching greedy search.", "All tokens become equally probable.", "The generation process diverges and crashes.", "The context window decreases to zero."],
                        "correct_answer": "The generation becomes highly deterministic, approaching greedy search.",
                        "explanation": "As T approaches 0, the probability mass concentrates almost entirely on the token with the highest logit value, making generation deterministic."
                    }
                ]
            }
        },
        "genai-m1-t4": {
            "title": "Mixture of Experts",
            "notes": {
                "learning_outcomes": [
                    "Explain sparse Mixture of Experts (MoE) routing gating mechanics.",
                    "Formulate load-balancing auxiliary loss functions."
                ],
                "sections": [
                    {
                        "title": "MoE Routing and Top-K experts",
                        "content": "Sparse Mixture of Experts (MoE) scales model parameters by replacing dense feedforward layers with multiple parallel networks ('experts'). A gating network dynamically routes tokens to the best experts:\n\n$$y = \\sum_{i=1}^E G(\\mathbf{x})_i E_i(\\mathbf{x})$$\n\nwhere $G(\\mathbf{x}) = \\text{softmax}(\\text{TopK}(\\mathbf{x}\\mathbf{W}_g, K))$. Typically $K=1$ or $K=2$. This allows scaling model parameter size while keeping the active compute cost (FLOPs) constant per token, as each token is processed by only a subset of experts.",
                        "callouts": []
                    },
                    {
                        "title": "Load-Balancing and Auxiliary Loss Functions",
                        "content": "A major challenge in MoE models is routing imbalance, where the gating network converges to selecting only a few popular experts, leaving other experts untrained. To resolve this, we optimize a load-balancing auxiliary loss during training:\n\n$$\\mathcal{L}_{aux} = E \\sum_{i=1}^E f_i \\cdot P_i$$\n\nwhere $f_i$ is the fraction of tokens routed to expert $i$, and $P_i$ is the average gating probability assigned to expert $i$ across the batch. Minimizing this loss encourages uniform routing distributions.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Mixture of Experts\n\n## 1. Gating Selection\n$$y = \\sum_{i=1}^E G(\\mathbf{x})_i E_i(\\mathbf{x})$$\n\n## 2. Load-Balancing Loss\n$$\\mathcal{L}_{aux} = E \\sum_{i=1}^E f_i P_i$$\n*   Minimizing this prevents router collapse to a single expert.\n",
            "interview": "# Interview Prep: MoE\n\n## Q1: Why do MoE models require load-balancing auxiliary losses during training?\n\n### Standard Answer\nWithout load-balancing losses, the routing network falls into a winner-take-all feedback loop. Early in training, a few experts are selected slightly more often than others, causing their weights to receive more updates. The router continues to favor them, leaving other experts untrained.",
            "example_code": "import numpy as np\n\ndef moe_gating(x, W_g, top_k=2):\n    scores = np.dot(x, W_g)\n    top_indices = np.argsort(scores)[-top_k:]\n    gate_weights = np.zeros_like(scores)\n    top_scores = scores[top_indices]\n    exp_scores = np.exp(top_scores - np.max(top_scores))\n    gate_weights[top_indices] = exp_scores / np.sum(exp_scores)\n    return gate_weights, top_indices\n\nif __name__ == '__main__':\n    print('MoE routing initialized.')\n",
            "practice_code": "import numpy as np\n\ndef moe_gating(x, W_g, top_k=2):\n    scores = np.dot(x, W_g)\n    top_indices = np.argsort(scores)[-top_k:]\n    gate_weights = np.zeros_like(scores)\n    top_scores = scores[top_indices]\n    exp_scores = np.exp(top_scores - np.max(top_scores))\n    gate_weights[top_indices] = exp_scores / np.sum(exp_scores)\n    return gate_weights, top_indices\n\ndef run_practice():\n    x = np.array([1.0, 0.0])\n    W_g = np.array([[1.0, 2.0, 3.0], [0.0, 0.0, 0.0]])\n    weights, idx = moe_gating(x, W_g, 2)\n    assert np.all(idx == np.array([1, 2]))\n    print('[PASS] MoE gating routing indices verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m1-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the key advantage of a sparse MoE model over a dense model of equal parameter size?",
                        "options": ["It scales the parameter size while keeping active flops (compute cost) constant per token.", "It reduces GPU RAM consumption.", "It eliminates the need for activations.", "It is immune to overfitting."],
                        "correct_answer": "It scales the parameter size while keeping active flops (compute cost) constant per token.",
                        "explanation": "Since each token is routed to only a subset of experts (Top-K), only those weights are computed, keeping flops constant."
                    }
                ]
            }
        },
        "genai-m1-t5": {
            "title": "Multimodal Tokenization",
            "notes": {
                "learning_outcomes": [
                    "Formulate CLIP text-image contrastive embedding alignments.",
                    "Explain visual token projection layer mappings."
                ],
                "sections": [
                    {
                        "title": "Multimodal Alignment and CLIP",
                        "content": "CLIP (Contrastive Language-Image Pre-training) aligns text and image representations in a shared semantic space. Given a batch of $B$ text-image pairs, the system encodes them into image features $\\mathbf{I}_i$ and text features $\\mathbf{T}_i$. The objective maximizes cosine similarity along the diagonal (correct pairs) while minimizing similarity for off-diagonal indices (unmatched pairs):\n\n$$\\mathcal{L} = -\\frac{1}{2B} \\sum_{i=1}^B \\left[ \\ln \\frac{\\exp(\\mathbf{I}_i^{\\top} \\mathbf{T}_i / \\tau)}{\\sum_j \\exp(\\mathbf{I}_i^{\\top} \\mathbf{T}_j / \\tau)} + \\ln \\frac{\\exp(\\mathbf{I}_i^{\\top} \\mathbf{T}_i / \\tau)}{\\sum_j \\exp(\\mathbf{I}_j^{\\top} \\mathbf{T}_i / \\tau)} \\right]$$\n\nwhere $\\tau$ is a learnable temperature parameter.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Multimodal Tokenization\n\n$$\\mathcal{L}_{CLIP} = \\text{CrossEntropy}(\\text{logits}, \\text{labels})_V + \\text{CrossEntropy}(\\text{logits}^{\\top}, \\text{labels})_H$$\n",
            "interview": "# Interview Prep: Multimodal\n\n## Q1: How does CLIP's contrastive learning loss function optimize text-image similarity scales?\n\n### Standard Answer\nCLIP computes a similarity matrix $\\mathbf{S} = \\mathbf{I} \\mathbf{T}^{\\top}$ scaled by a learnable temperature $\\tau$. Cross-entropy loss is applied along both columns and rows to maximize diagonal alignment (correct pairs) relative to all other indices in the batch.\n",
            "example_code": "import numpy as np\n\ndef clip_contrastive_logits(image_embeds, text_embeds, temperature=0.07):\n    I = image_embeds / np.linalg.norm(image_embeds, axis=-1, keepdims=True)\n    T = text_embeds / np.linalg.norm(text_embeds, axis=-1, keepdims=True)\n    return np.matmul(I, T.T) / temperature\n\nif __name__ == '__main__':\n    print('CLIP contrastive logits configured.')\n",
            "practice_code": "import numpy as np\n\ndef clip_contrastive_logits(image_embeds, text_embeds, temperature=0.07):\n    I = image_embeds / np.linalg.norm(image_embeds, axis=-1, keepdims=True)\n    T = text_embeds / np.linalg.norm(text_embeds, axis=-1, keepdims=True)\n    return np.matmul(I, T.T) / temperature\n\ndef run_practice():\n    I = np.array([[1.0, 0.0]])\n    T = np.array([[1.0, 0.0]])\n    logits = clip_contrastive_logits(I, T, 0.1)\n    assert np.allclose(logits, np.array([[10.0]]))\n    print('[PASS] Multimodal projection logits checked.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m1-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary role of the projection layer in a vision-language model like LLaVA?",
                        "options": ["To map visual features from the vision encoder into the same dimensional space as the LLM's text embeddings.", "To compress images to JPEG formats.", "To count image color values.", "To replace text tokenizers."],
                        "correct_answer": "To map visual features from the vision encoder into the same dimensional space as the LLM's text embeddings.",
                        "explanation": "VLM projection layers act as dimensional translators, converting ViT output matrices into equivalent visual token embedding arrays."
                    }
                ]
            }
        }
    }

    # Write files
    for topic_id, data in m1_data.items():
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

    print("\nSuccessfully generated enriched GenAI Module 1 files!")

if __name__ == "__main__":
    main()
