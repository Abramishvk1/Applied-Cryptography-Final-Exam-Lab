import hashlib
import json
import os
import shutil

def get_desktop_task5_folder():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    task5_folder = os.path.join(desktop, "task5")
    os.makedirs(task5_folder, exist_ok=True)
    return task5_folder

def compute_hashes(filepath):
    hashes = {
        'SHA256': hashlib.sha256(),
        'SHA1': hashlib.sha1(),
        'MD5': hashlib.md5()
    }
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            for h in hashes.values():
                h.update(chunk)
    return {name: h.hexdigest() for name, h in hashes.items()}

def save_hashes_to_json(hashes, json_path):
    with open(json_path, 'w') as f:
        json.dump(hashes, f, indent=4)
    print(f"[+] Hashes saved to {json_path}")

def load_hashes_from_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def simulate_tampering(filepath):
    with open(filepath, 'a') as f:
        f.write("\n[!] Tampered with malicious data.")
    print(f"[!] Simulated tampering in: {filepath}")

def check_integrity(original_hashes, new_hashes):
    print("\n[*] Checking file integrity...")
    modified = False
    for algo in original_hashes:
        if original_hashes[algo] != new_hashes[algo]:
            print(f"[!] {algo} hash mismatch detected!")
            modified = True
        else:
            print(f"[+] {algo} hash matches.")
    if modified:
        print("\n[!!!] WARNING: File has been MODIFIED!")
    else:
        print("\n[+] File integrity check PASSED.")

def main():
    folder = get_desktop_task5_folder()
    original_path = os.path.join(folder, "original.txt")
    tampered_path = os.path.join(folder, "tampered.txt")
    hash_file_path = os.path.join(folder, "hashes.json")

    with open(original_path, 'w') as f:
        f.write("This is the original secure content.\n")
    print(f"[+] Created file: {original_path}")

    original_hashes = compute_hashes(original_path)
    save_hashes_to_json(original_hashes, hash_file_path)

    shutil.copyfile(original_path, tampered_path)
    simulate_tampering(tampered_path)

    tampered_hashes = compute_hashes(tampered_path)
    saved_hashes = load_hashes_from_json(hash_file_path)
    check_integrity(saved_hashes, tampered_hashes)

if __name__ == "__main__":
    main()
