from nicegui import ui

NAME: str = "PLACEHOLDER NAME"
DESCRIPTION: str = "Placeholder Description"


@ui.page("/")
def input_method_page() -> None:
    """User interface frame for input method pages.

    Args:
        input_method: The input method to be generated on the page.

    """
    ui.add_css("""
        .header {
            height: 8vh;
            align-items: center;
        }
        .h1 {
            font-family: Arial;
            font-size: 35px;
            font-weight: bold;
        }
    """)

    with ui.header(wrap=False).style("background-color: #20A39E").classes("items-center justify-between header"):
        with ui.card().props("flat"):  # small logo placeholder
            pass
        ui.label(NAME).classes("h1")
        ui.button(on_click=lambda: right_drawer.toggle(), icon="menu").props("flat color=white")

    # Sidebar
    with (
        ui.right_drawer(
            value=False,
            fixed=False,
        )
        .style("background-color: #ebf1fa")
        .props("overlay")
        .classes("p-0") as right_drawer,
        ui.element("q-scroll-area").classes("fit"),
    ):
        with ui.list().classes("fit"), ui.item().props("clickable"), ui.item_section():
            ui.label("HOME")
        with ui.list().classes("fit"):
            ui.separator()
        with ui.list().classes("fit"):
            with ui.item().props("clickable"), ui.item_section():
                ui.label("RECORD PLAYER")
            with ui.item().props("clickable"), ui.item_section():
                ui.label("COLOR PICKER")


ui.run()
