from nicegui import ui

import wpm_tester

ui.page("/test/{method}")(wpm_tester.wpm_tester_page)

ui.run()
