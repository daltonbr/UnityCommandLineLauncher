# Unity Command Line Launcher

A lightweight command-line script designed to speed up opening Unity projects. With a single command, this script launches a Unity project directly from within the project's directory tree, bypassing the Unity Hub for enhanced speed and convenience. It's tailored for developers who prefer the efficiency of a terminal-based approach.

The script now also supports opening recent projects from Unity Hub, with a fuzzy finder for quick access.

## Support

The script currently only supports macOS.

## Setup

1. **Install Python 3:** The script is written in Python.
2. **Install `fzf` (Recommended):** For a better project selection UI, install `fzf`.

    ```bash
    brew install fzf
    ```

    `fzf` is a powerful command-line fuzzy finder. Learn more at [github.com/junegunn/fzf](https://github.com/junegunn/fzf).

3. **Place the script:** Put the `open-unity.py` script in a memorable location, like `~/bin/`.

4. **Create an alias:** Make the script easily accessible from your terminal by adding an alias to your shell's configuration file (e.g., `.zshrc` or `.bash_profile`).

    ```zsh
    # Add this line to your ~/.zshrc
    alias unity="~/bin/open-unity.py"
    ```

    Alternatively, you can add it by running this command:

    ```zsh
    echo 'alias unity="~/bin/open-unity.py"' >> ~/.zshrc
    ```

    Another option is to rename the script to `unity` and move it to a directory in your `PATH`.

## Customization

The script is intended to be used in source form so that it can be easily customized. For example, you can update the directories searched for the Unity project or change the default command-line arguments passed to Unity.

## Design

For more details on the design of the command-line interface, see the [CLI Design Document](docs/cli-design.md).

## Usage

The script has two main modes of operation:

### 1. Open Recent Projects (Default)

When run without any arguments, the script displays a list of your recent Unity projects, fetched from the Unity Hub's data.

```zsh
unity
```

This will open an interactive selector. If you have `fzf` (a command-line fuzzy finder) installed, you'll get a powerful search interface. Otherwise, it will present a simple numbered list of the 10 most recent projects.

You can also explicitly trigger this mode with the `--recent` flag:

```zsh
unity --recent
```

### 2. Open Project from Current Directory

To open a Unity project located in the current directory (or a parent directory), pass any argument to the script. This maintains the original behavior of the tool.

A common use case is to pass arguments directly to the Unity Editor:

```zsh
unity -force-metal
```

This is useful when you are already in a project's directory and want to open it with specific command-line flags.

Find the available Unity editor command line arguments in the [official documentation](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html).
