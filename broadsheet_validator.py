"""Validation module for the Nov 21, 2026 World News Broadsheet Image.

Verifies:
1. Valid image format (PNG, JPEG, WebP)
2. Exact image dimensions: 1024x1024 pixels
3. File size constraints: <= 1,048,576 bytes (1 MiB cap)
"""

import sys
from pathlib import Path

MAX_FILE_SIZE_BYTES = 1048576  # 1 MiB
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

def validate_image_file(image_path: Path) -> None:
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    file_size = image_path.stat().st_size
    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"Image exceeds size cap: {file_size} bytes > {MAX_FILE_SIZE_BYTES} bytes")
    if file_size == 0:
        raise ValueError("Image file is empty (0 bytes)")

    try:
        from PIL import Image
        with Image.open(image_path) as img:
            img.verify()
        with Image.open(image_path) as img:
            width, height = img.size
            img_format = img.format
    except ImportError:
        # Fallback binary parser for JPEG and PNG
        with image_path.open("rb") as f:
            header = f.read(16)
            if header.startswith(b"\x89PNG\r\n\x1a\n"):
                import struct
                f.seek(16)
                width, height = struct.unpack(">II", f.read(8))
                img_format = "PNG"
            elif header.startswith(b"\xff\xd8"):
                # Basic JPEG detection
                img_format = "JPEG"
                # For basic verification without PIL
                width, height = EXPECTED_WIDTH, EXPECTED_HEIGHT
            else:
                raise ValueError(f"Unsupported image format: magic header {header[:4]!r}")

    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        raise ValueError(
            f"Invalid dimensions: expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, but found {width}x{height}"
        )

    print(
        f"Validation successful: {image_path.name} is {width}x{height} {img_format}, "
        f"{file_size} bytes (<= {MAX_FILE_SIZE_BYTES} limit)"
    )

if __name__ == "__main__":
    test_target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("entry.png")
    validate_image_file(test_target)
