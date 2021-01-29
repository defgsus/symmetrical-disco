from typing import Union, TextIO


class Image:
    """
    A Portable Bitmap / Netpbm image writer

    https://en.wikipedia.org/wiki/Netpbm
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.data = [
            [
                [0, 0, 0]
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def write_bitmap(self, file_or_name: Union[TextIO, str], threshold: float = 0.5):
        """
        Write a Bitmap (0/1)
        """
        if isinstance(file_or_name, str):
            with open(file_or_name, "w") as file:
                self.write_bitmap(file)
        else:
            print("P1", file=file_or_name)
            print(self.width, self.height, file=file_or_name)
            for row in self.data:
                row = [
                    0 if c[0] >= threshold or c[1] >= threshold or c[2] >= threshold else 1
                    for c in row
                ]
                print(*row, file=file_or_name)

    def dump(self, file: TextIO = None):
        for row in self.data:
            row = [
                "\033[38;2;%s;%s;%sm██\033[0m" % (
                    max(0, min(255, int(c[0] * 255))),
                    max(0, min(255, int(c[1] * 255))),
                    max(0, min(255, int(c[2] * 255))),
                )
                for c in row
            ]
            print("".join(row), file=file)
