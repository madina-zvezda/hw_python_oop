# создаем класс для создания объектов сообщений
class InfoMessage:
    """Класс вывода сообщений"""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration
    
    def get_message(self) -> str:
        """Получить сообщение."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
            )

#создаем родительский класс Training
class Training:
    """базовый класс Training"""  
    LEN_STEP: float = 0.65
    M_IN_KM: float = (1000)
    MIN_IN_HOUR: float = 60
    TRAINING_TYPE = ''

    def __init__(self, action: int,duration: float,weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    
    # расчёт дистанции, которую пользователь преодолел за тренировку
    def get_distance(self: float)-> float:  
        """Расчет дистанции.""" 
        return (self.action * self.LEN_STEP / self.M_IN_KM) 
        

    #расчёт средней скорости движения во время тренировки
    def get_mean_speed(self: float)-> float:
        """Расчет средней скорости."""
        speed = (self.get_distance() / self.duration) 
        return speed
        
    
    #расчёт количества потраченных калорий за тренировку
    def get_spent_calories(self)-> float:
        """Получить значения потраченных калорий."""
        pass

    #сообщение о результатах тренировки
    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )

#объявляем дочерний класс Running
class Running(Training):
    """Тренировка - бег"""
    # создаём объект и в нём сохраняем их значения
    K_1 = 18
    K_2 = 20

    def get_spent_calories(self)-> float:
        """Получить значения потраченных калорий."""
        duration_in_min = round(self.duration * self.MIN_IN_HOUR)
        return ((self.K_1 * self.get_mean_speed() - self.K_2)* self.weight/ self.M_IN_KM* duration_in_min)


#объявляем дочерний класс SportsWalking
class SportsWalking(Training):
    """Тренировка - спортивная ходьба"""
    M_1 = 0.035
    M_2 = 0.029
    
    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self)-> float:
        """Получить значения потраченных калорий."""
        calories = (self.M_1 * self.weight+ (self.get_mean_speed() ** 2 // self.height) * self.M_2 * self.weight) * round(self.duration * self.MIN_IN_HOUR)
        return calories

#объявляем дочерний класс Swimming
class Swimming(Training):
    """Тренировка - плавание"""
    K_11 = 1.1
    K_12 = 2
    LEN_STEP = 1.38
     
    def __init__(self, action: int, duration: float, weight: float, length_pool:int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self: float)-> float:
        """Расчет средней скорости."""
        return (self.length_pool * self.count_pool /self. M_IN_KM / self.duration)
    
    def get_spent_calories(self)-> float:
        """Получить значения потраченных калорий."""
        return (self.get_mean_speed() + self.K_11) * self.K_12 * self.weight  

def read_package(workout_info: str, data_info: list) -> Training:
    """Получить данные от датчиков."""
    workout_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return workout_dict[workout_info](*data_info)

def main(training_info: Training) -> None:
    """Главная функция."""
    info = training_info.show_training_info()
    text = info.get_message()
    print(text)

if __name__ == '__main__':
    packages = [        
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training) 


    packages = [
     ('SWM', [720, 1, 80, 25, 40]),
     ('RUN', [15000, 1, 75]),
     ('WLK', [9000, 1, 75, 180]),
    ] 

