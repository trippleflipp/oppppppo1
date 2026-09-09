from models import Crop


class HarvestService:
    """
    Логика учёта урожая.
    """

    def __init__(self):
        self.crops = []


    def add_crop(self, name, area, yield_per_ha):
        """
        Добавляет новую культуру в список.
        """

        name = name.strip()

        if not name:
            raise ValueError("Введите название культуры.")

        if area <= 0:
            raise ValueError("Площадь посева должна быть больше нуля.")

        if yield_per_ha < 0:
            raise ValueError("Урожайность не может быть отрицательной.")

        crop = Crop(name, area, yield_per_ha)
        self.crops.append(crop)

        return crop


    def total_volume(self):
        """
        Возвращает общий объём урожая по всем культурам.
        """

        total = 0.0

        for crop in self.crops:
            total += crop.volume

        return total


    def clear(self):
        """
        Очищает список культур.
        """

        self.crops.clear()


    def has_crops(self):
        """
        Проверяет, есть ли добавленные культуры.
        """

        return len(self.crops) > 0