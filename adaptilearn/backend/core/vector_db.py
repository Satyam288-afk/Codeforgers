import os
import numpy as np
import google.generativeai as genai

class SemanticRouter:
    """
    An ultra-fast In-Memory Vector Database.
    Calculates Cosine Similarity between completely dynamic AI-extracted phrases 
    (e.g. 'Fmla Standards') and our Graph Nodes (e.g., 'FMLA') using Google Embeddings!
    """
    
    def __init__(self, known_nodes: list[str]):
        self.known_nodes = known_nodes
        self.node_embeddings = None
        
        try:
            print("🧠 Initializing Semantic Router: Pre-computing Tensor Space...")
            # We use gemini-embedding-001 to create the high-dimensional vectors
            result = genai.embed_content(
                model="models/gemini-embedding-001",
                content=known_nodes,
                task_type="semantic_similarity"
            )
            self.node_embeddings = np.array(result['embedding'])
            print(f"✅ Embedded {len(known_nodes)} curriculum nodes into Tensor Space!")
        except Exception as e:
            print(f"⚠️ Vector DB Init Failed (Offline mode active): {e}")

    def route_skill(self, extracted_skill: str, threshold: float = 0.55) -> str:
        """
        Maps a dynamic string to the mathematically closest Graph Node if similarity > threshold.
        Set threshold slightly loose (0.55 out of 1.0) because acronyms like FMLA vs FMLA Standards
        might have varied vector proximity depending on the model's textual understanding.
        """
        if self.node_embeddings is None:
            return extracted_skill
            
        try:
            result = genai.embed_content(
                model="models/gemini-embedding-001",
                content=[extracted_skill],
                task_type="semantic_similarity"
            )
            query_vector = np.array(result['embedding'][0]) # Get the single embedding
            
            # Compute Cosine Similarity against all graph nodes simultaneously
            dot_products = np.dot(self.node_embeddings, query_vector)
            norms = np.linalg.norm(self.node_embeddings, axis=1) * np.linalg.norm(query_vector)
            
            # Prevent division by zero
            norms[norms == 0] = 1e-10 
            
            similarities = dot_products / norms
            
            best_idx = int(np.argmax(similarities))
            best_score = similarities[best_idx]
            
            if best_score >= threshold:
                matched_node = self.known_nodes[best_idx]
                print(f"🧭 Routed: '{extracted_skill}' ➡️ '{matched_node}' (Confidence: {best_score*100:.1f}%)")
                return matched_node
                
            print(f"🔥 FIREWALL DROP: '{extracted_skill}' rejected. (Best Match {best_score*100:.1f}% < {threshold*100}%)")
            return None # No close mathematical match? DELETE the hallucination!
            
        except Exception as e:
            print(f"Semantic Routing failed for '{extracted_skill}': {e}")
            return extracted_skill
