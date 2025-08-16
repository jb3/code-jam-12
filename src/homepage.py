from nicegui import ui

from config import INPUT_METHODS, PROJECT_DESCRIPTION, PROJECT_NAME


def home() -> None:
    """Render the home page."""
    ui.add_css("""
    .thick-header {
        height: 350px;
        justify-content: center;
    }
    .site-title {
        font-family: Arial;
        font-weight: bold;
        text-align: center;
        font-size: 70px;
    }
    .site-subtitle {
        font-family: Arial;
        text-align: center;
        font-size: 20px;
    }
    .heading {
        font-family: Arial;
        font-size: 25px;
        font-weight: bold;
        text-align: center;
        color: #393D3F;
        padding: 30px;
    }
    .input-box {
        height: 300px;
        width: 300px;
        padding: 20px;
        text-color: 393D3F;
    }
    .input-grid {
        justify-content: center;
    }
    .page-div {
        position: absolute;
        width: 90vw;
        left: 50%;
        transform: translate(-50%);
    }
    .button-parent {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: center;
        padding-top: 30px;
        padding-bottom: 60px;
    }
    """)

    ui.query("body").style("background-color: #E9ECF5")

    with (
        ui.header(fixed=False).style("background-color: #20A39E").classes("items-center thick-header"),
        ui.column(align_items="center").style("gap: 0px;"),
    ):
        ui.label(PROJECT_NAME).classes("site-title")
        ui.label(PROJECT_DESCRIPTION).classes("site-subtitle")

    with ui.element("div").classes("page-div"):
        ui.label("CHOOSE YOUR INPUT METHOD").classes("heading")
        ui.separator()
        with ui.element("div").classes("button-parent"):
            for input in INPUT_METHODS:
                ui.button(
                    text=input["name"],
                    color="#F9F9F9",
                    on_click=lambda _, path=f"/test/{input['path']}": ui.navigate.to(path),
                ).classes("input-box")
