from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, cast, override

import reflex as rx

VAR_0 = rx.Var.create_safe(0)
VAR_1 = rx.Var.create_safe(1)

class Pagination(rx.ComponentState):
    _iterable: rx.Var
    __render_item__: Callable[[Any, int], rx.Component] = lambda item, idx: item

    page: int = 0
    items_per_page: int = 10

    @override
    @classmethod
    def create(
        cls,
        iterable: rx.Var | Iterable,
        render_item: Callable[[Any, int], rx.Component] = lambda item, idx: item,
        items_per_page: int = 10,
        *children,
        **props,
    ) -> rx.Component:
        cls._iterable = rx.Var.create_safe(iterable)
        cls._iterable._var_is_local = False
        cls.items_per_page = items_per_page
        cls.__render_item__ = render_item
        cls.__fields__["items_per_page"].default = items_per_page

        return super().create(*children, **props)

    def first_page(self) -> None:
        self.page = 0

    def next_page(self) -> None:
        self.page += 1

    def prev_page(self) -> None:
        self.page -= 1

    def set_page(self, page: int) -> None:
        self.page = page

    @classmethod
    def min(cls) -> rx.Var[int]:
        return rx.Var.create_safe(cls.page * cls.items_per_page)

    @classmethod
    def max(cls) -> rx.Var[int]:
        items_per_page = cast(rx.Var, cls.items_per_page)
        return rx.cond(
            (cls.min() + items_per_page) > cls._iterable.length(),
            cls._iterable.length(),
            cls.min() + items_per_page,
        )

    @classmethod
    def is_first_page(cls) -> rx.Var[bool]:
        page = cast(rx.Var, cls.page)
        return page == VAR_0

    @classmethod
    def is_last_page(cls) -> rx.Var[bool]:
        page = cast(rx.Var, cls.page)
        return page == (cls.total_pages() - VAR_1)

    @classmethod
    def total_pages(cls) -> rx.Var[int]:
        return cls._iterable.length().operation(
            "/", rx.Var.create_safe(cls.items_per_page), fn="Math.ceil"
        )

    @classmethod
    def get_component(cls, *children, **props) -> rx.Component:
        return cls.render()

    @classmethod
    def render(cls) -> rx.Component:
        return rx.vstack(
            cls.render_list(),
            cls.render_controls(),
        )

    @classmethod
    def render_list(cls) -> rx.Component:
        return rx.foreach(
            rx.Var.range(cls.min(), cls.max()),
            lambda item, idx: cls.__render_item__(cls._iterable[item], item),
        )

    @classmethod
    def render_first_button(cls) -> rx.Component:
        return rx.button(
            rx.icon(tag="chevron-first"),
            on_click=cls.first_page,
            disabled=cls.is_first_page(),
        )

    @classmethod
    def render_prev_button(cls) -> rx.Component:
        return rx.button(
            rx.icon(tag="chevron-left"),
            on_click=cls.prev_page,
            disabled=cls.is_first_page(),
        )

    @classmethod
    def render_next_button(cls) -> rx.Component:
        return rx.button(
            rx.icon(tag="chevron-right"),
            on_click=cls.next_page,
            disabled=cls.is_last_page(),
        )

    @classmethod
    def render_last_button(cls) -> rx.Component:
        return rx.button(
            rx.icon(tag="chevron-last"),
            on_click=lambda: cls.set_page(
                cls.total_pages() - VAR_1
            ),  # pyright: ignore[reportCallIssue]
            disabled=cls.is_last_page(),
        )

    @classmethod
    def render_text(cls) -> rx.Component:
        page = cast(rx.Var, cls.page)
        return rx.text(f"{page + VAR_1} / {cls.total_pages() }")

    @classmethod
    def render_page_count_select(cls) -> rx.Component:
        return rx.select(
            ["5", "10", "20", "50"],
            value=f"{cls.items_per_page}",
            on_change=cls.setvar("items_per_page"),
        )

    @classmethod
    def render_controls(cls) -> rx.Component:
        return rx.hstack(
            cls.render_first_button(),
            cls.render_prev_button(),
            cls.render_text(),
            cls.render_page_count_select(),
            cls.render_next_button(),
            cls.render_last_button(),
        )


pagination = Pagination.create
