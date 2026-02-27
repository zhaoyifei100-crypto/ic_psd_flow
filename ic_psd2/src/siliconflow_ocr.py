"""Run OCR via SiliconFlow DeepSeek-OCR (chat completions).

Usage:
    export SILICONFLOW_API_KEY="your_api_key"
    python siliconflow_ocr.py --input /path/to/image.png

Output:
    Writes a .v file to ./output/<input_basename>.v by default.
    Use --output to override the file path.
"""

import argparse
import base64
import json
import mimetypes
import os
import sys

import requests


API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL_NAME = "deepseek-ai/DeepSeek-OCR"
DEFAULT_OUTPUT_DIR = "output"


def build_data_url(file_path: str) -> str:
    """Create a data URL for an image or PDF file.

    Args:
        file_path: Local file path.

    Returns:
        Data URL string.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")

    return f"data:{mime_type};base64,{encoded}"


def run_ocr(api_key: str, image_path: str, max_tokens: int) -> str:
    """Call SiliconFlow DeepSeek-OCR via chat completions.

    Args:
        api_key: API key string.
        image_path: Local image path.
        max_tokens: Max tokens to generate.

    Returns:
        OCR text content.
    """
    data_url = build_data_url(image_path)

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "<image>\nFree OCR."},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    resp = requests.post(
        API_URL, headers=headers, data=json.dumps(payload), timeout=120
    )
    resp.raise_for_status()
    data = resp.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected response: {data}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description="SiliconFlow DeepSeek-OCR runner")
    parser.add_argument("--input", "-i", required=True, help="Input image/PDF path")
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output .v file path (default: ./output/<input_basename>.v)",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=4096, help="Max output tokens"
    )

    args = parser.parse_args()

    api_key = os.environ.get("SILICONFLOW_API_KEY")
    if not api_key:
        print("Missing SILICONFLOW_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    text = run_ocr(api_key, args.input, args.max_tokens)

    output_path = args.output
    if not output_path:
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        os.makedirs(args.output_dir, exist_ok=True)
        output_path = os.path.join(args.output_dir, f"{base_name}.v")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
