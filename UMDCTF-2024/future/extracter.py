import hashlib
import py7zr
import shutil

#
#   According to the builder-script there's a 1/2000 chance that possible_flag_* contain the flag 
#   So all we have to do is to extract files 
#   Password is MD5(<filename>)
# 
#   Set up folder "extracted_files" and "old"
#

def extract_file(file_path, password, extract_path="extracted_files"):
    try:
        with py7zr.SevenZipFile(file_path, mode='r', password=password) as z:
            z.extractall(path=extract_path)
        return True
    except Exception as e:
        print(f"Failed to extract {file_path} with password {password}: {e}")
        return False
    

#
#   Open textfiles and seach for "UMDCTF{"
#

def find_flag_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            if "UMDCTF{" in contents:
                print(f"Flag found in {file_path}: {contents}")
                exit()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

#
#   When a file has been extracted move it to folder old 
#

def move_file_to_old(file_path, old_dir="old"):
    os.makedirs(old_dir, exist_ok=True)
    shutil.move(file_path, os.path.join(old_dir, os.path.basename(file_path)))

#
#   Process all files in a directory 
#   Extract if .z7 or search for flag if .txt
#

def process_directory(directory):
    while True:
        something_extracted = False
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                if file.endswith('.7z'):
                    # Generate password from file name
                    password = hashlib.md5(file.encode()).hexdigest()
                    if extract_file(file_path, password, root):
                        move_file_to_old(file_path)
                        something_extracted = True
                elif file.endswith('.txt'):
                    find_flag_in_file(file_path)
        if not something_extracted:
            break  

def main():
    root_dir = "extracted_files" 
    process_directory(root_dir)

if __name__ == "__main__":
    main()

