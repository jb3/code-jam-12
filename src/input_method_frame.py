from nicegui import ui

import input_method_proto


def input_method_page(input_method: input_method_proto.IInputMethod) -> None:
    """User interface frame for input method pages.

    Args:
        input_method: The input method to be generated on the page.

    """


ui.run()
