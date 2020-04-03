class TransformationParameters:
    def __init__(self, **kwargs):
        self._param_set = frozenset(kwargs.items())

    def __hash__(self):
        return hash(self._param_set)


class SingleIntParameter(TransformationParameters):
    def __init__(self, *, int_value: str):
        value = int(int_value)

        super().__init__(value=value)

        self.int_value = value


class SingleFloatParameter(TransformationParameters):
    def __init__(self, *, float_value: str):
        value = float(float_value)

        super().__init__(value=value)

        self.float_value = value


class SingleStringParameter(TransformationParameters):
    def __init__(self, *, str_value: str):
        super().__init__(value=str_value)

        self.str_value = str_value


class IntXYParameters(TransformationParameters):
    def __init__(self, *, x: str, y: str):
        _x = int(x)
        _y = int(y)

        super().__init__(x=_x, y=_y)

        self.x = _x
        self.y = _y


class IntXYWHParameters(TransformationParameters):
    def __init__(self, *, x: str, y: str, w: str, h: str):
        _x = int(x)
        _y = int(y)
        _w = int(w)
        _h = int(h)

        super().__init__(x=_x, y=_y, w=_w, h=_h)

        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
