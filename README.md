<div align="center">
  <h1>⚡ SkillForge</h1>
  <p><b>An AI-Adaptive Onboarding & Competency Mapping Engine</b></p>
  <p>
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js" alt="Next.js" />
    <img src="https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
  </p>
</div>

## 🚀 The Problem
Modern enterprise onboarding processes are fundamentally broken. Employees are routinely forced through redundant, one-size-fits-all training modules that assume they know nothing, wasting countless hours of productivity. There is a total lack of precision in mapping an individual's *actual* existing skills against the *strict* requirements of their target job role.

## 💡 The Solution: SkillForge
**SkillForge** mathematically eliminates redundant training. It is an intelligent, AI-driven Learning Topology Engine that parses unstructured employee Resumes against target Job Descriptions, identifies the literal topological "Competency Gap", and generates a stunning, personalized learning roadmap using a custom vector database and knowledge graph.

---

## 🏆 Hackathon Judging Criteria Fulfillment

### 1. Technical Sophistication (20%)
We didn't just wrap a basic LLM prompt. SkillForge utilizes a highly sophisticated pipeline:
*   **Custom Knowledge Graph Engine:** A strict implementation of a Directed Acyclic Graph (`networkx`) that relies on Reverse-BFS and Forward-Pass algorithms to calculate missing prerequisites across domains.
*   **Mathematical Vector DB:** A custom `SemanticRouter` that uses Cosine Similarity against Google Gemini Embeddings to mathematically map noisy user text (e.g. *"vanilla JS"*) to standard schema nodes (*"JavaScript"*). 

### 2. Grounding and Reliability [Zero Hallucinations] (15%)
We implemented a strict "Firewall Drop" policy in our semantic vector router. If the vector distance of an AI-extracted skill does not meet a rigorous `0.55` cosine similarity threshold against our pre-defined curriculum catalog, **the skill is entirely rejected**. It is mathematically impossible for the system to hallucinate non-existent training modules.

### 3. Reasoning Trace (10%)
Absolute explainability is built into the UI. Our **"Reasoning Trace Engine"** explicitly outputs the cited logic connecting the final outcome directly back to the source text. *(Example: "CITED LOGIC: JD strictly requires React (Advanced), but it was not found in your Resume.")*

### 4. Product Impact (10%)
SkillForge generates targeted learning pathways composed **exclusively** of the "Missing Subgraph." By isolating only what the employee *needs* to know, the engine directly drives down redundant HR training costs and significantly accelerates Role-Specific Competency timelines.

### 5. User Experience (15%)
Built on **Next.js**, **Tailwind CSS**, and **Framer Motion**, the platform boasts a staggering deep-space "Neural Intelligence" aesthetic. The dynamic Knowledge Graph features animated glowing nodes, interactive edge drawing, and a premium Glassmorphism dashboard to ensure an elite user experience.

### 6. Cross-Domain Scalability (10%)
Our graph topology scales effortlessly. The current engine perfectly routes highly technical engineering paths (`HTML/CSS ➡️ React ➡️ Next.js`) while simultaneously mapping heavy-labor operational paths (`HR ➡️ OSHA ➡️ Warehouse Safety ➡️ Forklift Machinery`).

---

## 🛠 Setup & Installation

**1. FastAPI Backend Pipeline**
```bash
cd skillforge/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

**2. Next.js Client Terminal**
```bash
cd skillforge/frontend
npm install
npm run dev
```

The application will be accessible at `http://localhost:3000`.

---
<div align="center">
  <i>Built with 💙 for the Hackathon</i>
</div>
