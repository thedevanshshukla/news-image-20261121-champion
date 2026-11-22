"""Nov 21, 2026 World News Broadsheet Deployer.

Sum up 21 November 2026's world news in one image:
- Iranian strikes on Bahrain bases
- Magnitude 6.8 earthquake in southern Peru
- COP31 climate negotiations dragging into overtime
- Capture of cartel leader Fausto Isidro Meza Flores ('El Chapo Isidro')
"""

import os
import shutil
import sys
from pathlib import Path
from broadsheet_validator import validate_image_file

def deploy_broadsheet() -> None:
    source_path = Path(__file__).parent / "entry.png"
    if not source_path.exists():
        print(f"Error: Source image not found at {source_path}", file=sys.stderr)
        sys.exit(1)

    # 1. Pre-deployment validation of source image
    print("Performing pre-deployment validation on source broadsheet...")
    try:
        validate_image_file(source_path)
    except Exception as exc:
        print(f"Validation failed for source image: {exc}", file=sys.stderr)
        sys.exit(1)

    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    output_dir = Path(output_dir_env)
    output_dir.mkdir(parents=True, exist_ok=True)

    dest_path = output_dir / "entry.png"
    shutil.copy2(source_path, dest_path)

    # 2. Post-deployment integrity check on destination artifact
    print("Performing post-deployment integrity verification...")
    try:
        validate_image_file(dest_path)
    except Exception as exc:
        print(f"Post-deployment verification failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Successfully deployed and verified broadsheet image at {dest_path.resolve()} ({dest_path.stat().st_size} bytes)")

if __name__ == "__main__":
    deploy_broadsheet()
