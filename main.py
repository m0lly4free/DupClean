import hashlib
from pathlib import Path
import sys

target_dir = Path("test_folder")

def main():
    if not target_dir.exists():
        print("Folder is not found")
        return
    
    by_size = {}    
    for item in target_dir.rglob("*"):
        if item.is_file():
            size = item.stat().st_size
            by_size.setdefault(size, []).append(item)

    for size, group in by_size.items():
        if len(group) > 1:
            print(size, "->", [str(p.relative_to(target_dir)) for p in group])
            

if __name__ == "__main__":
    main()
