"""Global Domain"""


class Model(object):
    """In case model reflects HistoricalModel, historio will determine data to collect rather than seeking itself """

    def source(self):
        raise NotImplementedError("Subclasses should implement this!")

    def source_id(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_data(self):
        raise NotImplementedError("Subclasses should implement this!")
