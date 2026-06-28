"""Sentence Transformer embedder with palette cache."""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from sentence_transformers import SentenceTransformer


ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
PALETTES_PATH = DATA_DIR / "palettes.jsonl"


class PaletteEmbedder:
    """Loads sentence-transformer model, builds and caches palette embeddings."""

    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self):
        self.model: SentenceTransformer | None = None
        self.palettes: List[Dict[str, Any]] = []
        self.embeddings: np.ndarray | None = None
        self._load()

    def _load(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_path = CACHE_DIR / "palette_embeddings.pkl"

        # Load palettes
        self.palettes = []
        if PALETTES_PATH.exists():
            with open(PALETTES_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self.palettes.append(json.loads(line))

        # Try load cached embeddings
        if cache_path.exists():
            with open(cache_path, "rb") as f:
                cached = pickle.load(f)
                if cached.get("count") == len(self.palettes):
                    self.embeddings = cached["embeddings"]
                    print(f"[Embedder] Loaded {len(self.palettes)} palettes from cache.")
                    return

        # Build embeddings
        print(f"[Embedder] Building embeddings for {len(self.palettes)} palettes...")
        self.model = SentenceTransformer(self.MODEL_NAME)

        texts = []
        for p in self.palettes:
            # Combine name and tags for richer semantics
            tag_str = " ".join(p.get("tags", []))
            texts.append(f"{p.get('name', '')} {tag_str}".strip())

        self.embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        # Cache
        with open(cache_path, "wb") as f:
            pickle.dump({
                "count": len(self.palettes),
                "embeddings": self.embeddings
            }, f)

        print(f"[Embedder] Embeddings built and cached.")

    def encode_query(self, text: str) -> np.ndarray:
        """Encode user query to normalized embedding vector."""
        if self.model is None:
            self.model = SentenceTransformer(self.MODEL_NAME)
        vec = self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return vec

    def get_palette(self, index: int) -> Dict[str, Any]:
        return self.palettes[index]

    def get_embedding(self, index: int) -> np.ndarray:
        return self.embeddings[index]

    def __len__(self):
        return len(self.palettes)


# Singleton instance
_embedder_instance: PaletteEmbedder | None = None


def get_embedder() -> PaletteEmbedder:
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = PaletteEmbedder()
    return _embedder_instance