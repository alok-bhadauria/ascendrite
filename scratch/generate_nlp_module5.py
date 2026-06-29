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

    m5_data = {
        "nlp-m5-t1": {
            "title": "Sentence Embeddings",
            "notes": {
                "learning_outcomes": [
                    "Contrast Bi-Encoder and Cross-Encoder architectures.",
                    "Explain pooling strategies (mean, max, CLS) for sentence embeddings.",
                    "Formulate Contrastive Loss equations."
                ],
                "sections": [
                    {
                        "title": "Sentence Embedding Architectures",
                        "content": "To compute similarity between full sentences rather than individual words, we map sequences to fixed-size vectors. The architecture chosen defines the speed-accuracy trade-off:\n\n*   **Bi-Encoder:** Encodes sentences independently using two identical networks. Sentence similarity is evaluated using cosine similarity on the resulting vectors:\n\n$$\\text{sim}(s_1, s_2) = \\cos(f(s_1), f(s_2))$$\n\nBi-encoders are highly efficient for search, as sentence embeddings can be pre-computed and stored in a vector database offline.\n*   **Cross-Encoder:** Feeds both sentences into the network simultaneously (concatenated via a separator token `[SEP]`), allowing the self-attention layers to compute interactions between all tokens. Cross-encoders are highly accurate but computationally expensive, as they cannot be pre-computed offline.",
                        "callouts": []
                    },
                    {
                        "title": "Pooling Strategies and Contrastive Loss",
                        "content": "To generate a fixed-size sentence vector from transformer token hidden states $\\mathbf{H} \\in \\mathbb{R}^{T \\times d}$, we apply pooling:\n1. **CLS Pooling:** Uses the hidden state of the first special token `[CLS]` as the representation.\n2. **Mean Pooling:** Computes the average of all token hidden vectors: $\\mathbf{s} = \\frac{1}{T} \\sum_{t=1}^T \\mathbf{h}_t$.\n3. **Max Pooling:** Takes the maximum value along each dimension across all tokens.\n\nModels are trained using **Contrastive Loss** (e.g. InfoNCE) to minimize the distance between matching pairs $(u, v)$ while maximizing distance to unmatched negative pairs:\n\n$$\\mathcal{L}_{InfoNCE} = -\\ln \\frac{\\exp(\\cos(\\mathbf{u}, \\mathbf{v}) / \\tau)}{\\sum_{i=1}^B \\exp(\\cos(\\mathbf{u}, \\mathbf{v}_i) / \\tau)}$$\n\nwhere $\\tau$ is a temperature hyperparameter and $B$ is the batch size.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Sentence Embeddings\n\n## 1. Bi-Encoder vs Cross-Encoder\n*   **Bi-Encoder:** $\\text{sim}(s_1, s_2) = \\cos(f(s_1), f(s_2))$\n*   **Cross-Encoder:** $\\text{score} = f(s_1 || s_2)$\n\n## 2. InfoNCE Contrastive Loss\n$$\\mathcal{L} = -\\ln \\frac{\\exp(\\cos(\\mathbf{u}, \\mathbf{v}) / \\tau)}{\\sum_{i=1}^B \\exp(\\cos(\\mathbf{u}, \\mathbf{v}_i) / \\tau)}$$\n",
            "interview": "# Interview Prep: Sentence Embeddings\n\n## Q1: Why are Bi-Encoders preferred for web-scale semantic search engines despite having lower accuracy than Cross-Encoders?\n\n### Standard Answer\nBi-encoders compute sentence embeddings independently. In semantic search, document embeddings can be pre-computed and stored in a vector database offline. At query time, we only need to encode the query and perform a fast vector search. Cross-encoders require encoding the query with every document in the index, which is computationally intractable at scale.\n",
            "example_code": "import numpy as np\n\ndef bi_encoder_cosine(u, v):\n    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))\n\nif __name__ == '__main__':\n    print('Bi-encoder simulator loaded.')\n",
            "practice_code": "import numpy as np\n\ndef bi_encoder_cosine(u, v):\n    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))\n\ndef run_practice():\n    u = np.array([1.0, 0.0])\n    v = np.array([1.0, 0.0])\n    assert np.allclose(bi_encoder_cosine(u, v), 1.0)\n    print('[PASS] Bi-encoder check passed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m5-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary trade-off when selecting a Cross-Encoder over a Bi-Encoder?",
                        "options": ["Cross-encoders have higher accuracy but cannot compute offline index embeddings, leading to high latency.", "Cross-encoders have smaller parameter counts.", "Cross-encoders only support English.", "Bi-encoders require GPU clusters for inference."],
                        "correct_answer": "Cross-encoders have higher accuracy but cannot compute offline index embeddings, leading to high latency.",
                        "explanation": "Because Cross-encoders require input pair concatenation during the forward pass, we cannot pre-index document vectors."
                    }
                ]
            }
        },
        "nlp-m5-t2": {
            "title": "Information Retrieval & BM25",
            "notes": {
                "learning_outcomes": [
                    "Formulate the Okapi BM25 ranking metric.",
                    "Explain term frequency saturation and document length normalization."
                ],
                "sections": [
                    {
                        "title": "Okapi BM25 Ranking Model",
                        "content": "Okapi BM25 is a non-linear ranking function that improves on TF-IDF by incorporating term frequency saturation and document length normalization. The BM25 score for a document $D$ given query $Q$ containing search terms $q_i$ is:\n\n$$\\text{Score}(D, Q) = \\sum_{q_i \\in Q} \\text{IDF}(q_i) \\frac{f(q_i, D) \\cdot (k_1 + 1)}{f(q_i, D) + k_1 \\left( 1 - b + b \\frac{|D|}{\\text{avgdl}} \\right)}$$\n\nwhere:\n*   $f(q_i, D)$ is the frequency of query term $q_i$ in document $D$.\n*   $|D|$ and $\\text{avgdl}$ are the document length and average document length across the corpus.\n*   $k_1$ is a scaling parameter controlling term frequency saturation (typically $1.2 \\le k_1 \\le 2.0$).\n*   $b$ is a scaling parameter controlling document length normalization (typically $b=0.75$).",
                        "callouts": []
                    },
                    {
                        "title": "Term Saturation and Length Normalization Parameters",
                        "content": "In TF-IDF, score growth is linear or log-linear with term frequency: many occurrences of a query term can heavily distort the ranking. In BM25, as term frequency increases, the term's contribution asymptotically approaches a limit controlled by $k_1$. \n\nThe parameter $b$ controls length normalization. A longer document naturally contains more words, increasing the probability of matching query terms by chance. Setting $b=1$ applies full document length normalization, while $b=0$ disables it entirely.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# BM25 Model\n\n## 1. Mathematical Equation\n$$\\text{Score}(D, Q) = \\sum_{q_i \\in Q} \\text{IDF}(q_i) \\frac{f(q_i, D) (k_1 + 1)}{f(q_i, D) + k_1 (1 - b + b \\frac{|D|}{\\text{avgdl}})}$$\n\n## 2. Hyperparameter Defaults\n*   $k_1 \\approx 1.5$: Term frequency saturation parameter.\n*   $b \\approx 0.75$: Document length normalization parameter.\n",
            "interview": "# Interview Prep: BM25\n\n## Q1: How does parameter k_1 control term frequency saturation in BM25?\n\n### Standard Answer\nIn TF-IDF, the score scales linearly (or log-linearly) with term frequency, meaning that many occurrences of a query term can heavily distort the ranking. In BM25, as term frequency increases, the score asymptotically approaches a limit. The parameter $k_1$ controls how fast this saturation is reached; higher values scale the score longer before flattening.\n",
            "example_code": "import numpy as np\n\ndef compute_bm25_term(tf, idf, doc_len, avg_len, k1=1.5, b=0.75):\n    numerator = tf * (k1 + 1.0)\n    denominator = tf + k1 * (1.0 - b + b * (doc_len / avg_len))\n    return idf * (numerator / denominator)\n\nif __name__ == '__main__':\n    print('BM25 formula configured.')\n",
            "practice_code": "import numpy as np\n\ndef compute_bm25_term(tf, idf, doc_len, avg_len, k1=1.5, b=0.75):\n    numerator = tf * (k1 + 1.0)\n    denominator = tf + k1 * (1.0 - b + b * (doc_len / avg_len))\n    return idf * (numerator / denominator)\n\ndef run_practice():\n    score = compute_bm25_term(0.0, 1.0, 100, 100)\n    assert score == 0.0\n    print('[PASS] BM25 zero tf check validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m5-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What does setting parameter b = 0 in BM25 represent?",
                        "options": ["Length normalization is completely disabled.", "Term frequency saturation is infinite.", "All document scores are zero.", "IDF is bypassed."],
                        "correct_answer": "Length normalization is completely disabled.",
                        "explanation": "The parameter b controls document length scaling. Setting b = 0 nullifies the effect of document length relative to average length."
                    }
                ]
            }
        },
        "nlp-m5-t3": {
            "title": "Vector Databases & Search",
            "notes": {
                "learning_outcomes": [
                    "Explain HNSW skip-list graph traversal mechanics.",
                    "Formulate Inverted File Product Quantization (IVF-PQ) memory compression steps."
                ],
                "sections": [
                    {
                        "title": "Hierarchical Navigable Small World (HNSW) Graphs",
                        "content": "To query high-dimensional embeddings efficiently, vector databases implement Approximate Nearest Neighbors (ANN) indices. \n\n**HNSW** is a multi-layer graph based on skip-lists. Top layers have sparse connections for fast coarse routing across large distances, while bottom layers have dense connections for fine-grained search. Traversing down the hierarchy achieves $\\mathcal{O}(\\log N)$ search complexity.",
                        "callouts": []
                    },
                    {
                        "title": "Inverted File Product Quantization (IVF-PQ) Compression",
                        "content": "Storing raw float embeddings requires significant memory. **IVF-PQ** optimizes this storage footprint:\n\n1.  **Inverted File (IVF):** Groups vectors into Voronoi cells using K-Means. During query retrieval, the search is restricted to the closest centroids, reducing the search space.\n2.  **Product Quantization (PQ):** Compresses high-dimensional vectors. It splits a $d$-dimensional vector into $m$ sub-vectors of dimension $d/m$. It clusters each sub-space independently using K-Means to build a codebook. Each sub-vector is then replaced by its nearest centroid index. This compresses a 1024-byte float vector to a small sequence of 8-bit cluster indices, reducing memory usage by 90% or more.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Vector DB Search\n\n*   **HNSW:** Hierarchical skip-list graphs routing search queries in $\\mathcal{O}(\\log N)$ time.\n*   **IVF-PQ:** Clusters space (Inverted File) and compresses dimensions via sub-space quantization (Product Quantization).\n",
            "interview": "# Interview Prep: Vector DBs\n\n## Q1: How does Product Quantization (PQ) compress vector embedding datasets?\n\n### Standard Answer\nPQ splits a $d$-dimensional vector into $m$ sub-vectors of dimension $d/m$. It clusters each sub-space independently using K-Means to build a codebook. Each sub-vector is then replaced by its nearest centroid index. This compresses a 1024-byte float vector to a small sequence of 8-bit cluster indices, reducing memory usage by 90% or more.\n",
            "example_code": "import numpy as np\n\ndef quantize_vector(sub_vectors, centroids):\n    indices = []\n    for i, sv in enumerate(sub_vectors):\n        distances = np.linalg.norm(centroids[i] - sv, axis=1)\n        indices.append(np.argmin(distances))\n    return indices\n\nif __name__ == '__main__':\n    print('Product quantization module loaded.')\n",
            "practice_code": "import numpy as np\n\ndef quantize_vector(sub_vectors, centroids):\n    indices = []\n    for i, sv in enumerate(sub_vectors):\n        distances = np.linalg.norm(centroids[i] - sv, axis=1)\n        indices.append(np.argmin(distances))\n    return indices\n\ndef run_practice():\n    sub_vectors = [np.array([1.0, 1.0])]\n    centroids = [np.array([[0.0, 0.0], [1.2, 1.2]])]\n    idx = quantize_vector(sub_vectors, centroids)\n    assert idx == [1]\n    print('[PASS] Quantizer centroid allocation validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m5-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary purpose of Inverted File (IVF) index configurations in vector databases?",
                        "options": ["To restrict the query search space by only scanning centroids closest to the query vector.", "To encrypt the database storage.", "To perform sequence alignment checks.", "To count word frequencies."],
                        "correct_answer": "To restrict the query search space by only scanning centroids closest to the query vector.",
                        "explanation": "IVF groups database vectors into Voronoi cells. At query time, the search is restricted to the closest centroids, avoiding exhaustive scans."
                    }
                ]
            }
        },
        "nlp-m5-t4": {
            "title": "Hybrid Search",
            "notes": {
                "learning_outcomes": [
                    "Explain Reciprocal Rank Fusion (RRF) scoring mathematics.",
                    "Evaluate rank aggregation challenges for disparate similarity distributions."
                ],
                "sections": [
                    {
                        "title": "Lexical-Dense Fusion Challenges",
                        "content": "Hybrid search combines sparse keyword retrieval (e.g. BM25) and dense semantic vector retrieval. However, raw score distributions differ significantly: BM25 outputs unbounded positive scores, while dense retrieval outputs bounded similarities ($[-1, 1]$). Direct normalization is unstable.",
                        "callouts": []
                    },
                    {
                        "title": "Reciprocal Rank Fusion (RRF) Mathematics",
                        "content": "To resolve this, we rank documents using **Reciprocal Rank Fusion (RRF)**. RRF evaluates document ranks rather than raw scores, making it scale-invariant:\n\n$$\\text{RRF\\_Score}(d \\in \\mathcal{D}) = \\sum_{m \\in M} \\frac{1}{k + r_m(d)}$$\n\nwhere $M$ is the set of retrieval models, $r_m(d)$ is the rank of document $d$ under model $m$, and $k \\approx 60$ is a constant that prevents top-ranked documents from dominating the scoring metrics.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Hybrid Search & RRF\n\n$$\\text{RRF\\_Score}(d) = \\frac{1}{k + r_{\\text{sparse}}(d)} + \\frac{1}{k + r_{\\text{dense}}(d)}$$\n",
            "interview": "# Interview Prep: Hybrid Search\n\n## Q1: Why is raw score normalization unreliable for hybrid search, justifying the use of RRF?\n\n### Standard Answer\nRaw scores from BM25 (unbounded positive scores) and dense cosine similarity (bounded $[-1, 1]$) have completely different scale parameters and probability distributions. Normalizing these directly creates highly skewed results. RRF resolves this by using ranks, which are scale-invariant, to fuse the results.\n",
            "example_code": "import numpy as np\n\ndef compute_rrf_score(rank_sparse, rank_dense, k=60):\n    return 1.0 / (k + rank_sparse) + 1.0 / (k + rank_dense)\n\nif __name__ == '__main__':\n    print('RRF score fusion configured.')\n",
            "practice_code": "import numpy as np\n\ndef compute_rrf_score(rank_sparse, rank_dense, k=60):\n    return 1.0 / (k + rank_sparse) + 1.0 / (k + rank_dense)\n\ndef run_practice():\n    score = compute_rrf_score(1, 1, 60)\n    assert np.allclose(score, 2.0 / 61.0)\n    print('[PASS] RRF score computations verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m5-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the typical default value configured for parameter k in the RRF equation?",
                        "options": ["60", "0", "1", "1000"],
                        "correct_answer": "60",
                        "explanation": "A default value of 60 is widely used to prevent top-ranked documents from dominating the scoring metrics."
                    }
                ]
            }
        },
        "nlp-m5-t5": {
            "title": "Summarization & Translation Metrics",
            "notes": {
                "learning_outcomes": [
                    "Derive the Bilingual Evaluation Understudy (BLEU) metric equations and explain the brevity penalty.",
                    "Formulate ROUGE evaluation metrics and distinguish ROUGE-N from ROUGE-L."
                ],
                "sections": [
                    {
                        "title": "BLEU Score and Brevity Penalty",
                        "content": "To evaluate language generation tasks automatically, we compare candidate generations against human reference translations.\n\n**BLEU (Bilingual Evaluation Understudy)** measures n-gram precision with a brevity penalty. The precision $p_n$ is computed as the fraction of candidate n-grams that appear in the reference. The final score is:\n\n$$\\text{BLEU} = \\text{BP} \\cdot \\exp\\left( \\sum_{n=1}^N w_n \\ln p_n \\right)$$\n\nwhere $w_n = 1/N$ are weights. The **Brevity Penalty (BP)** scales the score down if the candidate translation length $c$ is shorter than the reference translation length $r$:\n\n$$\\text{BP} = \\begin{cases} 1 & \\text{if } c > r \\\\ \\exp\\left( 1 - \\frac{r}{c} \\right) & \\text{if } c \\le r \\end{cases}$$\n\nWithout BP, a model could generate extremely short outputs containing only high-confidence words (e.g. 'the') to achieve perfect precision.",
                        "callouts": []
                    },
                    {
                        "title": "ROUGE: Recall-Based Evaluation",
                        "content": "While BLEU focuses on precision, **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)** focuses on recall, measuring how much of the reference translation is captured by the candidate:\n\n1.  **ROUGE-N:** Measures n-gram recall:\n\n$$\\text{ROUGE-N} = \\frac{\\sum_{S \\in \\text{References}} \\sum_{\\text{gram}_n \\in S} \\text{Count}_{match}(\\text{gram}_n)}{\\sum_{S \\in \\text{References}} \\sum_{\\text{gram}_n \\in S} \\text{Count}(\\text{gram}_n)}$$\n\n2.  **ROUGE-L:** Evaluates the **Longest Common Subsequence (LCS)** alignment, capturing structural similarity without requiring consecutive n-gram matches.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Translation Metrics\n\n## 1. BLEU Equation\n$$\\text{BLEU} = \\text{BP} \\cdot \\exp\\left( \\sum_{n=1}^N w_n \\ln p_n \\right)$$\n\n## 2. Brevity Penalty (BP)\n$$\\text{BP} = \\exp(1 - r/c) \\quad (\\text{for } c \\le r)$$\n*   Penalizes short, high-precision candidate sentences.\n",
            "interview": "# Interview Prep: Generation Evals\n\n## Q1: Why is the Brevity Penalty (BP) required in BLEU evaluations?\n\n### Standard Answer\nWithout the brevity penalty, a model could generate extremely short outputs containing only high-confidence words (e.g. 'the') to achieve perfect precision. The brevity penalty scales the score down if the candidate translation length is shorter than the reference translation length.\n",
            "example_code": "import numpy as np\n\ndef compute_brevity_penalty(c_len, r_len):\n    if c_len > r_len:\n        return 1.0\n    return np.exp(1.0 - r_len / c_len) if c_len > 0 else 0.0\n\nif __name__ == '__main__':\n    print('Brevity penalty metric loaded.')\n",
            "practice_code": "import numpy as np\n\ndef compute_brevity_penalty(c_len, r_len):\n    if c_len > r_len:\n        return 1.0\n    return np.exp(1.0 - r_len / c_len) if c_len > 0 else 0.0\n\ndef run_practice():\n    bp = compute_brevity_penalty(5, 10)\n    assert np.allclose(bp, np.exp(-1.0))\n    print('[PASS] Brevity penalty calculation matches.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What does a BLEU score of 0.0 indicate for a candidate translation?",
                        "options": ["Zero overlapping n-grams with the human reference translation.", "A perfect translation.", "An infinitely long sequence.", "A negative loss function."],
                        "correct_answer": "Zero overlapping n-grams with the human reference translation.",
                        "explanation": "If there is no overlapping n-gram matches at all, the precision term is zero, yielding a final BLEU score of 0.0."
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
        write_file(os.path.join(nlp_dir, "notes", f"{topic_id}.json"), json.dumps(notes_content, indent=2))
        write_file(os.path.join(nlp_dir, "revision", f"{topic_id}.md"), data["revision"])
        write_file(os.path.join(nlp_dir, "interview", f"{topic_id}.md"), data["interview"])
        write_file(os.path.join(nlp_dir, "examples", f"{topic_id}-ex1.py"), data["example_code"])
        write_file(os.path.join(nlp_dir, "practice", f"{topic_id}-prac1.py"), data["practice_code"])
        write_file(os.path.join(nlp_dir, "quiz", f"{topic_id}-quiz.json"), json.dumps(data["quiz"], indent=2))

    print("\nSuccessfully generated enriched NLP Module 5 files!")

if __name__ == "__main__":
    main()
