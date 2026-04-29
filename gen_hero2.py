# -*- coding: utf-8 -*-
"""
Genera una nueva imagen hero para la pagina principal.
Escena: sala de estar con pared de acento en verde bosque.
Guarda el composite antes/despues en public/realisations/.
"""

import io
import os
import sys
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("ERROR: pip install Pillow")
    sys.exit(1)

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("ERROR: Pon GEMINI_API_KEY en variables de entorno")
    sys.exit(1)

MODEL = "gemini-3.1-flash-image-preview"
OUTPUT_PATH = Path(__file__).parent / "public" / "realisations" / "terrebonne-sejour-before-after.png"

PROMPT_AVANT = (
    "Photorealistic wide-angle interior photo of a living room with old dull beige walls. "
    "Large comfortable light grey sofa facing the camera with three pillows neatly stacked. "
    "Wooden coffee table in center with nothing on it. "
    "Floor lamp with white shade in far right corner. "
    "Large window on the left wall with beige linen curtains fully closed. "
    "Empty floating shelf on the back wall. TV mounted on the right wall. "
    "Light hardwood flooring. Flat dull lighting, dated look. "
    "Real estate photography, wide angle, 1:1 square crop."
)

PROMPT_APRES = (
    "This is the exact same living room after a professional painting renovation. "
    "Same room layout, same camera angle, same sofa position, same window, same TV wall, same lamp. "
    "The back accent wall is now painted in rich deep forest green (Benjamin Moore Tarrytown Green). "
    "The other three walls are freshly painted in crisp warm white. White ceiling. "
    "Small lived-in details added: "
    "a plaid throw blanket draped over one sofa arm, "
    "two cushions rearranged casually, "
    "a white ceramic vase with dried pampas grass on the coffee table, "
    "a design book lying flat on the coffee table, "
    "curtains now open letting in bright natural light, "
    "a small plant on the floating shelf. "
    "Do NOT move furniture, change window position, or add new architectural elements. "
    "Real estate photography, wide angle, bright and welcoming, 1:1 square crop."
)


def generer_image(prompt: str, label: str) -> Image.Image | None:
    client = genai.Client(api_key=API_KEY)
    print(f"  Generando {label}...")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                img = Image.open(io.BytesIO(part.inline_data.data))
                print(f"  OK {label}: {img.size}")
                return img
        print(f"  !! Sin imagen para {label}")
        return None
    except Exception as e:
        print(f"  ERROR {label}: {e}")
        return None


def combinar_lado_a_lado(img_avant: Image.Image, img_apres: Image.Image, size: int = 1024) -> Image.Image:
    half = size // 2
    left = img_avant.resize((half, size), Image.LANCZOS)
    right = img_apres.resize((half, size), Image.LANCZOS)
    combined = Image.new("RGB", (size, size), (255, 255, 255))
    combined.paste(left, (0, 0))
    combined.paste(right, (half, 0))
    return combined


def main():
    print("=" * 55)
    print("  Peinture Terrebonne — Nueva imagen hero")
    print(f"  Modelo : {MODEL}")
    print(f"  Destino: {OUTPUT_PATH}")
    print("=" * 55)

    img_avant = generer_image(PROMPT_AVANT, "AVANT")
    if img_avant is None:
        print("FALLO: no se pudo generar la imagen AVANT")
        sys.exit(1)

    img_apres = generer_image(PROMPT_APRES, "APRES")
    if img_apres is None:
        print("FALLO: no se pudo generar la imagen APRES")
        sys.exit(1)

    composite = combinar_lado_a_lado(img_avant, img_apres, size=1024)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    composite.save(OUTPUT_PATH, "PNG", optimize=True)
    print(f"\n  Guardado: {OUTPUT_PATH}")
    print("=" * 55)


if __name__ == "__main__":
    main()
