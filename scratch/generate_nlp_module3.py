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

    m3_data = {
        "nlp-m3-t1": {
            "title": "Word2Vec Framework",
            "notes": {
                "learning_outcomes": [
                    "Compare CBOW and Skip-Gram neural architectures.",
                    "Formulate projection layer representations and output softmax equations.",
                    "Explain why the projection layer is linear."
                ],
                "sections": [
                    {
                        "title": "Word2Vec Architectural Taxonomies",
                        "content": "Word2Vec maps words to dense vector representations by training a shallow neural network on context window occurrences. It offers two architectures:\n\n1.  **Skip-Gram:** Predicts surrounding context words given a target word $w_t$. Skip-gram works well with small training datasets and represents rare words effectively.\n2.  **Continuous Bag of Words (CBOW):** Predicts a target word $w_t$ given its surrounding context words. CBOW is faster to train and shows slightly better performance on frequent words.",
                        "callouts": []
                    },
                    {
                        "title": "Projection and Softmax Derivations",
                        "content": "In both models, words are represented as one-hot vectors $\\mathbf{x} \\in \\mathbb{R}^{V}$. The input projection matrix is $\\mathbf{W} \\in \\mathbb{R}^{V \\times d}$, and the output matrix is $\\mathbf{W}' \\in \\mathbb{R}^{d \\times V}$.\n\nIn the **Skip-Gram** model, given target word index $i$, the projected vector is:\n\n$$\\mathbf{v}_{w_i} = \\mathbf{W}_{i, :}$$\n\nTo predict context word $w_o$, we compute the score $z = \\mathbf{v}'^{\\top}_{w_o} \\mathbf{v}_{w_i}$ and pass it to a Softmax layer:\n\n$$P(w_o \\mid w_i) = \\frac{\\exp(\\mathbf{v}'^{\\top}_{w_o} \\mathbf{v}_{w_i})}{\\sum_{w=1}^V \\exp(\\mathbf{v}'^{\\top}_{w} \\mathbf{v}_{w_i})}$$\n\nThe projection layer contains no non-linear activation functions (it is linear). This is because the projection step acts as a simple lookup table, mapping sparse one-hot vectors to dense embeddings. Adding non-linear activations would slow down training without yielding better representations.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Word2Vec Framework\n\n## 1. Skip-Gram Objective\n$$\\mathcal{L} = \\frac{1}{T} \\sum_{t=1}^T \\sum_{-c \\le j \\le c, j \\neq 0} \\ln P(w_{t+j} \\mid w_t)$$\n\n## 2. Output Softmax Probability\n$$P(w_o \\mid w_i) = \\frac{\\exp(\\mathbf{v}'^{\\top}_{w_o} \\mathbf{v}_{w_i})}{\\sum_{w=1}^V \\exp(\\mathbf{v}'^{\\top}_{w} \\mathbf{v}_{w_i})}$$\n",
            "interview": "# Interview Prep: Word2Vec\n\n## Q1: Why is the projection layer of Word2Vec linear (lacks activation function)?\n\n### Standard Answer\nThe projection layer in Word2Vec acts as a simple lookup table. Since we want to map sparse one-hot vectors $\\mathbf{x} \\in \\mathbb{R}^V$ to dense vectors $\\mathbf{v} \\in \\mathbb{R}^d$, the forward pass is just $\\mathbf{v} = \\mathbf{W}_{in} \\mathbf{x}$. Adding non-linear activations would slow down training without yielding better representations.\n",
            "example_code": "import numpy as np\n\ndef lookup_embedding(W_in, word_index):\n    return W_in[word_index]\n\nif __name__ == '__main__':\n    print('Embedding lookup initialized.')\n",
            "practice_code": "import numpy as np\n\ndef lookup_embedding(W_in, word_index):\n    return W_in[word_index]\n\ndef run_practice():\n    W_in = np.array([[1.0, 2.0], [3.0, 4.0]])\n    assert np.allclose(lookup_embedding(W_in, 1), np.array([3.0, 4.0]))\n    print('[PASS] Lookup checks succeeded.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m3-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Which Word2Vec architecture is generally faster to train and shows slightly better performance on frequent words?",
                        "options": ["Continuous Bag of Words (CBOW)", "Skip-Gram", "Hierarchical Softmax", "GloVe"],
                        "correct_answer": "Continuous Bag of Words (CBOW)",
                        "explanation": "CBOW pools context words into a single projection step to predict a target, making it faster to train than Skip-Gram."
                    }
                ]
            }
        },
        "nlp-m3-t2": {
            "title": "Word2Vec Optimization",
            "notes": {
                "learning_outcomes": [
                    "Derive the computational bottleneck of the standard Softmax denominator.",
                    "Derive Negative Sampling (NEG) loss functions from binary logistic regressions.",
                    "Explain Hierarchical Softmax binary Huffman tree path routing."
                ],
                "sections": [
                    {
                        "title": "The Softmax Bottleneck and Negative Sampling",
                        "content": "Evaluating the standard Softmax denominator $\\sum_{w=1}^V \\exp(\\mathbf{v}'^{\\top}_{w} \\mathbf{v}_{w_i})$ requires a summation over the entire vocabulary $V$ at each step. This is computationally expensive for large vocabularies ($V > 100,000$).\n\n**Negative Sampling (NEG)** resolves this by converting the multinomial classification problem into a set of binary classification tasks. The objective is to distinguish the target context word $w_O$ from $k$ randomly sampled noise words (negative samples). The loss function is:\n\n$$\\mathcal{L}_{NEG} = -\\ln \\sigma(\\mathbf{v}'^{\\top}_{w_O} \\mathbf{v}_{w_I}) - \\sum_{i=1}^k \\ln \\sigma(-\\mathbf{v}'^{\\top}_{w_i} \\mathbf{v}_{w_I})$$\n\nwhere $\\sigma(x) = \\frac{1}{1 + e^{-x}}$. The negative samples are drawn from a unigram distribution raised to the 3/4 power: $P_n(w) \\propto U(w)^{0.75}$. This increases the probability of selecting rare words as negative samples, preventing highly frequent words (like 'the') from dominating the updates.",
                        "callouts": []
                    },
                    {
                        "title": "Hierarchical Softmax Mechanics",
                        "content": "An alternative optimization is **Hierarchical Softmax**. It structures the vocabulary as the leaf nodes of a binary Huffman tree. The path from the root node to a word $w$ is defined by a sequence of left/right choices. The probability of selecting word $w$ is the product of the probabilities of these branching choices:\n\n$$P(w \\mid w_I) = \\prod_{j=1}^{L(w)-1} \\sigma\\left( \\text{sign}(n(w, j)) \\cdot \\mathbf{v}'^{\\top}_{n(w, j)} \\mathbf{v}_{w_I} \\right)$$\n\nwhere $L(w)$ is the path length, and $n(w, j)$ is the $j$-th node on the path. This reduces the computational complexity from $\\mathcal{O}(V)$ to $\\mathcal{O}(\\log V)$.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Word2Vec Optimization\n\n## 1. Negative Sampling Loss\n$$\\mathcal{L} = -\\ln \\sigma(\\mathbf{v}'^{\\top}_{O} \\mathbf{v}_{I}) - \\sum_{j=1}^k \\ln \\sigma(-\\mathbf{v}'^{\\top}_{N_j} \\mathbf{v}_{I})$$\n\n## 2. Noise Distribution\n$$P_n(w) \\propto U(w)^{0.75}$$\n*   Bumps rare word sampling probabilities to balance updates.\n",
            "interview": "# Interview Prep: W2V Opt\n\n## Q1: Why do we raise word frequencies to the 3/4 power in the negative sampling distribution?\n\n### Standard Answer\nRaising counts to the 3/4 power ($U(w)^{0.75}$) increases the probability of selecting rare words as negative samples. For example, if a rare word has a frequency of $0.00001$ and a common word has a frequency of $0.01$ (a 1000x difference), raising them to the $0.75$ power yields $0.00017$ and $0.031$ (now a 180x difference). This prevents highly frequent words from dominating the negative selections, ensuring the model learns robust representations for rare terms.\n",
            "example_code": "import numpy as np\n\ndef sigmoid(x):\n    return 1.0 / (1.0 + np.exp(-x))\n\ndef neg_sampling_loss(v_in, v_out_pos, v_out_negs):\n    loss = -np.log(sigmoid(np.dot(v_out_pos, v_in)))\n    for v_neg in v_out_negs:\n        loss -= np.log(sigmoid(-np.dot(v_neg, v_in)))\n    return loss\n\nif __name__ == '__main__':\n    print('Negative Sampling loss tools ready.')\n",
            "practice_code": "import numpy as np\n\ndef sigmoid(x):\n    return 1.0 / (1.0 + np.exp(-x))\n\ndef neg_sampling_loss(v_in, v_out_pos, v_out_negs):\n    loss = -np.log(sigmoid(np.dot(v_out_pos, v_in)))\n    for v_neg in v_out_negs:\n        loss -= np.log(sigmoid(-np.dot(v_neg, v_in)))\n    return loss\n\ndef run_practice():\n    v_in = np.array([1.0, 0.0])\n    v_pos = np.array([0.0, 0.0])\n    v_negs = [np.array([0.0, 0.0])]\n    loss = neg_sampling_loss(v_in, v_pos, v_negs)\n    assert np.allclose(loss, 1.386294)\n    print('[PASS] Neg sampling math verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m3-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary computational benefit of using Hierarchical Softmax instead of a full Softmax output layer?",
                        "options": ["It reduces output complexity from O(V) to O(log V) using a binary Huffman tree.", "It eliminates the need for any backpropagation.", "It makes embedding vectors orthogonal.", "It dynamically prunes the vocabulary during model execution."],
                        "correct_answer": "It reduces output complexity from O(V) to O(log V) using a binary Huffman tree.",
                        "explanation": "Hierarchical Softmax structures words in a binary tree where path selections act as a series of sigmoid splits, dropping complexity to O(log V)."
                    }
                ]
            }
        },
        "nlp-m3-t3": {
            "title": "Global Vectors (GloVe)",
            "notes": {
                "learning_outcomes": [
                    "Formulate the GloVe log co-occurrence ratio equations.",
                    "Derive the weighted least-squares loss objective.",
                    "Contrast window-based skip-gram models with global matrix factorization models."
                ],
                "sections": [
                    {
                        "title": "GloVe Log Co-occurrence Mechanics",
                        "content": "Word2Vec is a local window model that fails to exploit global co-occurrence statistics. Global matrix factorization models (like LSA) capture global statistics but perform poorly on analogies.\n\n**GloVe (Global Vectors for Word Representation)** combines the strengths of both. It fits parameters directly on global co-occurrence ratios. Let $X_{ij}$ be the number of times word $j$ appears in the context of word $i$. The probability of word $j$ appearing in the context of word $i$ is $P(w_j \\mid w_i) = P_{ij} = X_{ij} / X_i$. \n\nGloVe demonstrates that the ratio of co-occurrence probabilities containing a probe word $k$ (e.g. $P_{ik} / P_{jk}$) corresponds to semantic relationships. To map this ratio to vector offsets, GloVe derives the relation:\n\n$$\\mathbf{w}_i^{\\top} \\tilde{\\mathbf{w}}_j + b_i + \\tilde{b}_j = \\ln X_{ij}$$",
                        "callouts": []
                    },
                    {
                        "title": "Weighted Least-Squares Objective",
                        "content": "To fit this relation across the corpus, GloVe minimizes a weighted least-squares objective function:\n\n$$J = \\sum_{i,j=1}^V f(X_{ij}) \\left( \\mathbf{w}_i^{\\top} \\tilde{\\mathbf{w}}_j + b_i + \\tilde{b}_j - \\ln X_{ij} \\right)^2$$\n\nwhere the weighting function $f(x)$ limits the influence of highly frequent pairs while ignoring unobserved pairs ($X_{ij} = 0$, where $\\ln(0)$ is undefined):\n\n$$f(x) = \\begin{cases} \\left( \\frac{x}{x_{\\max}} \\right)^\\alpha & \\text{if } x < x_{\\max} \\\\ 1.0 & \\text{otherwise} \\end{cases}$$\n\nTypically, parameters are set to $x_{\\max} = 100$ and $\\alpha = 0.75$.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# GloVe Mechanics\n\n## 1. Objective Function\n$$J = \\sum_{i,j=1}^V f(X_{ij}) (\\mathbf{w}_i^{\\top} \\tilde{\\mathbf{w}}_j + b_i + \\tilde{b}_j - \\ln X_{ij})^2$$\n\n## 2. Weighting Function\n$$f(x) = (x / x_{\\max})^\\alpha \\quad (\\text{for } x < x_{\\max})$$\n*   Ensures that rare co-occurrences are not weighted heavily, and frequent co-occurrences do not dominate gradients.\n",
            "interview": "# Interview Prep: GloVe\n\n## Q1: How does GloVe combine the advantages of global matrix factorization and local context window models?\n\n### Standard Answer\nMatrix factorization models (like LSA) capture global co-occurrence statistics across the entire corpus but are computationally expensive and perform poorly on analogies. Local window models (like Word2Vec) capture local semantic patterns and perform well on analogies, but fail to exploit global co-occurrence statistics.\n\nGloVe combines these approaches by training directly on the non-zero cells of the global co-occurrence matrix $X$. It derives a log-bilinear relation: $\\mathbf{w}_i^{\\top} \\tilde{\\mathbf{w}}_j + b_i + \\tilde{b}_j = \\ln X_{ij}$, which is optimized using a weighted least-squares loss. This achieves efficient training on global statistics while preserving local semantic structure.",
            "example_code": "import numpy as np\n\ndef glove_weight(x, x_max=100, alpha=0.75):\n    return (x / x_max)**alpha if x < x_max else 1.0\n\nif __name__ == '__main__':\n    print('GloVe weighting metrics active.')\n",
            "practice_code": "def glove_weight(x, x_max=100, alpha=0.75):\n    return (x / x_max)**alpha if x < x_max else 1.0\n\ndef run_practice():\n    assert glove_weight(100) == 1.0\n    assert glove_weight(200) == 1.0\n    print('[PASS] GloVe weighting checks passed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m3-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary role of the weighting function f(X_ij) in the GloVe objective?",
                        "options": ["To prevent very frequent word pairings from dominating the gradient updates and to ignore zero occurrences.", "To scale the dimensions of the embedding vectors.", "To compute cosine similarities during model inference.", "To perform Viterbi parses."],
                        "correct_answer": "To prevent very frequent word pairings from dominating the gradient updates and to ignore zero occurrences.",
                        "explanation": "The weighting function caps the influence of frequent pairs (where X_ij is huge) and ensures that unobserved pairs (where X_ij = 0, log(X_ij) = undefined) contribute 0.0 weight to the loss."
                    }
                ]
            }
        },
        "nlp-m3-t4": {
            "title": "FastText Subword Embeddings",
            "notes": {
                "learning_outcomes": [
                    "Formulate subword n-gram representation mathematics.",
                    "Explain how FastText generates vectors for out-of-vocabulary (OOV) tokens."
                ],
                "sections": [
                    {
                        "title": "FastText Model",
                        "content": "Word2Vec and GloVe represent words as atomic units, failing to capture morphological relationships (e.g. 'running' and 'runner' share the root 'run' but have independent vectors). This creates issues for morphologically rich languages.\n\n**FastText** resolves this by representing each word as a bag of character n-grams. For a word $w$, we append boundary markers `<` and `>` and extract character n-grams of lengths $n$ (typically $3 \\le n \\le 6$). For example, the word 'where' with $n=3$ is represented by the character n-grams: `<wh`, `whe`, `her`, `ere`, `re>` and the special sequence `<where>`. The final word vector is the sum of these subword vectors:\n\n$$\\mathbf{v}(w) = \\sum_{g \\in \\mathcal{G}_w} \\mathbf{v}_g$$\n\nwhere $\\mathcal{G}_w$ is the set of character n-grams constructing word $w$.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# FastText Subword Embeddings\n\n$$\\mathbf{v}(w) = \\sum_{g \\in \\mathcal{G}_w} \\mathbf{v}_g$$\n*   Represents words as sums of character n-gram embeddings.\n*   Enables generating vectors for unseen tokens by aggregating subword pieces.\n",
            "interview": "# Interview Prep: FastText\n\n## Q1: How does FastText construct representation vectors for completely unseen, out-of-vocabulary (OOV) words at test time?\n\n### Standard Answer\nSince FastText represents words as sums of character n-gram embeddings, an unseen word can still be tokenized into its constituent character n-grams. FastText sums the pre-trained embeddings of these subword n-grams to produce a representation vector, capturing morphological patterns (e.g., matching the suffix '-ly').\n",
            "example_code": "import numpy as np\n\ndef get_char_ngrams(word, n=3):\n    extended_word = '<' + word + '>'\n    return [extended_word[i:i+n] for i in range(len(extended_word)-n+1)]\n\nif __name__ == '__main__':\n    print('FastText char n-gram generator loaded.')\n",
            "practice_code": "def get_char_ngrams(word, n=3):\n    extended_word = '<' + word + '>'\n    return [extended_word[i:i+n] for i in range(len(extended_word)-n+1)]\n\ndef run_practice():\n    ngrams = get_char_ngrams('cat', 3)\n    assert '<ca' in ngrams\n    assert 'at>' in ngrams\n    print('[PASS] FastText n-gram generation verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m3-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary advantage of FastText over standard Word2Vec?",
                        "options": ["It can generate semantic vector representations for unseen (OOV) words by aggregating subword n-gram embeddings.", "It has a smaller dictionary size.", "It uses a deep feedforward network.", "It uses recurrent states."],
                        "correct_answer": "It can generate semantic vector representations for unseen (OOV) words by aggregating subword n-gram embeddings.",
                        "explanation": "Because it builds vectors from character-level chunks, FastText retains the ability to represent morphologically similar OOV tokens."
                    }
                ]
            }
        },
        "nlp-m3-t5": {
            "title": "Semantic Analogies",
            "notes": {
                "learning_outcomes": [
                    "Formulate vector arithmetic calculations for analogies.",
                    "Apply cosine similarity projections.",
                    "Explain the 3CosMul equation."
                ],
                "sections": [
                    {
                        "title": "Vector Arithmetic and Projections",
                        "content": "Word embeddings capture relational semantics through linear structural translations. The classical relation 'king - man + woman = queen' is solved by searching for the vocabulary token that maximizes cosine similarity:\n\n$$\\mathbf{w}^* = \\arg\\max_{\\mathbf{w} \\in \\mathcal{V} \\setminus \\{a, b, c\\}} \\text{sim}(\\mathbf{w}, \\mathbf{v}_b - \\mathbf{v}_a + \\mathbf{v}_c)$$\n\nwhere $\\mathbf{v}_a, \\mathbf{v}_b, \\mathbf{v}_c$ are the vectors for 'man', 'king', and 'woman' respectively.",
                        "callouts": [
                            {
                                "type": "Student Trap",
                                "title": "Dominance of Similarity Terms",
                                "content": "The linear formulation (3CosAdd) can be dominated by a single term that has high similarity to the target vector. For example, if a word is highly similar to $\\mathbf{v}_c$, it can be selected even if it does not satisfy the analogy relationship. To resolve this, use the multiplicative formulation (3CosMul) instead."
                            }
                        ]
                    },
                    {
                        "title": "The 3CosMul Formulation",
                        "content": "To prevent a single term from dominating the analogy search, Levy and Goldberg introduced **3CosMul**:\n\n$$\\mathbf{w}^* = \\arg\\max_{\\mathbf{w} \\in \\mathcal{V} \\setminus \\{a, b, c\\}} \\frac{\\text{sim}(\\mathbf{w}, \\mathbf{v}_b) \\times \\text{sim}(\\mathbf{w}, \\mathbf{v}_c)}{\\text{sim}(\\mathbf{w}, \\mathbf{v}_a) + \\epsilon}$$\n\nwhere $\\epsilon = 0.001$ prevents division by zero. This balances the similarities multiplicatively, requiring candidate tokens to have high similarity to both positive terms ($b$ and $c$) while keeping similarity to the negative term ($a$) low.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Semantic Analogies\n\n## 1. 3CosAdd Formulation\n$$\\mathbf{w}^* = \\arg\\max_{\\mathbf{w}} \\operatorname{sim}(\\mathbf{w}, \\mathbf{v}_b - \\mathbf{v}_a + \\mathbf{v}_c)$$\n\n## 2. 3CosMul Formulation\n$$\\mathbf{w}^* = \\arg\\max_{\\mathbf{w}} \\frac{\\operatorname{sim}(\\mathbf{w}, \\mathbf{v}_b) \\times \\operatorname{sim}(\\mathbf{w}, \\mathbf{v}_c)}{\\operatorname{sim}(\\mathbf{w}, \\mathbf{v}_a) + \\epsilon}$$\n",
            "interview": "# Interview Prep: Analogies\n\n## Q1: Why does the 3CosMul formulation perform better than 3CosAdd for solving analogies in word embedding spaces?\n\n### Standard Answer\nThe 3CosAdd formulation evaluates similarity using linear addition:\n\n$$\\arg\\max_{\\mathbf{w}} \\left[ \\text{sim}(\\mathbf{w}, \\mathbf{v}_b) - \\text{sim}(\\mathbf{w}, \\mathbf{v}_a) + \\text{sim}(\\mathbf{w}, \\mathbf{v}_c) \\right]$$\n\nThis additive combination allows a word that is extremely close to $\\mathbf{v}_c$ to dominate the optimization, even if it has no relation to the query. For example, in the analogy 'man:king :: apple:?', the model might output 'apples' simply because 'apples' is highly similar to 'apple'.\n\n3CosMul converts this relationship to a product of ratios:\n\n$$\\arg\\max_{\\mathbf{w}} \\frac{\\text{sim}(\\mathbf{w}, \\mathbf{v}_b) \\times \\text{sim}(\\mathbf{w}, \\mathbf{v}_c)}{\\text{sim}(\\mathbf{w}, \\mathbf{v}_a) + \\epsilon}$$\n\nThis multiplicative combination acts as an AND gate. A candidate must be similar to both $b$ and $c$ while being distinct from $a$, preventing single-term dominance.",
            "example_code": "import numpy as np\n\ndef find_analogy(a, b, c, word_matrix, vocab_list):\n    target = b - a + c\n    scores = np.dot(word_matrix, target) / (np.linalg.norm(word_matrix, axis=1) * np.linalg.norm(target))\n    return vocab_list[np.argmax(scores)]\n\nif __name__ == '__main__':\n    print('Analogy calculation module compiled.')\n",
            "practice_code": "import numpy as np\n\ndef run_practice():\n    matrix = np.array([[1.0, 0.0], [0.0, 1.0], [0.7, 0.7]])\n    vocab = ['a', 'b', 'c']\n    target = np.array([0.5, 0.5])\n    scores = np.dot(matrix, target) / (np.linalg.norm(matrix, axis=1) * np.linalg.norm(target))\n    assert np.argmax(scores) == 2\n    print('[PASS] Analogy argmax validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m3-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the baseline search constraint applied when solving the analogy a:b :: c:d?",
                        "options": ["The candidate token 'd' must be different from 'a', 'b', and 'c'.", "The vector norm must equal 1.0.", "It must be an out-of-vocabulary word.", "It must be a stopword."],
                        "correct_answer": "The candidate token 'd' must be different from 'a', 'b', and 'c'.",
                        "explanation": "To prevent trivial identity returns, the input tokens a, b, and c are explicitly excluded from the candidate search space."
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
        write_file(os.path.join(nlp_dir, "notes", f"{topic_id}.json"), json.dumps(notes_content, indent=2))
        write_file(os.path.join(nlp_dir, "revision", f"{topic_id}.md"), data["revision"])
        write_file(os.path.join(nlp_dir, "interview", f"{topic_id}.md"), data["interview"])
        write_file(os.path.join(nlp_dir, "examples", f"{topic_id}-ex1.py"), data["example_code"])
        write_file(os.path.join(nlp_dir, "practice", f"{topic_id}-prac1.py"), data["practice_code"])
        write_file(os.path.join(nlp_dir, "quiz", f"{topic_id}-quiz.json"), json.dumps(data["quiz"], indent=2))

    print("\nSuccessfully generated enriched NLP Module 3 files!")

if __name__ == "__main__":
    main()
