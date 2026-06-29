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

    m2_data = {
        "nlp-m2-t1": {
            "title": "Bag of Words & N-Grams",
            "notes": {
                "learning_outcomes": [
                    "Formulate CountVectorizer document frequency occurrences and representation maps.",
                    "Analyze n-gram feature expansions and vocabulary scaling bottlenecks.",
                    "Apply vocabulary pruning parameters (max_df, min_df, max_features)."
                ],
                "sections": [
                    {
                        "title": "The Bag of Words (BoW) Representation Model",
                        "content": "The **Bag of Words (BoW)** model is a vector space representation of text. It discards word order and grammatical structure, representing a document strictly as a frequency vector over a vocabulary. \n\nGiven a corpus $\\mathcal{C}$ with vocabulary $\\mathcal{V} = \\{w_1, \\dots, w_{|\\mathcal{V}|}\\}$, a document $d$ is represented by a vector $\\mathbf{d} \\in \\mathbb{R}^{|\\mathcal{V}|}$ where the $j$-th element is the frequency of word $w_j$ in $d$:\n\n$$d_j = \\sum_{t \\in \\text{tokens}(d)} \\mathbb{I}(t = w_j)$$\n\nCollecting these vectors for all $M$ documents in the corpus yields the document-term matrix $\\mathbf{X} \\in \\mathbb{R}^{M \\times |\\mathcal{V}|}$. This matrix is highly sparse, as most documents contain only a tiny fraction of the vocabulary.",
                        "callouts": [
                            {
                                "type": "Student Trap",
                                "title": "Information Loss in BoW",
                                "content": "Because BoW discards word order, sentences with opposite meanings can yield identical vectors. For example, 'not bad, rather good' and 'rather bad, not good' yield identical Bag of Words vectors. Do not use standard BoW for tasks that depend heavily on word order or syntactic patterns."
                            }
                        ]
                    },
                    {
                        "title": "N-Gram Vocabulary Expansion and Constraints",
                        "content": "To capture local context and word order, we extend the vocabulary using **N-Grams** (continuous sequences of $N$ tokens). \n\n*   **Unigrams (N=1):** `['the', 'cat', 'sat']`\n*   **Bigrams (N=2):** `['the cat', 'cat sat']`\n*   **Trigrams (N=3):** `['the cat sat']`\n\nWhile adding n-grams preserves word order, it causes the vocabulary size to scale exponentially. For a base vocabulary of size $V$, there are $V^n$ theoretical n-gram combinations. This exponential growth leads to severe memory constraints and data sparsity, as most n-grams never appear in training.",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Vocabulary Pruning Strategies",
                                "content": "To prevent vocabulary explosion, always configure pruning thresholds:\n1. `min_df`: Discard terms that appear in fewer than $K$ documents (removes noise and typos).\n2. `max_df`: Discard terms that appear in more than $P\\%$ of documents (removes corpus-specific stopwords).\n3. `max_features`: Keep only the top $F$ terms ranked by frequency."
                            }
                        ]
                    }
                ]
            },
            "revision": "# Bag of Words & N-Grams\n\n## 1. BoW Vector Representation\nGiven vocabulary $\\mathcal{V}$, document vector $\\mathbf{d} \\in \\mathbb{R}^{|\\mathcal{V}|}$ is:\n\n$$d_j = \\sum_{t \\in \\text{tokens}} \\mathbb{I}(t = w_j)$$\n\n## 2. N-Gram Complexity\n*   Theoretical vocabulary size scales as $\\mathcal{O}(|\\mathcal{V}|^n)$.\n*   Pruned using `min_df`, `max_df`, and `max_features` constraints.\n",
            "interview": "# Interview Prep: BoW & N-Grams\n\n## Q1: Explain why N-gram representations suffer from the 'curse of dimensionality' and how vocabulary pruning mitigates this.\n\n### Standard Answer\nAs $n$ increases, the theoretical vocabulary size scales exponentially as $|\\mathcal{V}|^n$. For a vocabulary of 10,000 words, bigrams yield $10^8$ possible features and trigrams yield $10^{12}$, creating massive sparsity and memory requirements. Most features will have zero counts across the dataset, causing statistical classifiers to overfit.\n\nVocabulary pruning mitigates this by applying constraints:\n1. `min_df`: Removes rare terms that do not contribute to generalization.\n2. `max_df`: Removes high-frequency terms that act as stopwords.\n3. `max_features`: Bounds the feature space size to a manageable limit (e.g. 5,000 to 10,000 features).\n",
            "example_code": "import numpy as np\n\ndef get_ngrams(tokens, n):\n    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]\n\nif __name__ == '__main__':\n    print(get_ngrams(['the', 'cat', 'sat', 'on', 'the', 'mat'], 2))\n",
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
                    "Derive Term Frequency (TF) and Inverse Document Frequency (IDF) mathematics.",
                    "Apply sublinear scaling functions to term frequencies.",
                    "Prove the significance of L2 normalization in document length invariance."
                ],
                "sections": [
                    {
                        "title": "TF-IDF Mathematical Formulation",
                        "content": "TF-IDF weights term occurrences inside a document against corpus-wide distribution. The score is defined as:\n\n$$\\text{TF-IDF}(t, d, \\mathcal{C}) = \\text{TF}(t, d) \\times \\text{IDF}(t, \\mathcal{C})$$\n\nwhere:\n\n1.  **Inverse Document Frequency (IDF):** Measures the information content of a term. Terms that appear in many documents (low IDF) are penalized as generic, while rare terms (high IDF) are weighted heavily:\n\n$$\\text{IDF}(t, \\mathcal{C}) = \\ln \\frac{1 + M}{1 + \\text{DF}(t)} + 1$$\n\nwhere $M = |\\mathcal{C}|$ is the total number of documents, and $\\text{DF}(t)$ is the number of documents containing term $t$. Adding 1 to the numerator and denominator prevents division by zero.",
                        "callouts": []
                    },
                    {
                        "title": "Sublinear TF Scaling and L2 Normalization",
                        "content": "Raw term frequency grows linearly, but semantic significance does not (a term appearing 20 times in a document is not 20 times more important than a term appearing once). We apply **sublinear TF scaling** to map frequencies logarithmically:\n\n$$\\text{TF}_{sub}(t, d) = \\begin{cases} 1 + \\ln(\\text{TF}(t, d)) & \\text{if } \\text{TF}(t, d) > 0 \\\\ 0 & \\text{otherwise} \\end{cases}$$\n\nTo prevent document length bias, we apply **L2 normalization** to the document vectors, mapping them to a unit sphere:\n\n$$\\mathbf{d}_{norm} = \\frac{\\mathbf{d}}{\\|\\mathbf{d}\\|_2} = \\frac{\\mathbf{d}}{\\sqrt{\\sum_{j=1}^{|\\mathcal{V}|} d_j^2}}$$\n\nThis normalization ensures that similarity calculations depend strictly on the relative distribution of terms rather than raw document lengths.",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Zero-IDF Edge Cases",
                                "content": "Without smooth formulations, if a term appears in every document ($DF(t) = M$), $\\text{IDF} = \\ln(M/M) = \\ln(1) = 0.0$. This completely zeroes out the term's weight. Modern libraries add $1$ to the final IDF score to ensure it remains positive."
                            }
                        ]
                    }
                ]
            },
            "revision": "# TF-IDF Mathematics\n\n## 1. Formulas\n$$\\text{TF-IDF}(t, d) = \\text{TF}(t, d) \\times \\text{IDF}(t)$$\n$$\\text{IDF}(t) = \\ln \\frac{M}{1 + \\text{DF}(t)} + 1$$\n\n## 2. Sublinear Scaling\n$$\\text{TF}_{sub} = 1 + \\ln(\\text{TF}) \\quad (\\text{for } \\text{TF} > 0)$$\n\n## 3. L2 Normalization\n$$\\mathbf{d}_{norm} = \\frac{\\mathbf{d}}{\\|\\mathbf{d}\\|_2}$$\n",
            "interview": "# Interview Prep: TF-IDF\n\n## Q1: Why do we apply L2 normalization to TF-IDF vectors, and how does it affect cosine similarity calculations?\n\n### Standard Answer\nL2 normalization divides each element of a vector by its Euclidean length:\n\n$$\\mathbf{d}_{norm} = \\frac{\\mathbf{d}}{\\|\\mathbf{d}\\|_2}$$\n\nThis ensures that longer documents, which contain more words (and thus higher raw term frequencies), do not dominate similarity calculations. \n\nWhen we compute the cosine similarity between two L2-normalized vectors, the denominator of the cosine equation is equal to 1.0:\n\n$$\\cos(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2} = \\mathbf{u}_{norm} \\cdot \\mathbf{v}_{norm}$$\n\nThis reduces the similarity calculation to a simple dot product, accelerating retrieval performance.",
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
                    "Derive Cosine Similarity and analyze its mathematical bounds.",
                    "Contrast Cosine Similarity with Jaccard and Euclidean metrics.",
                    "Explain when to use which metric based on data representations."
                ],
                "sections": [
                    {
                        "title": "Cosine Similarity Mathematics",
                        "content": "Cosine Similarity measures the cosine of the angle between two multi-dimensional vectors in a vector space:\n\n$$\\text{sim}(\\mathbf{u}, \\mathbf{v}) = \\cos(\\theta) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2} = \\frac{\\sum_{i=1}^d u_i v_i}{\\sqrt{\\sum_{i=1}^d u_i^2} \\sqrt{\\sum_{i=1}^d v_i^2}}$$\n\nIf the vectors contain only non-negative elements (such as TF-IDF or count frequencies), the similarity score lies in the range $[0, 1]$. Cosine similarity evaluates direction rather than magnitude, rendering it invariant to document length.",
                        "callouts": []
                    },
                    {
                        "title": "Alternative Metrics: Jaccard and Euclidean",
                        "content": "Depending on the text representation, other similarity metrics can be used:\n\n1.  **Jaccard Similarity:** Measures overlap between two binary sets (e.g. present/absent vocabulary words). It is defined as the size of the intersection divided by the size of the union:\n\n$$J(A, B) = \\frac{|A \\cap B|}{|A \\cup B|}$$\n\n2.  **Euclidean Distance:** Measures the straight-line distance between two points in a Euclidean space:\n\n$$d(\\mathbf{u}, \\mathbf{v}) = \\|\\mathbf{u} - \\mathbf{v}\\|_2 = \\sqrt{\\sum_{i=1}^d (u_i - v_i)^2}$$\n\nEuclidean distance is sensitive to vector magnitudes, making it poor for raw frequency vectors of varying document lengths unless the vectors are first L2-normalized.",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Equivalence of Normalized Euclidean and Cosine",
                                "content": "For two L2-normalized vectors $\\mathbf{u}$ and $\\mathbf{v}$ (where $\\|\\mathbf{u}\\| = \\|\\mathbf{v}\\| = 1$), the squared Euclidean distance relates directly to Cosine similarity:\n\n$$\\|\\mathbf{u} - \\mathbf{v}\\|_2^2 = \\|\\mathbf{u}\\|^2 + \\|\\mathbf{v}\\|^2 - 2(\\mathbf{u} \\cdot \\mathbf{v}) = 2 - 2\\cos(\\theta)$$\n\nMinimizing Euclidean distance between normalized vectors is mathematically equivalent to maximizing Cosine similarity."
                            }
                        ]
                    }
                ]
            },
            "revision": "# Similarity Metrics\n\n## 1. Cosine Similarity\n$$\\text{sim}(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2}$$\n\n## 2. Jaccard Similarity\n$$J(A, B) = \\frac{|A \\cap B|}{|A \\cup B|}$$\n\n## 3. Normalized Distance Equivalence\n$$\\|\\mathbf{u}_{norm} - \\mathbf{v}_{norm}\\|_2^2 = 2 - 2\\cos(\\theta)$$\n",
            "interview": "# Interview Prep: Similarity Metrics\n\n## Q1: Explain why Euclidean distance is inadequate for document similarity checks on raw term frequencies. Show how L2 normalization resolves this.\n\n### Standard Answer\nEuclidean distance measures the straight-line distance between coordinates:\n\n$$d(\\mathbf{u}, \\mathbf{v}) = \\sqrt{\\sum (u_i - v_i)^2}$$\n\nIf two documents have the same term distribution but one is twice as long as the other, their raw frequency vectors will point in the same direction but have different magnitudes. The Euclidean distance between them will be large, indicating they are dissimilar. Cosine similarity evaluates only the angle, correctly identifying them as identical in content.\n\nApplying L2 normalization maps both vectors to unit length (norm = 1.0). Once normalized, the squared Euclidean distance is $2 - 2\\cos(\\theta)$, aligning the two metrics.\n",
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
                    "Formulate MLE estimations for N-Gram language models under the Markov assumption.",
                    "Explain Laplace (add-one) smoothing and Kneser-Ney continuation distributions."
                ],
                "sections": [
                    {
                        "title": "N-Gram Probability Distributions",
                        "content": "An N-Gram language model estimates the probability distribution of word sequences. By applying the chain rule of probability:\n\n$$P(w_1, \\dots, w_k) = \\prod_{i=1}^k P(w_i \\mid w_1, \\dots, w_{i-1})$$\n\nUnder the Markov assumption, the probability of the next word depends only on the preceding $N-1$ words:\n\n$$P(w_i \\mid w_1, \\dots, w_{i-1}) \\approx P(w_i \\mid w_{i-N+1}, \\dots, w_{i-1})$$\n\nThe Maximum Likelihood Estimate (MLE) is computed from corpus counts:\n\n$$P_{MLE}(w_i \\mid w_{i-1}) = \\frac{C(w_{i-1}, w_i)}{C(w_{i-1})}$$\n\nIf the prefix $w_{i-1}$ never appeared in training, this estimate is undefined. If the prefix occurred but the pair $(w_{i-1}, w_i)$ did not, the probability is $0.0$, zeroing out the entire sequence probability.",
                        "callouts": []
                    },
                    {
                        "title": "Smoothing Mechanisms: Laplace and Kneser-Ney",
                        "content": "To resolve the zero-frequency problem, we apply smoothing:\n\n1.  **Laplace (Add-One) Smoothing:** Adds 1 to all vocabulary counts. While simple, it shifts too much probability mass from observed words to unseen words in large vocabularies.\n2.  **Kneser-Ney Smoothing:** An advanced smoothing technique. It estimates probabilities based on how likely a word is to complete an unseen context. Words that appear in many contexts (high continuation probability) are favored over words that have high individual frequency but only occur in specific contexts (e.g. 'Francisco' is frequent but almost exclusively follows 'San').",
                        "callouts": []
                    }
                ]
            },
            "revision": "# N-Gram Language Models\n\n## 1. MLE Estimation\n$$P_{MLE}(w_i \\mid w_{i-1}) = \\frac{C(w_{i-1}, w_i)}{C(w_{i-1})}$$\n\n## 2. Laplace Smoothing\n$$P_{Laplace}(w_i \\mid w_{i-1}) = \\frac{C(w_{i-1}, w_i) + 1}{C(w_{i-1}) + |\\mathcal{V}|}$$\n",
            "interview": "# Interview Prep: N-Gram LMs\n\n## Q1: Explain Kneser-Ney smoothing. Why does it outperform simple absolute discounting models?\n\n### Standard Answer\nKneser-Ney smoothing incorporates the **continuation probability** of lower-order n-grams. The probability of a word $w$ is defined as:\n\n$$P_{KN}(w_i \\mid w_{i-1}) = \\frac{\\max(C(w_{i-1}, w_i) - d, 0)}{C(w_{i-1})} + \\lambda(w_{i-1}) P_{continuation}(w_i)$$\n\nwhere $d$ is a discounting parameter, and $\\lambda$ is a normalization constant. The continuation probability $P_{continuation}(w_i)$ measures how likely a word is to follow an arbitrary prefix, computed as:\n\n$$P_{continuation}(w_i) = \\frac{|\\{w_{i-1} : C(w_{i-1}, w_i) > 0\\}|}{\\sum_{w'} |\\{w_{i-1} : C(w_{i-1}, w') > 0\\}|}$$\n\nThis prevents words with high unigram frequency that only occur in specific contexts (like 'Francisco' in 'San Francisco') from being predicted in incorrect contexts.\n",
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
                    "Calculate Word Error Rate (WER) using Levenshtein distance matrix alignments."
                ],
                "sections": [
                    {
                        "title": "Perplexity (PPL) Mathematics",
                        "content": "Perplexity is a metric for evaluating language models. It measures how well a probability model predicts a test sequence. Mathematically, it is the exponentiated cross-entropy of the model on the sequence.\n\nGiven a word sequence $W = (w_1, \\dots, w_N)$, the perplexity is:\n\n$$\\text{PPL}(W) = P(w_1, \\dots, w_N)^{-\\frac{1}{N}} = \\sqrt[N]{\\prod_{i=1}^N \\frac{1}{P(w_i \\mid w_1, \\dots, w_{i-1})}}$$\n\nTaking the natural logarithm:\n\n$$\\ln \\text{PPL}(W) = -\\frac{1}{N} \\sum_{i=1}^N \\ln P(w_i \\mid w_1, \\dots, w_{i-1})$$\n\nThis is the definition of cross-entropy. Thus, $\\text{PPL}(W) = e^{H(W)}$. A lower perplexity indicates the model is more confident in its predictions.",
                        "callouts": []
                    },
                    {
                        "title": "Word Error Rate (WER) and Alignment",
                        "content": "For sequence generation tasks (like speech-to-text or machine translation), we evaluate outputs using **Word Error Rate (WER)**. WER is computed by aligning the hypothesis sequence against a reference sequence using **Levenshtein Distance**:\n\n$$\\text{WER} = \\frac{S + D + I}{N}$$\n\nwhere:\n*   $S$ is the number of substitutions.\n*   $D$ is the number of deletions.\n*   $I$ is the number of insertions.\n*   $N$ is the number of words in the reference sequence.\n\nThis alignment is solved using dynamic programming to find the path that minimizes edit distance.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Perplexity & Evaluation\n\n## 1. Perplexity Equation\n$$\\text{PPL}(W) = P(w_1, \\dots, w_N)^{-\\frac{1}{N}} = e^{H(W)}$$\n\n## 2. Word Error Rate\n$$\\text{WER} = \\frac{S + D + I}{N}$$\n*   Computed via Levenshtein alignment matrices.\n",
            "interview": "# Interview Prep: Perplexity\n\n## Q1: Prove how perplexity corresponds to the average branching factor of a language model.\n\n### Standard Answer\nConsider a language model predicting the next token from a vocabulary of size $V$. If the model is completely uniform (i.e. $P(w_i \\mid \\text{context}) = \\frac{1}{K}$ for exactly $K$ words, and $0$ for others), the perplexity is:\n\n$$\\text{PPL}(W) = \\left( \\prod_{i=1}^N \\frac{1}{K} \\right)^{-\\frac{1}{N}} = \\left( K^{-N} \\right)^{-\\frac{1}{N}} = K$$\n\nThus, a perplexity of $K$ indicates that the model is as confused as if it had to choose uniformly from $K$ candidates at each step. $K$ represents the **average branching factor** of the language.",
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
        }
    }

    # Write files
    for topic_id, data in m2_data.items():
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

    print("\nSuccessfully generated enriched NLP Module 2 files!")

if __name__ == "__main__":
    main()
