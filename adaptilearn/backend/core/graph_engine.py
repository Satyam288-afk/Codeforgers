import networkx as nx

class KnowledgeGraphEngine:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._seed_mock_knowledge_graph()
        
    def _seed_mock_knowledge_graph(self):
        edges = [
            ("Python", "FastAPI"),
            ("Python", "Data Science"),
            ("FastAPI", "Microservices"),
            ("Docker", "Kubernetes"),
            ("Microservices", "Kubernetes"),
            ("HTML/CSS", "React"),
            ("JavaScript", "React"),
            ("React", "Next.js"),
            
            # Paths starting from User's base skills for the exact demo
            ("Algorithms", "Functional Programming"),
            ("Functional Programming", "Ocaml"),
            
            ("Data Structures", "Memory Management"),
            ("Memory Management", "Systems Programming"),
            ("Systems Programming", "Rust"),
            
            ("Rust", "High-Frequency Trading"),
            ("Trading", "High-Frequency Trading"),
            ("Quantitative", "High-Frequency Trading"),
            ("Blockchain", "Smart Contracts"),
            
            # Cybersecurity Pathways
            ("Python", "Networks"),
            ("Networks", "Systems"),
            ("Systems", "Security"),
            ("Security", "Cybersecurity"),
            ("Cybersecurity", "Vulnerabilities"),
            ("Smart Contracts", "Cryptography"),
            ("Cryptography", "Cybersecurity"),
            
            # Human Resources Pathways (Auto-mined)
            ("Employee Relations", "Human Resources"),
            ("Recruiting", "Human Resources"),
            ("Talent Acquisition", "Human Resources"),
            
            # --- CROSS-DOMAIN TOPOLOGY: OPERATIONAL / LABOR ROLES ---
            ("Warehouse Safety", "Forklift Operation"),
            ("Inventory Management", "Supply Chain Operations"),
            ("Forklift Operation", "Heavy Machinery"),
            ("OSHA", "Warehouse Safety"), # Incredible cross-domain linking (HR -> Manual Labor)
            ("Quality Control", "Manufacturing"),
            ("Supply Chain Operations", "Manufacturing"),
            ("Benefits", "Compensation"),
            ("Compensation", "Human Resources"),
            ("HR", "Human Resources"),
            ("HRIS", "Payroll"),
            ("Payroll", "Human Resources"),
            ("FMLA", "Compliance"),
            ("OSHA", "Compliance"),
            ("Compliance", "Human Resources"),
            
            # Mobile Development Pathways (Kaggle Mined)
            ("JavaScript", "React Native"),
            ("React", "React Native"),
            ("React Native", "Cross-Platform"),
            ("Dart", "Flutter"),
            ("Flutter", "Cross-Platform"),
            ("Cross-Platform", "Mobile Development"),
            ("Swift", "iOS"),
            ("Kotlin", "Android"),
            ("iOS", "Mobile Development"),
            ("Android", "Mobile Development"),
            ("Mobile Development", "UI/UX")
        ]
        self.graph.add_edges_from(edges)
        
    def get_missing_subgraph(self, user_skills: list, required_skills: list) -> dict:
        target_skills = set(required_skills) - set(user_skills)
        if not target_skills:
            return {"nodes": [], "edges": []}
            
        path_nodes = set()
        path_edges = []
        
        # Reverse BFS to construct the learning path from target down to fundamental prerequisites
        visited = set()
        queue = list(target_skills)
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            path_nodes.add(current)
            
            for u, v in self.graph.edges():
                if v == current:
                    path_nodes.add(u)
                    path_edges.append({"source": u, "target": v})
                    if u not in user_skills and u not in visited:
                        queue.append(u)
                        
        # Forward pass to guarantee the user's base skills (foundations) connect upwards to the path
        for sk in user_skills:
            for u, v in self.graph.edges():
                if u == sk and v in path_nodes:
                    path_nodes.add(u)
                    path_edges.append({"source": u, "target": v})
                        
        nodes = [{"id": sk, "data": {"label": sk}, "position": {"x": 0, "y": 0}} for sk in path_nodes]
        edges_formatted = [{"id": f"{e['source']}-{e['target']}", "source": e["source"], "target": e["target"]} for e in path_edges]
        
        # Deduplicate edges
        seen_edges = set()
        unique_edges = []
        for e in edges_formatted:
            if e["id"] not in seen_edges:
                seen_edges.add(e["id"])
                unique_edges.append(e)
        
        return {
            "nodes": nodes,
            "edges": unique_edges
        }
