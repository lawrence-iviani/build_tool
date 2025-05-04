import os
import datetime
import glob
from zipfile import ZipFile
import shutil

def find_app_zip_package(build_dir, prefix):
    pattern = os.path.join(build_dir, f"{prefix}-*.zip")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No files found matching: {pattern}")
    return matches[0]

def get_build_version(zip_file):
    base = os.path.basename(zip_file)
    version = base.rsplit('.', 1)[0].rsplit('-', 1)[-1]
    if version == "main":
        return datetime.datetime.now().strftime("%m%d%Y%H%M")
    return version


def extract_zip(zip_path, target_folder):
    with ZipFile(zip_path, 'r') as zipf:
        # Detect common top-level folder
        members = zipf.namelist()
        top_dirs = set(m.split('/')[0] for m in members if '/' in m)
        common_prefix = top_dirs.pop() if len(top_dirs) == 1 else None

        temp_dir = os.path.join(target_folder, '__temp__')
        os.makedirs(temp_dir, exist_ok=True)
        zipf.extractall(temp_dir)

        if common_prefix:
            source_root = os.path.join(temp_dir, common_prefix)
        else:
            source_root = temp_dir

        for item in os.listdir(source_root):
            src = os.path.join(source_root, item)
            dst = os.path.join(target_folder, item)
            shutil.move(src, dst)

        shutil.rmtree(temp_dir)


def extract_zip2(zip_path, target_folder, remove_top_folder=True):
    with ZipFile(zip_path, 'r') as zipf:
        members = zipf.namelist()

        # Detect common top-level folder (e.g., HelloWorldApp-master/)
        top_dirs = set(p.split('/')[0] for p in members if '/' in p)
        common_prefix = top_dirs.pop() if len(top_dirs) == 1 else None

        temp_extract = os.path.join(target_folder, "__temp_extract__")
        os.makedirs(temp_extract, exist_ok=True)
        zipf.extractall(temp_extract)

        if remove_top_folder and common_prefix:
            source = os.path.join(temp_extract, common_prefix)
            for item in os.listdir(source):
                s = os.path.join(source, item)
                d = os.path.join(target_folder, item)
                shutil.move(s, d)
            shutil.rmtree(temp_extract)
        else:
            # Move everything from temp_extract into target_folder
            for item in os.listdir(temp_extract):
                s = os.path.join(temp_extract, item)
                d = os.path.join(target_folder, item)
                shutil.move(s, d)
            shutil.rmtree(temp_extract)


def extract_zip1(zip_path, target_folder, remove_top_folder=None):
    with ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(target_folder)
