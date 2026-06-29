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

    m4_data = {
        "genai-m4-t1": {
            "title": "Reward Model Training",
            "notes": {
                "learning_outcomes": [
                    "Explain pairwise preference loss functions.",
                    "Formulate Bradley-Terry preference alignment model math."
                ],
                "sections": [
                    {
                        "title": "Pairwise Human Preferences and Bradley-Terry Model",
                        "content": "To train a reward model $r_\\psi(\\mathbf{x}, \\mathbf{y})$ that evaluates text outputs, we construct a dataset of pairwise human preferences: $\\mathcal{D}_{pref} = \\{(\\mathbf{x}, \\mathbf{y}_w, \\mathbf{y}_l)\\}$ where $\\mathbf{y}_w$ is the preferred response and $\\mathbf{y}_l$ is the rejected response.\n\nUsing the **Bradley-Terry model**, the probability that $\\mathbf{y}_w$ is preferred over $\\mathbf{y}_l$ is modeled as a sigmoid of their reward differences:\n\n$$P(\\mathbf{y}_w \\succ \\mathbf{y}_l \\mid \\mathbf{x}) = \\sigma\\left( r_\\psi(\\mathbf{x}, \\mathbf{y}_w) - r_\\psi(\\mathbf{x}, \\mathbf{y}_l) \\right) = \\frac{1}{1 + e^{-\\left( r_\\psi(\\mathbf{x}, \\mathbf{y}_w) - r_\\psi(\\mathbf{x}, \\mathbf{y}_l) \\right)}}$$\n\nThe reward model is trained by minimizing the negative log-likelihood (binary cross-entropy loss):\n\n$$\\mathcal{L}_R = -\\mathbb{E}_{(\\mathbf{x}, \\mathbf{y}_w, \\mathbf{y}_l) \\sim \\mathcal{D}} \\left[ \\ln \\sigma\\left( r_\\psi(\\mathbf{x}, \\mathbf{y}_w) - r_\\psi(\\mathbf{x}, \\mathbf{y}_l) \\right) \\right]$$",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Reward Model Training\n\n$$\\mathcal{L} = -\\ln \\sigma(r(x, y_w) - r(x, y_l))$$\n",
            "interview": "# Interview Prep: Reward Models\n\n## Q1: Why is a pairwise ranking loss used to train reward models instead of a standard absolute regression loss?\n\n### Standard Answer\nHuman evaluations are highly subjective and uncalibrated; different annotators assign different scores to the same response. Humans are much more consistent when asked to perform comparative judgments (ranking). Pairwise loss trains the model to align with these relative comparisons, yielding more stable gradients.\n",
            "example_code": "import numpy as np\n\ndef binary_preference_loss(r_pos, r_neg):\n    return -np.log(1.0 / (1.0 + np.exp(-(r_pos - r_neg))))\n\nif __name__ == '__main__':\n    print('Bradley-Terry preference losses active.')\n",
            "practice_code": "import numpy as np\n\ndef binary_preference_loss(r_pos, r_neg):\n    return -np.log(1.0 / (1.0 + np.exp(-(r_pos - r_neg))))\n\ndef run_practice():\n    loss = binary_preference_loss(1.0, 1.0)\n    assert np.allclose(loss, 0.693147)\n    print('[PASS] Preference loss calculation matches predictions.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m4-t1-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What does a reward model loss value approaching 0.0 imply during training?",
                        "options": ["The model assigns a much higher reward score to the preferred response than to the rejected response.", "All generated responses score zero.", "The model has diverged.", "Labels are uniform."],
                        "correct_answer": "The model assigns a much higher reward score to the preferred response than to the rejected response.",
                        "explanation": "As the score difference (r_pos - r_neg) grows, the sigmoid approaches 1.0, making the negative log loss approach 0.0."
                    }
                ]
            }
        },
        "genai-m4-t2": {
            "title": "PPO Alignment Loop",
            "notes": {
                "learning_outcomes": [
                    "Trace Proximal Policy Optimization (PPO) model update loops.",
                    "Formulate KL divergence penalty constraints."
                ],
                "sections": [
                    {
                        "title": "The RLHF PPO Alignment Objective",
                        "content": "In RLHF, we optimize the active policy $\\pi_\\theta$ using reinforcement learning. To prevent the policy from exploiting the reward model (reward hacking) and generating garbage outputs, we add a Kullback-Leibler (KL) divergence constraint penalty to the reward:\n\n$$R_{\\text{pen}}(\\mathbf{x}, \\mathbf{y}) = r_\\psi(\\mathbf{x}, \\mathbf{y}) - \\beta D_{KL}(\\pi_\\theta(\\mathbf{y} \\mid \\mathbf{x}) \\parallel \\pi_{ref}(\\mathbf{y} \\mid \\mathbf{x}))$$\n\nwhere $\\pi_{ref}$ is the frozen initial pre-trained model, and $\\beta$ is a hyperparameter scaling the penalty. The token-level KL penalty is computed as:\n\n$$D_{KL} = \\ln \\pi_\\theta(y_t \\mid \\mathbf{x}, y_{<t}) - \\ln \\pi_{ref}(y_t \\mid \\mathbf{x}, y_{<t})$$",
                        "callouts": []
                    }
                ]
            },
            "revision": "# PPO Alignment Loop\n\n$$R_{\\text{step}} = r(x, y) - \\beta (\\log \\pi_\\theta(y_t \\mid c) - \\log \\pi_{\\text{ref}}(y_t \\mid c))$$\n",
            "interview": "# Interview Prep: PPO Loop\n\n## Q1: What is the risk of setting the KL scaling hyperparameter beta to zero during PPO training?\n\n### Standard Answer\nIf $\\beta=0$, there is no constraint limiting deviations from the reference policy. The actor will exploit blind spots in the reward model (e.g. generating repetitive phrases that happen to score high), leading to **policy collapse** and gibberish outputs.\n",
            "example_code": "import numpy as np\n\ndef compute_kl_penalty(log_p_actor, log_p_ref, beta=0.1):\n    return beta * (log_p_actor - log_p_ref)\n\nif __name__ == '__main__':\n    print('PPO KL penalty trackers loaded.')\n",
            "practice_code": "import numpy as np\n\ndef compute_kl_penalty(log_p_actor, log_p_ref, beta=0.1):\n    return beta * (log_p_actor - log_p_ref)\n\ndef run_practice():\n    pen = compute_kl_penalty(np.log(0.5), np.log(0.25), 0.1)\n    assert np.allclose(pen, 0.0693147)\n    print('[PASS] KL penalty calculations verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m4-t2-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary role of the reference policy model in the PPO training loop?",
                        "options": ["To calculate a KL divergence constraint, preventing the active policy from shifting too far from baseline behaviors.", "To generate token lookups.", "To decode log probability matrices.", "To train the tokenizer."],
                        "correct_answer": "To calculate a KL divergence constraint, preventing the active policy from shifting too far from baseline behaviors.",
                        "explanation": "The reference model is frozen and acts as a constraint baseline; the KL penalty keeps the active model's logits within safe boundaries."
                    }
                ]
            }
        },
        "genai-m4-t3": {
            "title": "Direct Preference Optimization",
            "notes": {
                "learning_outcomes": [
                    "Derive the Direct Preference Optimization (DPO) loss function.",
                    "Explain why DPO eliminates the need for reinforcement learning."
                ],
                "sections": [
                    {
                        "title": "DPO Derivation and closed-form formulation",
                        "content": "Standard PPO RLHF requires maintaining four models in memory simultaneously (policy, value, reward, reference), making it computationally expensive and unstable to train.\n\n**Direct Preference Optimization (DPO)** mathematically derives the optimal policy under the KL-constrained reward objective, expressing the reward function directly in terms of the policy log ratios. The DPO loss function is:\n\n$$\\mathcal{L}_{DPO}(\\pi_\\theta; \\pi_{ref}) = -\\mathbb{E}_{(\\mathbf{x}, \\mathbf{y}_w, \\mathbf{y}_l) \\sim \\mathcal{D}} \\left[ \\ln \\sigma \\left( \\beta \\ln \\frac{\\pi_\\theta(\\mathbf{y}_w \\mid \\mathbf{x})}{\\pi_{ref}(\\mathbf{y}_w \\mid \\mathbf{x})} - \\beta \\ln \\frac{\\pi_\\theta(\\mathbf{y}_l \\mid \\mathbf{x})}{\\pi_{ref}(\\mathbf{y}_l \\mid \\mathbf{x})} \\right) \\right]$$\n\nThis closed-form formulation allows DPO to align models directly on preference pairs using standard supervised cross-entropy loss, eliminating the need for reinforcement learning.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Direct Preference Optimization (DPO)\n\n$$\\mathcal{L}_{DPO} = -\\ln \\sigma \\left( \\beta \\ln \\frac{\\pi_\\theta(y_w \\mid x)}{\\pi_{ref}(y_w \\mid x)} - \\beta \\ln \\frac{\\pi_\\theta(y_l \\mid x)}{\\pi_{ref}(y_l \\mid x)} \\right)$$\n",
            "interview": "# Interview Prep: DPO Math\n\n## Q1: Why does DPO simplify the MLOps pipeline compared to standard PPO?\n\n### Standard Answer\nStandard PPO requires maintaining four large models in memory simultaneously during training: the actor policy, reference policy, value network, and reward model. This creates high GPU memory demands. DPO requires only the actor and reference policy models, reducing hardware requirements and eliminating PPO hyperparameter tuning.\n",
            "example_code": "import numpy as np\n\ndef dpo_loss(pi_w_logratio, pi_l_logratio, beta=0.1):\n    diff = beta * (pi_w_logratio - pi_l_logratio)\n    return -np.log(1.0 / (1.0 + np.exp(-diff)))\n\nif __name__ == '__main__':\n    print('DPO loss function loaded.')\n",
            "practice_code": "import numpy as np\n\ndef dpo_loss(pi_w_logratio, pi_l_logratio, beta=0.1):\n    diff = beta * (pi_w_logratio - pi_l_logratio)\n    return -np.log(1.0 / (1.0 + np.exp(-diff)))\n\ndef run_practice():\n    loss = dpo_loss(0.0, 0.0, 0.1)\n    assert np.allclose(loss, 0.693147)\n    print('[PASS] DPO loss calculations verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m4-t3-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the implicit reward function parameterized inside the DPO loss?",
                        "options": ["r(x, y) = beta * log( pi_theta(y | x) / pi_ref(y | x) )", "r(x, y) = log(y) + x", "r(x, y) = cross_entropy(y)", "r(x, y) = 1.0"],
                        "correct_answer": "r(x, y) = beta * log( pi_theta(y | x) / pi_ref(y | x) )",
                        "explanation": "DPO derives from the closed-form relation between the optimal policy and its reference, allowing the log ratio to act as the implicit reward function."
                    }
                ]
            }
        },
        "genai-m4-t4": {
            "title": "KTO Optimization",
            "notes": {
                "learning_outcomes": [
                    "Explain Kahneman-Tversky Optimization (KTO) utility metrics.",
                    "Contrast KTO binary label datasets with pairwise alignments."
                ],
                "sections": [
                    {
                        "title": "Prospect Theory and Loss Aversion in Alignment",
                        "content": "While DPO simplifies RLHF, it still requires pairwise preference data (identifying a winner and a loser for each prompt). **Kahneman-Tversky Optimization (KTO)** operates directly on binary preference labels (marking a single response as desirable or undesirable).\n\nKTO optimizes a utility function derived from Prospect Theory, which models human loss aversion: humans perceive losses more strongly than equivalent gains. The loss function applies an asymmetric scale parameter $\\lambda > 1$ to penalize undesirable outputs, aligning models without requiring paired data.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# KTO Optimization\n\n*   **Data Format:** Single prompt-response pairs labeled as desirable ($y \\in \\{+1\\}$) or undesirable ($y \\in \\{-1\\}$).\n*   **Prospect Theory link:** Models human decision-making, where losses are perceived more strongly than equivalent gains.\n",
            "interview": "# Interview Prep: KTO\n\n## Q1: Why is KTO easier to scale in enterprise annotation pipelines than DPO?\n\n### Standard Answer\nPairwise preference annotation requires generating and comparing multiple model outputs for each prompt, which adds complexity. KTO only requires annotators to label a single output as positive or negative, which is faster and easier to scale.\n",
            "example_code": "import numpy as np\n\ndef prospect_utility(r, lambda_coef=1.3):\n    return r if r > 0 else lambda_coef * r\n\nif __name__ == '__main__':\n    print('Prospect utility calculator active.')\n",
            "practice_code": "import numpy as np\n\ndef prospect_utility(r, lambda_coef=1.3):\n    return r if r > 0 else lambda_coef * r\n\ndef run_practice():\n    assert prospect_utility(2.0) == 2.0\n    assert prospect_utility(-1.0, 1.5) == -1.5\n    print('[PASS] Prospect utility loss-aversion metrics verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m4-t4-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What is the primary constraint of Prospect Theory incorporated inside KTO?",
                        "options": ["Loss aversion, where human utility drops more sharply for losses than it rises for equivalent gains.", "Linear scale weights.", "Symmetric gain-loss distributions.", "The softmax constraint."],
                        "correct_answer": "Loss aversion, where human utility drops more sharply for losses than it rises for equivalent gains.",
                        "explanation": "Prospect theory models human decision-making under risk, incorporating an asymmetric scaling parameter (lambda > 1) to penalize undesirable outputs."
                    }
                ]
            }
        },
        "genai-m4-t5": {
            "title": "Alignment Tax & Evaluation",
            "notes": {
                "learning_outcomes": [
                    "Explain the alignment tax and its impact on model capabilities.",
                    "Formulate pairwise win-rate evaluation metrics."
                ],
                "sections": [
                    {
                        "title": "The Alignment Tax",
                        "content": "Fine-tuning models to be helpful and harmless often degrades their performance on raw mathematical reasoning or coding tasks. This trade-off is known as the **Alignment Tax**. Evaluating aligned models requires relative benchmarking suites (like MT-Bench or AlpacaEval) that use a strong language model (e.g. GPT-4) as a judge to evaluate and compare response quality.",
                        "callouts": []
                    }
                ]
            },
            "revision": "# Alignment Tax & Evaluation\n\n*   **Alignment Tax:** The loss of generalization and reasoning accuracy due to safety tuning.\n*   **Win Rate:** \n    \n    $$\\text{Win Rate} = \\frac{\\text{wins} + 0.5 \\times \\text{ties}}{\\text{total matches}}$$\n",
            "interview": "# Interview Prep: Alignment Tax\n\n## Q1: Why is an LLM-based judge (e.g. GPT-4) used to evaluate open-ended generation benchmarks instead of standard lexical metrics (like ROUGE)?\n\n### Standard Answer\nLexical metrics compare n-gram overlaps against a reference. Open-ended generation tasks (like creative writing or code explanation) have many valid formulations that do not share n-grams. Strong language models can evaluate semantic coherence, correctness, and style directly, showing high correlation with human judgments.\n",
            "example_code": "def compute_win_rate(wins, ties, losses):\n    total = wins + ties + losses\n    return (wins + 0.5 * ties) / total if total > 0 else 0.0\n\nif __name__ == '__main__':\n    print('Evaluation metrics modules initialized.')\n",
            "practice_code": "def compute_win_rate(wins, ties, losses):\n    total = wins + ties + losses\n    return (wins + 0.5 * ties) / total if total > 0 else 0.0\n\ndef run_practice():\n    wr = compute_win_rate(10, 10, 10)\n    assert wr == 0.5\n    print('[PASS] Win rate calculation verified.')\n\nif __name__ == '__main__':\n    run_practice()\n",
            "quiz": {
                "quiz_id": "genai-m4-t5-quiz",
                "questions": [
                    {
                        "question_id": "q1",
                        "text": "What does a win rate of 75% indicate in an AlpacaEval tournament match containing 100 evaluations?",
                        "options": ["The candidate model defeated the baseline in 75 matches (assuming no ties).", "The candidate model was faster by 75%.", "The context window increased.", "All models scored 0.0."],
                        "correct_answer": "The candidate model defeated the baseline in 75 matches (assuming no ties).",
                        "explanation": "AlpacaEval uses a pairwise comparison matrix to evaluate performance. A 75% win rate indicates that the candidate model was preferred in 75 out of 100 matches."
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
        write_file(os.path.join(genai_dir, "notes", f"{topic_id}.json"), json.dumps(notes_content, indent=2))
        write_file(os.path.join(genai_dir, "revision", f"{topic_id}.md"), data["revision"])
        write_file(os.path.join(genai_dir, "interview", f"{topic_id}.md"), data["interview"])
        write_file(os.path.join(genai_dir, "examples", f"{topic_id}-ex1.py"), data["example_code"])
        write_file(os.path.join(genai_dir, "practice", f"{topic_id}-prac1.py"), data["practice_code"])
        write_file(os.path.join(genai_dir, "quiz", f"{topic_id}-quiz.json"), json.dumps(data["quiz"], indent=2))

    print("\nSuccessfully generated enriched GenAI Module 4 files!")

if __name__ == "__main__":
    main()
