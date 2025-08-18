from nicegui import ui

from homepage import home
from wpm_tester import wpm_tester_page

ui.page("/")(home)
ui.page("/test/{method}")(wpm_tester_page)

ui.run(title="Dynamic Typing")
