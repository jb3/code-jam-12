from nicegui import ui


NAME: str = "PLACEHOLDER NAME"
DESCRIPTION: str = "Placeholder Description"


@ui.page('/')
def home() -> None:
    ui.colors(primary="#20A39E", secondary="#8E7DBE", dark="#393D3F", accent="#E9ECF5")
    pass


ui.run()