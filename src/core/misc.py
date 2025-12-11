from dataclasses import dataclass
from typing import Any


JsonSchema = dict[str, Any]


@dataclass
class LineWindow:
    previous: list[str]
    current: list[str]
    next: list[str]


def window_lines(text: str, ctx_size: int, win_size: int) -> list[LineWindow]:
    lines = text.splitlines()

    return [
        LineWindow(
            lines[i - ctx_size : i],
            lines[i : i + win_size],
            lines[i + win_size : i + win_size + ctx_size],
        )
        for i in range(0, len(lines), win_size)
    ]


def print_window(win: LineWindow):
    print("PREVIOUS:")
    for line in win.previous:
        print(line)

    print("\n\nWINDOW:")
    for line in win.current:
        print(line)

    print("\n\nRIGHT:")
    for line in win.next:
        print(line)
