import os
import sys
from pathlib import Path


class RAGEngine:
    """Simple file-based RAG without ML dependencies"""

    def __init__(self, persist_dir: str = "./knowledge_base"):
        self.persist_dir = Path(persist_dir)
        self.documents = {}
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        sys.stdout.write("[RAG] Initialized (file-based)\n")
        sys.stdout.flush()
        self.ingest_documents()

    def ingest_documents(self) -> int:
        """Load all markdown files from knowledge_base"""
        self.documents = {}
        
        if not self.persist_dir.exists():
            sys.stdout.write(f"[RAG] Path not found: {self.persist_dir}\n")
            sys.stdout.flush()
            return 0

        for md_file in self.persist_dir.glob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.documents[md_file.stem] = {
                        "content": content,
                        "source": md_file.name
                    }
                    sys.stdout.write(f"[RAG] Loaded: {md_file.name}\n")
                    sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f"[RAG] Error loading {md_file.name}: {e}\n")
                sys.stdout.flush()

        sys.stdout.write(f"[RAG] Ingested {len(self.documents)} documents\n")
        sys.stdout.flush()
        return len(self.documents)

    def _keyword_search(self, query: str, top_k: int = 3) -> list:
        """Simple keyword-based search"""
        query_words = set(query.lower().split())
        results = []

        for doc_id, doc_data in self.documents.items():
            content = doc_data["content"].lower()
            source = doc_data["source"]
            
            # Count matching keywords
            matches = sum(1 for word in query_words if word in content)
            
            if matches > 0:
                # Extract relevant snippet (first 300 chars)
                snippet = doc_data["content"][:300]
                results.append({
                    "id": doc_id,
                    "source": source,
                    "content": snippet,
                    "relevance": matches
                })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:top_k]

    def retrieve_context(self, query: str, top_k: int = 3) -> list:
        """Retrieve relevant documents for query"""
        try:
            results = self._keyword_search(query, top_k)
            
            formatted = []
            for result in results:
                text = f"[{result['source']}]\n{result['content']}..."
                formatted.append(text)
                sys.stdout.write(f"[RAG] Retrieved: {result['source']}\n")
                sys.stdout.flush()
            
            return formatted
        except Exception as e:
            sys.stdout.write(f"[RAG] Retrieval error: {e}\n")
            sys.stdout.flush()
            return []

    def add_knowledge(self, content: str, source: str, doc_id: str = None) -> bool:
        """Add knowledge dynamically"""
        try:
            if not doc_id:
                doc_id = f"{source}_{hash(content) % 10000}"
            
            self.documents[doc_id] = {
                "content": content,
                "source": source
            }
            sys.stdout.write(f"[RAG] Added knowledge: {doc_id}\n")
            sys.stdout.flush()
            return True
        except Exception as e:
            sys.stdout.write(f"[RAG] Add error: {e}\n")
            sys.stdout.flush()
            return False

    def get_stats(self) -> dict:
        """Get RAG statistics"""
        return {
            "mode": "file-based keyword search",
            "documents": len(self.documents),
            "storage": str(self.persist_dir),
            "documents_list": list(self.documents.keys())
        }
