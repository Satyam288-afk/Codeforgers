from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.extraction import MockExtractionEngine
from core.graph_engine import KnowledgeGraphEngine
from core.vector_db import SemanticRouter
import io
import PyPDF2

app = FastAPI(title="SkillForge Backend API")

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PathRequest(BaseModel):
    resume_text: str
    jd_text: str

graph_engine = KnowledgeGraphEngine()
extractor = MockExtractionEngine()

# Initialize the Serverless Vector DB with all mathematical nodes from the graph
all_graph_nodes = list(graph_engine.graph.nodes())
semantic_router = SemanticRouter(all_graph_nodes)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "SkillForge Engine Running"}

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = ""
    try:
        if file.filename.lower().endswith(".pdf"):
            pdf_file = io.BytesIO(content)
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        else:
            text = content.decode("utf-8", errors="ignore")
    except Exception as e:
        text = f"Error extracting PDF: {str(e)}"
        
    return {"filename": file.filename, "text": text}

import concurrent.futures

@app.post("/api/generate_path")
def generate_path(req: PathRequest):
    # 1. Extract skills and experience levels IN PARALLEL
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_resume = executor.submit(extractor.extract_entities, req.resume_text, "resume")
        future_jd = executor.submit(extractor.extract_entities, req.jd_text, "jd")
        
        user_skills_raw = future_resume.result()
        required_skills_raw = future_jd.result()
        
    # 1.5 Semantic Routing & Strict Grounding Firewall (Zero Hallucinations)
    user_skills_filtered = []
    for sk in user_skills_raw:
        routed_name = semantic_router.route_skill(sk["skill"])
        if routed_name is not None:
            sk["skill"] = routed_name
            user_skills_filtered.append(sk)
    user_skills_raw = user_skills_filtered
        
    required_skills_filtered = []
    for sk in required_skills_raw:
        routed_name = semantic_router.route_skill(sk["skill"])
        if routed_name is not None:
            sk["skill"] = routed_name
            required_skills_filtered.append(sk)
    required_skills_raw = required_skills_filtered
    
    # Extract structural keys for the Mathematical Graph
    user_skill_keys = list(set(sk["skill"] for sk in user_skills_raw))
    required_skill_keys = list(set(sk["skill"] for sk in required_skills_raw))
    
    # 2. Graph routing logic (calculating missing vertices)
    dag = graph_engine.get_missing_subgraph(user_skill_keys, required_skill_keys)
    
    # 3. Create Reasoning Traces (Explainability mapping)
    reasoning = []
    for sk_obj in required_skills_raw:
        skill = sk_obj["skill"]
        req_level = sk_obj["level"]
        if skill not in user_skill_keys:
            reasoning.append({
                "skill": skill,
                "reason": f"JD strictly requires {skill} ({req_level}), but it was not found in your Resume."
            })
            
    return {
        "status": "success",
        "data": {
            "user_skills": user_skills_raw,
            "required_skills": required_skills_raw,
            "reasoning": reasoning,
            "graph": dag
        }
    }
