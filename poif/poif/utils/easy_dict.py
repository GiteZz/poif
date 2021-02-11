class EasyDict(dict):
    def __init__(self, base_dict: dict = None):
        super().__init__()
        if base_dict is not None:
            self.__dict__ = base_dict

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            self[name] = EasyDict()
            return self[name]

    def __setattr__(self, name, value):
        try:
            if isinstance(value, dict):
                self[name] = EasyDict(value)
            else:
                self[name] = value
        except AttributeError:
            self[name] = EasyDict()
            return self[name]
