"""Defines GUI elements."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable

import js  # type: ignore[import]
from pyodide.ffi import create_proxy

# Note: Disregarding N815, N802, and ANN401 are
# done for classes and functions that directly
# interact with or reflect the JS API


class HTMLElement(Protocol):
    """Define a protocol for HTML elements to allow for type checking. This is a subset of the DOM API."""

    id: str
    textContent: str  # noqa: N815
    innerHTML: str  # noqa: N815
    value: str
    style: Any
    className: str  # noqa: N815

    def appendChild(self, child: HTMLElement) -> None:  # noqa: N802
        """Append a child element to this element."""
        ...

    def removeChild(self, child: HTMLElement) -> None:  # noqa: N802
        """Remove a child element from this element."""
        ...

    def addEventListener(self, event: str, handler: Callable) -> None:  # noqa: N802
        """Add an event listener to this element."""
        ...

    def setAttribute(self, name: str, value: str) -> None:  # noqa: N802
        """Set an attribute on this element."""
        ...


class Element:
    """Base class for all GUI elements. This is a wrapper around an HTML element.

    Element provides several convenience methods for accessing the underlying HTML element.
    Getting or setting an item will access the underlying HTML element directly.

    ```py
    element = Element("div")
    element["style"].color = "red"
    ```

    If a convenience method exists on Element, it should be used instead of accessing the
    underlying HTML element directly.
    """

    _html_element: HTMLElement

    def __init__(
        self,
        tag_name: str | None = None,
        *,
        element: HTMLElement | None = None,
        parent: HTMLElement | Element | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        if element is not None:
            # Initialize from an existing HTML element
            if tag_name is not None:
                msg = "Cannot specify both element and tag name"
                raise ValueError(msg)
            if parent is not None:
                msg = "Cannot specify both element and parent"
                raise ValueError(msg)
            if kwargs:
                msg = "Cannot specify both element and kwargs"
                raise ValueError(msg)
            self._html_element = element
            return

        self._html_element = js.document.createElement(tag_name)

        for key, value in kwargs.items():
            self._html_element.setAttribute(key, value)

        if isinstance(parent, Element):
            root = parent.html_element
        elif parent is None:
            root = js.document.body
        else:
            root = parent

        root.appendChild(self.html_element)

    @property
    def html_element(self) -> HTMLElement:
        """Get the underlying HTML element. This is a read-only property."""
        return self._html_element

    def on(self, event: str, handler: Callable[[Any], None]) -> None:
        """Add an event handler to the element. The handler will be called with the element as the first argument."""

        def event_handler(event: Any) -> None:  # noqa: ANN401
            handler(event)

        self.html_element.addEventListener(event, create_proxy(event_handler))

    @property
    def text(self) -> str:
        """Get or set the text content of the element."""
        return self.html_element.textContent

    @text.setter
    def text(self, value: str) -> None:
        self.html_element.textContent = value

    @property
    def html(self) -> str:
        """Get or set the HTML content of the element."""
        return self.html_element.innerHTML

    @html.setter
    def html(self, value: str) -> None:
        """Set the HTML content of the element."""
        self.html_element.innerHTML = value

    @property
    def class_name(self) -> str:
        """Get or set the class name of the element."""
        return self.html_element.className

    @class_name.setter
    def class_name(self, value: str) -> None:
        self.html_element.className = value

    def append_child(self, child: Element) -> None:
        """Append a child element to this element."""
        self.html_element.appendChild(child.html_element)

    def remove_child(self, child: Element) -> None:
        """Remove a child element from this element."""
        self.html_element.removeChild(child.html_element)

    def __getitem__(self, key: str) -> Any:  # noqa: ANN401
        """Get an attribute on the underlying HTML element."""
        return getattr(self.html_element, key)

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        """Set an attribute on the underlying HTML element."""
        setattr(self.html_element, key, value)


class Button(Element):
    """A button element."""

    def __init__(self, parent: HTMLElement | Element | None = None, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__("button", parent=parent, **kwargs)

    def on_click(self, handler: Callable[[Any], None]) -> None:
        """Add a click event handler to the button."""
        self.on("click", handler)


class Input(Element):
    """An input element."""

    def __init__(self, parent: HTMLElement | Element | None = None, **kwargs: Any) -> None:  # noqa: ANN401
        super().__init__("input", parent=parent, **kwargs)

    def on_change(self, handler: Callable[[Any], None]) -> None:
        """Add a change event handler to the input."""
        self.on("change", handler)

    def on_input(self, handler: Callable[[Any], None]) -> None:
        """Add an input event handler to the input."""
        self.on("input", handler)
