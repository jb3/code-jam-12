from nicegui import ui


@ui.page("/controller")
def sub_page():
    ui.label("test")
