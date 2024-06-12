# reflex-pagination

Use the pagination like this
```python

# Snippet from reflex_pagination.py example app. 
    ...
    pagination(
        State.fruit,
        render_item=lambda item, idx: rx.text(f"{idx} {item}"),
    ),

```

Subclass it an override the rendering functions if you like.

```python

class CustomPagination(Pagination):

    @override
    @classmethod
    def render(cls) -> rx.Component:
        return rx.vstack(cls.render_controls(), cls.render_list())


custom_pagination = CustomPagination.create

```

So it basically works exactly like `rx.foreach`, but paginates the output.
