import os
import shutil
from jinja2 import Environment, FileSystemLoader
from build_tool.config import BuildConfig, ROOT_DIR, DEFAULT_CONFIG_PATH
from build_tool.utils import extract_zip

def create_structure(portable_package):
    if os.path.exists(portable_package):
        shutil.rmtree(portable_package)
    os.makedirs(os.path.join(portable_package, 'app'), exist_ok=True)

def extract_and_copy_all(cfg):
    extract_zip(cfg.app_zip, os.path.join(cfg.portable_package, 'app'))
    shutil.copytree(cfg.python_folder_source, os.path.join(cfg.portable_package, cfg.python_folder_destination))

    if "license_file" in cfg.goodies:
        shutil.copy(cfg.goodies["license_file"], cfg.portable_package)

    if "extras_folder" in cfg.goodies:
        shutil.copytree(cfg.goodies["extras_folder"], os.path.join(cfg.portable_package, 'extras'))

    for readme in cfg.goodies.get("readmes", []):
        shutil.copy(readme, cfg.portable_package)

def render_scripts(cfg):
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT_DIR, "build_tool", "templates")))
    context = {
        "python_dir": os.path.basename(cfg.python_folder_destination),
        "main_entry": cfg.entry_points.get("main", "main.py"),
    }

    for script_name in ["setup.bat", "run.bat"]:
        template = env.get_template(f"{script_name}.j2")
        with open(os.path.join(cfg.portable_package, script_name), "w", encoding="utf-8") as f:
            f.write(template.render(context))

def zip_package(cfg):
    archive_name = os.path.join(os.path.dirname(cfg.portable_package), f'{cfg.app_name}_{cfg.build_version}')
    shutil.make_archive(archive_name, 'zip', cfg.portable_package)
    print(f"ZIP created: {archive_name}.zip")

def build_all(config_path=DEFAULT_CONFIG_PATH, skip_zip=False):
    cfg = BuildConfig(config_path=config_path)
    print(f"Building portable package at: {cfg.portable_package}")
    create_structure(cfg.portable_package)
    extract_and_copy_all(cfg)
    render_scripts(cfg)
    if not skip_zip:
        zip_package(cfg)
