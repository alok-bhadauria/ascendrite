import os
import json

def seed_kb():
    # Resolve target paths
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kb_path = os.path.join(app_dir, "platform", "server", "app", "knowledge-base")
    
    print(f"Creating local knowledge-base repository seeds at: '{kb_path}'")
    
    # Define syllabus tracks details
    tracks = {
        "ai": {
            "machine-learning": {
                "metadata": {
                    "name": "Machine Learning",
                    "difficulty": "Medium",
                    "estimated_hours": 40
                },
                "syllabus": {
                    "modules": [
                        {
                            "id": "ml-foundations",
                            "title": "Machine Learning Foundations",
                            "description": "Linear regressions, gradient descents, loss parameters, and error fitting calculations.",
                            "unlocked": True,
                            "completed": True,
                            "duration": "45m",
                            "difficulty": "Medium",
                            "topics": ["Gradient Descent Derivations", "MSE Cost Fit", "Overfitting Optimization"]
                        },
                        {
                            "id": "deep-learning",
                            "title": "Deep Learning Networks",
                            "description": "Multi-layer feed-forward networks, backpropagation calculus, and weights updates.",
                            "unlocked": True,
                            "completed": False,
                            "duration": "60m",
                            "difficulty": "Hard",
                            "topics": ["Backpropagation Chain Rule", "Activation Functions (ReLU, Sigmoid)", "Weights & Biases Mapping"]
                        },
                        {
                            "id": "multi-agents",
                            "title": "Multi-Agent Architectures",
                            "description": "Orchestrating autonomous agents, communication paradigms, and tool capabilities.",
                            "unlocked": False,
                            "completed": False,
                            "duration": "75m",
                            "difficulty": "Expert",
                            "topics": ["Agent Coordination Protocols", "Execution Tree Planning", "Context Allocation Limits"]
                        }
                    ]
                },
                "notes": {
                    "ml-foundations": {
                        "title": "Linear Regressions & Gradient Fit",
                        "duration": "45m",
                        "difficulty": "Medium",
                        "content": "Linear regression maps a scalar response to one or more explanatory variables using linear predictor functions. The weights are updated iteratively using the Gradient Descent optimization algorithm:\n\n\\theta_j := \\theta_j - \\alpha \\frac{\\partial}{\\partial \\theta_j} J(\\theta)\n\nWhere J(\\theta) represents the Mean Squared Error (MSE) cost function:\n\nJ(\\theta) = \\frac{1}{2m} \\sum_{i=1}^{m} (h_\\theta(x^{(i)}) - y^{(i)})^2\n\nBy minimizing this loss matrix, the model aligns the regression predictor line to the training coordinate parameters.",
                        "attachments": [
                            {"name": "regression_gradient_descent_proof.pdf", "size": "1.4 MB"},
                            {"name": "mse_loss_matrix_derivation.pdf", "size": "890 KB"}
                        ],
                        "nextId": "deep-learning",
                        "nextTitle": "Deep Learning Networks"
                    },
                    "deep-learning": {
                        "title": "Backpropagation Calculus & Network Layers",
                        "duration": "60m",
                        "difficulty": "Hard",
                        "content": "Backpropagation calculates the gradient of the error function with respect to the neural network's weights. It applies the multi-variable Chain Rule calculus layer by layer:\n\n\\frac{\\partial E}{\\partial w_{ij}} = \\frac{\\partial E}{\\partial a_{j}} \\cdot \\frac{\\partial a_j}{\\partial w_{ij}}\n\nBy propagating error derivatives backward from the output layer, weights are fine-tuned to match expected values.",
                        "attachments": [
                            {"name": "backprop_chain_rule_calculus.pdf", "size": "2.1 MB"},
                            {"name": "neural_weights_matrix_ref.xlsx", "size": "420 KB"}
                        ],
                        "nextId": "multi-agents",
                        "nextTitle": "Multi-Agent Architectures"
                    }
                }
            }
        },
        "core-cs": {
            "operating-systems": {
                "metadata": {
                    "name": "Operating Systems",
                    "difficulty": "Hard",
                    "estimated_hours": 50
                },
                "syllabus": {
                    "modules": [
                        {
                            "id": "dbms-engines",
                            "title": "DBMS Database Engines",
                            "description": "Relational storage engines, locking schemas, and index tree traversals.",
                            "unlocked": True,
                            "completed": True,
                            "duration": "40m",
                            "difficulty": "Medium",
                            "topics": ["B-Tree Index Traversals", "ACID Transactions Isolation", "Query Execution Planners"]
                        },
                        {
                            "id": "os-threads",
                            "title": "Operating Systems & Threads",
                            "description": "Thread scheduling, CPU registers, process execution bounds, and locks.",
                            "unlocked": True,
                            "completed": False,
                            "duration": "50m",
                            "difficulty": "Hard",
                            "topics": ["Mutex & Semaphores", "CPU Thread Context Switching", "Memory Mappings"]
                        }
                    ]
                },
                "notes": {}
            }
        },
        "software-engineering": {
            "design-patterns": {
                "metadata": {
                    "name": "Design Patterns",
                    "difficulty": "Medium",
                    "estimated_hours": 35
                },
                "syllabus": {
                    "modules": [
                        {
                            "id": "oop-design",
                            "title": "Object-Oriented System Design",
                            "description": "SOLID patterns, separation of domain rules, and class encapsulation.",
                            "unlocked": True,
                            "completed": True,
                            "duration": "35m",
                            "difficulty": "Medium",
                            "topics": ["SOLID Code Design", "Dependency Injections", "Encapsulation Limits"]
                        }
                    ]
                },
                "notes": {}
            }
        },
        "web-development": {
            "frontend-frameworks": {
                "metadata": {
                    "name": "Frontend Frameworks",
                    "difficulty": "Medium",
                    "estimated_hours": 45
                },
                "syllabus": {
                    "modules": [
                        {
                            "id": "html-css-git",
                            "title": "Web Core Layouts & Git",
                            "description": "Semantic HTML structures, flexbox alignments, responsive layout models, and branches.",
                            "unlocked": True,
                            "completed": True,
                            "duration": "30m",
                            "difficulty": "Easy",
                            "topics": ["Semantic Document Landmarks", "Responsive Media Queries", "Git Branches & Tags Merges"]
                        }
                    ]
                },
                "notes": {}
            }
        }
    }

    # Write folders & JSON files
    for cat, subjects in tracks.items():
        cat_dir = os.path.join(kb_path, cat)
        os.makedirs(cat_dir, exist_ok=True)
        
        for sub, data in subjects.items():
            sub_dir = os.path.join(cat_dir, sub)
            os.makedirs(sub_dir, exist_ok=True)
            
            # Write subject-metadata.json
            with open(os.path.join(sub_dir, "subject-metadata.json"), "w", encoding="utf-8") as f:
                json.dump(data["metadata"], f, indent=2)
                
            # Write syllabus.json
            with open(os.path.join(sub_dir, "syllabus.json"), "w", encoding="utf-8") as f:
                json.dump(data["syllabus"], f, indent=2)
                
            # Write notes
            notes_dir = os.path.join(sub_dir, "notes")
            os.makedirs(notes_dir, exist_ok=True)
            for note_id, note_data in data.get("notes", {}).items():
                with open(os.path.join(notes_dir, f"{note_id}.json"), "w", encoding="utf-8") as f:
                    json.dump(note_data, f, indent=2)

    print("Knowledge base seeding complete.")

if __name__ == "__main__":
    seed_kb()
