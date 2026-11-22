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

def deploy_broadsheet() -> None:
    source_path = Path(__file__).parent / "entry.png"
    if not source_path.exists():
        print(f"Error: Source image not found at {source_path}", file=sys.stderr)
        sys.exit(1)

    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    output_dir = Path(output_dir_env)
    output_dir.mkdir(parents=True, exist_ok=True)

    dest_path = output_dir / "entry.png"
    shutil.copy2(source_path, dest_path)
    print(f"Successfully deployed broadsheet image to {dest_path.resolve()} ({dest_path.stat().st_size} bytes)")

if __name__ == "__main__":
    deploy_broadsheet()
