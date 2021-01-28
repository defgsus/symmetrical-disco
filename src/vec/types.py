from typing import Sequence, Union, Optional

Number = Union[int, float]
Vector3 = Sequence[Number]


def is_number(x):
    return isinstance(x, (int, float))


