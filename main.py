import hashlib
from pathlib import Path
import sys
from tkinter import Tk
from tkinter import filedialog

DRY_RUN = False

root = Tk()
root.withdraw()
tar_dir = filedialog.askdirectory(title="Select folder")
if not tar_dir:
    print("Folder not selected")
    sys.exit()

print("Folder selected: ", tar_dir)
target_dir = Path(tar_dir)
quarantine = target_dir / "duplicates"

def main():
    if not target_dir.exists():
        print("Folder is not found")
        return

    moved = 0
    
    by_size = {} 
    for item in target_dir.rglob("*"):
        if item.is_relative_to(quarantine):
            continue
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
                    for dup in dup_group[1:]:
                        dest = quarantine / dup.relative_to(target_dir)
                        if DRY_RUN:
                            print("Would move: ", dup.relative_to(target_dir))
                        else:
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            dup.rename(dest)
                        moved += 1

    if DRY_RUN:
        print("Dry run: nothing was moved. Would move: ", moved, " files")
    else:
        print("Moved: ", moved, " files to ", quarantine)

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
