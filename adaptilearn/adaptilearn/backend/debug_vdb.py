import os
import google.generativeai as genai
from core.vector_db import SemanticRouter
from core.graph_engine import KnowledgeGraphEngine
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

graph_engine = KnowledgeGraphEngine()
all_nodes = list(graph_engine.graph.nodes())

print(f"Total nodes: {len(all_nodes)}")
router = SemanticRouter(all_nodes)

test_skills = ["Fmla Standards", "State And Federal Compliance", "Osha Standards"]

for skill in test_skills:
    print(f"\n--- Testing '{skill}' ---")
    res = router.route_skill(skill, threshold=0.40)
    print(f"Final output: {res}")
