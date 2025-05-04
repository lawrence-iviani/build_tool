# Portable Builder
Tool to create a portable app package with configurable components.

# Use default config and ZIP
build-zip

# Use custom config
build-zip --config path/to/custom.yaml

# Skip ZIP step (just prepare the folder)
build-zip --skip-zip