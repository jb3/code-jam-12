from nicegui import ui

import audio_style_input as _audio  # noqa: F401
import homepage

# We probably want to figure out a more clean way to do this without the noqa.
import rpg_text_input as _  # noqa: F401 Importing creates the subpage.
import wpm_tester

ui.label("Hello NiceGUI!")
ui.page("/test/{method}")(wpm_tester.wpm_tester_page)


ui.page("/")(homepage.home)


ui.run()

