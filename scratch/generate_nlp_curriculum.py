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

    topics_data = {
        # --- MODULE 1 ---
        "nlp-m1-t3": {
            "title": "POS Tagging & Named Entity Recognition",
            "notes": {
                "learning_outcomes": [
                    "Explain sequence labeling paradigms for POS tagging and NER.",
                    "Derive transition and emission probabilities in Hidden Markov Models (HMM).",
                    "Implement the Viterbi algorithm for finding the optimal state sequence."
                ],
                "sections": [
                    {
                        "title": "Sequence Labeling and POS Tagging",
                        "content": "Sequence labeling is the task of assigning a categorical label to each token in a sequence. Part-of-Speech (POS) tagging maps words to their syntactic roles (e.g., noun, verb, adjective), while Named Entity Recognition (NER) identifies span-based entities (e.g., persons, locations, organizations) using boundary tags like BIO (Begin, Inside, Outside).",
                        "callouts": [{"type": "Student Trap", "title": "BIO Tagging Ambiguity", "content": "When parsing NER outputs, ensure that an 'I-ORG' tag is never permitted to follow an 'O' tag without an intervening 'B-ORG' tag. Enforce strict transition grammar rules in your decoder."}]
                    },
                    {
                        "title": "Hidden Markov Models (HMM) Mathematics",
                        "content": "A Hidden Markov Model (HMM) is a generative transition model. The joint probability of a sequence of states (POS tags) $\\mathbf{y} = (y_1, \\dots, y_T)$ and observations (words) $\\mathbf{x} = (x_1, \\dots, x_T)$ is:\n\n$$P(\\mathbf{x}, \\mathbf{y}) = \\prod_{t=1}^T P(y_t \\mid y_{t-1}) P(x_t \\mid y_t)$$\n\nwhere $P(y_t \\mid y_{t-1})$ is the transition probability, and $P(x_t \\mid y_t)$ is the emission probability. These are computed using maximum likelihood estimates from a tagged training corpus.",
                        "callouts": [{"type": "Engineering Note", "title": "Laplace Smoothing for Unseen Emissions", "content": "If a word never appeared with a tag in training, its emission probability $P(x_t \\mid y_t)$ is $0.0$, zeroing out the entire joint probability. Always apply add-one (Laplace) smoothing to transition and emission counts."}]
                    }
                ]
            },
            "revision": "# POS Tagging & Named Entity Recognition\n\n## 1. Sequence Labeling\nMaps $\\mathbf{x} \\to \\mathbf{y}$. POS tagging assigns syntactic tags, while NER assigns span categories (e.g., Person, Location) using BIO tagging schemes.\n\n## 2. HMM Probabilities\nJoint probability of sequence:\n\n$$P(\\mathbf{x}, \\mathbf{y}) = \\prod_{t=1}^T P(y_t \\mid y_{t-1}) P(x_t \\mid y_t)$$\n\n*   **Transition Probability:** $P(y_t \\mid y_{t-1}) = \\frac{C(y_{t-1}, y_t)}{C(y_{t-1})}$\n*   **Emission Probability:** $P(x_t \\mid y_t) = \\frac{C(y_t, x_t)}{C(y_t)}$\n",
            "interview": "# Interview Prep: POS Tagging & NER\n\n## Q1: How does the Viterbi algorithm compute the most likely sequence of hidden states in an HMM?\n\n### Standard Answer\nThe Viterbi algorithm is a dynamic programming algorithm. It computes the trellis of maximum path probabilities:\n\n$$v_t(j) = \\max_{i} [ v_{t-1}(i) \\times P(y_t=j \\mid y_{t-1}=i) ] \\times P(x_t \\mid y_t=j)$$\n\nwhich represents the probability of the most likely state sequence ending in state $j$ at time $t$. By storing backpointers, we reconstruct the optimal path.\n\n|INTERVIEW TRAP: Underflow in Trellis Multiplication Repeated multiplication of small probabilities causes floating-point underflow. Always compute Viterbi updates in the log domain: $\\log v_t(j) = \\max_{i} [ \\log v_{t-1}(i) + \\log P(y_t \\mid y_{t-1}) ] + \\log P(x_t \\mid y_t)$.|\n|---|\n",
            "example_code": "import numpy as np\n\ndef viterbi_decode(obs, states, start_p, trans_p, emit_p):\n    T = len(obs)\n    N = len(states)\n    viterbi = np.zeros((N, T))\n    backpointer = np.zeros((N, T), dtype=int)\n    for s in range(N):\n        viterbi[s, 0] = start_p[s] * emit_p[s, obs[0]]\n    for t in range(1, T):\n        for s in range(N):\n            prob = viterbi[:, t-1] * trans_p[:, s] * emit_p[s, obs[t]]\n            viterbi[s, t] = np.max(prob)\n            backpointer[s, t] = np.argmax(prob)\n    best_path = []\n    state = np.argmax(viterbi[:, T-1])\n    best_path.append(state)\n    for t in range(T-1, 0, -1):\n        state = backpointer[state, t]\n        best_path.insert(0, state)\n    return best_path, viterbi\n\nif __name__ == '__main__':\n    print('POS Viterbi implementation loaded successfully.')\n",
            "practice_code": "import numpy as np\n\ndef run_practice():\n    states = [0, 1]  # Noun, Verb\n    obs = [0, 1]     # 'cat', 'runs'\n    trans = np.array([[0.4, 0.6], [0.5, 0.5]])\n    emit = np.array([[0.8, 0.2], [0.1, 0.9]])\n    start = np.array([0.9, 0.1])\n    v0 = start * emit[:, obs[0]]\n    v1_noun = np.max(v0 * trans[:, 0] * emit[0, obs[1]])\n    assert np.allclose(v1_noun, 0.0576)\n    print('[PASS] Viterbi manual calculation matches assertions.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m1-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the time complexity of the Viterbi decoding algorithm in terms of the number of states N and the sequence length T?",
                        "options": ["O(N^2 * T)", "O(N * T^2)", "O(N^2 * T^2)", "O(N^3 * T)"],
                        "correct_answer": "O(N^2 * T)",
                        "explanation": "At each of the T time steps, the algorithm computes transition updates from all N preceding states to all N current states, yielding N * N = N^2 operations per step, resulting in a total complexity of O(N^2 * T)."
                    }
                ]
            }
        },
        "nlp-m1-t4": {
            "title": "Topic Modeling",
            "notes": {
                "learning_outcomes": [
                    "Formulate Latent Dirichlet Allocation (LDA) probabilistic model parameters.",
                    "Explain Dirichlet priors and their impact on topic sparsity.",
                    "Trace Gibbs sampling iterations for parameter estimations."
                ],
                "sections": [
                    {
                        "title": "Latent Dirichlet Allocation (LDA)",
                        "content": "Latent Dirichlet Allocation (LDA) is a generative model for identifying topics within a text corpus. Under LDA, each document is modeled as a mixture of latent topics, and each topic is modeled as a distribution over words. The Dirichlet distribution serves as a conjugate prior for the multinomial topic and word distributions, simplifying posterior inference.",
                        "callouts": [{"type": "Student Trap", "title": "Unsupervised Topic Labels", "content": "LDA does not name topics. It output word probability distributions (e.g. topic 1 has high probability for 'bank', 'finance', 'money'). Labelling these topics requires manual domain validation."}]
                    }
                ]
            },
            "revision": "# Topic Modeling (LDA)\n\n## 1. LDA Probabilistic Generation\nFor each document $d \\in \\mathcal{D}$:\n1. Choose topic distribution $\\theta_d \\sim \\text{Dirichlet}(\\alpha)$\n2. For each word $w_i$ in $d$:\n   a. Choose a topic $z_i \\sim \\text{Multinomial}(\\theta_d)$\n   b. Choose word $w_i \\sim \\text{Multinomial}(\\phi_{z_i})$ where $\\phi_k \\sim \\text{Dirichlet}(\\beta)$\n",
            "interview": "# Interview Prep: LDA\n\n## Q1: How does Gibbs Sampling estimate parameters in LDA?\n\n### Standard Answer\nGibbs sampling estimates the latent topic assignments by iteratively sampling the topic of each word $i$ conditional on all other assignments:\n\n$$P(z_i = k \\mid \\mathbf{z}_{-i}, \\mathbf{w}, \\alpha, \\beta) \\propto \\frac{n_{k,-i}^{(v)} + \\beta}{\\sum_{v=1}^V (n_{k,-i}^{(v)} + \\beta)} \\times \\frac{n_{d,-i}^{(k)} + \\alpha}{\\sum_{k'=1}^K (n_{d,-i}^{(k')} + \\alpha)}$$\n\nwhere $n_{k,-i}^{(v)}$ is the count of word $v$ assigned to topic $k$ excluding the current token.\n",
            "example_code": "import numpy as np\n\ndef sample_topic(p_dist):\n    return np.random.choice(len(p_dist), p=p_dist/np.sum(p_dist))\n\nif __name__ == '__main__':\n    print('Gibbs sampler helper module loaded.')\n",
            "practice_code": "import numpy as np\n\ndef run_practice():\n    t1 = 5.1 / 101.0\n    t2 = 2.1 / 10.2\n    expected = t1 * t2\n    assert np.allclose(expected, 0.01039, atol=1e-4)\n    print('[PASS] Gibbs math checks validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m1-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What happens if we decrease the Dirichlet hyperparameters alpha and beta toward zero?",
                        "options": ["The distributions become highly sparse, forcing documents to contain few topics and topics to contain few words.", "The distributions become uniform, representing flat probabilities.", "The vocabulary size shrinks.", "LDA fails to compile."],
                        "correct_answer": "The distributions become highly sparse, forcing documents to contain few topics and topics to contain few words.",
                        "explanation": "Dirichlet distributions with parameter values less than 1 concentrate probability mass at the boundaries (vertices of the simplex), resulting in sparse distributions."
                    }
                ]
            }
        },
        "nlp-m1-t5": {
            "title": "Sentiment Analysis",
            "notes": {
                "learning_outcomes": [
                    "Compare rule-based sentiment systems (VADER) with classification models.",
                    "Formulate Naive Bayes log-likelihood calculations for text classification."
                ],
                "sections": [
                    {
                        "title": "Lexicon-Based Sentiment Analysis",
                        "content": "Lexicon-based sentiment analysis maps terms to predefined polarity values (e.g., 'good' = 2.0, 'terrible' = -3.0). VADER (Valence Aware Dictionary and sEntiment Reasoner) incorporates grammatical rules like intensifiers (e.g., 'very good') and negations ('not good') to compute normalized compound polarity scores.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Sentiment Analysis\n\n## 1. Naive Bayes Classification\nSelect tag $c$ maximizing:\n\n$$c_{NB} = \\arg\\max_{c \\in \\mathcal{C}} \\log P(c) + \\sum_{i=1}^W \\log P(w_i \\mid c)$$\n",
            "interview": "# Interview Prep: Sentiment Analysis\n\n## Q1: Why does Naive Bayes perform well on sentiment tasks despite the 'naive' independence assumption?\n\n### Standard Answer\nNaive Bayes assumes token probabilities are conditionally independent given the class. While untrue (since syntax and grammar create strong word correlations), text classification tasks only require correct ranking boundaries (argmax) rather than exact probability calibration. Even if joint probabilities are skewed, the decision boundary remains highly robust.\n",
            "example_code": "import numpy as np\n\ndef naive_bayes_predict(log_prior, log_likelihood, doc_tokens):\n    class_scores = log_prior.copy()\n    for t in doc_tokens:\n        if t in log_likelihood:\n            class_scores += log_likelihood[t]\n    return class_scores\n\nif __name__ == '__main__':\n    print('Naive Bayes prediction framework initialized.')\n",
            "practice_code": "import numpy as np\n\ndef run_practice():\n    prior = np.array([np.log(0.5), np.log(0.5)])\n    likelihood = {'good': np.array([np.log(0.8), np.log(0.2)]), 'bad': np.array([np.log(0.1), np.log(0.9)])}\n    scores = prior + likelihood['good'] + likelihood['bad']\n    expected = np.array([np.log(0.5*0.8*0.1), np.log(0.5*0.2*0.9)])\n    assert np.allclose(scores, expected)\n    print('[PASS] Naive Bayes likelihood manual calculation passes.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m1-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Which Naive Bayes parameter estimation method is commonly used to prevent multiplying by zero probabilities for unseen terms?",
                        "options": ["Laplace (add-one) smoothing", "Gibbs sampling", "Vector quantization", "Backoff model scaling"],
                        "correct_answer": "Laplace (add-one) smoothing",
                        "explanation": "Laplace smoothing adds a constant (typically 1) to both the numerator and denominator counts, guaranteeing non-zero probabilities for all features."
                    }
                ]
            }
        },
        # --- MODULE 2 ---
        "nlp-m2-t1": {
            "title": "Bag of Words & N-Grams",
            "notes": {
                "learning_outcomes": [
                    "Formulate CountVectorizer document frequency occurrences.",
                    "Map N-Gram bound parameters and vocabulary limits."
                ],
                "sections": [
                    {
                        "title": "Text Vectorization via Bag of Words",
                        "content": "Bag of Words (BoW) models discard syntax and grammar, representing documents strictly as a count vector over a vocabulary. The document matrix $\\mathbf{X} \\in \\mathbb{R}^{M \\times N}$ stores the occurrence frequencies of terms.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Bag of Words & N-Grams\n\n## 1. BoW Occurrence Representation\nGiven vocabulary $\\mathcal{V}$, document vector $\\mathbf{d} \\in \\mathbb{R}^{|\\mathcal{V}|}$ is:\n\n$$d_j = \\sum_{t \\in \\text{tokens}} \\mathbb{I}(t = w_j)$$\n",
            "interview": "# Interview Prep: BoW & N-Grams\n\n## Q1: Why does N-gram modeling lead to vocabulary scaling bottlenecks?\n\n### Standard Answer\nAs $n$ increases, the theoretical vocabulary size scales exponentially as $|\\mathcal{V}|^n$. For a modest vocabulary of 10,000 words, bigrams yield $10^8$ possible combinations and trigrams yield $10^{12}$, creating massive sparsity and RAM constraints.\n",
            "example_code": "import numpy as np\n\ndef get_ngrams(tokens, n):\n    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]\n\nif __name__ == '__main__':\n    print('N-Gram generator initialized.')\n",
            "practice_code": "def run_practice():\n    toks = ['the', 'cat', 'sat']\n    bigrams = [('the', 'cat'), ('cat', 'sat')]\n    assert [tuple(toks[i:i+2]) for i in range(len(toks)-1)] == bigrams\n    print('[PASS] N-gram tests completed.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m2-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary constraint of the Bag of Words representation?",
                        "options": ["It completely discards word order and grammatical context.", "It is slow to compute.", "It cannot handle integer weights.", "It requires a deep neural network to parse."],
                        "correct_answer": "It completely discards word order and grammatical context.",
                        "explanation": "Bag of Words models documents as unstructured frequency counts, ignoring the syntactic order of terms."
                    }
                ]
            }
        },
        "nlp-m2-t2": {
            "title": "TF-IDF Mathematics",
            "notes": {
                "learning_outcomes": [
                    "Derive Term Frequency and Inverse Document Frequency math.",
                    "Apply sublinear scaling and L2 normalization parameters."
                ],
                "sections": [
                    {
                        "title": "TF-IDF Equations",
                        "content": "TF-IDF balances term occurrences inside a document against corpus-wide distribution. Mathematically:\n\n$$\\text{TF-IDF}(t, d, \\mathcal{C}) = \\text{TF}(t, d) \\times \\text{IDF}(t, \\mathcal{C})$$\n\nwhere $\\text{IDF}(t, \\mathcal{C}) = \\log \\frac{1 + M}{1 + |\\{d \\in \\mathcal{C} : t \\in d\\}|} + 1$. Normalizing documents using the L2 norm eliminates length biases.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# TF-IDF Mathematics\n\n## 1. Equations\n$$\\text{TF-IDF}(t, d) = \\text{TF}(t, d) \\times \\text{IDF}(t)$$\n$$\\text{IDF}(t) = \\log \\frac{M}{1 + \\text{DF}(t)} + 1$$\n",
            "interview": "# Interview Prep: TF-IDF\n\n## Q1: Why do we apply L2 normalization to TF-IDF document vectors?\n\n### Standard Answer\nL2 normalization divides each element by the vector's Euclidean length. This ensures that longer documents, which naturally contain more words (and thus higher raw term counts), do not skew similarity metrics. Normalization maps all document representations to a unit sphere.\n",
            "example_code": "import numpy as np\n\ndef compute_tfidf(tf, df, M):\n    idf = np.log(M / (1 + df)) + 1.0\n    return tf * idf\n\nif __name__ == '__main__':\n    print('TF-IDF equations compiled.')\n",
            "practice_code": "import numpy as np\n\ndef run_practice():\n    idf = np.log(100.0 / 10.0) + 1.0\n    tfidf = 2.0 * idf\n    assert np.allclose(tfidf, 6.60517)\n    print('[PASS] TF-IDF equations manual verification passes.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m2-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What does a high TF-IDF score indicate for a given term in a document?",
                        "options": ["The term is highly frequent in the current document but rare across the general corpus.", "The term is common in all documents.", "The term is a stopword.", "The term has been normalized to zero."],
                        "correct_answer": "The term is highly frequent in the current document but rare across the general corpus.",
                        "explanation": "TF-IDF reaches its maximum when a term appears frequently in a single document (high TF) but is relatively unique in the rest of the corpus (high IDF)."
                    }
                ]
            }
        },
        "nlp-m2-t3": {
            "title": "Vector Similarity Metrics",
            "notes": {
                "learning_outcomes": [
                    "Derive Cosine Similarity bounds.",
                    "Contrast Euclidean distance with Cosine metrics."
                ],
                "sections": [
                    {
                        "title": "Cosine Similarity",
                        "content": "Cosine Similarity measures the angular alignment between two multi-dimensional vectors:\n\n$$\\text{sim}(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2}$$\n\nIf vectors have non-negative elements, the similarity metric lies in $[0, 1]$.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Similarity Metrics\n\n$$\\text{Cosine}(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2}$$\n",
            "interview": "# Interview Prep: Similarity Metrics\n\n## Q1: Explain why Euclidean distance is inadequate for document similarity checks on raw term frequencies.\n\n### Standard Answer\nEuclidean distance measures the physical distance between coordinates. Two documents with identical topics but different lengths will lie on the same vector direction but have a large Euclidean distance. Cosine similarity looks strictly at the angle, rendering it invariant to document length.\n",
            "example_code": "import numpy as np\n\ndef cosine_similarity(u, v):\n    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))\n\nif __name__ == '__main__':\n    print('Similarity metric modules configured.')\n",
            "practice_code": "import numpy as np\n\ndef run_practice():\n    u = np.array([1, 1, 0])\n    v = np.array([0, 1, 1])\n    sim = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))\n    assert np.allclose(sim, 0.5)\n    print('[PASS] Cosine calculation matches expectation.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m2-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the cosine similarity score between two perpendicular vectors?",
                        "options": ["0.0", "1.0", "-1.0", "0.5"],
                        "correct_answer": "0.0",
                        "explanation": "If two vectors are perpendicular (orthogonal), their dot product is 0.0, rendering their cosine similarity 0.0."
                    }
                ]
            }
        },
        "nlp-m2-t4": {
            "title": "N-Gram Language Models",
            "notes": {
                "learning_outcomes": [
                    "Formulate MLE language models.",
                    "Trace Kneser-Ney smoothing distributions."
                ],
                "sections": [
                    {
                        "title": "Language Models",
                        "content": "An N-Gram language model estimates probability distribution patterns over sequences. Under the Markov assumption, the next word depends only on the preceding $N-1$ words:\n\n$$P(w_i \\mid w_1 \\dots w_{i-1}) \\approx P(w_i \\mid w_{i-N+1} \\dots w_{i-1})$$",
                        "callouts": []
                    }
                ]
            },
            "revision": "# N-Gram Language Models\n\n## 1. MLE Estimation\n$$P_{MLE}(w_i \\mid w_{i-1}) = \\frac{C(w_{i-1}, w_i)}{C(w_{i-1})}$$\n",
            "interview": "# Interview Prep: N-Gram LMs\n\n## Q1: How does Kneser-Ney smoothing improve on simple backoff smoothing models?\n\n### Standard Answer\nKneser-Ney smoothing estimates probabilities based on how likely a word is to complete an unseen context. Words that appear in many contexts (high continuation probability) are favored over words that have high individual frequency but only occur in specific contexts.\n",
            "example_code": "import numpy as np\n\ndef mle_probability(pair_count, prefix_count):\n    return pair_count / prefix_count if prefix_count > 0 else 0.0\n\nif __name__ == '__main__':\n    print('MLE LM initialized.')\n",
            "practice_code": "def run_practice():\n    assert 5 / 10 == 0.5\n    print('[PASS] N-gram probability test validated.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m2-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the key limitation of Laplace (add-one) smoothing for language modeling?",
                        "options": ["It shifts too much probability mass from observed words to unseen words in large vocabularies.", "It cannot handle zero counts.", "It violates Markov assumptions.", "It is slow to parse."],
                        "correct_answer": "It shifts too much probability mass from observed words to unseen words in large vocabularies.",
                        "explanation": "Adding 1 to every word in a large vocabulary V drastically reduces the probability of frequent observed patterns, skewing the overall model."
                    }
                ]
            }
        },
        "nlp-m2-t5": {
            "title": "Perplexity & Evaluation",
            "notes": {
                "learning_outcomes": [
                    "Derive Perplexity equations from entropy metrics.",
                    "Formulate Word Error Rate metrics."
                ],
                "sections": [
                    {
                        "title": "Perplexity (PPL)",
                        "content": "Perplexity is a measurement evaluating how well a probability model predicts a sample sequence. It is the exponentiated cross-entropy:\n\n$$\\text{PPL}(W) = P(w_1 w_2 \\dots w_N)^{-\\frac{1}{N}} = 2^{H(p)}$$",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Perplexity & Evaluation\n\n$$\\text{PPL}(W) = \\left( \\prod_{i=1}^N P(w_i \\mid w_{1} \\dots w_{i-1}) \\right)^{-\\frac{1}{N}}$$\n",
            "interview": "# Interview Prep: Perplexity\n\n## Q1: How does a perplexity score of 100 translate to random branching factor representations?\n\n### Standard Answer\nA perplexity of 100 indicates that the model is as confused as if it had to choose uniformly from a vocabulary of 100 possibilities for each next token prediction. Lower perplexity scores imply a more confident model.\n",
            "example_code": "import numpy as np\n\ndef compute_perplexity(log_likelihoods):\n    avg_neg_log_likelihood = -np.mean(log_likelihoods)\n    return np.exp(avg_neg_log_likelihood)\n\nif __name__ == '__main__':\n    print('PPL tools initialized.')\n",
            "practice_code": "import numpy as np\n\ndef compute_perplexity(log_likelihoods):\n    avg_neg_log_likelihood = -np.mean(log_likelihoods)\n    return np.exp(avg_neg_log_likelihood)\n\ndef run_practice():\n    ll = np.array([np.log(0.1), np.log(0.1)])\n    ppl = compute_perplexity(ll)\n    assert np.allclose(ppl, 10.0)\n    print('[PASS] PPL validation matches expected value.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m2-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the relationship between perplexity (PPL) and language model entropy (H)?",
                        "options": ["PPL = e^H (or 2^H)", "PPL = log(H)", "PPL = 1 / H", "PPL = H^2"],
                        "correct_answer": "PPL = e^H (or 2^H)",
                        "explanation": "Perplexity is defined as the exponential of the average cross-entropy of the predictive model, representing the equivalent choice size."
                    }
                ]
            }
        },
        # --- MODULE 3 ---
        "nlp-m3-t1": {
            "title": "Word2Vec Framework",
            "notes": {
                "learning_outcomes": [
                    "Explain CBOW vs Skip-Gram architecture details.",
                    "Formulate projection layer equations."
                ],
                "sections": [
                    {
                        "title": "Word2Vec Foundations",
                        "content": "Word2Vec models word vectors by training a shallow two-layer neural network on word context occurrences. Under the Skip-Gram paradigm, the model predicts surrounding context words given a target word. Under the CBOW (Continuous Bag of Words) paradigm, the model predicts a target word given context words.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Word2Vec Framework\n\n## 1. Skip-Gram Objective\nMaximize average log probability:\n\n$$\\mathcal{L} = \\frac{1}{T} \\sum_{t=1}^T \\sum_{-c \\le j \\le c, j \\neq 0} \\log P(w_{t+j} \\mid w_t)$$\n",
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
                    "Derive Negative Sampling loss functions.",
                    "Explain Hierarchical Softmax structures."
                ],
                "sections": [
                    {
                        "title": "Negative Sampling Math",
                        "content": "To avoid updating the entire output projection layer at each step, negative sampling converts the multinomial classification problem into a set of binary classification tasks. The objective function is:\n\n$$\\mathcal{L}_{SG-NEG} = \\log \\sigma(\\mathbf{v}'^{\\top}_{w_O} \\mathbf{v}_{w_I}) + \\sum_{i=1}^k \\mathbb{E}_{w_i \\sim P_n(w)} [\\log \\sigma(-\\mathbf{v}'^{\\top}_{w_i} \\mathbf{v}_{w_I})]$$",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Word2Vec Optimization\n\n$$\\mathcal{L} = \\log \\sigma(\\mathbf{v}'^{\\top}_{O} \\mathbf{v}_{I}) + \\sum_{j=1}^k \\log \\sigma(-\\mathbf{v}'^{\\top}_{N_j} \\mathbf{v}_{I})$$\n",
            "interview": "# Interview Prep: W2V Opt\n\n## Q1: Why do we raise word frequencies to the 3/4 power in the negative sampling distribution?\n\n### Standard Answer\nRaising counts to the 3/4 power ($U(w)^{0.75}$) increases the probability of selecting rare words as negative samples, preventing highly frequent words (like 'the') from dominating the negative selections.\n",
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
                    "Formulate GloVe co-occurrence matrix math.",
                    "Derive weighted least-squares loss objectives."
                ],
                "sections": [
                    {
                        "title": "GloVe (Global Vectors for Word Representation)",
                        "content": "GloVe maps words into a semantic space by fitting parameters directly on global co-occurrence statistics. The objective function minimizes weighted squared reconstruction errors:\n\n$$J = \\sum_{i,j=1}^V f(X_{ij}) (w_i^{\\top} \\tilde{w}_j + b_i + \\tilde{b}_j - \\log X_{ij})^2$$\n\nwhere $f(x) = (x / x_{max})^\\alpha$ if $x < x_{max}$ else $1.0$.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# GloVe Mechanics\n\n$$J = \\sum_{i,j=1}^V f(X_{ij}) (w_i^{\\top} \\tilde{w}_j + b_i + \\tilde{b}_j - \\log X_{ij})^2$$\n",
            "interview": "# Interview Prep: GloVe\n\n## Q1: How does GloVe combine the advantages of global matrix factorization and local context window models?\n\n### Standard Answer\nMatrix factorization (like LSA) captures global co-occurrence distributions but is computationally expensive and performs poorly on analogies. Local window models (like Word2Vec) capture local semantic patterns but fail to exploit co-occurrence statistics. GloVe trains on global co-occurrence ratios directly, achieving efficient model iterations.\n",
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
                    "Explain subword n-gram representation math.",
                    "Handle out-of-vocabulary (OOV) tokens via character n-grams."
                ],
                "sections": [
                    {
                        "title": "FastText Model",
                        "content": "FastText generalises Word2Vec by representing each word as a bag of character n-grams. For instance, the word 'where' with $n=3$ is represented by the character n-grams: `<wh`, `whe`, `her`, `ere`, `re>` and the special sequence `<where>`. The final word vector is the sum of these subword vectors.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# FastText Subword Embeddings\n\n$$v(w) = \\sum_{g \\in \\mathcal{G}_w} v_g$$\n\nwhere $\\mathcal{G}_w$ is the set of character n-grams constructing word $w$.\n",
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
                    "Apply cosine similarity projections."
                ],
                "sections": [
                    {
                        "title": "Word Vector Analogies",
                        "content": "Word embeddings capture relational semantics through linear structural translations. The classical relation 'king - man + woman = queen' is solved by searching for the vocabulary token that maximizes cosine similarity:\n\n$$\\mathbf{w}^* = \\arg\\max_{\\mathbf{w} \\in \\mathcal{V} \\setminus \\{a, b, c\\}} \\text{sim}(\\mathbf{w}, \\mathbf{b} - \\mathbf{a} + \\mathbf{c})$$",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Semantic Analogies\n\n$$\\mathbf{w}^* = \\arg\\max_{\\mathbf{w}} \\operatorname{Cosine}(\\mathbf{w}, \\mathbf{v}_b - \\mathbf{v}_a + \\mathbf{v}_c)$$\n",
            "interview": "# Interview Prep: Analogies\n\n## Q1: Why does linear vector arithmetic fail to capture analogies in poorly-trained semantic spaces?\n\n### Standard Answer\nLinear transitions rely on uniform vector spacing. If the embedding space is not well-regularized (e.g. low context dimension or insufficient training updates), words drift, and the directional offset vectors (e.g. gender or tense vectors) fail to align.\n",
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
        },
        # --- MODULE 4 ---
        "nlp-m4-t1": {
            "title": "Self-Attention Mechanics",
            "notes": {
                "learning_outcomes": [
                    "Explain Query, Key, and Value projections.",
                    "Derive the scaled dot-product attention equation and scaling factor."
                ],
                "sections": [
                    {
                        "title": "Scaled Dot-Product Attention",
                        "content": "Given a sequence matrix $\\mathbf{H} \\in \\mathbb{R}^{T \\times d}$, self-attention projects it into Query ($\\mathbf{Q}$), Key ($\\mathbf{K}$), and Value ($\\mathbf{V}$) matrices using projection weights:\n\n$$\\mathbf{Q} = \\mathbf{H}\\mathbf{W}_Q, \\quad \\mathbf{K} = \\mathbf{H}\\mathbf{W}_K, \\quad \\mathbf{V} = \\mathbf{H}\\mathbf{W}_V$$\n\nAttention outputs are computed as a weighted sum of the values:\n\n$$\\text{Attention}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{softmax}\\left( \\frac{\\mathbf{Q}\\mathbf{K}^{\\top}}{\\sqrt{d_k}} \\right)\\mathbf{V}$$\n\nwhere $d_k$ is the dimensionality of the key vectors. The scaling factor $\\sqrt{d_k}$ prevents the dot products from growing excessively large, which would push the softmax function into regions with extremely small gradients.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Self-Attention Mechanics\n\n$$\\text{Attention}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{softmax}\\left( \\frac{\\mathbf{Q}\\mathbf{K}^{\\top}}{\\sqrt{d_k}} \\right)\\mathbf{V}$$\n",
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
                    "Formulate parallel projection dimensions.",
                    "Derive concatenated output dimension matrices."
                ],
                "sections": [
                    {
                        "title": "Multi-Head Attention (MHA)",
                        "content": "Rather than performing attention once with the full dimensionality $d_{model}$, Multi-Head Attention projects queries, keys, and values $h$ times in parallel. The outputs are concatenated and projected again:\n\n$$\\text{MHA}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{Concat}(\\text{head}_1, \\dots, \\text{head}_h)\\mathbf{W}^O$$\n\nwhere $\\text{head}_i = \\text{Attention}(\\mathbf{Q}\\mathbf{W}_i^Q, \\mathbf{K}\\mathbf{W}_i^K, \\mathbf{V}\\mathbf{W}_i^V)$.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Multi-Head Attention\n\n$$\\text{head}_i = \\operatorname{Attention}(\\mathbf{Q}\\mathbf{W}_i^Q, \\mathbf{K}\\mathbf{W}_i^K, \\mathbf{V}\\mathbf{W}_i^V)$$\n$$\\text{Output} = \\operatorname{Concat}(\\text{head}_1, \\dots, \\text{head}_h)\\mathbf{W}^O$$\n",
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
                    "Contrast Pre-LN and Post-LN architectures.",
                    "Formulate Rotary Position Embedding (RoPE) mechanisms."
                ],
                "sections": [
                    {
                        "title": "Layer Normalization and Positional Encoding",
                        "content": "Transformer blocks use Layer Normalization (LN) to stabilize activations. Post-LN normalizes after the residual block addition, while Pre-LN normalizes the input to the sublayer before the attention step. Pre-LN is widely used in modern models because it stabilizes gradient flows, allowing models to scale to hundreds of layers without warmup tricks.\n\nTo represent token positions, models apply positional encodings. Rotary Position Embedding (RoPE) applies a rotation matrix to the 2D slices of query and key projections, naturally encoding relative distance properties.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Transformer Block Components\n\n## 1. Pre-LN vs Post-LN\n*   **Post-LN:** $\\mathbf{x}_{l+1} = \\text{LN}(\\mathbf{x}_l + \\text{SubLayer}(\\mathbf{x}_l))$\n*   **Pre-LN:** $\\mathbf{x}_{l+1} = \\mathbf{x}_l + \\text{SubLayer}(\\text{LN}(\\mathbf{x}_l))$\n\n## 2. RoPE Rotation\nFor a 2D vector $\\mathbf{q} = [q_1, q_2]^\\top$, rotated by angle $m\\theta$:\n\n$$\\mathbf{R}_{m\\theta} \\mathbf{q} = \\begin{bmatrix} \\cos m\\theta & -\\sin m\\theta \\\\ \\sin m\\theta & \\cos m\\theta \\end{bmatrix} \\begin{bmatrix} q_1 \\\\ q_2 \\end{bmatrix}$$\n",
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
                    "Explain causal masking metrics in autoregressive generation.",
                    "Formulate cross-attention routing layers."
                ],
                "sections": [
                    {
                        "title": "Causal Masking and Cross-Attention",
                        "content": "Autoregressive decoders must not look ahead at future tokens. This is enforced by applying a causal mask to the self-attention matrix before the softmax step. The causal mask is a lower-triangular matrix filled with $-\\infty$ in the upper triangle, setting attention probabilities for future tokens to $0.0$.\n\nCross-attention maps source sequences to target sequences. The Query matrix is projected from the target sequence (decoder states), while Key and Value matrices are projected from the source sequence (encoder states).",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Causal Decoders & Cross-Attention\n\n## 1. Causal Masking\n$$\\mathbf{M}_{ij} = \\begin{cases} 0 & \\text{if } i \\ge j \\\\ -\\infty & \\text{if } i < j \\end{cases}$$\n$$\\text{Attn} = \\text{softmax}\\left( \\frac{\\mathbf{Q}\\mathbf{K}^{\\top}}{\\sqrt{d_k}} + \\mathbf{M} \\right)\\mathbf{V}$$\n",
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
                    "Explain BERT MLM and NSP objectives.",
                    "Formulate GPT causal autoregressive training."
                ],
                "sections": [
                    {
                        "title": "BERT Masked Language Modeling (MLM)",
                        "content": "BERT is pre-trained using two objectives: Masked Language Modeling (MLM) and Next Sentence Prediction (NSP). In MLM, 15% of the input tokens are sampled, with 80% replaced by a `[MASK]` token, 10% replaced by a random token, and 10% left unchanged. The model is trained to predict the original tokens, learning bidirectional representations.",
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
        },
        # --- MODULE 5 ---
        "nlp-m5-t1": {
            "title": "Sentence Embeddings",
            "notes": {
                "learning_outcomes": [
                    "Compare Bi-Encoder and Cross-Encoder layouts.",
                    "Formulate Contrastive Loss equations."
                ],
                "sections": [
                    {
                        "title": "Bi-Encoders vs. Cross-Encoders",
                        "content": "Bi-Encoders project input sentences into independent vectors and evaluate their similarity using a cosine projection. This allows sentence embeddings to be computed and indexed offline. Cross-Encoders feed both sentences into the model simultaneously, letting self-attention evaluate cross-sentence interactions. Cross-encoders are highly accurate but computationally expensive, as they cannot be indexed offline.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Sentence Embeddings\n\n## 1. Architectures\n*   **Bi-Encoder:** $\\text{sim}(s_1, s_2) = \\cos(f(s_1), f(s_2))$\n*   **Cross-Encoder:** $\\text{score} = f(s_1 || s_2)$\n",
            "interview": "# Interview Prep: Sentence Embeddings\n\n## Q1: Why are Bi-Encoders preferred for web-scale semantic search engines?\n\n### Standard Answer\nBi-encoders compute sentence embeddings independently. In semantic search, document embeddings can be pre-computed and stored in a vector database offline. At query time, we only need to encode the query and perform a fast vector search. Cross-encoders require encoding the query with every document in the index, which is computationally intractable at scale.\n",
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
                    "Explain term frequency saturation."
                ],
                "sections": [
                    {
                        "title": "Okapi BM25 Ranking Model",
                        "content": "Okapi BM25 is a non-linear ranking function that improves on TF-IDF by incorporating term frequency saturation and document length normalization. The BM25 score for a document $D$ given query $Q$ is:\n\n$$\\text{Score}(D, Q) = \\sum_{q_i \\in Q} \\text{IDF}(q_i) \\frac{f(q_i, D) \\cdot (k_1 + 1)}{f(q_i, D) + k_1 \\left( 1 - b + b \\frac{|D|}{\\text{avgdl}} \\right)}$$\n\nwhere $k_1$ controls term frequency saturation and $b$ controls document length normalization.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# BM25 Model\n\n$$\\text{Score}(D, Q) = \\sum_{q_i \\in Q} \\text{IDF}(q_i) \\frac{f(q_i, D) (k_1 + 1)}{f(q_i, D) + k_1 (1 - b + b \\frac{|D|}{\\text{avgdl}})}$$\n",
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
                    "Explain HNSW graph traversal metrics.",
                    "Formulate IVF-PQ quantization steps."
                ],
                "sections": [
                    {
                        "title": "Vector Indexing Mechanisms",
                        "content": "To query high-dimensional embeddings efficiently, vector databases implement Approximate Nearest Neighbors (ANN) indices. Hierarchical Navigable Small World (HNSW) uses a multi-layer graph where top layers have sparse connections for fast coarse routing, and bottom layers have dense connections for fine search. Inverted File Product Quantization (IVF-PQ) clusters vectors to reduce the search space, and quantizes dimensions to compress memory footprints.",
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
                    "Explain Reciprocal Rank Fusion (RRF) scoring math.",
                    "Combine lexical and semantic scores."
                ],
                "sections": [
                    {
                        "title": "Reciprocal Rank Fusion (RRF)",
                        "content": "Hybrid search combines sparse keyword retrieval (e.g., BM25) and dense semantic vector retrieval. Because score distributions differ significantly, we rank documents using Reciprocal Rank Fusion (RRF):\n\n$$\\text{RRF\\_Score}(d \\in \\mathcal{D}) = \\sum_{m \\in M} \\frac{1}{k + r_m(d)}$$\n\nwhere $M$ is the set of retrieval models, $r_m(d)$ is the rank of document $d$ under model $m$, and $k$ is a constant (typically 60) that stabilizes the ranking.",
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
                    "Derive BLEU precision metric equations.",
                    "Formulate ROUGE recall metrics."
                ],
                "sections": [
                    {
                        "title": "BLEU and ROUGE Evaluation",
                        "content": "To evaluate language generation tasks automatically, we compare candidate generations against human reference translations. BLEU measures n-gram precision with a brevity penalty, while ROUGE evaluates n-gram recall (ROUGE-N) and Longest Common Subsequence alignments (ROUGE-L).",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Translation Metrics\n\n*   **BLEU:** $\\text{BP} \\cdot \\exp\\left( \\sum_{n=1}^N w_n \\log p_n \\right)$\n*   **ROUGE-L:** Longest Common Subsequence (LCS) F-measure.\n",
            "interview": "# Interview Prep: Generation Evals\n\n## Q1: Why is the Brevity Penalty (BP) required in BLEU evaluations?\n\n### Standard Answer\nWithout the brevity penalty, a model could generate extremely short outputs containing only high-confidence words (e.g. 'the') to achieve perfect precision. The brevity penalty scales the score down if the candidate translation length is shorter than the reference translation length.\n",
            "example_code": "import numpy as np\n\ndef compute_brevity_penalty(c_len, r_len):\n    if c_len > r_len:\n        return 1.0\n    return np.exp(1.0 - r_len / c_len) if c_len > 0 else 0.0\n\nif __name__ == '__main__':\n    print('Brevity penalty metric loaded.')\n",
            "practice_code": "import numpy as np\n\ndef compute_brevity_penalty(c_len, r_len):\n    if c_len > r_len:\n        return 1.0\n    return np.exp(1.0 - r_len / c_len) if c_len > 0 else 0.0\n\ndef run_practice():\n    bp = compute_brevity_penalty(5, 10)\n    assert np.allclose(bp, np.exp(-1.0))\n    print('[PASS] Brevity penalty calculation matches.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m5-t5-quiz",
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

    for topic_id, data in topics_data.items():
        module_num = topic_id.split("-")[1]
        topic_num = topic_id.split("-")[2]
        
        notes_content = {
            "topic_id": topic_id,
            "title": data["title"],
            "version": "1.0.0",
            "topic_metadata": {
                "difficulty": "Hard" if "m4" in module_num or "m5" in module_num else "Medium",
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

    print("\nSuccessfully generated all remaining NLP files!")

if __name__ == "__main__":
    main()
