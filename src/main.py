from pathlib import Path

from nicegui import app, ui

from homepage import home
from wpm_tester import wpm_tester_page

media = Path("./static")
app.add_media_files("/media", media)

ui.page("/")(home)
ui.page("/test/{method}")(wpm_tester_page)

ui.run(title="Dynamic Typing")
