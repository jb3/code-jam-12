from nicegui import ui


NAME: str = "PLACEHOLDER NAME"
DESCRIPTION: str = "Placeholder Description"


@ui.page('/')
def home() -> None:
    pass


ui.run()