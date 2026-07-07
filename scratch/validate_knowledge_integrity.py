import os
import json
import sys

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kb_path = os.path.join(base_dir, "knowledge-base")
    
    print("Starting cross-repository validation checks...")
    
    errors = []
    
    # 1. Load root configuration indexes
    platform_struct_file = os.path.join(kb_path, "platform-structure.json")
    domain_tax_file = os.path.join(kb_path, "domain-taxonomy.json")
    knowledge_graph_file = os.path.join(kb_path, "knowledge-graph.json")
    curriculum_map_file = os.path.join(kb_path, "curriculum-map.json")
    
    # Ensure they exist
    for f in [platform_struct_file, domain_tax_file, knowledge_graph_file, curriculum_map_file]:
        if not os.path.exists(f):
            print(f"Error: Required file missing: {f}")
            sys.exit(1)
            
    try:
        with open(platform_struct_file, "r", encoding="utf-8") as f:
            platform_struct = json.load(f)
        with open(domain_tax_file, "r", encoding="utf-8") as f:
            domain_tax = json.load(f)
        with open(knowledge_graph_file, "r", encoding="utf-8") as f:
            knowledge_graph = json.load(f)
        with open(curriculum_map_file, "r", encoding="utf-8") as f:
            curriculum_map = json.load(f)
    except Exception as e:
        print(f"Error parsing global indexes: {e}")
        sys.exit(1)
        
    # 2. Extract structural identifiers
    # Physical subjects
    physical_subject_ids = set()
    subject_paths = {}
    for cat in platform_struct.get("categories", []):
        for sub in cat.get("subjects", []):
            sub_id = sub.get("id")
            physical_subject_ids.add(sub_id)
            subject_paths[sub_id] = os.path.join(kb_path, sub.get("relative_path"))
            
    # Taxonomy subjects
    def extract_taxonomy_subjects(node):
        subjects = set()
        if "children" in node and len(node["children"]) == 0:
            subjects.add(node["id"])
        elif "children" in node:
            for child in node["children"]:
                subjects.update(extract_taxonomy_subjects(child))
        return subjects
        
    taxonomy_subject_ids = extract_taxonomy_subjects(domain_tax)
    
    # Knowledge graph subjects and disciplines
    graph_concept_ids = set()
    graph_discipline_ids = set()
    for node in knowledge_graph.get("nodes", []):
        graph_concept_ids.add(node.get("id"))
        graph_discipline_ids.add(node.get("discipline_id"))
        
    # Curriculum mapped subjects
    curriculum_subject_ids = set()
    curriculum_module_ids = set()
    curriculum_topic_ids = set()
    curriculum_concept_refs = set()
    
    for sub in curriculum_map.get("subjects", []):
        sub_id = sub.get("subject_id")
        curriculum_subject_ids.add(sub_id)
        for mod in sub.get("modules", []):
            curriculum_module_ids.add(mod.get("module_id"))
            for topic in mod.get("topics", []):
                curriculum_topic_ids.add(topic.get("topic_id"))
                for c_ref in topic.get("concept_nodes", []):
                    curriculum_concept_refs.add(c_ref)
                    
    # 3. Reference Consistency Checks
    # Subjects checks
    for sub_id in physical_subject_ids:
        # Check taxonomy reference
        if sub_id not in taxonomy_subject_ids:
            errors.append(f"Subject '{sub_id}' defined in platform-structure.json is missing in domain-taxonomy.json classification.")
            
    for sub_id in taxonomy_subject_ids:
        # Check physical reference
        if sub_id not in physical_subject_ids:
            errors.append(f"Subject '{sub_id}' classified in domain-taxonomy.json has no physical path in platform-structure.json.")
            
    for sub_id in curriculum_subject_ids:
        if sub_id not in physical_subject_ids:
            errors.append(f"Subject '{sub_id}' in curriculum-map.json does not exist in platform-structure.json.")
            
    # Concept references in curriculum must exist in the knowledge graph
    for c_ref in curriculum_concept_refs:
        if c_ref not in graph_concept_ids:
            errors.append(f"Topic in curriculum-map.json references concept '{c_ref}' which does not exist in knowledge-graph.json nodes.")
            
    # Knowledge graph edges must reference existing concept nodes
    for edge in knowledge_graph.get("edges", []):
        src = edge.get("source")
        tgt = edge.get("target")
        if src not in graph_concept_ids:
            errors.append(f"Graph edge references non-existent source concept node: '{src}'")
        if tgt not in graph_concept_ids:
            errors.append(f"Graph edge references non-existent target concept node: '{tgt}'")
            
    # 4. Physical Asset Ingestion Mappings & ID Verification
    # For every subject in curriculum-map, verify that the subject's local metadata matches
    for sub_id in curriculum_subject_ids:
        sub_path = subject_paths.get(sub_id)
        if not sub_path:
            continue
            
        metadata_file = os.path.join(sub_path, "subject-metadata.json")
        syllabus_file = os.path.join(sub_path, "syllabus.json")
        
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, "r", encoding="utf-8") as f:
                    sub_meta = json.load(f)
                if sub_meta.get("id") != sub_id:
                    errors.append(f"Metadata ID mismatch for subject '{sub_id}': found '{sub_meta.get('id')}' in subject-metadata.json")
            except Exception as e:
                errors.append(f"Error parsing metadata for subject '{sub_id}': {e}")
                
        if os.path.exists(syllabus_file):
            try:
                with open(syllabus_file, "r", encoding="utf-8") as f:
                    syllabus = json.load(f)
                
                # Check topics consistency between syllabus.json and curriculum-map.json
                syllabus_topic_ids = set()
                for mod in syllabus.get("modules", []):
                    for topic in mod.get("topics", []):
                        syllabus_topic_ids.add(topic.get("id"))
                        
                # Verify that curriculum-mapped topics for this subject exist in the syllabus.json
                for sub in curriculum_map.get("subjects", []):
                    if sub.get("subject_id") == sub_id:
                        for mod in sub.get("modules", []):
                            for topic in mod.get("topics", []):
                                t_id = topic.get("topic_id")
                                if t_id not in syllabus_topic_ids:
                                    errors.append(f"Topic '{t_id}' in curriculum-map.json does not exist in local syllabus.json for subject '{sub_id}'")
            except Exception as e:
                errors.append(f"Error parsing syllabus for subject '{sub_id}': {e}")
                
    # 5. Output Verification report
    if errors:
        print("\nCross-Repository Integrity Check Failed!")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("\nCross-repository integrity validated successfully with no errors!")
        sys.exit(0)

if __name__ == "__main__":
    main()
