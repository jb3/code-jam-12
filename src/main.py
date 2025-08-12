from nicegui import ui

from homepage import home
from wpm_tester import wpm_tester_page

###from rpg_text_input import rpg_text_input_page so it doesnt think it's code


ui.page("/")(home)
ui.page("/test/{method}")(wpm_tester_page)

# http://localhost:8080/test/audio_input


ui.run()
