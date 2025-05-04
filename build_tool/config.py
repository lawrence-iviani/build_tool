import os
import yaml
from build_tool.utils import find_app_zip_package, get_build_version

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_CONFIG_PATH = os.path.join(ROOT_DIR, "build_config.yaml")
DEFAULT_DESTINATION_PYTHON_FOLDER = "python"

class BuildConfig:
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        with open(config_path, "r", encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)
        self.root_dir = self.cfg.get("build_root_path", "./build") # root_dir
        self.app_name = self.cfg["app_name"]
        self.zip_app_path = os.path.join(self.root_dir, self.cfg["zip_app_path"])

        self.app_zip = find_app_zip_package(self.zip_app_path, self.app_name)
        self.build_version = get_build_version(self.app_zip)
        self.portable_package = os.path.join(self.root_dir, f"{self.app_name}_{self.build_version}")

        self.python_folder_source = os.path.join(
            self.root_dir,
            self.cfg.get("python_path", "python/python-3.12.3.amd64")
        )
        self.python_folder_destination = self.cfg.get("python_path_destination", DEFAULT_DESTINATION_PYTHON_FOLDER)

        self.entry_points = self.cfg.get("entry_points", {})
        self.goodies = self._resolve_goodies()

    def _resolve_goodies(self):
        raw = self.cfg.get("goodies", {})
        result = {}
        for key, value in raw.items():
            if isinstance(value, list):
                result[key] = [os.path.join(self.root_dir, v) for v in value]
            elif value:
                result[key] = os.path.join(self.root_dir, value)
        return result
