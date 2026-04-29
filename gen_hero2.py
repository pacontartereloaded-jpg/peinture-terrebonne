# -*- coding: utf-8 -*-
"""
Genera una nueva imagen hero para la pagina principal.
Escena: comedor con pared de acento azul marino.
Metodo identico a generar_imagenes_v3.py:
  1. AVANT generado solo con texto
  2. APRES generado con [imagen_avant, prompt] -> coherencia garantizada
  3. Composite lado a lado guardado en public/realisations/
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

client = genai.Client(api_key=API_KEY)

PROMPT_AVANT = (
    "Photorealistic wide-angle photo of a living room with old dull faded beige walls. "
    "Large light grey fabric sofa centered against the far wall facing the camera, "
    "three matching pillows neatly stacked on it. "
    "Rectangular wooden coffee table centered in front of sofa with nothing on it. "
    "Floor lamp with white shade standing in the right corner. "
    "Large window on the left wall, beige linen curtains fully closed blocking all light. "
    "White floating shelf on back wall above the sofa, completely empty. "
    "Light hardwood flooring. Flat dull lighting, dated worn-out look. "
    "Real estate photography, wide angle lens, sharp focus, 1:1 square format."
)

PROMPT_APRES = (
    "This is the exact same living room after a professional interior painting job. "
    "Same room, same camera angle, same sofa position, same coffee table, same lamp corner, "
    "same window on the left, same floating shelf above sofa, same hardwood floor. "
    "The back wall behind the sofa is now painted in rich deep navy blue. "
    "The three remaining walls and ceiling are freshly painted crisp warm white. "
    "Small natural lived-in details added only: "
    "a folded textured throw blanket draped over the left sofa arm, "
    "the three pillows rearranged — two flat and one propped, "
    "a white ceramic vase with dried pampas grass on the left side of the coffee table, "
    "a hardcover design book lying flat on the right side of the coffee table, "
    "the curtains now open halfway letting in warm natural light, "
    "a small potted monstera plant on the floating shelf. "
    "Do NOT move furniture, add windows, change room layout, or alter the floor. "
    "Professional real estate photography, bright and welcoming, 1:1 square format."
)


def generar_avant(prompt: str) -> Image.Image | None:
    print("  [1/2] Generando AVANT (solo texto)...")
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
                print(f"  OK AVANT: {img.size}")
                return img
        print("  !! Sin imagen en la respuesta AVANT")
        return None
    except Exception as e:
        print(f"  ERROR AVANT: {e}")
        return None


def generar_apres(imagen_avant: Image.Image, prompt: str) -> Image.Image | None:
    print("  [2/2] Generando APRES (imagen AVANT + prompt)...")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[imagen_avant, prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                img = Image.open(io.BytesIO(part.inline_data.data))
                print(f"  OK APRES: {img.size}")
                return img
        print("  !! Sin imagen en la respuesta APRES")
        return None
    except Exception as e:
        print(f"  ERROR APRES: {e}")
        return None


def combinar_lado_a_lado(img_avant: Image.Image, img_apres: Image.Image, size: int = 1024) -> Image.Image:
    half = size // 2
    left = img_avant.resize((half, size), Image.LANCZOS)
    right = img_apres.resize((half, size), Image.LANCZOS)
    composite = Image.new("RGB", (size, size), (255, 255, 255))
    composite.paste(left, (0, 0))
    composite.paste(right, (half, 0))
    return composite


def main():
    print("=" * 55)
    print("  Peinture Terrebonne - Nueva imagen hero")
    print(f"  Modelo : {MODEL}")
    print(f"  Metodo : AVANT texto -> APRES [img+texto] (v3)")
    print(f"  Destino: {OUTPUT_PATH}")
    print("=" * 55)

    img_avant = generar_avant(PROMPT_AVANT)
    if img_avant is None:
        print("FALLO: no se pudo generar AVANT")
        sys.exit(1)

    img_apres = generar_apres(img_avant, PROMPT_APRES)
    if img_apres is None:
        print("FALLO: no se pudo generar APRES")
        sys.exit(1)

    composite = combinar_lado_a_lado(img_avant, img_apres, size=1024)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    composite.save(OUTPUT_PATH, "PNG", optimize=True)
    print(f"\n  Guardado: {OUTPUT_PATH}")
    print("=" * 55)


if __name__ == "__main__":
    main()
