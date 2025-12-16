#!/usr/bin/env python3

import os
import sys
import re
import subprocess
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

@dataclass
class UnityProject:
    """Represents a Unity project entry from Unity Hub's data."""
    path: Path
    title: str
    version: str
    last_modified: Optional[datetime]

    @staticmethod
    def from_json(json_data: dict):
        last_modified_timestamp = json_data.get("lastModified")
        last_modified = None
        if last_modified_timestamp:
            # The lastModified timestamp is in milliseconds, so we convert it to seconds.
            last_modified = datetime.fromtimestamp(last_modified_timestamp / 1000)

        return UnityProject(
            path=Path(json_data["path"]),
            title=json_data["title"],
            version=json_data["version"],
            last_modified=last_modified,
        )

def get_recent_projects():
    """Load and return recent Unity projects from Unity Hub."""
    unity_hub_projects_file = Path.home() / "Library/Application Support/UnityHub/projects-v1.json"
    if not unity_hub_projects_file.is_file():
        return []

    with open(unity_hub_projects_file, "r") as file:
        projects_data = json.load(file)

    projects = [
        UnityProject.from_json(data)
        for data in projects_data.get("data", {}).values()
        if is_valid_project_data(data)
    ]

    # Sort projects by last modified date, most recent first.
    projects.sort(key=lambda p: p.last_modified, reverse=True)
    return projects

def is_valid_project_data(data: dict) -> bool:
    """Check if project data contains all required fields."""
    required_fields = ["path", "title", "version", "lastModified"]
    return all(field in data and data.get(field) for field in required_fields)

def main():
    # If a path is provided as the first argument, open that project.
    # Otherwise, show the recent projects list.
    if len(sys.argv) > 1 and (sys.argv[1] == '.' or os.path.isdir(sys.argv[1])):
        project_path = Path(sys.argv[1]).resolve()
        extra_args = sys.argv[2:]
        open_project_from_path(project_path, extra_args)
    else:
        open_recent_project()

def open_recent_project():
    recent_projects = get_recent_projects()
    if not recent_projects:
        exit_with_error("Couldn't find any recent Unity projects.", 1)

    project = show_project_selection(recent_projects)
    if project:
        launch_unity(project.path, project.version)

def show_project_selection(projects):
    try:
        # Use fzf for a better selection UI, if available.
        project_strings = [f"{p.title} ({p.path.parent.name}) - {p.version}" for p in projects]
        fzf_process = subprocess.run(
            ['fzf', '--height', '40%', '--reverse', '--prompt', 'Select a Unity Project> '],
            input='\n'.join(project_strings),
            capture_output=True,
            text=True,
            check=True
        )
        selected_string = fzf_process.stdout.strip()
        if selected_string:
            selected_index = project_strings.index(selected_string)
            return projects[selected_index]
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Fallback to a simple numbered list if fzf is not installed or fails.
        print("Recent projects:")
        for i, project in enumerate(projects[:10]):
            print(f"  {i + 1}: {project.title} ({project.version})")
        try:
            selection = int(input("Select a project (1-10): "))
            if 1 <= selection <= len(projects[:10]):
                return projects[selection - 1]
        except (ValueError, IndexError):
            exit_with_error("Invalid selection.", 1)
    return None

def open_project_from_path(project_path: Path, args: list):
    # Check for the Unity ProjectVersion file in the specified path.
    project_settings_file = project_path / 'ProjectSettings' / 'ProjectVersion.txt'

    if not project_settings_file.is_file():
        exit_with_error(f"Couldn't find ProjectSettings/ProjectVersion.txt in:\n{project_path}", 1)

    unity_version = find_version(project_settings_file)

    if unity_version is None:
        exit_with_error("Couldn't find Unity version in ProjectSettings file", 2)

    launch_unity(project_path, unity_version, args)

def launch_unity(project_path: Path, unity_version: str, extra_args: list = None):
    if extra_args is None:
        extra_args = []

    unity_editor_path = f"/Applications/Unity/Hub/Editor/{unity_version}/Unity.app/Contents/MacOS/Unity"

    if not os.path.isfile(unity_editor_path):
        exit_with_error(f"Couldn't find Unity Editor installation at {unity_editor_path}", 3)

    # Invoke the Unity Editor with the found project path and some global arguments.
    command = [
        unity_editor_path,
        '-projectPath', str(project_path),
        '-cacheServerEnableDownload', 'false',
        '-cacheServerEnableUpload', 'false',
    ]

    # Add any custom arguments passed to this script.
    command.extend(extra_args)

    print(f"Starting Unity {unity_version} with arguments: {' '.join(command[1:])}")

    # Start a new process which continues to live even after the shell is closed.
    subprocess.Popen(command)

def find_version(project_settings_path):
    # Extract the Unity version from the ProjectSettings file.
    version_pattern = re.compile(r'm_EditorVersion: (.*)')
    with open(project_settings_path, 'r') as file:
        for line in file:
            match = version_pattern.match(line)
            if match:
                return match.group(1)
    return None

def exit_with_error(message: str, code: int):
    if sys.stderr.isatty():
        # Use ANSI colors in terminal output, but not when piping to a file.
        red_start = "\033[31m"
        reset = "\033[0m"
        message = f"{red_start}{message}{reset}"
    sys.stderr.write(message + '\n')
    sys.exit(code)

if __name__ == '__main__':
    main()
