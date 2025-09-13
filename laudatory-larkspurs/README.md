# Good Image Terminal

<p align="center">
<a href="https://github.com/Miras3210/codejam-laudatory-larkspurs/actions/workflows/lint.yaml"><img src="https://github.com/Miras3210/codejam-laudatory-larkspurs/actions/workflows/lint.yaml/badge.svg" alt="Lint"></a>
<a href="https://github.com/Miras3210/codejam-laudatory-larkspurs/actions/workflows/build.yaml"><img src="https://github.com/Miras3210/codejam-laudatory-larkspurs/actions/workflows/build.yaml/badge.svg" alt="Build"></a>
<a href="https://github.com/Miras3210/codejam-laudatory-larkspurs/actions/workflows/deploy.yaml"><img src="https://github.com/Miras3210/codejam-laudatory-larkspurs/actions/workflows/deploy.yaml/badge.svg" alt="Deploy"></a>
<a href="https://github.com/Miras3210/codejam-laudatory-larkspurs/actions/workflows/pages/pages-build-deployment"><img src="https://github.com/Miras3210/codejam-laudatory-larkspurs/actions/workflows/pages/pages-build-deployment/badge.svg" alt="Deploy"></a>
</p>

<p align="center">
    <img src="docs/_media/icon.svg" width="192" height="192" alt="Logo" style="max-width: 192px; max-height: 192px;" />
</p>

<p align="center">
    <em>An image editor. In the terminal. In the browser.</em>
</p>

This project is a web-based image editing tool that runs entirely in the browser through a terminal. It uses Pyodide to enable Python-based image processing without the need for a backend server. All while letting JavaScript sit back, relax, and just load the page.

The tool allows users to upload images and apply edits through various commands, all within a user-friendly interface.

The inherently visual task of image editing performed entirely through programmatic terminal commands makes Good Image Terminal the "Wrong tool for the job." Despite this dissonance, we've made GIT comfortable and responsive.

## Project Structure

```text
codejam-laudatory-larkspurs/
├─ build.py                  # Build + serve script (Pyodide bundling)
├─ Dockerfile                # Docker configuration
├─ pyproject.toml            # Project & dependency metadata
├─ uv.lock                   # Locked dependency versions
├─ README.md / CONTRIBUTING.md
├─ LICENSE
├─ .pre-commit-config.yaml   # Lint & format hooks
├─ .github/workflows/
│   ├─ build.yaml            # CI build pipeline
│   ├─ deploy.yaml           # CI deployment pipeline
│   └─ lint.yaml             # CI lint pipeline
├─ docs/                     # Documentation files
├─ public/                   # Static assets
│   ├─ index.html
│   ├─ favicon.* / icons
│   ├─ site.webmanifest
│   └─ templates/
│       └─ app_template.html
└─ src/                      # Application source (runs in Pyodide)
    ├─ main.py               # Entry point
    ├─ terminal.py           # Terminal UI
    ├─ image.py              # Image model
    ├─ commands/             # Individual terminal commands
    │   ├─ background.py
    │   ├─ base_command.py
    │   ├─ draw_circle.py
    │   ├─ draw_line.py
    │   ├─ draw_pixel.py
    │   ├─ draw_polygon.py
    │   ├─ draw_rectangle.py
    │   ├─ foreground.py
    │   ├─ help.py
    │   ├─ image_info.py
    │   ├─ load_image.py
    │   ├─ ls.py
    │   ├─ ping.py
    │   ├─ save_image.py
    │   ├─ terminal_background.py
    │   ├─ undo.py
    │   └─ __init__.py
    ├─ gui/                   # Lightweight GUI abstraction
    │   ├─ element.py
    │   ├─ layout.py
    │   ├─ components/
    │   │   ├─ description.py
    │   │   ├─ drag_drop_handler.py
    │   │   ├─ file_upload_handler.py
    │   │   ├─ image_display_manager.py
    │   │   ├─ image_preview.py
    │   │   ├─ separator.py
    │   │   ├─ terminal_gui.py
    │   │   ├─ terminal_input.py
    │   │   ├─ terminal_io.py
    │   │   └─ __init__.py
    │   └─ __init__.py
    ├─ images/
    │   └─ default.png
    └─ utils/
        ├─ color.py
        └─ __init__.py
```

## Setup

1. First we set up our python enviroment

```shell
python -m venv .venv
```

2. Entering it

```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```

3. Installing development dependecies

```shell
pip install --group dev
```

_If it gives errors try:_

```shell
python -m pip install --upgrade pip
```

4. If we want to exit our enviroment we do

```shell
deactivate
```

## Running the project

To build the project, run

```shell
python build.py --serve --port 8000
```

This will serve the project on `http://localhost:8000` after building it to `build/`. If you make changes to your code, run `build.py` again to rebuild the project.

### Running with Docker

You can run the app without a local Python setup using the provided `Dockerfile`.

Build the image:

```shell
docker build -t good-image-terminal:latest .
```

Run (default port `8000`):

```shell
docker run --rm --name good-image-terminal -e PORT=8000 -p 8000:8000 good-image-terminal:latest
```

Custom port:

```shell
docker run --rm --name good-image-terminal -e PORT=9000 -p 9000:9000 good-image-terminal:latest
```

The container runs `python build.py --serve --port $PORT` on startup:

- Builds fresh each run (output in container at `/app/build`).
- Serves the site at `http://localhost:<PORT>`.

Faster rebuilds during iteration:

```shell
docker build -t good-image-terminal:latest .  # after changing code
```

## Contributors

[![Contributors](https://contrib.rocks/image?repo=Miras3210/codejam-laudatory-larkspurs)](https://github.com/Miras3210/codejam-laudatory-larkspurs/graphs/contributors)
