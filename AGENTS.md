# AGENTS.md

## Build/Lint/Test Commands

This is a Python script project with no complex build process.

- Lint: `ruff check .` or `pylint open-unity.py`
- Test: No automated tests currently exist; manual testing via `python open-unity.py` is recommended. The `tests/projects-v1.json` file is a copy from `Unity Hub` (v`3.15.3`) with anonymized data, preserving the structure for testing.

## Code Style Guidelines

- Python code follows PEP8 style guidelines
- Use 4 spaces for indentation
- Import statements should be grouped (standard library, third-party, local)
- Function and variable names use snake_case
- Class names use PascalCase
- Error handling with try/except blocks where appropriate
- Docstrings for all functions
- Type hints should be included for function parameters and return values

## Special Notes

- This is a simple Python command-line utility for macOS
- The script is designed to be easily customizable
- Uses pathlib for path operations
- ANSI color codes for error messages in terminal output
- Supports command-line arguments passed to Unity editor
