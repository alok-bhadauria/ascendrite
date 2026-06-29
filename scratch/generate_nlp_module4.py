import os
import json

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nlp_dir = os.path.join(base_dir, "knowledge-base", "ai", "nlp")

    m4_data = {
        "nlp-m4-t1": {
            "title": "Self-Attention Mechanics",
            "notes": {
                "learning_outcomes": [
                    "Explain the role of Query, Key, and Value projection weight matrices.",
                    "Derive the scaled dot-product attention equation and explain the need for the scaling factor 1/sqrt(d_k)."
                ],
                "sections": [
                    {
                        "title": "Projections and Attention Matrices",
                        "content": "Given an input sequence representation matrix $\\mathbf{H} \\in \\mathbb{R}^{T \\times d}$, the self-attention layer projects it into Query ($\\mathbf{Q}$), Key ($\\mathbf{K}$), and Value ($\\mathbf{V}$) matrices using learned linear weight transformations:\n\n$$\\mathbf{Q} = \\mathbf{H}\\mathbf{W}_Q, \\quad \\mathbf{K} = \\mathbf{H}\\mathbf{W}_K, \\quad \\mathbf{V} = \\mathbf{H}\\mathbf{W}_V$$\n\nwhere $\\mathbf{W}_Q, \\mathbf{W}_K \\in \\mathbb{R}^{d \\times d_k}$ and $\\mathbf{W}_V \\in \\mathbb{R}^{d \\times d_v}$. \n\nAttention weights are computed by evaluating the dot products between Queries and Keys, representing the similarity of each token to all other tokens in the sequence. The attention output is the weighted sum of the Values:\n\n$$\\text{Attention}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{softmax}\\left( \\frac{\\mathbf{Q}\\mathbf{K}^{\\top}}{\\sqrt{d_k}} \\right)\\mathbf{V}$$",
                        "callouts": []
                    },
                    {
                        "title": "Derivation of the Scaling Factor",
                        "content": "To understand the need for the scaling factor $\\frac{1}{\\sqrt{d_k}}$, let the components of query and key vectors $\\mathbf{q}, \\mathbf{k} \\in \\mathbb{R}^{d_k}$ be independent random variables with mean $0$ and variance $1$. The dot product is:\n\n$$\\mathbf{q} \\cdot \\mathbf{k} = \\sum_{i=1}^{d_k} q_i k_i$$\n\nThe expected value of the dot product is $0$. Assuming independence, the variance is the sum of the variances of each term:\n\n$$\\text{Var}(\\mathbf{q} \\cdot \\mathbf{k}) = \\sum_{i=1}^{d_k} \\text{Var}(q_i k_i) = \\sum_{i=1}^{d_k} \\left[ \\mathbb{E}(q_i^2)\\mathbb{E}(k_i^2) - (\\mathbb{E}(q_i)\\mathbb{E}(k_i))^2 \\right] = \\sum_{i=1}^{d_k} (1 \\cdot 1 - 0) = d_k$$\n\nAs the dimensionality $d_k$ grows large, the variance of the dot product increases to $d_k$. This causes the dot products to grow large in magnitude, pushing the softmax function into regions with extremely small gradients (saturating the softmax). Dividing by $\\sqrt{d_k}$ scales the variance of the dot product back to $1.0$, stabilizing gradient updates during training.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Self-Attention Mechanics\n\n## 1. Mathematical Equation\n$$\\text{Attention}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{softmax}\\left( \\frac{\\mathbf{Q}\\mathbf{K}^{\\top}}{\\sqrt{d_k}} \\right)\\mathbf{V}$$\n\n## 2. Scaling Derivation\n*   If $q_i, k_i \\sim \\mathcal{N}(0, 1)$, then $\\text{Var}(\\mathbf{q} \\cdot \\mathbf{k}) = d_k$.\n*   Dividing by $\\sqrt{d_k}$ scales the variance back to $1.0$, preventing softmax saturation.\n",
            "interview": "# Interview Prep: Self-Attention\n\n## Q1: Prove mathematically why the scaling factor 1/sqrt(d_k) is required in the self-attention equation.\n\n### Standard Answer\nLet key and query vectors $\\mathbf{q}, \\mathbf{k} \\in \\mathbb{R}^{d_k}$ have components that are independent random variables with mean $0$ and variance $1$. The dot product is $q \\cdot k = \\sum_{i=1}^{d_k} q_i k_i$. The mean of the sum is $0$. Since components are independent, the variance of the sum is the sum of the variances:\n\n$$\\text{Var}(q \\cdot k) = \\sum_{i=1}^{d_k} \\text{Var}(q_i k_i) = d_k$$\n\nFor large values of $d_k$, the variance is $d_k$, causing the dot products to grow large. The softmax function will saturate, leading to vanishing gradients. Dividing by $\\sqrt{d_k}$ scales the variance of the dot product back to $1.0$.\n",
            "example_code": "import numpy as np\n\ndef scaled_dot_product_attention(Q, K, V):\n    dk = Q.shape[-1]\n    scores = np.matmul(Q, K.T) / np.sqrt(dk)\n    weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)\n    return np.matmul(weights, V), weights\n\nif __name__ == '__main__':\n    print('Attention module loaded.')\n",
            "practice_code": "import numpy as np\n\ndef scaled_dot_product_attention(Q, K, V):\n    dk = Q.shape[-1]\n    scores = np.matmul(Q, K.T) / np.sqrt(dk)\n    weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)\n    return np.matmul(weights, V), weights\n\ndef run_practice():\n    Q = np.array([[1.0, 0.0]])\n    K = np.array([[1.0, 0.0]])\n    V = np.array([[10.0, 20.0]])\n    out, w = scaled_dot_product_attention(Q, K, V)\n    assert np.allclose(out, V)\n    print('[PASS] Attention forward calculation matches.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m4-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary consequence of omitting the 1/sqrt(d_k) scaling factor in self-attention when d_k is very large?",
                        "options": ["The softmax function saturates, causing gradients to vanish during backpropagation.", "The training loss diverges to negative infinity.", "The keys and values become identical.", "Sequence representations overflow to zero."],
                        "correct_answer": "The softmax function saturates, causing gradients to vanish during backpropagation.",
                        "explanation": "Without scaling, the dot products grow large, causing softmax outputs to approach 0 or 1, where the local gradient is virtually zero."
                    }
                ]
            }
        },
        "nlp-m4-t2": {
            "title": "Multi-Head Attention",
            "notes": {
                "learning_outcomes": [
                    "Explain parallel subspace projections in Multi-Head Attention.",
                    "Formulate head concatenation matrices and final output weight mappings."
                ],
                "sections": [
                    {
                        "title": "Multi-Head Subspaces",
                        "content": "Rather than performing self-attention once with a single dimension $d_{\\text{model}}$, **Multi-Head Attention (MHA)** projects queries, keys, and values $h$ times in parallel using different projection matrices. This allows the model to attend to information from different representation subspaces simultaneously (e.g. one head tracks syntactic relationships, while another tracks semantic themes).\n\nThe outputs from each head are concatenated and projected again to produce the final representation:\n\n$$\\text{MHA}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{Concat}(\\text{head}_1, \\dots, \\text{head}_h)\\mathbf{W}^O$$\n\nwhere $\\text{head}_i = \\text{Attention}(\\mathbf{Q}\\mathbf{W}_i^Q, \\mathbf{K}\\mathbf{W}_i^K, \\mathbf{V}\\mathbf{W}_i^V)$.",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Head Dimensionality Division",
                                "content": "To maintain constant compute cost relative to single-head attention, we scale the projection dimensions down: $d_k = d_v = d_{\\text{model}} / h$. This ensures that the total parameter count and operations are identical to single-head attention with full dimensionality."
                            }
                        ]
                    }
                ]
            },
            "revision": "# Multi-Head Attention\n\n## 1. Architectural Equation\n$$\\text{head}_i = \\operatorname{Attention}(\\mathbf{Q}\\mathbf{W}_i^Q, \\mathbf{K}\\mathbf{W}_i^K, \\mathbf{V}\\mathbf{W}_i^V)$$\n$$\\text{Output} = \\operatorname{Concat}(\\text{head}_1, \\dots, \\text{head}_h)\\mathbf{W}^O$$\n\n## 2. Projection Dimensions\n*   $d_k = d_{\\text{model}} / h$\n*   Keeps computational cost equivalent to single-head attention.\n",
            "interview": "# Interview Prep: MHA\n\n## Q1: Why is the model dimension d_model divided by the number of heads h (i.e. d_k = d_model / h) in production implementations?\n\n### Standard Answer\nDividing $d_{model}$ by $h$ ensures that the computational cost of Multi-Head Attention is identical to that of single-head attention with full dimensionality. The total parameter count and operations are kept constant, while allowing the model to attend to information from different representation subspaces simultaneously.\n",
            "example_code": "import numpy as np\n\ndef concat_heads(heads):\n    return np.concatenate(heads, axis=-1)\n\nif __name__ == '__main__':\n    print('MHA concatenation helper loaded.')\n",
            "practice_code": "import numpy as np\n\ndef concat_heads(heads):\n    return np.concatenate(heads, axis=-1)\n\ndef run_practice():\n    h1 = np.array([[1.0]])\n    h2 = np.array([[2.0]])\n    merged = concat_heads([h1, h2])\n    assert np.allclose(merged, np.array([[1.0, 2.0]]))\n    print('[PASS] Concatenation assertions passed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m4-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "If d_model = 512 and we configure h = 8 heads, what is the output dimension d_k of the query projection matrix for each individual head?",
                        "options": ["64", "512", "8", "4096"],
                        "correct_answer": "64",
                        "explanation": "d_k is calculated as d_model / h = 512 / 8 = 64."
                    }
                ]
            }
        },
        "nlp-m4-t3": {
            "title": "Transformer Block Components",
            "notes": {
                "learning_outcomes": [
                    "Contrast LayerNorm configurations (Pre-LN vs Post-LN).",
                    "Explain absolute positional encodings and the Rotary Position Embedding (RoPE) relative distance rotation."
                ],
                "sections": [
                    {
                        "title": "Layer Normalization: Pre-LN vs. Post-LN",
                        "content": "Transformer blocks use Layer Normalization (LN) to stabilize activations. \n\n*   **Post-LN:** Normalization occurs after the residual addition: $\\mathbf{x}_{l+1} = \\text{LN}(\\mathbf{x}_l + \\text{SubLayer}(\\mathbf{x}_l))$. While historically common, Post-LN requires linear learning rate warmup schedules to prevent gradient explosions in early layers during initialization.\n*   **Pre-LN:** Normalization is applied to the input before the sublayer: $\\mathbf{x}_{l+1} = \\mathbf{x}_l + \\text{SubLayer}(\\text{LN}(\\mathbf{x}_l))$. Pre-LN maintains a direct identity path from the first layer to the last, stabilizing gradient flows. This allows models to scale to hundreds of layers without warmup tricks.",
                        "callouts": []
                    },
                    {
                        "title": "Rotary Position Embeddings (RoPE)",
                        "content": "Since self-attention is permutation-invariant, models require positional encodings. Modern architectures replace absolute positional encodings with **Rotary Position Embedding (RoPE)**.\n\nRoPE projects position information by rotating query and key vectors in complex space. For a 2D vector slice $\\mathbf{q} = [q_1, q_2]^{\\top}$ at position $m$, the rotation is:\n\n$$\\mathbf{R}_{m\\theta} \\mathbf{q} = \\begin{bmatrix} \\cos m\\theta & -\\sin m\\theta \\\\ \\sin m\\theta & \\cos m\\theta \\end{bmatrix} \\begin{bmatrix} q_1 \\\\ q_2 \\end{bmatrix}$$\n\nThis rotation preserves relative distance: the dot product between a query at position $m$ and a key at position $n$ depends only on their relative distance $m-n$. This allows the model to generalize to context lengths beyond those seen during training.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Transformer Block Components\n\n## 1. Pre-LN vs Post-LN\n*   **Post-LN:** $\\mathbf{x}_{l+1} = \\text{LN}(\\mathbf{x}_l + \\text{SubLayer}(\\mathbf{x}_l))$\n*   **Pre-LN:** $\\mathbf{x}_{l+1} = \\mathbf{x}_l + \\text{SubLayer}(\\text{LN}(\\mathbf{x}_l))$\n\n## 2. RoPE Rotation Matrix\n$$\\mathbf{R}_{m\\theta} = \\begin{bmatrix} \\cos m\\theta & -\\sin m\\theta \\\\ \\sin m\\theta & \\cos m\\theta \\end{bmatrix}$$\n*   Encodes relative distance properties directly during the attention dot product calculation.\n",
            "interview": "# Interview Prep: Block Components\n\n## Q1: Why does Pre-LN enable stable deep model training without requiring linear learning-rate warmups?\n\n### Standard Answer\nIn Post-LN, the gradient of the residual connection is scaled by the LayerNorm derivative. As layer depth increases, the scale of gradients in early layers diminishes. Pre-LN maintains a direct identity path from input to output, keeping gradients stable.\n",
            "example_code": "import numpy as np\n\ndef apply_rope_2d(q, m, theta=10000.0):\n    angle = m / theta\n    R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])\n    return np.dot(R, q)\n\nif __name__ == '__main__':\n    print('RoPE 2D modules active.')\n",
            "practice_code": "import numpy as np\n\ndef apply_rope_2d(q, m, theta=10000.0):\n    angle = m / theta\n    R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])\n    return np.dot(R, q)\n\ndef run_practice():\n    q = np.array([1.0, 0.0])\n    out = apply_rope_2d(q, 0.0)\n    assert np.allclose(out, q)\n    print('[PASS] RoPE identity rotation verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m4-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the key advantage of Rotary Position Embeddings (RoPE) over absolute sinusoidal encodings?",
                        "options": ["It encodes relative distance properties naturally when calculating Query-Key dot products.", "It reduces parameter counts.", "It replaces LayerNorm.", "It functions only in the log domain."],
                        "correct_answer": "It encodes relative distance properties naturally when calculating Query-Key dot products.",
                        "explanation": "Because RoPE rotates the 2D slices of key and query vectors, the dot product of two rotated vectors depends only on their relative distance (m - n)."
                    }
                ]
            }
        },
        "nlp-m4-t4": {
            "title": "Causal Decoders & Cross-Attention",
            "notes": {
                "learning_outcomes": [
                    "Explain causal masking in autoregressive generation.",
                    "Formulate cross-attention routing layers."
                ],
                "sections": [
                    {
                        "title": "Causal Masking",
                        "content": "Autoregressive generation generates tokens sequentially, left-to-right. To prevent the model from looking ahead at future tokens during training, we apply a **causal mask** to the self-attention matrix before the softmax step.\n\nThe mask is a lower-triangular matrix $\\mathbf{M}$ where:\n\n$$\\mathbf{M}_{ij} = \\begin{cases} 0 & \\text{if } i \\ge j \\\\ -\\infty & \\text{if } i < j \\end{cases}$$\n\nAdding this mask to the scaled dot-product attention scores zeroes out attention weights for future tokens:\n\n$$\\text{Attention}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{softmax}\\left( \\frac{\\mathbf{Q}\\mathbf{K}^{\\top}}{\\sqrt{d_k}} + \\mathbf{M} \\right)\\mathbf{V}$$",
                        "callouts": []
                    },
                    {
                        "title": "Cross-Attention Mechanics",
                        "content": "In sequence-to-sequence architectures (like encoder-decoder translation models), **cross-attention** maps the target sequence in the decoder to the source sequence in the encoder.\n\nThe Query matrix $\\mathbf{Q}$ is projected from the decoder's activation states, while the Key ($\\mathbf{K}$) and Value ($\\mathbf{V}$) matrices are projected from the encoder's output representations. This allows the decoder to attend to the relevant parts of the input sequence for each generated target token.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Causal Decoders & Cross-Attention\n\n## 1. Causal Masking\n$$\\mathbf{M}_{ij} = \\begin{cases} 0 & \\text{if } i \\ge j \\\\ -\\infty & \\text{if } i < j \\end{cases}$$\n*   Forces decoder attention to be strictly autoregressive.\n\n## 2. Cross-Attention Setup\n*   Queries ($\\mathbf{Q}$) projected from the decoder.\n*   Keys ($\\mathbf{K}$) and Values ($\\mathbf{V}$) projected from the encoder.\n",
            "interview": "# Interview Prep: Causal Decoders\n\n## Q1: How does cross-attention connect the encoder and decoder states in translation models?\n\n### Standard Answer\nIn cross-attention, Query vectors represent target tokens in the decoder, while Key and Value vectors represent source tokens in the encoder. This allows the decoder to attend to the relevant parts of the input sequence for each generated target token.\n",
            "example_code": "import numpy as np\n\ndef apply_causal_mask(scores):\n    seq_len = scores.shape[-1]\n    mask = np.tril(np.ones((seq_len, seq_len))) == 0\n    scores[mask] = -1e9\n    return scores\n\nif __name__ == '__main__':\n    print('Causal masking utilities loaded.')\n",
            "practice_code": "import numpy as np\n\ndef apply_causal_mask(scores):\n    seq_len = scores.shape[-1]\n    mask = np.tril(np.ones((seq_len, seq_len))) == 0\n    scores[mask] = -1e9\n    return scores\n\ndef run_practice():\n    scores = np.zeros((3, 3))\n    masked = apply_causal_mask(scores)\n    assert masked[0, 1] == -1e9\n    assert masked[1, 0] == 0.0\n    print('[PASS] Causal mask boundaries verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m4-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Which vectors are derived from the encoder outputs in a standard Seq2Seq cross-attention block?",
                        "options": ["Keys and Values", "Queries and Keys", "Queries only", "Values only"],
                        "correct_answer": "Keys and Values",
                        "explanation": "In cross-attention, encoder outputs act as the source memory keys and values, while queries are projected from the decoder."
                    }
                ]
            }
        },
        "nlp-m4-t5": {
            "title": "Pre-training Objectives",
            "notes": {
                "learning_outcomes": [
                    "Compare BERT MLM/NSP and GPT Causal LM pre-training objectives.",
                    "Formulate cross-entropy loss optimization formulas for sequence modeling."
                ],
                "sections": [
                    {
                        "title": "BERT: Masked Language Modeling (MLM)",
                        "content": "BERT is pre-trained using two objectives:\n\n1.  **Masked Language Modeling (MLM):** 15% of the input tokens are sampled for prediction. To prevent the model from adapting only to `[MASK]` tokens (which do not appear at test time), the sampled tokens are replaced by `[MASK]` 80% of the time, by a random token 10% of the time, and left unchanged 10% of the time. The objective function minimizes cross-entropy loss over the sampled subset:\n\n$$\\mathcal{L}_{MLM} = -\\sum_{i \\in M} \\ln P(x_i \\mid \\mathbf{x}_{\\setminus M})$$\n\n2.  **Next Sentence Prediction (NSP):** A binary classification task predicting whether sentence $B$ follows sentence $A$ in the corpus. While useful for coherence, modern models often omit NSP to prioritize long-context sequence modeling.",
                        "callouts": []
                    },
                    {
                        "title": "GPT: Causal Language Modeling (CLM)",
                        "content": "GPT is pre-trained using **Causal Language Modeling (CLM)**, which optimizes the model to predict the next token given preceding context. The model is trained by minimizing the cross-entropy loss at each token position:\n\n$$\\mathcal{L}_{CLM} = -\\sum_{t=1}^T \\ln P(x_t \\mid x_1, \\dots, x_{t-1})$$\n\nThis objective encourages the model to learn causal, unidirectional relationships, serving as a foundation for downstream generation tasks.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Pre-training Objectives\n\n*   **BERT MLM:** Predicts masked tokens using bidirectional contexts: $\\mathcal{L} = -\\sum_{i \\in M} \\log P(x_i \\mid \\mathbf{x}_{\\setminus M})$\n*   **GPT CLM:** Autoregressive generation predicting the next token using causal context: $\\mathcal{L} = -\\sum_{t=1}^T \\log P(x_t \\mid x_1 \\dots x_{t-1})$\n",
            "interview": "# Interview Prep: Pre-training\n\n## Q1: Why did modern LLMs shift away from Next Sentence Prediction (NSP) training?\n\n### Standard Answer\nSubsequent studies (like RoBERTa) demonstrated that the NSP task is too easy and can degrade downstream performance. Training the model on longer contiguous text blocks with MLM is sufficient to capture long-range coherence.",
            "example_code": "import numpy as np\n\ndef sample_mlm_mask(seq_len, mask_prob=0.15):\n    return np.random.rand(seq_len) < mask_prob\n\nif __name__ == '__main__':\n    print('MLM mask helper loaded.')\n",
            "practice_code": "import numpy as np\n\ndef sample_mlm_mask(seq_len, mask_prob=0.15):\n    return np.random.rand(seq_len) < mask_prob\n\ndef run_practice():\n    mask = sample_mlm_mask(100, 1.0)\n    assert np.all(mask)\n    print('[PASS] MLM mask helper checked.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m4-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary training loss function used in both BERT MLM and GPT next-token prediction?",
                        "options": ["Cross-Entropy Loss", "Mean Squared Error", "Contrastive Loss", "Hinge Loss"],
                        "correct_answer": "Cross-Entropy Loss",
                        "explanation": "Pre-training tasks classify vocabulary indices, optimizing classification cross-entropy loss."
                    }
                ]
            }
        }
    }

    # Write files
    for topic_id, data in m4_data.items():
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
        write_file(os.path.join(nlp_dir, "notes", f"{topic_id}.json"), json.dumps(notes_content, indent=2))
        write_file(os.path.join(nlp_dir, "revision", f"{topic_id}.md"), data["revision"])
        write_file(os.path.join(nlp_dir, "interview", f"{topic_id}.md"), data["interview"])
        write_file(os.path.join(nlp_dir, "examples", f"{topic_id}-ex1.py"), data["example_code"])
        write_file(os.path.join(nlp_dir, "practice", f"{topic_id}-prac1.py"), data["practice_code"])
        write_file(os.path.join(nlp_dir, "quiz", f"{topic_id}-quiz.json"), json.dumps(data["quiz"], indent=2))

    print("\nSuccessfully generated enriched NLP Module 4 files!")

if __name__ == "__main__":
    main()
