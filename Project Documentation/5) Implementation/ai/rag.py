from pathlib import Path
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class RAGEngine:
    """
    RAG Engine based on the notebook implementation.
    Uses sentence-transformers for embeddings and FAISS for vector search.
    Connects to Groq via OpenAI-compatible API.
    """

    def __init__(
        self,
        knowledge_path: str,
        groq_api_key: str = "",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_model: str = "llama-3.3-70b-versatile",
        chunk_size: int = 120,
        chunk_overlap: int = 20,
    ):
        self.knowledge_path = str(Path(knowledge_path).resolve())
        if not Path(self.knowledge_path).is_file():
            raise FileNotFoundError(f"Knowledge base file not found: {self.knowledge_path}")
        
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=groq_api_key,
        )
        self._embed_model = SentenceTransformer(embedding_model)
        self._chunks = []
        self._index = None

    def load(self):
        text = self.load_text()
        self._chunks = self.chunk_text(text)
        embeddings = self.embed_chunks(self._chunks)
        self._index = self.create_faiss_index(embeddings)
        return len(self._chunks)

    def load_text(self):
        with open(self.knowledge_path, "r", encoding="utf-8") as f:
            return f.read()

    def chunk_text(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = " ".join(words[i : i + self.chunk_size])
            chunks.append(chunk)
        return chunks

    def embed_chunks(self, chunks):
        embeddings = self._embed_model.encode(chunks, convert_to_numpy=True)
        return embeddings

    def create_faiss_index(self, embeddings):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index

    def search_index(self, query, k=3):
        if self._index is None:
            raise RuntimeError("RAG engine not loaded. Call .load() first.")
        query_embedding = self._embed_model.encode([query], convert_to_numpy=True)
        distances, indices = self._index.search(query_embedding, k)
        return [self._chunks[i] for i in indices[0]]

    def search(self, query: str, k: int = 3):
        return self.search_index(query, k)

    def generate(self, query: str, k: int = 3, max_tokens: int = 4096, role: str = "Maintenance Engineer"):
        top_chunks = self.search_index(query, k)
        context = "\n\n".join(top_chunks)
        system_instruction = self._get_role_prompt(role, context)
        return self.generate_maintenance_text(system_instruction, f"Question: {query}", max_tokens)

    def generate_maintenance_text(self, system_instruction, user_question, max_tokens=4096):
        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_question},
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during generation: {str(e)}"

    def _get_role_prompt(self, role, context):
        if role == "Maintenance Engineer":
            return f"""You are TurboMind, a specialized AI assistant for NASA C-MAPSS turbofan engine predictive maintenance. You are currently assisting a Maintenance Engineer.

## Your Role
You are an expert in turbofan engine degradation, sensor data analysis, RUL estimation, and aviation maintenance engineering. Your user expects technically rigorous, evidence-based responses.

## Communication Style
- Use precise technical terminology.
- Reference specific sensors (S01-S21), degradation mechanisms (HPC fouling, turbine blade creep, seal wear, etc.), and quantitative thresholds.
- Cite specific evidence from the retrieved C-MAPSS documentation.
- Structure responses with: Background -> Analysis -> Evidence -> Recommendation.

Reference information:
{context}"""

        elif role == "Field Monitoring Worker":
            return f"""You are TurboMind, a specialized AI assistant for NASA C-MAPSS turbofan engine predictive maintenance. You are currently assisting a Field Monitoring Worker.

## Your Role
You help field technicians and monitoring personnel quickly understand the health status of a turbofan engine and what action to take. Your user needs practical, clear, and immediate guidance.

## Communication Style
- Use simple, practical language. Avoid jargon unless you explain it immediately.
- Always start your response with a clear status summary using this format:
  CRITICAL - [one-sentence summary of the concern]
  MONITOR CLOSELY - [one-sentence summary of the concern]
  HEALTHY - [one-sentence summary]
- Give clear, actionable next steps.
- Use a checklist format when appropriate.
- Explain what the readings or indicators mean in plain terms.

Reference information:
{context}"""

        else:
            return f"""You are TurboMind, a specialized AI assistant for NASA C-MAPSS turbofan engine predictive maintenance. You are assisting a general user.

## Your Role
You serve field monitoring workers, maintenance engineers, and general users seeking information about turbofan engine health, RUL prediction, and maintenance planning.

## Communication Style
- Provide high-level summary first, then optional deeper dive.
- Avoid excessive technical jargon.
- Be helpful and informative.
- Offer to elaborate on specific topics.

Reference information:
{context}"""
