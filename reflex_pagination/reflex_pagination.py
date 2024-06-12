"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from typing import override
import reflex as rx

from reflex_pagination.pagination import Pagination, pagination
from rxconfig import config


class CustomPagination(Pagination):

    @override
    @classmethod
    def render(cls) -> rx.Component:
        return rx.vstack(cls.render_controls(), cls.render_list())


custom_pagination = CustomPagination.create


class State(rx.State):
    """The app state."""

    fruit: list[str] = [
        "🍈",
        "🍉",
        "🍌",
        "🍍",
        "🥭",
        "🍎",
        "🍏",
        "🍐",
        "🍑",
        "🍓",
        "🥑",
        "🥕",
        "🥒",
    ]


def index() -> rx.Component:
    return rx.container(
        rx.heading("Default pagination"),
        pagination(
            State.fruit,
            render_item=lambda item, idx: rx.text(f"{idx} {item}"),
        ),
        rx.spacer(height="4vh"),
        rx.heading("Custom pagination (controls at the top)"),
        custom_pagination(
            State.fruit,
            render_item=lambda item, idx: rx.text(f"{idx} {item}"),
        ),
        padding_top="4vh",
    )


app = rx.App()
app.add_page(index)
