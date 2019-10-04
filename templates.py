import dominate.tags as t
from dominate.util import raw

import cccp


import random


emojis = "😂,❤️,💜,🙏,L,O,L,🎉,💩".split(",")


def create_matrix(content=None, width=100, height=100, cell_size=20):
    css = cccp.style_tag_with_css(
        cccp.CustomTemplate(
            """
        .wrapper {
            display: grid;
            grid-template-columns: $$cells_in_row;
        }
        * {box-sizing: border-box;}

        .wrapper {
        width: $$width_pixel;
        border: 0px;
        }

        .wrapper > div {
        line-height: $$unit;
        font-size: $$unit;
        font-family: monospace;
        width: $$unit;
        height: $$unit;
        border: 0px;
        padding: 0px;
        }
        """
        ).substitute(
            {
                "cells_in_row": " ".join(["1fr"] * width),
                "width_pixel": f"{width * cell_size}px",
                "unit": f"{cell_size}px",
            }
        )
    )
    content = content or {}
    return (
        css,
        t.div(
            [t.div(random.choice(emojis)) for index in range(width * height)],
            cls="wrapper",
        ),
    )


def index():
    css, grid = create_matrix()
    return cccp.render(
        t.html(
            [
                t.head(
                    [
                        cccp.raw(
                            """    <!-- Required meta tags -->
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            """
                        ),
                        cccp.REQUIRED,
                        css,
                    ]
                ),
                t.body(t.div(grid, cls="content-container")),
            ]
        )
    )


print(index())
