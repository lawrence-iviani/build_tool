import os
import yaml
from build_tool.utils import find_app_zip_package, get_build_version

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_CONFIG_PATH = os.path.join(ROOT_DIR, "build_config.yaml")
DEFAULT_DESTINATION_PYTHON_FOLDER = "python"

class BuildConfig:
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = os.path.abspath(config_path)
        self.config_dir = os.path.dirname(self.config_path)
        with open(config_path, "r", encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)
        self.root_dir = self._resolve_path(self.cfg.get("build_root_path", "./build"))
        self.app_name = self.cfg.get("app_name") or self.cfg.get("zip_code_prefix")
        if not self.app_name:
            raise KeyError("Config must define either 'app_name' or 'zip_code_prefix'.")
        zip_app_path_value = self.cfg.get("zip_app_path", "build_goodies")
        self.zip_app_path = self._resolve_path(zip_app_path_value)

        self.app_zip = find_app_zip_package(self.zip_app_path, self.app_name)
        self.build_version = get_build_version(self.app_zip)
        self.portable_package = os.path.join(self.root_dir, f"{self.app_name}_{self.build_version}")

        python_source_value = self.cfg.get("python_path") or self.cfg.get("winpython_path") or "python/python-3.12.3.amd64"
        self.python_folder_source = self._resolve_path(python_source_value)
        self.python_folder_destination = self.cfg.get("python_path_destination", DEFAULT_DESTINATION_PYTHON_FOLDER)

        self.entry_points = self.cfg.get("entry_points", {})
        self.fixed_scripts = self._resolve_fixed_scripts()
        self.hooks = self._resolve_hooks()
        self.goodies = self._resolve_goodies()

    def _resolve_goodies(self):
        raw = self.cfg.get("goodies", {})
        result = {}
        for key, value in raw.items():
            if isinstance(value, list):
                result[key] = [self._resolve_path(v) for v in value]
            elif value:
                result[key] = self._resolve_path(value)
        return result

    def _resolve_fixed_scripts(self):
        raw = self.cfg.get("fixed_scripts", {}) or {}
        return {
            "setup_script": self._resolve_optional_path(raw.get("setup_script")),
            "run_script": self._resolve_optional_path(raw.get("run_script")),
        }

    def _resolve_hooks(self):
        raw_hooks = self.cfg.get("hooks", {}) or {}
        legacy_setup = self.cfg.get("setup_steps", []) or []
        legacy_run = self.cfg.get("run_steps", []) or []
        return {
            "prebuild": list(raw_hooks.get("prebuild", []) or []),
            "setup": list(raw_hooks.get("setup", legacy_setup) or []),
            "run": list(raw_hooks.get("run", legacy_run) or []),
        }

    def _resolve_optional_path(self, value):
        if not value:
            return None
        return self._resolve_path(value)

    def _resolve_path(self, value):
        if not value:
            return value
        if os.path.isabs(value):
            return os.path.abspath(value)
        return os.path.abspath(os.path.join(self.config_dir, value))
