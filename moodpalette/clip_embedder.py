"""CLIP-based color embedder for text-to-color mapping."""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer


ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"


class CLIPColorEmbedder:
    """Uses CLIP to map text directly to color space."""

    # Multilingual CLIP that understands Russian
    MODEL_NAME = "sentence-transformers/clip-ViT-B-32-multilingual-v1"

    # Predefined color vocabulary - 144 colors
    COLOR_VOCAB = [
        # Reds
        ("#FF0000", "яркий красный", "bright red"),
        ("#8B0000", "тёмно-красный", "dark red"),
        ("#DC143C", "малиновый", "crimson"),
        ("#B22222", "кирпичный", "fire brick"),
        ("#CD5C5C", "индийский красный", "indian red"),
        ("#F08080", "светло-коралловый", "light coral"),
        ("#FA8072", "лососевый", "salmon"),
        ("#E9967A", "тёмный лососевый", "dark salmon"),
        ("#FFA07A", "светлый лососевый", "light salmon"),
        ("#FF6347", "томатный", "tomato"),
        ("#FF4500", "оранжево-красный", "orange red"),
        ("#FF7F50", "коралловый", "coral"),

        # Oranges
        ("#FFA500", "оранжевый", "orange"),
        ("#FF8C00", "тёмно-оранжевый", "dark orange"),
        ("#FF7F00", "оранжевый", "orange"),
        ("#D2691E", "шоколадный", "chocolate"),
        ("#F4A460", "песочный", "sandy brown"),
        ("#DEB887", "бежевый", "burlywood"),
        ("#D2B48C", "телесный", "tan"),
        ("#BC8F8F", "розово-коричневый", "rosy brown"),
        ("#CD853F", "перу", "peru"),

        # Yellows
        ("#FFFF00", "жёлтый", "yellow"),
        ("#FFD700", "золотой", "gold"),
        ("#FFA500", "оранжевый", "orange"),
        ("#F0E68C", "хаки", "khaki"),
        ("#BDB76B", "тёмный хаки", "dark khaki"),
        ("#EEE8AA", "бледный желтоватый", "pale goldenrod"),
        ("#FAFAD2", "светло-жёлтый", "light goldenrod"),
        ("#FFFACD", "лимонный шифон", "lemon chiffon"),
        ("#FFEFD5", "папайя", "papaya whip"),
        ("#FFE4B5", "мокасиновый", "moccasin"),
        ("#FFDAB9", "персиковый", "peach puff"),
        ("#FFE4E1", "туманный розовый", "misty rose"),

        # Greens
        ("#008000", "зелёный", "green"),
        ("#006400", "тёмно-зелёный", "dark green"),
        ("#228B22", "лесной зелёный", "forest green"),
        ("#2E8B57", "морской зелёный", "sea green"),
        ("#3CB371", "средний морской", "medium sea green"),
        ("#20B2AA", "светлый морской", "light sea green"),
        ("#66CDAA", "средний аквамарин", "medium aquamarine"),
        ("#8FBC8F", "тёмный морской", "dark sea green"),
        ("#90EE90", "светло-зелёный", "light green"),
        ("#98FB98", "бледно-зелёный", "pale green"),
        ("#00FF7F", "весенний зелёный", "spring green"),
        ("#00FA9A", "средний весенний", "medium spring green"),
        ("#32CD32", "лаймовый", "lime green"),
        ("#7CFC00", "лайм", "lawn green"),
        ("#7FFF00", "шартрез", "chartreuse"),
        ("#ADFF2F", "жёлто-зелёный", "green yellow"),
        ("#556B2F", "тёмный оливковый", "dark olive green"),
        ("#6B8E23", "оливковый", "olive drab"),
        ("#808000", "оливковый", "olive"),
        ("#9ACD32", "жёлто-оливковый", "yellow green"),

        # Cyans
        ("#00FFFF", "циан", "cyan"),
        ("#00CED1", "тёмный бирюзовый", "dark turquoise"),
        ("#40E0D0", "бирюзовый", "turquoise"),
        ("#48D1CC", "средний бирюзовый", "medium turquoise"),
        ("#AFEEEE", "бледный бирюзовый", "pale turquoise"),
        ("#7FFFD4", "аквамарин", "aquamarine"),
        ("#5F9EA0", "кадетский синий", "cadet blue"),
        ("#4682B4", "стальной синий", "steel blue"),
        ("#B0C4DE", "светлый стальной", "light steel blue"),
        ("#ADD8E6", "светло-синий", "light blue"),
        ("#B0E0E6", "порошковый синий", "powder blue"),
        ("#87CEEB", "небесно-голубой", "sky blue"),
        ("#87CEFA", "светло-небесный", "light sky blue"),
        ("#00BFFF", "глубокий небесный", "deep sky blue"),

        # Blues
        ("#0000FF", "синий", "blue"),
        ("#00008B", "тёмно-синий", "dark blue"),
        ("#0000CD", "средний синий", "medium blue"),
        ("#191970", "полуночный синий", "midnight blue"),
        ("#1E90FF", "доджер синий", "dodger blue"),
        ("#4169E1", "королевский синий", "royal blue"),
        ("#6495ED", "васильковый", "cornflower blue"),
        ("#7B68EE", "средний лазурный", "medium slate blue"),
        ("#6A5ACD", "лазурный", "slate blue"),
        ("#483D8B", "тёмный лазурный", "dark slate blue"),
        ("#5F9EA0", "кадетский синий", "cadet blue"),
        ("#4682B4", "стальной синий", "steel blue"),

        # Purples
        ("#800080", "пурпурный", "purple"),
        ("#8B008B", "тёмно-пурпурный", "dark magenta"),
        ("#9400D3", "тёмный фиолетовый", "dark violet"),
        ("#9932CC", "тёмная орхидея", "dark orchid"),
        ("#8A2BE2", "сине-фиолетовый", "blue violet"),
        ("#9370DB", "средний пурпурный", "medium purple"),
        ("#7B68EE", "средний лазурный", "medium slate blue"),
        ("#6A5ACD", "лазурный", "slate blue"),
        ("#483D8B", "тёмный лазурный", "dark slate blue"),
        ("#BA55D3", "средняя орхидея", "medium orchid"),
        ("#DDA0DD", "сливовый", "plum"),
        ("#EE82EE", "фиолетовый", "violet"),
        ("#DA70D6", "орхидея", "orchid"),
        ("#C71585", "средний фиолетово-красный", "medium violet red"),
        ("#FF00FF", "магента", "magenta"),
        ("#FF1493", "глубокий розовый", "deep pink"),
        ("#FF69B4", "ярко-розовый", "hot pink"),
        ("#FFB6C1", "светло-розовый", "light pink"),
        ("#FFC0CB", "розовый", "pink"),

        # Browns
        ("#A52A2A", "коричневый", "brown"),
        ("#8B4513", "жжёный", "saddle brown"),
        ("#D2691E", "шоколадный", "chocolate"),
        ("#CD853F", "перу", "peru"),
        ("#DEB887", "бежевый", "burlywood"),
        ("#D2B48C", "телесный", "tan"),
        ("#F4A460", "песочный", "sandy brown"),
        ("#BC8F8F", "розово-коричневый", "rosy brown"),
        ("#F5DEB3", "пшеничный", "wheat"),
        ("#FFE4C4", "бисквитный", "bisque"),
        ("#FFEBCD", "бланманже", "blanched almond"),
        ("#FAEBD7", "античный белый", "antique white"),

        # Whites/Greys/Blacks
        ("#FFFFFF", "белый", "white"),
        ("#F5F5F5", "дымчатый", "white smoke"),
        ("#DCDCDC", "гейнсборо", "gainsboro"),
        ("#C0C0C0", "серебряный", "silver"),
        ("#A9A9A9", "тёмно-серый", "dark grey"),
        ("#808080", "серый", "grey"),
        ("#696969", "тусклый серый", "dim grey"),
        ("#778899", "светлый серо-стальной", "light slate grey"),
        ("#708090", "серо-стальной", "slate grey"),
        ("#2F4F4F", "тёмный сине-зелёный", "dark slate grey"),
        ("#000000", "чёрный", "black"),
        ("#1C1C1C", "почти чёрный", "almost black"),
        ("#2C2C2C", "очень тёмный серый", "very dark grey"),
        ("#3C3C3C", "тёмный серый", "dark grey"),
        ("#4C4C4C", "угольный", "charcoal"),
        ("#5C5C5C", "серый", "grey"),

        # Additional mood colors
        ("#0D1B2A", "глубокая ночь", "deep night"),
        ("#1B263B", "ночное небо", "night sky"),
        ("#415A77", "сумерки", "twilight"),
        ("#778DA9", "туман", "mist"),
        ("#E0E1DD", "серебристый", "silver"),
        ("#FCA311", "теплый оранжевый", "warm orange"),
        ("#FFD166", "солнечный", "sunny"),
        ("#FFE29A", "мягкий жёлтый", "soft yellow"),
        ("#FFF3D6", "кремовый", "cream"),
        ("#4B3F3A", "тёмный шоколад", "dark chocolate"),
        ("#7A5C58", "мокко", "mocha"),
        ("#A4877B", "капучино", "cappuccino"),
        ("#D0B8A8", "латте", "latte"),
        ("#ECE2D0", "ваниль", "vanilla"),
        ("#8ECAE6", "ледяной", "icy"),
        ("#219EBC", "океан", "ocean"),
        ("#023047", "глубина", "depth"),
        ("#FFB703", "медовый", "honey"),
        ("#FF006E", "неоновый розовый", "neon pink"),
        ("#8338EC", "неоновый фиолетовый", "neon purple"),
        ("#3A86FF", "неоновый синий", "neon blue"),
        ("#0D0D0D", "чёрная дыра", "black hole"),
    ]

    def __init__(self):
        self.model: SentenceTransformer | None = None
        self.color_embeddings: np.ndarray | None = None
        self.colors: List[Tuple[str, str, str]] = []
        self._load()

    def _load(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_path = CACHE_DIR / "clip_color_embeddings.pkl"

        self.colors = self.COLOR_VOCAB

        # Try load cached embeddings
        if cache_path.exists():
            try:
                with open(cache_path, "rb") as f:
                    cached = pickle.load(f)
                    if cached.get("count") == len(self.colors):
                        self.color_embeddings = cached["embeddings"]
                        print(f"[CLIP] Loaded {len(self.colors)} color embeddings from cache.")
                        return
            except Exception:
                pass  # Rebuild if cache corrupted

        # Build embeddings
        print(f"[CLIP] Building embeddings for {len(self.colors)} colors...")
        self.model = SentenceTransformer(self.MODEL_NAME)

        # Create rich text descriptions for each color
        texts = []
        for hex_color, ru_name, en_name in self.colors:
            # Combine descriptions for better semantic matching
            texts.append(f"{ru_name} цвет, {en_name} color, {hex_color}")

        self.color_embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        # Cache
        with open(cache_path, "wb") as f:
            pickle.dump({
                "count": len(self.colors),
                "embeddings": self.color_embeddings
            }, f)

        print(f"[CLIP] Color embeddings built and cached.")

    def get_colors_for_text(
        self,
        text: str,
        num_colors: int = 5,
        temperature: float = 1.0
    ) -> List[str]:
        """
        Get top-N colors that best match the text description.

        Args:
            text: Text description (e.g., "тёмный зелёный лес")
            num_colors: Number of colors to return
            temperature: Higher = more diverse colors, Lower = more focused
        """
        if self.model is None:
            self.model = SentenceTransformer(self.MODEL_NAME)

        # Encode the query
        query_vec = self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

        # Compute similarities with all colors
        similarities = np.dot(self.color_embeddings, query_vec)

        # Apply temperature scaling for diversity control
        if temperature != 1.0:
            similarities = similarities / temperature

        # Get top colors
        top_indices = np.argsort(similarities)[::-1][:num_colors * 2]  # Get more, then filter

        # Filter out too similar colors
        selected = []
        selected_hex = []

        for idx in top_indices:
            if len(selected) >= num_colors:
                break

            hex_color = self.colors[idx][0]

            # Check not too similar to already selected
            too_similar = False
            for existing in selected_hex:
                if self._color_distance(hex_color, existing) < 30:
                    too_similar = True
                    break

            if not too_similar:
                selected.append(hex_color)
                selected_hex.append(hex_color)

        # If not enough unique colors, fill with variations
        while len(selected) < num_colors:
            base = selected[-1] if selected else "#808080"
            selected.append(self._vary_color(base, len(selected)))

        return selected[:num_colors]

    def _color_distance(self, c1: str, c2: str) -> float:
        """Euclidean distance between two hex colors."""
        def hex_to_rgb(h):
            h = h.lstrip("#")
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

        r1, g1, b1 = hex_to_rgb(c1)
        r2, g2, b2 = hex_to_rgb(c2)

        return ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) ** 0.5

    def _vary_color(self, hex_color: str, variation: int) -> str:
        """Create a slight variation of a color."""
        import colorsys

        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255

        h, l, s = colorsys.rgb_to_hls(r, g, b)

        # Vary lightness slightly
        l = max(0.05, min(0.95, l + variation * 0.05))

        nr, ng, nb = colorsys.hls_to_rgb(h, l, s)
        return f"#{int(nr*255):02X}{int(ng*255):02X}{int(nb*255):02X}"


# Singleton instance
_clip_instance: CLIPColorEmbedder | None = None


def get_clip_embedder() -> CLIPColorEmbedder:
    global _clip_instance
    if _clip_instance is None:
        _clip_instance = CLIPColorEmbedder()
    return _clip_instance
