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
            by_hash = {}
            for path in group:
                by_hash.setdefault(file_hash(path), []).append(path)

            for digest, dup_group in by_hash.items():
                if len(dup_group) > 1:
                    print("Duplicates: ", [str(p.relative_to(target_dir)) for p in dup_group])

def file_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024*1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()
    




if __name__ == "__main__":
    main()
