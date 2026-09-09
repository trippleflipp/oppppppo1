class Crop:
    """
    Структура для хранения данных об одной культуре.
    """

    def __init__(self, name, area, yield_per_ha):
        self.name = name
        self.area = area
        self.yield_per_ha = yield_per_ha
        self.volume = area * yield_per_ha