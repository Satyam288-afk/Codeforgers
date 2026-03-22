<div align="center">
  <h1>⚡ SkillForge</h1>
  <p><b>An AI-Adaptive Onboarding & Competency Mapping Engine</b></p>
  <p>
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js" alt="Next.js" />
    <img src="https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/NetworkX-4C8CBF?style=for-the-badge" alt="NetworkX" />
  </p>
</div>

---

## 🚀 The Problem

Modern enterprise onboarding is fundamentally broken. Employees are routinely forced through redundant, one-size-fits-all training modules that assume they know nothing—wasting countless hours of productivity. There is a total lack of precision in mapping an individual's **actual** existing skills against the **strict** requirements of their target job role.

## 💡 The Solution: SkillForge

**SkillForge** mathematically eliminates redundant training. It is an intelligent, AI-driven **Learning Topology Engine** that:

1. **Parses** unstructured employee Résumés and target Job Descriptions.
2. **Extracts** skills using Google Gemini 2.5 Flash (with an offline failover).
3. **Grounds** every extracted skill against a curated curriculum via a custom vector database—making hallucinations mathematically impossible.
4. **Computes** the exact topological "Competency Gap" using a DAG-based Knowledge Graph.
5. **Generates** a personalized, explainable learning roadmap containing **only** what the employee still needs to learn.

---

## 📐 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         SkillForge Pipeline                         │
│                                                                      │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────┐ │
│  │  INPUT   │───▶│  STAGE 1     │───▶│  STAGE 2     │───▶│ STAGE 3 │ │
│  │ Resume + │    │  LLM Skill   │    │  Semantic    │    │  Graph  │ │
│  │ Job Desc │    │  Extraction  │    │  Routing &   │    │  Gap    │ │
│  │ (PDF/Txt)│    │  (Gemini AI) │    │  Grounding   │    │ Compute │ │
│  └─────────┘    └──────────────┘    └──────────────┘    └────┬────┘ │
│                                                              │      │
│                                                              ▼      │
│                                                     ┌──────────────┐│
│                                                     │  STAGE 4     ││
│                                                     │  Reasoning   ││
│                                                     │  Trace &     ││
│                                                     │  Roadmap     ││
│                                                     └──────────────┘│
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Skill-Gap Analysis Logic — Deep Dive

### Stage 1 — AI Skill Extraction (`core/extraction.py`)

The `MockExtractionEngine` uses a **Hybrid Execution** strategy:

| Mode | Trigger | Technology |
|---|---|---|
| **Primary** | Default (API available) | Google **Gemini 2.5 Flash** (`temperature: 0.1`, JSON response mode) |
| **Failover** | API timeout / network drop | Offline regex-based keyword dictionary (~50 skills across 6+ domains) |

- Both the Résumé and Job Description are processed **in parallel** via `concurrent.futures.ThreadPoolExecutor` to minimize latency.
- The LLM outputs a structured JSON array of `{skill, level}` objects where `level ∈ {Beginner, Intermediate, Advanced}`.

### Stage 2 — Semantic Routing & Grounding Firewall (`core/vector_db.py`)

Every AI-extracted skill passes through the **SemanticRouter** — a custom in-memory vector database:

1. **Pre-computation**: At startup, all Knowledge Graph node names are embedded into high-dimensional vectors using `gemini-embedding-001`.
2. **Runtime routing**: Each extracted skill string is embedded and compared against all graph nodes via **Cosine Similarity**:

   ```
   similarity(A, B) = (A · B) / (‖A‖ × ‖B‖)
   ```

3. **Firewall threshold** (`≥ 0.55`): If the best match falls **below** this threshold, the skill is **dropped entirely** — guaranteeing zero hallucinations. The system cannot invent training modules that don't exist in the curriculum.

> *Example:* `"vanilla JS"` → routed to `"JavaScript"` (87.3% confidence) ✅  
> *Example:* `"quantum knitting"` → **FIREWALL DROP** (best match 23.1%) 🔥

### Stage 3 — Knowledge Graph Gap Computation (`core/graph_engine.py`)

The `KnowledgeGraphEngine` maintains a **Directed Acyclic Graph (DAG)** of skill prerequisites using `networkx.DiGraph`. The gap is computed mathematically:

