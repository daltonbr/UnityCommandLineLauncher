# Proposal: New CLI Behavior for `open-unity`

This document outlines the proposed changes to the command-line interface for the `open-unity` script to incorporate the new feature of opening recent projects.

## Guiding Principle

The primary goal is to make the most common workflow—opening a recent project—as fast and intuitive as possible, while retaining the original functionality for opening a project from the current directory.

## Proposed CLI Design

The script will operate in one of two modes based on the arguments provided.

### 1. Default Mode: Open Recent Project (No Arguments)

When the script is executed without any arguments, it will be the primary and default behavior.

```bash
open-unity
```

**Action:**

1. The script will read the `projects-v1.json` file from Unity Hub's application support directory.
2. It will parse the list of projects, sort them by the `lastModified` date (most recent first).
3. It will display an interactive selector to the user:
    - **If `fzf` is installed:** Use `fzf` to show a fuzzy-findable list of recent projects. This provides the best user experience.
    - **If `fzf` is not installed:** Fall back to a simple, numbered list of the top 10 recent projects, prompting the user to enter a number.
4. Once a project is selected, the script will launch the corresponding Unity Editor version with the selected project path.

### 2. Legacy Mode: Open Project from Current Directory (With Arguments)

When the script is executed with a valid directory path as its first argument, it will trigger the legacy behavior. This path is mandatory to enter this mode. Any additional arguments will be forwarded to the Unity Editor.

```bash
# Open project in the current directory
open-unity .

# Open project in a specific directory
open-unity /path/to/my/project

# Open project in the current directory with extra arguments for Unity
open-unity . -force-metal -batchmode
```

**Action:**

1. The script will check if the first argument is a valid directory path (e.g., `.` or `/path/to/project`).
2. If it is a valid path, it will look for a `ProjectSettings/ProjectVersion.txt` file directly within that path. The script will no longer search parent or common subdirectories.
3. If a project is found, it will launch the corresponding Unity Editor.
4. All subsequent arguments (`-force-metal`, `-batchmode`, etc.) are forwarded directly to the Unity Editor executable.
5. If no arguments are provided, or if the first argument is not a valid directory path (e.g., it's a flag like `-h`), the script will default to showing the recent projects list.
This design makes opening recent projects the default, most accessible feature, while a simple argument like `.` or any Unity flag cleanly switches to the context-sensitive local project opening.
