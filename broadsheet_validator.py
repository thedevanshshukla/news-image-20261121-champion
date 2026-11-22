"""Validation module for the Nov 21, 2026 World News Broadsheet Image.

Verifies:
1. PNG magic header signature
2. Exact image dimensions: 1024x1024 pixels via IHDR chunk parsing
3. File size constraints: <= 1,048,576 bytes (1 MiB cap)
"""

import struct
from pathlib import Path

MAX_FILE_SIZE_BYTES = 1048576  # 1 MiB
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

def validate_image_file(image_path: Path) -> None:
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    file_size = image_path.stat().st_size
    if file_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"Image exceeds size cap: {file_size} bytes > {MAX_FILE_SIZE_BYTES} bytes")
    if file_size == 0:
        raise ValueError("Image file is empty (0 bytes)")

    with image_path.open("rb") as f:
        header = f.read(8)
        if header != PNG_MAGIC:
            raise ValueError(f"Invalid PNG magic bytes: {header!r}")

        # Next chunk must be IHDR
        ihdr_length_bytes = f.read(4)
        chunk_type = f.read(4)
        if chunk_type != b"IHDR":
            raise ValueError(f"Expected IHDR chunk, got {chunk_type!r}")

        ihdr_data = f.read(13)
        if len(ihdr_data) < 8:
            raise ValueError("Corrupt IHDR chunk data")

        width, height = struct.unpack(">II", ihdr_data[:8])

    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        raise ValueError(
            f"Invalid dimensions: expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, but found {width}x{height}"
        )

    print(f"Validation successful: {image_path.name} is {width}x{height} PNG, {file_size} bytes (<= {MAX_FILE_SIZE_BYTES} limit)")

if __name__ == "__main__":
    import sys
    test_target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("entry.png")
    validate_image_file(test_target)