1. **Set Difference**: `target_skills = required_skills − user_skills` → the raw gap.
2. **Reverse BFS**: Starting from each target skill, traverse **backwards** through all prerequisite edges to discover every foundational skill the user must also learn.
3. **Forward Pass**: From the user's existing skills, traverse **forward** to connect their foundations into the missing subgraph, creating a complete learning path.
4. **Output**: A deduplicated subgraph of `{nodes, edges}` formatted for [React Flow](https://reactflow.dev/) visualization.

The graph covers **6+ domains** including Software Engineering, Cybersecurity, Human Resources, Mobile Development, Manufacturing/Operations, and Quantitative Finance.

### Stage 4 — Reasoning Trace Generation (`main.py`)

For every required skill **not** found in the user's résumé, the engine generates an explicit, cited reasoning trace:

```
"JD strictly requires React (Advanced), but it was not found in your Resume."
```

This provides full **explainability** — every gap in the final roadmap is directly traceable back to the source documents. 
---
## 📦 Dependencies

### Backend (Python)

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | 0.110.0 | High-performance async REST API framework |
| `uvicorn` | 0.28.0 | ASGI server for serving the FastAPI application |
| `pydantic` | 2.6.3 | Data validation and serialization via Python type hints |
| `google-generativeai` | 0.4.1 | Google Gemini API client for LLM skill extraction & text embeddings |
| `PyPDF2` | 3.0.1 | PDF text extraction from uploaded résumé documents |
| `networkx` | 3.2.1 | Directed Acyclic Graph (DAG) engine for Knowledge Graph construction |
| `python-multipart` | 0.0.9 | Multipart form data parsing for file uploads |

### Frontend (Node.js / TypeScript)

| Package | Version | Purpose |
|---|---|---|
| `next` | 16.2.0 | React framework with SSR, routing, and API layer |
| `react` / `react-dom` | 19.2.4 | UI component library |
| `tailwindcss` | ^4 | Utility-first CSS framework for rapid UI styling |
| `framer-motion` | ^12.38.0 | Declarative animations and micro-interactions |
| `reactflow` | ^11.11.4 | Interactive Knowledge Graph visualization (nodes, edges, zoom, pan) |
| `lucide-react` | ^0.577.0 | Modern SVG icon library |
| `clsx` / `tailwind-merge` | Latest | Conditional CSS class utilities |

---

## 🛠 Setup & Installation

### Prerequisites

- **Python** 3.10+
- **Node.js** 18+ and **npm**
- A **Google Gemini API Key** ([Get one here](https://aistudio.google.com/apikey))

### 1. Clone the Repository

```bash
git clone https://github.com/<your-org>/skillforge.git
cd skillforge
```

### 2. Backend Setup (FastAPI)

```bash
cd adaptilearn/backend

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Environment Variables

Create a `.env` file in `adaptilearn/backend/`:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

#### Start the Backend Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

### 3. Frontend Setup (Next.js)

```bash
cd adaptilearn/frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The application will be accessible at `http://localhost:3000`.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check — returns `{ status: "ok" }` |
| `POST` | `/api/upload` | Upload a PDF or text file; returns extracted text |
| `POST` | `/api/generate_path` | Accepts `{ resume_text, jd_text }`; returns the full skill-gap analysis with graph, reasoning traces, and skill lists |

### Example `/api/generate_path` Response

```json
{
  "status": "success",
  "data": {
    "user_skills": [{ "skill": "Python", "level": "Advanced" }],
    "required_skills": [{ "skill": "React", "level": "Advanced" }],
    "reasoning": [
      {
        "skill": "React",
        "reason": "JD strictly requires React (Advanced), but it was not found in your Resume."
      }
    ],
    "graph": {
      "nodes": [{ "id": "React", "data": { "label": "React" }, "position": { "x": 0, "y": 0 } }],
      "edges": [{ "id": "JavaScript-React", "source": "JavaScript", "target": "React" }]
    }
  }
}
```

---

## 📂 Project Structure

```
adaptilearn/
├── backend/
│   ├── main.py                 # FastAPI app entry point & API routes
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (GEMINI_API_KEY)
│   └── core/
│       ├── extraction.py       # Hybrid AI/Offline skill extraction engine
│       ├── graph_engine.py     # DAG-based Knowledge Graph & gap computation
│       └── vector_db.py        # Semantic Router (in-memory vector DB)
├── frontend/
│   ├── app/                    # Next.js App Router pages
│   ├── components/             # Reusable React components
│   ├── package.json            # Node.js dependencies
│   └── ...
```

---

## 🚢 Deployment

| Service | Platform | URL |
|---|---|---|
| Backend API | [Render](https://render.com) | `https://<your-render-url>.onrender.com` |
| Frontend App | [Vercel](https://vercel.com) | `https://<your-vercel-url>.vercel.app` |

> ⚡ **Note:** The backend runs on Render's free tier, which has a ~30s cold start after periods of inactivity. Once warmed up, all API responses are near-instant. The initial boot also pre-computes a full embedding tensor space via Google's API for the Semantic Router — this is by design for zero-latency inference at runtime.

---

<div align="center">
  <i>Built with 💙 by Team CodeForgers</i>
</div>
