# Installation Guide

Choose one of the methods below to get started.

## Source code

### 1. Fork the repository

```bash
git clone https://github.com/Miras3210/codejam-laudatory-larkspurs.git && cd codejam-laudatory-larkspurs
```

### 2. Setup and activate a Python environment

```bash
python -m venv .venv
```

Linux / macOS

```bash
source .venv/bin/activate
```

Windows, cmd.exe

```
.venv\Scripts\activate.bat
```

Windows, PowerShell

```
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install .
```

> [!NOTE]
> If you encounter issues, try upgrading pip.

```bash
pip install --upgrade pip
```

### 4. Build and serve the project

```bash
python build.py --serve --port 8000
```

Open [http://localhost:8000](http://localhost:8000).

## Dev Install

```bash
pip install --upgrade pip
pip install --group dev
```

## Docker

You can run the app without a local Python setup using the provided `Dockerfile`.

### 1. Build the image

```bash
docker build -t good-image-terminal:latest .
```

### 2. Run on default port `8000`

```bash
docker run --rm --name good-image-terminal -e PORT=8000 -p 8000:8000 good-image-terminal:latest
```

Then visit [http://localhost:8000](http://localhost:8000).
