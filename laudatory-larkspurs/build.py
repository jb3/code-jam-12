"""The build script for the website."""

import argparse
import http.server
import pathlib
import shutil
import socketserver

_this_dir = pathlib.Path(__file__).parent.resolve()

# Project directories
BUILD_DIR = _this_dir / "build"
PUBLIC_DIR = _this_dir / "public"
SRC_DIR = _this_dir / "src"


def _zip_dir(src: pathlib.Path, dest: pathlib.Path) -> None:
    """Create a zip file from a directory and places it in `dest`."""
    shutil.make_archive(str(dest), "zip", str(src))


class _DevHandler(http.server.SimpleHTTPRequestHandler):
    """Allows for serving the website locally for development."""

    def __init__(self, request, client_address, server) -> None:  # noqa: ANN001
        super().__init__(request, client_address, server, directory=BUILD_DIR)


def main() -> None:
    """Define the build entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-clean", action="store_false", dest="clean", default=True)
    parser.add_argument("--serve", action="store_true", default=False)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if not BUILD_DIR.exists():  # FileNotFoundError if this isn't here
        BUILD_DIR.mkdir(exist_ok=True)

    elif args.clean:
        shutil.rmtree(BUILD_DIR)
        BUILD_DIR.mkdir(exist_ok=True)

    _zip_dir(SRC_DIR, BUILD_DIR / "src")
    shutil.copytree(PUBLIC_DIR, BUILD_DIR, dirs_exist_ok=True)

    if args.serve:
        print(f"Serving on http://localhost:{args.port}")
        httpd = socketserver.TCPServer(("", args.port), _DevHandler)
        httpd.serve_forever()
    else:
        print("Add --serve to start")


if __name__ == "__main__":
    main()
