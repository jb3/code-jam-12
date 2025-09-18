# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "uvicorn~=0.35.0",
#     "starlette~=0.48.0",
#     "python-multipart~=0.0.20",
# ]
# ///
"""Run with `uv run image_server.py`"""

from pathlib import Path

from starlette.applications import Starlette
from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.routing import Route

HOST = "localhost"
PORT = 8001  # 8000 is used by Reflex.
UPLOAD_FOLDER = Path("./images")
UPLOAD_FOLDER.mkdir(exist_ok=True)


async def fake_config(_request: Request) -> Response:
    """Return a fake auth token for their client."""
    return Response(f'PF.obj.config.auth_token = "{"deadFA112bad" + "0" * 28}";')


async def upload_image(request: Request) -> Response:
    """Save an uploaded image to disk."""
    form = await request.form()
    file = form.get("source")
    if not isinstance(file, UploadFile):
        return Response(status_code=400, content="No image provided")
    filename = file.filename
    if not filename:
        return Response(status_code=400, content="No filename provided")
    content = await file.read()
    Path(UPLOAD_FOLDER).joinpath(filename).write_bytes(content)
    return Response(status_code=200)


async def search_images(_request: Request) -> HTMLResponse:
    """Return all images (the project only ever uses one search term)."""
    images = UPLOAD_FOLDER.iterdir()
    return HTMLResponse("\n".join(f'<img src="http://{HOST}:{PORT}/image/{img.name}"/>' for img in images))


async def get_image(request: Request) -> Response:
    """Serve an image from disk."""
    filepath = UPLOAD_FOLDER.joinpath(request.path_params["filename"])
    if not filepath.exists():
        return Response(status_code=404)
    return Response(filepath.read_bytes(), media_type="image/png")


routes = [
    Route("/upload", fake_config, methods=["GET"]),
    Route("/json", upload_image, methods=["POST"]),
    Route("/search/images/", search_images, methods=["GET"]),
    Route("/image/{filename}", get_image, methods=["GET"]),
]
app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
