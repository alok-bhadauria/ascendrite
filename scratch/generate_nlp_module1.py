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

    m1_data = {
        "nlp-m1-t1": {
            "title": "Text Corpora & Normalization",
            "notes": {
                "learning_outcomes": [
                    "Define a text corpus and explain statistical distribution patterns using Zipf's Law.",
                    "Explain text normalization steps including case folding, tokenization boundaries, and stopword filters.",
                    "Contrast stemming algorithms (Porter vs. Lancaster) with morphological lemmatization.",
                    "Calculate Porter's measure $m$ for complex suffixes and map character state transitions."
                ],
                "sections": [
                    {
                        "title": "Text Corpora and Zipf's Law Mathematics",
                        "content": "A text corpus is a structured dataset of machine-readable texts selected for linguistic analysis or model training. A fundamental property of natural language corpora is the highly skewed distribution of word frequencies, formalised by **Zipf's Law**.\n\nZipf's Law states that the frequency of any word $f$ is inversely proportional to its rank $r$ in the frequency table:\n\n$$f(r) \\propto \\frac{1}{r^s}$$\n\nwhere $s \\approx 1$ is a parameter of the corpus. Mathematically, this can be written as $f(r) = \\frac{C}{r^s}$ where $C$ is a normalization constant. Taking the logarithm of both sides yields a linear relationship:\n\n$$\\ln f(r) = \\ln C - s \\ln r$$\n\nPlotting log-frequency against log-rank displays a straight line with a slope of $-s$. This power-law distribution implies that a tiny number of words (e.g., 'the', 'of', 'and') account for the vast majority of tokens in a corpus, while a massive number of words appear only once (hapax legomena). This sparsity creates severe data challenges for statistical NLP models.",
                        "callouts": [
                            {
                                "type": "Student Trap",
                                "title": "Zipf's Law and Vocabulary Size",
                                "content": "Zipf's law applies to word frequencies, not vocabulary growth. Vocabulary growth relative to corpus size is modeled by Heap's Law: $V = k N^\\beta$, where $V$ is vocabulary size, $N$ is token count, and $\\beta \\approx 0.5$. Do not confuse the power-law distribution of term frequencies with the sublinear growth of vocabulary size."
                            }
                        ]
                    },
                    {
                        "title": "Preprocessing Pipelines and Tokenization Boundaries",
                        "content": "Before text is fed into statistical models, it must undergo normalization:\n1. **Case Folding:** Converting all characters to lowercase to map identical tokens (e.g. 'Cat' and 'cat') to the same vocabulary slot. This is typically bypassed in modern transformer models to preserve named entity casing.\n2. **Tokenization:** Splitting continuous character streams into discrete units (tokens) based on boundaries. While spaces serve as basic boundaries in English, they fail for languages without spacing (e.g., Chinese, Japanese) or highly inflected agglutinative languages (e.g., Finnish, Turkish).\n3. **Stopword Filtering:** Discarding high-frequency, low-information functional words. Standard practice sets threshold boundaries (e.g. removing terms with document frequency $\\text{DF} > 95\\%$ or using predefined stopword lists) to focus models on semantic content.",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Downstream Impact of Stopword Removal",
                                "content": "While stopword removal is beneficial for search indexing (TF-IDF/BM25) and classification models, it degrades sequence-to-sequence generation, dependency parsing, and language modeling. Transformer models require stopwords to compute contextual attention steps and parse syntactic structures; do not apply stopword filters when training modern LLMs."
                            }
                        ]
                    },
                    {
                        "title": "Stemming Mechanics vs. Morphological Lemmatization",
                        "content": "Stemming and lemmatization reduce inflected words to their base forms:\n\n*   **Stemming:** A crude, heuristic process that chops off suffixes. The **Porter Stemmer** uses a sequence of conditional rewrite rules based on the word's measure $m$, defined by the consonant-vowel state pattern $[C](VC)^m[V]$. For example, step 1a rewrites plural endings (e.g. `sses` $\\to$ `ss`, `ies` $\\to$ `i`). The **Lancaster Stemmer** is a more aggressive, rule-table-driven algorithm that can lead to overstemming (reducing unrelated words to the same stem, e.g., 'organization' and 'organ' to 'org').\n*   **Lemmatization:** A morphosemantic analysis that maps inflected tokens back to their dictionary base forms (lemmas). Unlike stemmers, lemmatizers utilize lexical databases (e.g. WordNet) and require Part-of-Speech (POS) tags to resolve ambiguities (e.g. mapping 'saw' to 'see' if flagged as a verb, or keeping it as 'saw' if flagged as a noun).",
                        "callouts": [
                            {
                                "type": "Interview Tip",
                                "title": "Choosing Between Stemming and Lemmatization",
                                "content": "If asked to choose, state that stemming is computationally cheap, fast, and suitable for search query expansions where speed is critical. Lemmatization is slower and memory-intensive but preserves morphological correctness, which is necessary for translation, grammar checking, and detailed text analytics."
                            }
                        ]
                    }
                ]
            },
            "revision": "# Preprocessing, Normalization & Zipf's Law\n\n## 1. Zipf's Law Distribution\n$$\\ln f(r) = \\ln C - s \\ln r$$\n*   Natural language term frequencies follow a power-law distribution, creating high vocabulary sparsity.\n\n## 2. Vocabulary Growth (Heap's Law)\n$$V = k N^\\beta \\quad (0 < \\beta < 1)$$\n*   Vocabulary size grows sublinearly with the number of tokens in the corpus.\n\n## 3. Porter Stemmer Measure\n$$[C](VC)^m[V]$$\n*   **Consonants (C):** Sequences of consonants (including 'y' if preceded by a vowel).\n*   **Vowels (V):** Sequences of vowels (including 'y' if preceded by a consonant).\n*   *Rewrite rule conditions* depend on $m$. For example, step 1b replaces `eed` with `ee` only if $m > 0$.\n",
            "interview": "# Interview Prep: Preprocessing & Normalization\n\n## Q1: Prove mathematically how to estimate the normalization constant C in Zipf's law for a vocabulary of size V.\n\n### Standard Answer\nUnder Zipf's law with exponent $s=1$, the frequency of a word at rank $r$ is $f(r) = \\frac{C}{r}$. The sum of frequencies of all words in the vocabulary must equal the total number of tokens $N$ in the corpus:\n\n$$\\sum_{r=1}^V f(r) = \\sum_{r=1}^V \\frac{C}{r} = C \\sum_{r=1}^V \\frac{1}{r} = N$$\n\nThe term $\\sum_{r=1}^V \\frac{1}{r}$ is the harmonic number $H_V$, which can be approximated as $\\ln V + \\gamma$ (where $\\gamma \\approx 0.5772$ is the Euler-Mascheroni constant). Thus, we can estimate $C$ as:\n\n$$C = \\frac{N}{H_V} \\approx \\frac{N}{\\ln V + \\gamma}$$\n\n|INTERVIEW TRAP: Zipfian Tails and Sparsity For a large vocabulary, Zipf's law predicts that words with rank $r > V/2$ will have theoretical frequencies of less than 1. This math reflects the reality of natural language corpora: a large fraction of the vocabulary appears exactly once (hapax legomena). Statistical models that do not account for this sparsity will suffer from severe variance issues.|\n|---|\n",
            "example_code": "import re\n\ndef clean_text(text):\n    # Lowercasing and cleaning\n    text = text.lower()\n    # Simple word tokenization\n    tokens = re.findall(r'\\b\\w+\\b', text)\n    return tokens\n\nif __name__ == '__main__':\n    print(clean_text('The quick brown fox jumps over the lazy dog.'))\n",
            "practice_code": "def calculate_porter_measure(word: str) -> int:\n    \"\"\"Calculates Porter's measure m for a word, representing VC repetitions.\"\"\"\n    # Determine vowel/consonant flags\n    vowels = 'aeiou'\n    is_vowel = []\n    for i, char in enumerate(word):\n        if char in vowels:\n            is_vowel.append(True)\n        elif char == 'y' and i > 0 and not is_vowel[i-1]:\n            is_vowel.append(True)\n        else:\n            is_vowel.append(False)\n    \n    # Convert flags to states: V (True) or C (False)\n    # Compress consecutive identical flags\n    states = []\n    for val in is_vowel:\n        if not states or states[-1] != val:\n            states.append(val)\n            \n    # Count 'VC' transitions\n    m = 0\n    state_str = ''.join(['V' if s else 'C' for s in states])\n    # Find patterns of 'VC'\n    idx = 0\n    while True:\n        pos = state_str.find('VC', idx)\n        if pos != -1:\n            m += 1\n            idx = pos + 2\n        else:\n            break\n    return m\n\ndef run_practice():\n    assert calculate_porter_measure('tree') == 0 # C V (no VC transition)\n    assert calculate_porter_measure('troubles') == 2 # C V C V C (VC transitions: ou->bl, e->s)\n    print('[PASS] Porter measure m calculations verified successfully.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m1-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "According to Zipf's Law, if the most frequent word in a corpus occurs 100,000 times, how many times is the 10th most frequent word expected to occur?",
                        "options": ["10,000", "50,000", "1,000", "100,000"],
                        "correct_answer": "10,000",
                        "explanation": "Zipf's law states that f(r) = C / r. If r=1 has f(1) = 100,000, then C = 100,000. For the 10th most frequent word (r=10), the frequency is f(10) = 100,000 / 10 = 10,000."
                    }
                ]
            }
        },
        "nlp-m1-t2": {
            "title": "Statistical Tokenization",
            "notes": {
                "learning_outcomes": [
                    "Compare word-level, character-level, and subword-level tokenization paradigms.",
                    "Explain the training and tokenization loops of Byte Pair Encoding (BPE).",
                    "Formulate the WordPiece scoring equation and explain how it differs from BPE.",
                    "Explain the SentencePiece model's reversible stream and lossless detokenization."
                ],
                "sections": [
                    {
                        "title": "Subword Tokenization Paradigms",
                        "content": "Traditional word-level tokenization leads to vocabulary bloating and struggles with out-of-vocabulary (OOV) words. Character-level tokenization solves the OOV problem but yields long token sequences, which increases computational complexity and weakens contextual tracking. \n\n**Subword tokenization** balances this trade-off. It keeps frequent words intact while decomposing rare or complex words into smaller, meaningful subword units (e.g., 'unbelievable' $\\to$ `un` + `believ` + `able`). This bounds the vocabulary budget $V$ while ensuring the model can represent any unseen text sequence.",
                        "callouts": []
                    },
                    {
                        "title": "Byte Pair Encoding (BPE) & WordPiece Mechanics",
                        "content": "BPE and WordPiece are bottom-up subword tokenization algorithms:\n\n*   **Byte Pair Encoding (BPE):** Starts with character-level units and iteratively merges the most frequent adjacent symbol pair. Merged symbols are added to the vocabulary until the target vocabulary size is reached. BPE is deterministic and frequency-driven.\n*   **WordPiece:** Used in models like BERT, WordPiece also starts with character-level units but merges pairs based on a likelihood score rather than raw frequency:\n\n$$\\text{Score}(A, B) = \\frac{\\text{count}(AB)}{\\text{count}(A) \\times \\text{count}(B)}$$\n\nThis score is proportional to the pointwise mutual information (PMI) of the two tokens, prioritizing pairs that appear together significantly more often than expected by chance (e.g. prioritizing 'Roentgen' over common prepositional pairs like 'of the').",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Byte-Level BPE (BBPE)",
                                "content": "Standard BPE initializes the vocabulary with every unique character in the corpus. In multilingual contexts, this can lead to vocabulary bloating. Byte-Level BPE (BBPE) resolves this by initializing the vocabulary with the 256 possible byte values. This guarantees that any UTF-8 string can be represented without triggering out-of-vocabulary (`[UNK]`) errors."
                            }
                        ]
                    },
                    {
                        "title": "SentencePiece and Unigram Language Models",
                        "content": "Standard BPE and WordPiece require language-specific pre-tokenizers to split text into words before subword decomposition. This fails for languages without explicit spacing.\n\n**SentencePiece** treats the input as a raw character stream, replacing spaces with the meta-symbol `_` (U+2581). This allows spaces to be treated as regular characters, enabling **lossless detokenization**:\n\n$$\\text{detok}(\\text{tokens}) = \\text{replace}(\\text{join}(\\text{tokens}), \\text{'_'}, \\text{' '})$$\n\nSentencePiece implements both BPE and the **Unigram Language Model** algorithm. The Unigram model starts with a large vocabulary and iteratively prunes low-probability tokens using Viterbi segmentation, optimizing corpus likelihood.",
                        "callouts": [
                            {
                                "type": "Student Trap",
                                "title": "SentencePiece is not an Algorithm",
                                "content": "Do not refer to SentencePiece as a distinct tokenization algorithm. SentencePiece is a software wrapper and library that implements BPE and Unigram tokenization directly on raw character streams, bypassing language-specific pre-tokenizers."
                            }
                        ]
                    }
                ]
            },
            "revision": "# Statistical Tokenization\n\n## 1. WordPiece Selection Score\n$$\\text{Score}(A, B) = \\frac{\\text{count}(AB)}{\\text{count}(A) \\times \\text{count}(B)}$$\n*   Prioritizes pairs that maximize pointwise mutual information rather than raw frequency.\n\n## 2. SentencePiece Lossless Detokenization\n$$\\text{detok}(\\text{tokens}) = \\text{replace}(\\text{join}(\\text{tokens}), \\text{'_'}, \\text{' '})$$\n*   Preserves spaces as explicit characters, enabling reversible detokenization.\n",
            "interview": "# Interview Prep: Statistical Tokenization\n\n## Q1: Contrast BPE with the Unigram Language Model tokenization algorithm. How does Unigram tokenization resolve segmentation ambiguity?\n\n### Standard Answer\nBPE is a bottom-up algorithm that merges frequent characters into larger subwords. It is deterministic, resolving segmentation ambiguity by applying its trained merge rules sequentially.\n\nUnigram is a top-down, probabilistic model. It starts with a large vocabulary and prunes low-probability tokens. At inference, a word can often be segmented in multiple ways. Unigram resolves this ambiguity by selecting the segmentation $S$ that maximizes the joint probability:\n\n$$S^* = \\arg\\max_{S} \\prod_{x_i \\in S} P(x_i)$$\n\nThis optimization problem is solved efficiently using the Viterbi algorithm. This probabilistic framework enables subword regularization during training, where the model randomly samples from the top segmentations rather than always choosing the absolute maximum, improving generalization.\n",
            "example_code": "def run_bpe_step(corpus, vocab):\n    # Simple BPE merge step helper\n    pairs = {}\n    for word, freq in corpus.items():\n        symbols = word.split()\n        for i in range(len(symbols)-1):\n            pair = (symbols[i], symbols[i+1])\n            pairs[pair] = pairs.get(pair, 0) + freq\n    if not pairs:\n        return corpus, vocab\n    best_pair = max(pairs, key=pairs.get)\n    # Merge best pair\n    new_corpus = {}\n    merged = ''.join(best_pair)\n    vocab.add(merged)\n    for word, freq in corpus.items():\n        new_word = word.replace(' '.join(best_pair), merged)\n        new_corpus[new_word] = freq\n    return new_corpus, vocab\n\nif __name__ == '__main__':\n    corpus = {'l o w': 5, 'l o w e r': 2, 'n e w e s t': 6}\n    vocab = set(['l', 'o', 'w', 'e', 'r', 'n', 's', 't'])\n    new_c, new_v = run_bpe_step(corpus, vocab)\n    print('BPE vocabulary after 1 step:', sorted(list(new_v)))\n",
            "practice_code": "def calculate_wordpiece_score(pair_count: int, count_a: int, count_b: int) -> float:\n    \"\"\"Calculates the WordPiece score for a pair (A, B).\"\"\"\n    if count_a == 0 or count_b == 0:\n        return 0.0\n    return float(pair_count) / (count_a * count_b)\n\ndef run_practice():\n    # Pair count = 50, Individual count A = 100, B = 200\n    score = calculate_wordpiece_score(50, 100, 200)\n    assert np.allclose(score, 0.0025)\n    print('[PASS] WordPiece scoring checks passed.')\n\nif __name__ == '__main__':\n    import numpy as np\n    run_practice()\n",
            "quiz": {
                "quiz_id": "nlp-m1-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "Which subword tokenization algorithm merges adjacent pairs by maximizing the pointwise mutual information score rather than raw frequency?",
                        "options": ["WordPiece", "Byte Pair Encoding", "Unigram LM", "Lancaster Stemmer"],
                        "correct_answer": "WordPiece",
                        "explanation": "WordPiece merges pairs by maximizing count(AB) / (count(A) * count(B)), which is proportional to the pointwise mutual information (PMI)."
                    }
                ]
            }
        },
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
                        "title": "Sequence Labeling, POS Tagging, and BIO Schemes",
                        "content": "Sequence labeling maps an input sequence of tokens $\\mathbf{x} = (x_1, \\dots, x_T)$ to a corresponding sequence of labels $\\mathbf{y} = (y_1, \\dots, y_T)$. \n\n*   **Part-of-Speech (POS) Tagging:** Assigns syntactic roles (e.g. Noun, Verb, Adjective) to words. This is useful for parsing syntactic structures and resolving lexical ambiguities.\n*   **Named Entity Recognition (NER):** Identifies span-based entities (e.g., Person, Location, Organization). Because entities often span multiple tokens, models use boundary tagging schemes like **BIO (Begin, Inside, Outside)**. For example, 'New York City' is labeled as `[B-LOC, I-LOC, I-LOC]`, while non-entities are labeled as `[O]`.",
                        "callouts": [
                            {
                                "type": "Student Trap",
                                "title": "BIO Tagging Ambiguity",
                                "content": "When parsing NER outputs, ensure that an 'I-ORG' tag is never permitted to follow an 'O' tag without an intervening 'B-ORG' tag. Enforce strict transition grammar rules in your decoder."
                            }
                        ]
                    },
                    {
                        "title": "Hidden Markov Models (HMM) Mathematics",
                        "content": "A Hidden Markov Model (HMM) is a generative transition model. The joint probability of a sequence of states (POS tags) $\\mathbf{y} = (y_1, \\dots, y_T)$ and observations (words) $\\mathbf{x} = (x_1, \\dots, x_T)$ is:\n\n$$P(\\mathbf{x}, \\mathbf{y}) = \\prod_{t=1}^T P(y_t \\mid y_{t-1}) P(x_t \\mid y_t)$$\n\nwhere $P(y_t \\mid y_{t-1})$ is the transition probability, and $P(x_t \\mid y_t)$ is the emission probability. These are computed using maximum likelihood estimates from a tagged training corpus:\n\n*   **Transition Probability:** $P(y_t = s_j \\mid y_{t-1} = s_i) = \\frac{C(s_i, s_j)}{C(s_i)}$\n*   **Emission Probability:** $P(x_t = w_k \\mid y_t = s_j) = \\frac{C(s_j, w_k)}{C(s_j)}$",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Laplace Smoothing for Unseen Emissions",
                                "content": "If a word never appeared with a tag in training, its emission probability $P(x_t \\mid y_t)$ is $0.0$, zeroing out the entire joint probability. Always apply add-one (Laplace) smoothing to transition and emission counts."
                            }
                        ]
                    },
                    {
                        "title": "Viterbi Decoding Optimization",
                        "content": "To find the most likely hidden state sequence $\\mathbf{y}^* = \\arg\\max_{\\mathbf{y}} P(\\mathbf{x}, \\mathbf{y})$, an exhaustive search would require checking $N^T$ combinations, which is computationally intractable. The **Viterbi Algorithm** solves this using dynamic programming.\n\nIt computes the trellis of maximum path probabilities $v_t(j)$ for each state $j$ at time $t$:\n\n$$v_t(j) = \\max_{i} [ v_{t-1}(i) \\times P(y_t=j \\mid y_{t-1}=i) ] \\times P(x_t \\mid y_t=j)$$\n\nBy storing backpointers at each step, we reconstruct the optimal path. The time complexity is reduced from $O(N^T)$ to $O(N^2 T)$, where $N$ is the number of states and $T$ is the sequence length.",
                        "callouts": [
                            {
                                "type": "Interview Tip",
                                "title": "Underflow in Trellis Multiplication",
                                "content": "Repeated multiplication of small probabilities causes floating-point underflow. Always compute Viterbi updates in the log domain: $\\log v_t(j) = \\max_{i} [ \\log v_{t-1}(i) + \\log P(y_t \\mid y_{t-1}) ] + \\log P(x_t \\mid y_t)$."
                            }
                        ]
                    }
                ]
            },
            "revision": "# POS Tagging & NER\n\n## 1. HMM Joint Probability\n$$P(\\mathbf{x}, \\mathbf{y}) = \\prod_{t=1}^T P(y_t \\mid y_{t-1}) P(x_t \\mid y_t)$$\n*   **Transition:** $P(y_t \\mid y_{t-1}) = \\frac{C(y_{t-1}, y_t)}{C(y_{t-1})}$\n*   **Emission:** $P(x_t \\mid y_t) = \\frac{C(y_t, x_t)}{C(y_t)}$\n\n## 2. Viterbi Trellis Update\n$$v_t(j) = \\max_{i} [ v_{t-1}(i) \\times P(y_t=j \\mid y_{t-1}=i) ] \\times P(x_t \\mid y_t=j)$$\n*   Reduces decoding complexity from $O(N^T)$ to $O(N^2 T)$.\n",
            "interview": "# Interview Prep: POS Tagging & NER\n\n## Q1: Explain how the Viterbi algorithm computes the most likely hidden state sequence in an HMM. Write the update step in the log domain.\n\n### Standard Answer\nThe Viterbi algorithm is a dynamic programming algorithm. It computes the trellis of maximum path probabilities $v_t(j)$, representing the probability of the most likely state sequence ending in state $j$ at time $t$:\n\n$$v_t(j) = \\max_{i} [ v_{t-1}(i) \\times P(y_t=j \\mid y_{t-1}=i) ] \\times P(x_t \\mid y_t=j)$$\n\nTo prevent floating-point underflow, we perform the computation in the log domain:\n\n$$\\ln v_t(j) = \\max_{i} \\left[ \\ln v_{t-1}(i) + \\ln P(y_t=j \\mid y_{t-1}=i) \\right] + \\ln P(x_t \\mid y_t=j)$$\n\nAt each step, we record the backpointer:\n\n$$\\text{bp}_t(j) = \\arg\\max_{i} \\left[ \\ln v_{t-1}(i) + \\ln P(y_t=j \\mid y_{t-1}=i) \\right]$$\n\nAt the final step $T$, we select the state maximizing $v_T(j)$ and backtrack using the stored backpointers to reconstruct the optimal sequence.\n",
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
                        "content": "Latent Dirichlet Allocation (LDA) is a generative model for identifying topics within a text corpus. Under LDA, each document is modeled as a mixture of latent topics, and each topic is modeled as a distribution over words. The Dirichlet distribution serves as a prior for the multinomial topic and word distributions, simplifying posterior inference.",
                        "callouts": [
                            {
                                "type": "Student Trap",
                                "title": "Unsupervised Topic Labels",
                                "content": "LDA does not name topics. It output word probability distributions (e.g. topic 1 has high probability for 'bank', 'finance', 'money'). Labelling these topics requires manual domain validation."
                            }
                        ]
                    },
                    {
                        "title": "Dirichlet Priors and Hyperparameter Impact",
                        "content": "The Dirichlet distribution with parameter vector $\\boldsymbol{\\alpha}$ has the probability density function:\n\n$$p(\\boldsymbol{\\theta} \\mid \\boldsymbol{\\alpha}) = \\frac{\\Gamma(\\sum_{k=1}^K \\alpha_k)}{\\prod_{k=1}^K \\Gamma(\\alpha_k)} \\prod_{k=1}^K \\theta_k^{\\alpha_k - 1}$$\n\nwhere $\\boldsymbol{\\theta}$ lies on a simplex (i.e. $\\sum_k \\theta_k = 1, \\theta_k \\ge 0$). In LDA, we use two Dirichlet priors:\n\n1.  **$\\alpha$:** Hyperparameter controlling the document-topic distribution $\\boldsymbol{\\theta}_d$.\n2.  **$\\beta$:** Hyperparameter controlling the topic-word distribution $\\boldsymbol{\\phi}_k$.\n\nSetting $\\alpha < 1$ and $\\beta < 1$ forces the distributions to be sparse (concentrated at the vertices of the simplex). This reflects the reality that documents typically cover only a few topics, and topics are defined by a small set of terms.",
                        "callouts": []
                    },
                    {
                        "title": "Parameter Estimation via Gibbs Sampling",
                        "content": "Because the exact posterior distribution of LDA is intractable to compute, we use approximate inference algorithms like **Gibbs Sampling**. Gibbs sampling iteratively updates the topic assignment $z_i$ of each word $w_i$, conditional on the assignments of all other words:\n\n$$P(z_i = k \\mid \\mathbf{z}_{-i}, \\mathbf{w}, \\alpha, \\beta) \\propto \\frac{n_{k,-i}^{(v)} + \\beta}{\\sum_{v=1}^V (n_{k,-i}^{(v)} + \\beta)} \\times \\frac{n_{d,-i}^{(k)} + \\alpha}{\\sum_{k'=1}^K (n_{d,-i}^{(k')} + \\alpha)}$$\n\nwhere $n_{k,-i}^{(v)}$ is the count of word $v$ assigned to topic $k$ excluding the current token, and $n_{d,-i}^{(k)}$ is the count of topic $k$ occurrences in document $d$ excluding the current token.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Topic Modeling (LDA)\n\n## 1. Probabilistic Generation\nFor each document $d \\in \\mathcal{D}$:\n1. Choose topic distribution $\\theta_d \\sim \\text{Dirichlet}(\\alpha)$\n2. For each word $w_i$ in $d$:\n   a. Choose a topic $z_i \\sim \\text{Multinomial}(\\theta_d)$\n   b. Choose word $w_i \\sim \\text{Multinomial}(\\phi_{z_i})$ where $\\phi_k \\sim \\text{Dirichlet}(\\beta)$\n\n## 2. Gibbs Sampling Equation\n$$P(z_i = k \\mid \\mathbf{z}_{-i}) \\propto \\frac{n_{k,-i}^{(v)} + \\beta}{\\sum_v (n_{k,-i}^{(v)} + \\beta)} \\times \\frac{n_{d,-i}^{(k)} + \\alpha}{\\sum_k' (n_{d,-i}^{(k')} + \\alpha)}$$\n",
            "interview": "# Interview Prep: Topic Modeling\n\n## Q1: Explain why the Dirichlet distribution is used as a prior for the multinomial distribution in LDA.\n\n### Standard Answer\nThe Dirichlet distribution is the **conjugate prior** of the multinomial distribution. This means that if the prior distribution of a variable is Dirichlet and the likelihood is multinomial, the posterior distribution is also a Dirichlet distribution. This property allows us to compute posterior distributions analytically, simplifying parameter estimation in algorithms like Gibbs sampling.\n",
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
                        "title": "Rule-Based Sentiment Analysis & VADER",
                        "content": "Sentiment analysis classifies text polarity (e.g. positive, negative, neutral). Lexicon-based systems map terms to predefined valence values (e.g., 'excellent' = 3.0, 'bad' = -2.0). \n\n**VADER (Valence Aware Dictionary and sEntiment Reasoner)** improves on simple word counts by incorporating grammatical rules:\n\n1.  **Intensifiers:** Words like 'very' scale valence scores (e.g. 'very good' vs 'good').\n2.  **Negations:** Words like 'not' invert valence (e.g. 'not good').\n3.  **Conjunctions:** Words like 'but' shift focus (e.g. 'the food was good, but the service was slow' weights the negative clause higher).",
                        "callouts": []
                    },
                    {
                        "title": "Naive Bayes Classification Mathematics",
                        "content": "For statistical text classification, the **Naive Bayes Classifier** maximizes the posterior probability of class $c$ given document features $\\mathbf{d} = (w_1, \\dots, w_W)$:\n\n$$c_{NB} = \\arg\\max_{c \\in \\mathcal{C}} P(c \\mid \\mathbf{d}) = \\arg\\max_{c \\in \\mathcal{C}} P(c) \\prod_{i=1}^W P(w_i \\mid c)$$\n\nApplying the logarithm to avoid floating-point underflow converts multiplications to additions:\n\n$$c_{NB} = \\arg\\max_{c \\in \\mathcal{C}} \\left[ \\ln P(c) + \\sum_{i=1}^W \\ln P(w_i \\mid c) \\right]$$\n\nwhere the prior is $P(c) = \\frac{N_c}{N}$ and the conditional likelihood is estimated using Laplace (add-one) smoothing:\n\n$$P(w_i \\mid c) = \\frac{C(c, w_i) + 1}{\\sum_{w \\in \\mathcal{V}} C(c, w) + |\\mathcal{V}|}$$",
                        "callouts": [
                            {
                                "type": "Engineering Note",
                                "title": "Numerical Stability of Naive Bayes",
                                "content": "Directly evaluating raw probabilities can lead to floating-point underflow. Always implement Naive Bayes using log-likelihood calculations to maintain numerical stability."
                            }
                        ]
                    }
                ]
            },
            "revision": "# Sentiment Analysis\n\n## 1. Naive Bayes Classification\nSelect tag $c$ maximizing:\n\n$$c_{NB} = \\arg\\max_{c \\in \\mathcal{C}} \\left[ \\ln P(c) + \\sum_{i=1}^W \\ln P(w_i \\mid c) \\right]$$\n\n## 2. Laplace-Smoothed Likelihood\n$$P(w \\mid c) = \\frac{C(c, w) + 1}{\\sum_{w'} C(c, w') + |\\mathcal{V}|}$$\n",
            "interview": "# Interview Prep: Sentiment Analysis\n\n## Q1: Explain why the Naive Bayes conditional independence assumption is 'naive' and why the model still performs well on text classification.\n\n### Standard Answer\nThe 'naive' assumption is that all feature tokens $w_i$ are conditionally independent given the class label $c$:\n\n$$P(w_1, \\dots, w_W \\mid c) = \\prod_{i=1}^W P(w_i \\mid c)$$\n\nThis is untrue in natural language, where syntactic structures and word co-occurrences create strong dependencies (e.g. 'San' is highly dependent on 'Francisco').\n\nDespite this violation, Naive Bayes performs well because classification only requires correct **ranking boundaries** (argmax) rather than exact probability calibration. Even if joint probabilities are skewed, the decision boundary remains highly robust.\n",
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
        write_file(os.path.join(nlp_dir, "notes", f"{topic_id}.json"), json.dumps(notes_content, indent=2))
        write_file(os.path.join(nlp_dir, "revision", f"{topic_id}.md"), data["revision"])
        write_file(os.path.join(nlp_dir, "interview", f"{topic_id}.md"), data["interview"])
        write_file(os.path.join(nlp_dir, "examples", f"{topic_id}-ex1.py"), data["example_code"])
        write_file(os.path.join(nlp_dir, "practice", f"{topic_id}-prac1.py"), data["practice_code"])
        write_file(os.path.join(nlp_dir, "quiz", f"{topic_id}-quiz.json"), json.dumps(data["quiz"], indent=2))

    print("\nSuccessfully generated enriched NLP Module 1 files!")

if __name__ == "__main__":
    main()
