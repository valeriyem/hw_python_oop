class InfoMessage:
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.')


class Training:
    LEN_STEP = 0.65
    M_IN_KM = 1000
    HOURS_TO_MINUTES = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) \
            * self.weight / self.M_IN_KM \
            * (self.duration * self.HOURS_TO_MINUTES)


class SportsWalking(Training):
    HOURS_TO_MINUTES = 60
    FIRST_COEFFICIENT = 0.035
    SECOND_COEFFICIENT = 0.029
    CM_TO_METER = 100
    KM_PER_HOUR_TO_METER_PER_SECOND = 0.278

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.FIRST_COEFFICIENT * self.weight
                 + ((self.get_mean_speed()
                    * self.KM_PER_HOUR_TO_METER_PER_SECOND)**2
                    / (self.height / self.CM_TO_METER))
                * self.SECOND_COEFFICIENT * self.weight)
                * self.duration * self.HOURS_TO_MINUTES)


class Swimming(Training):
    LEN_STEP = 1.38
    FIRST_COEF = 1.1
    SECOND_COEF = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.FIRST_COEF) \
            * self.SECOND_COEF * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    training_types = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}
    training_type: Training = training_types[workout_type](*data)
    return training_type


def main(training: Training) -> None:
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
