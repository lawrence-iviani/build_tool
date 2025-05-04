import argparse
from build_tool.builder import build_all

def main():
    parser = argparse.ArgumentParser(description="Build a portable zip-based Python application.")
    parser.add_argument('--config', type=str, help='Path to YAML config file', default=None)
    parser.add_argument('--skip-zip', action='store_true', help='Skip zip packaging step')
    args = parser.parse_args()

    build_all(config_path=args.config, skip_zip=args.skip_zip)


if __name__ == "__main__":
    main()