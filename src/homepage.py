from nicegui import ui

NAME: str = "PLACEHOLDER NAME"
DESCRIPTION: str = "Placeholder Description"


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
        left: 50%;
        transform: translate(-50%);
        top: 30px;
    }
    """)

    ui.query("body").style("background-color: #E9ECF5")

    with (
        ui.header().style("background-color: #20A39E").classes("items-center thick-header"),
        ui.column(align_items="center").style("gap: 0px;"),
    ):
        ui.label(NAME).classes("site-title")
        ui.label(DESCRIPTION).classes("site-subtitle")

    with ui.element("div").classes("page-div"), ui.column(align_items="center").style("gap: 30px;"):
        ui.label("CHOOSE YOUR INPUT METHOD").classes("heading")
        ui.separator()
        with ui.row(align_items="center", wrap=False).style("gap: 50px;"):
            for i in range(4):
                ui.button(text=f"Input method {i + 1}", color="#F9F9F9").classes("input-box")
