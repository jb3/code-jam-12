from nicegui import ui


NAME: str = "PLACEHOLDER NAME"
DESCRIPTION: str = "Placeholder Description"


@ui.page('/')
def home() -> None:
    ui.query('body').style('background-color: #E9ECF5;')


ui.run()