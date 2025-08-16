from nicegui import ui

from config import COLOR_STYLE, INPUT_METHODS, PROJECT_NAME


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

    ui.query("body").style(f"background-color: {COLOR_STYLE['primary_bg']}")

    with (
        ui.header(wrap=False)
        .style(f"background-color: {COLOR_STYLE['secondary_bg']}")
        .classes("items-center justify-between header")
    ):
        with ui.card().props("flat"):  # small logo placeholder
            pass
        ui.label(PROJECT_NAME.upper()).style(f"color: {COLOR_STYLE['primary']}").classes("h1")
        ui.button(on_click=lambda: right_drawer.toggle(), icon="menu").props("flat color=white")

    # Sidebar
    with (
        ui.right_drawer(
            value=False,
            fixed=False,
        )
        .style(f"background-color: {COLOR_STYLE['secondary_bg']}")
        .props("overlay")
        .classes("p-0") as right_drawer,
        ui.element("q-scroll-area").classes("fit"),
    ):
        with (
            ui.list().classes("fit"),
            ui.item(on_click=lambda: ui.navigate.to("/")).props("clickable"),
            ui.item_section(),
        ):
            ui.label("HOME").style(f"color: {COLOR_STYLE['contrast']}")
        with ui.list().classes("fit"):
            ui.separator()
        with ui.list().classes("fit"):
            for input in INPUT_METHODS:
                with (
                    ui.item(on_click=lambda _, path=f"/test/{input['path']}": ui.navigate.to(path)).props("clickable"),
                    ui.item_section(),
                ):
                    ui.label(input["name"].upper()).style(f"color: {COLOR_STYLE['contrast']}")


ui.run()
