import os
import shutil

def clean_dir(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Removed file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Removed directory: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def copy_dir(src_path, dest_path):
    os.makedirs(dest_path, exist_ok=True)
    for item in os.listdir(src_path):
        s = os.path.join(src_path, item)
        d = os.path.join(dest_path, item)
        try:
            if os.path.isfile(s):
                shutil.copy2(s, d)
                print(f"Copied file: {s} to {d}")
            elif os.path.isdir(s):
                copy_dir(s, d)
        except Exception as e:
            print(f"Failed to copy {s} to {d}. Reason: {e}")

def main():
    public_path = "./public"
    static_path = "./static"

    os.makedirs(public_path, exist_ok=True)
    clean_dir(public_path)

    if os.path.exists(static_path):
        copy_dir(static_path, public_path)
    else:
        print(f"Source path '{static_path}' does not exist. Nothing to copy.")

if __name__ == "__main__":
    main()
