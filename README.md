# 📦 Portable Builder v4

**Generic Python packager** that creates a self-contained, ZIP-based portable application with dynamic script generation and optional goodies.

---

## 🧰 Project Structure Example

```
your-project/
├── build_goodies/
│   ├── HelloWorldApp-main.zip           ← App archive (must match prefix)
│   ├── LICENSE.txt                      ← Extra file
│   ├── README.txt                       ← Extra file
│   └── extra_assets/                    ← Extra folder to include
├── build_config.yaml                    ← Configuration file
├── portable_builder_v4/                ← The builder tool
└── main.py                              ← Your actual app (in the archive)
```

---

## ⚙️ Example `build_config.yaml`

```yaml
zip_code_prefix: "HelloWorldApp"

winpython_path: "build_goodies/python-3.12.3.amd64"

fixed_scripts:
  setup_script: null
  run_script: null

entry_points:
  main: "main.py"
  launcher: "main.py"

goodies:
  license_file: "build_goodies/LICENSE.txt"
  extras_folder: "build_goodies/extra_assets"
  readmes:
    - "build_goodies/README.txt"
```

---

## 🔨 Build Commands

```bash
# Install the builder
pip install -e .

# Build with default config
build-zip

# Build with a custom config file
build-zip --config path/to/your_config.yaml

# Skip the zip step (just generate the folder structure)
build-zip --skip-zip
```

---

## 🧪 Example `main.py` (inside your zip)

```python
# main.py
print("Hello from your portable app!")
```

To test:
```bash
zip HelloWorldApp-main.zip main.py
```

Then place the zip into `build_goodies/`.

---

## 🗂️ Example Output Folder

```
HelloWorldApp_05042025/
├── app/
│   └── main.py
├── extras/
│   └── image.png
├── LICENSE.txt
├── README.txt
├── python/                          ← WinPython
├── setup.bat                        ← Auto-generated
└── run.bat                          ← Auto-generated
```

---

## ⚡ Auto-generated `setup.bat` Summary

```bat
SET WINPYTHON_PATH=%~dp0\python-3.12.3.amd64
SET VENV_DIR=%~dp0venv

IF NOT EXIST "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
)

CALL "%VENV_DIR%\Scripts\activate.bat"
pip install -r "%~dp0\app\requirements.txt"

cd "%~dp0app"
python main.py
```

---

## 🧪 Alternate Usage: Run Without Installing the Builder

If you prefer **not to install** the builder via `pip install -e .`, you can run it directly from the environment:

```bash
# From the project root
python -m build_tool.cli
```

With options:

```bash
# Use a custom config
python -m build_tool.cli --config path/to/your_config.yaml

# Skip the ZIP packaging
python -m build_tool.cli --skip-zip
```

---

## 🧪 Using a Virtual Environment (Recommended)

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m build_tool.cli
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m build_tool.cli
```

This avoids cluttering your global Python environment.

---
