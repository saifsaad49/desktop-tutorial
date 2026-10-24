"""Simple vector-memory mock - dict based, no external DB."""
class VectorMemory:
    def __init__(self):
        self.store=[]
    def add(self, text, meta=None):
        self.store.append({"text": text, "meta": meta or {}})
    def search(self, query, k=3):
        # naive keyword match mock
        q=query.lower()
        ranked=sorted(self.store, key=lambda x: q in x["text"].lower(), reverse=True)
        return ranked[:k]
    def has_tried(self, tool, target):
        return any(s["meta"].get("tool")==tool and s["meta"].get("target")==target for s in self.store)
