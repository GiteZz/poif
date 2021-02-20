class MetaCollection:
    def __init__(self):
        self.base_dict = {}

    def __getattr__(self, name):
        try:
            return self.base_dict[name]
        except:
            raise AttributeError

    def __setitem__(self, key, value):
        self.base_dict[key] = value

    def __getitem__(self, key):
        return self.base_dict[key]

    def __add__(self, other: "MetaCollection") -> "MetaCollection":
        combined_dict = {}
        for key, value in self.base_dict.items():
            combined_dict[key] = value
        for key, value in other.base_dict.items():
            combined_dict[key] = value
        new_collection = MetaCollection()
        new_collection.base_dict = combined_dict

        return new_collection
