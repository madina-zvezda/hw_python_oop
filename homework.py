from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Класс вывода сообщений"""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """ Получить сообщение. """
        return self.MESSAGE.format(**asdict(self))


class Training:
    """базовый класс Training"""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self: float) -> float:
        """Расчет дистанции."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self: float) -> float:
        """Расчет средней скорости."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить значения потраченных калорий."""
        raise NotImplementedError(
            'Определить значение калорий' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),)


class Running(Training):
    """Тренировка - бег"""
    COEFF_CALORIE1: int = 18
    COEFF_CALORIE2: int = 20

    def get_spent_calories(self) -> float:
        """Получить значения потраченных калорий."""
        duration_in_min = round(self.duration * self.MIN_IN_HOUR)
        return (
            (self.COEFF_CALORIE1 * self.get_mean_speed() - self.COEFF_CALORIE2)
            * self.weight
            / self.M_IN_KM
            * duration_in_min)


class SportsWalking(Training):
    """Тренировка - спортивная ходьба"""
    COEF_CALORIE01: float = 0.035
    COEF_CALORIE02: float = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить значения потраченных калорий."""
        return ((self.COEF_CALORIE01 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEF_CALORIE02 * self.weight)
                * round(self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка - плавание"""
    COEF_CALORIE3: float = 1.1
    COEF_CALORIE4: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self: float) -> float:
        """Расчет средней скорости."""
        speed = self.length_pool * self.count_pool / self. M_IN_KM
        return speed / self.duration

    def get_spent_calories(self) -> float:
        """Получить значения потраченных калорий."""
        calorie = self.get_mean_speed() + self.COEF_CALORIE3
        return calorie * self.COEF_CALORIE4 * self.weight


def read_package(workout_info: str, data_info: list) -> Training:
    """Получить данные от датчиков."""
    workout_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    try:
        return workout_dict[workout_info](*data_info)
    except (KeyError, TypeError) as type_error:
        raise ValueError('Неверный тип тренировки {0}'.format(type_error))


def main(training_info: Training) -> None:
    """Главная функция."""
    info = training_info.show_training_info()
    text = info.get_message()
    print(text)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]), ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
