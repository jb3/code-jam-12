from collections.abc import Iterator

from nicegui import ui


class input_view(ui.element):  # noqa: N801 this is the nicegui convention
    """The component which will display the user's input.

    :param full_text: The original text displayed under the user's input. This can be changed later.
    """

    CSS = """
.input-view {
    display: block;
    position: relative;
    padding: 8px;
    border-radius: 5px;
    background-color: var(--q-dark);
    font-family: monospace;
    color: var(--q-secondary);
    word-break: break-all;
}

.input-view-fg {
    position: absolute;
    inset: 0;
    margin: 8px;
}

.input-view-fg div {
    display: inline;
}

.input-view-fg span.c, .input-view-fg div.c {
    background-color: var(--q-positive);
    color: var(--q-dark);
}

.input-view-fg span.w, .input-view-fg div.w {
    background-color: var(--q-negative);
}

.input-view-fg span.cursor, .input-view-fg div.cursor {
    color: white;
    display: inline-block;
}
"""

    def __init__(self, full_text: str) -> None:
        super().__init__("div")
        ui.add_css(self.CSS)

        self.classes("input-view")
        with self:
            self.full_text_label = ui.label(full_text).classes("input-view-bg")
            self.text_input = ui.element().classes("input-view-fg")

        self.full_text = full_text
        self.value = ""

    def _parse_text(self, user_text: str) -> Iterator[tuple[str, bool]]:
        """Get a token list of string slices and whether they are correct."""
        if len(user_text) == 0:
            return iter(())

        mask = bytearray(user_text[i] == self.full_text[i] for i in range(min(len(self.full_text), len(user_text))))
        index = 0
        cur_v = mask[0]

        while index < len(mask):
            next_change_at = mask.find(cur_v ^ 1, index)
            if next_change_at == -1:
                next_change_at = len(mask)
            yield (user_text[index:next_change_at], bool(cur_v))
            index = next_change_at
            cur_v ^= 1

    def set_original_text(self, value: str) -> None:
        """Reset the background text (full_text)."""
        self.full_text = value
        self.full_text_label.set_text(value)

    def set_text(self, value: str) -> None:
        """Set the current input.

        Sets the foreground value to the user's input, and adds some highlighting based on where
        the user's input is right and wrong.
        """
        self.text_input.clear()
        if value == "":
            return
        parsed = self._parse_text(value)
        with self.text_input:
            for tok in parsed:
                ui.label(tok[0]).classes("c" if tok[1] else "w")
            ui.label("_").classes("cursor")
