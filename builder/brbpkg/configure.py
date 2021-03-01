#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Dict, Tuple, TypeVar

from clickgen.util import PNGProvider

from brbpkg.constants import WIN_CURSORS_CFG, WIN_DELAY, X_CURSORS_CFG, X_DELAY


X = TypeVar("X")


def to_tuple(x: X) -> Tuple[X, X]:
    return (x, x)


def get_config(bitmaps_dir, **kwargs) -> Dict[str, Any]:
    """Return configuration of `Bibata Rainbow` pointers.

    ```
    Args:

    :bitmaps_dir: (str | Path) Path to .png file's directory.


    Keywords Args:

    :x_sizes: (List[int]) List of pixel-sizes for xcursors.

    :win_canvas_size: (int) Windows cursor's canvas pixel-size.

    :win_size: (int) Pixel-size for Windows cursor.

    ```

    Example:

    ```python
        get_config(
            "./bitmaps",
            x_sizes=[(24, 24), (32, 32)],
            win_canvas_size=(32, 32),
            win_size=(24, 24),
        )
    ```
    """

    w_size = to_tuple(kwargs.pop("win_size"))
    w_canvas_size = to_tuple(kwargs.pop("win_canvas_size"))
    raw_x_sizes = kwargs.pop("x_sizes")

    x_sizes = []
    for size in raw_x_sizes:
        x_sizes.append(to_tuple(size))

    config: Dict[str, Any] = {}

    for key, item in X_CURSORS_CFG.items():
        x_hot: int = int(item.get("xhot", 0))
        y_hot: int = int(item.get("yhot", 0))
        hotspot: Tuple[int, int] = (x_hot, y_hot)

        delay: int = int(item.get("delay", X_DELAY))
        pngs = PNGProvider(bitmaps_dir).get(key)

        if not pngs:
            raise FileNotFoundError(f"{key} not found in {bitmaps_dir}")

        data = {
            "png": pngs,
            "x_sizes": x_sizes,
            "hotspot": hotspot,
            "delay": delay,
        }

        win_data = WIN_CURSORS_CFG.get(key)

        if win_data:
            win_key: str = str(win_data.get("to"))

            position: str = str(win_data.get("position", "center"))
            win_delay: int = int(win_data.get("delay", WIN_DELAY))

            canvas_size = win_data.get("canvas_size", w_canvas_size)
            win_size = win_data.get("size", w_size)

            # Because provided cursor size is bigger than cursor's canvas.
            # Also, "position" settings will not effect on cursor because the
            # cursor's canvas and cursor sizes are equals.
            if (win_size[0] > canvas_size[0]) | (win_size[1] > canvas_size[1]):
                canvas_size = win_size

            config[key] = {
                **data,
                "win_key": win_key,
                "position": position,
                "canvas_size": canvas_size,
                "win_size": win_size,
                "win_delay": win_delay,
            }
        else:
            config[key] = data

    return config
