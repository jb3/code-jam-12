from pathlib import Path

from nicegui import app, ui

from color_style import ColorStyle
from config import INPUT_METHODS, PROJECT_DESCRIPTION, PROJECT_NAME

COLOR_STYLE = ColorStyle()

media = Path("./static")
app.add_media_files("/media", media)


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
        padding: 30px;
    }
    .input-box {
        height: 300px;
        width: 300px;
        padding: 20px;
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

    ui.query("body").style(f"background-color: {COLOR_STYLE.primary_bg}")

    with (
        ui.header(fixed=False)
        .style(f"background-color: {COLOR_STYLE.secondary_bg}")
        .classes("items-center thick-header"),
        ui.column(align_items="center").style("gap: 0px;"),
    ):
        ui.label(PROJECT_NAME).style(f"color: {COLOR_STYLE.primary}").classes("site-title")
        ui.label(PROJECT_DESCRIPTION).style(f"color: {COLOR_STYLE.contrast}").classes("site-subtitle")

    with ui.element("div").classes("page-div"):
        ui.label("CHOOSE YOUR INPUT METHOD").style(f"color: {COLOR_STYLE.secondary}").classes("heading")
        ui.separator().style("background-color: #313131;")
        with ui.element("div").classes("button-parent"):
            for input in INPUT_METHODS:
                (
                    ui.button(
                        text=input["name"],
                        color=COLOR_STYLE.secondary_bg,
                        on_click=lambda _, path=f"/test/{input['path']}": ui.navigate.to(path),
                    )
                    .style(f"color: {COLOR_STYLE.contrast}")
                    .props("rounded")
                    .classes(f"input-box hover:!bg-[{COLOR_STYLE.primary}] transition-colors duration-300")
                )
