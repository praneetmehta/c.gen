from dataclasses import dataclass


@dataclass
class Pair:
    _x : int
    _y : int

    @property
    def X(self) -> int:
        return self._x

    @X.setter
    def X(self, val : int) -> None:
        self._x = val

    @property
    def Y(self) -> int:
        return self._y

    @Y.setter
    def Y(self, val : int) -> None:
        self._y = val

@dataclass
class Triplet(Pair):
    _z : int

    @property
    def Z(self) -> int:
        return self._z

    @Z.setter
    def Z(self, val : int) -> None:
        self._Z = val


