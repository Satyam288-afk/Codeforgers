import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class MockExtractionEngine:
    """
    Hybrid Execution Engine: 
    Attempts to use Google Gemini 1.5 Models for maximum semantic accuracy.
    If the API fails (e.g., timeout or network drop), fails over instantly to 
    an offline Localized Extraction mechanism.
    """
    
    @staticmethod
    def extract_entities(text: str, doc_type: str = "resume") -> list[dict]:
        if not text.strip() or len(text.strip()) < 5:
            return []
            
        prompt = f"""
        You are an expert technical intelligence AI.
        Analyze the following text (which is a {doc_type}) and extract all technical, theoretical, or domain-specific skills.
        For each skill, infer the experience level (or required level) based directly on the context.
        The level MUST be one of exactly three strings: "Beginner", "Intermediate", or "Advanced".
        
        CRITICAL: Respond ONLY with a valid JSON array of objects.
        Format Example: [{{"skill": "React", "level": "Advanced"}}]
        
        Text to analyze:
        {text}
        """
        
        try:
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                generation_config={
                    "temperature": 0.1,
                    "response_mime_type": "application/json",
                }
            )
            response = model.generate_content(prompt)
            content = response.text.strip()
                
            parsed_data = json.loads(content)
            
            formatted_outputs = []
            for item in parsed_data:
                skill_name = str(item.get("skill", "")).title()
                level = str(item.get("level", "Intermediate")).title()
                if skill_name:
                    # Sync formatting patches
                    if skill_name.lower() == "ios": skill_name = "iOS"
                    if skill_name.lower() == "hr": skill_name = "HR"
                    if skill_name.lower() == "fmla": skill_name = "FMLA"
                    if skill_name.lower() == "osha": skill_name = "OSHA"
                    if skill_name.lower() == "hris": skill_name = "HRIS"
                    
                    formatted_outputs.append({"skill": skill_name, "level": level})
                    
            return formatted_outputs
            
        except Exception as e:
            # 2. FAILOVER PIPELINE (Offline Dictionary Mode)
            print(f"Gemini Warning: {e}. Failing over to Offline Heuristic Engine...")
            return MockExtractionEngine._offline_fallback_extraction(text, doc_type)

    @staticmethod
    def _offline_fallback_extraction(text: str, doc_type: str) -> list[dict]:
        """
        Rock-solid offline mock parsing to ensure the application NEVER crashes during a live demo
        due to network drops.
        """
        text_lower = text.lower()
        skills_found = set()
        
        tech_keywords = {
            "python": "Python", "fastapi": "FastAPI", "docker": "Docker", "kubernetes": "Kubernetes",
            "react": "React", "next.js": "Next.js", "javascript": "JavaScript", "ocaml": "OCaml",
            "rust": "Rust", "c++": "C++", "trading": "Trading", "quantitative": "Quantitative",
            "algorithms": "Algorithms", "data structures": "Data Structures", "blockchain": "Blockchain",
            "smart contracts": "Smart Contracts", "go": "Go", "java": "Java", "sql": "SQL",
            "aws": "AWS", "gcp": "GCP", "azure": "Azure", "machine learning": "Machine Learning",
            "ai": "AI", "deep learning": "Deep Learning", "system design": "System Design",
            "cybersecurity": "Cybersecurity", "security": "Security", "networks": "Networks",
            "vulnerabilities": "Vulnerabilities", "incident response": "Incident Response",
            "penetration testing": "Penetration Testing", "cryptography": "Cryptography",
            "cloud security": "Cloud Security", "systems": "Systems",
            "hr": "HR", "human resources": "Human Resources", "recruiting": "Recruiting",
            "payroll": "Payroll", "benefits": "Benefits", "employee relations": "Employee Relations",
            "on-boarding": "On-boarding", "hris": "HRIS", "fmla": "FMLA", "osha": "OSHA",
            "compliance": "Compliance", "labor relations": "Labor Relations", "compensation": "Compensation",
            "flutter": "Flutter", "dart": "Dart", "mobile development": "Mobile Development", 
            "ios": "iOS", "android": "Android", "swift": "Swift", "kotlin": "Kotlin",
            "react native": "React Native", "ui/ux": "UI/UX", "cross-platform": "Cross-Platform"
        }
        
        for kw_lower, kw_proper in tech_keywords.items():
            pattern = r'\b' + re.escape(kw_lower) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                skills_found.add(kw_proper)
                
        if doc_type == "jd":
            raw_skills = text.split(',')
            for skill in raw_skills:
                skill = skill.strip()
                if skill and len(skill.split()) <= 3 and len(skill) <= 25:
                    lower_skill = skill.lower()
                    if lower_skill in tech_keywords:
                        skills_found.add(tech_keywords[lower_skill])
                    else:
                        skills_found.add(skill.title())
                    
        level = "Intermediate"
        if any(w in text_lower for w in ["senior", "experienced", "years", "expert", "lead"]):
            level = "Advanced"
        elif any(w in text_lower for w in ["junior", "intern", "undergraduate", "beginner", "fresher"]):
            level = "Beginner"
            
        return [{"skill": skill, "level": level} for skill in list(skills_found)]
