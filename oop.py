from tabulate import tabulate

class Car:
    def __init__(self, number, firm, model, car_license, colour,
                 engine_power, fuel, volume, mileage,
                 drive, transmission):
        self.number = number
        self.firm = firm
        self.model = model
        self.car_license = car_license
        self.colour = colour
        self.engine_power = engine_power
        self.fuel = fuel
        self.volume = volume
        self.mileage = mileage
        self.drive = drive
        self.transmission = transmission

    def __str__(self):
        return [f"{self.number}", f"{self.firm}", f"{self.model}", f"{self.car_license}", f"{self.colour}",
                f"{self.engine_power}", f"{self.fuel}", f"{self.volume}", f"{self.mileage}", f"{self.drive}",
                f"{self.transmission}"]

    def edit_car(self, parameter_name, new_value):
        out = check_parameter(parameter_name)
        if out != "ОК":
            return out
        else:
            out = check_value(parameter_name, new_value)
            if out != None:
                return out
            else:
                for key in translator.keys():
                    if key == parameter_name:
                        if parameter_name == "Коробка передач":
                            new_value += "\n"
                        setattr(self, translator[key], new_value)
                return "Успешно изменено"

    @staticmethod
    def show_all():
        cars = load_data("oop.txt")
        table = [["Номер", "Производитель", "Модель", "Госномер", "Цвет", "Мощность двигателя(л.с.)", "Тип топлива",
                  "Объём бака(л)", "Пробег(км)", "Привод", "Коробка передач\n"]]
        for car in cars:
            table.append(Car.__str__(car))
        table = tabulate(table, headers="firstrow", tablefmt="fancy_grid")
        return table

    @staticmethod
    def search(parameter_name, parameter_value, cars):
        out = "Ничего не найдено"
        if check_parameter(parameter_name) != "ОК":
            return check_parameter(parameter_name)
        for car in cars:
            for key in translator.keys():
                if parameter_name == key:
                    for value in car.__dict__.items():
                        if value[0] == translator[key]:
                            if value[1] == parameter_value:
                                out = Car.__str__(car)
        return out

    @staticmethod
    def add_car():
        cars = load_data("oop.txt")
        parameters = [str(len(cars) + 1)]
        for key in translator.keys():
            if key == "Номер":
                continue
            else:
                flag = False
                while not flag:
                    print(f"Введите {key}", end=": ")
                    parameter = input()
                    if check_value(key, parameter) is None:
                        parameters.append(parameter)
                        flag = True
                    else:
                        print(check_value(key, parameter))
        new_car = Car(*parameters)
        cars.append(new_car)
        save_data(cars, "oop.txt")
        return "Машина успешно добавлена"

    @staticmethod
    def delete_car(car_license, cars):
        out = "Нет машины с таким госномером!"
        car_number = -1
        for i in range(len(cars)):
            if cars[i].car_license == car_license:
                car_number = i
        if car_number != -1:
            del cars[car_number]
            for i in range(len(cars)):
                cars[i].number = str(i + 1)
            out = "Машина успешно удалена"
        return out


def load_data(n):
    with open(n, "r", encoding="UTF-8") as file:
        filedata = file.readlines()
    cars = []
    for i in range(len(filedata)):
        car_data = filedata[i].split(',')
        car = Car(*car_data)
        cars.append(car)
    return cars


def save_data(cars, n):
    with open(n, "w", encoding="UTF-8") as file:
        new_data = []
        for car in cars:
            car_string = ""
            for value in car.__dict__.items():
                car_string += (value[1] + ",")
            car_string = car_string[:-1]
            new_data.append(car_string)
        file.writelines(new_data)
    return None


def menu():
    return """
    Выберите действие:
    Введите "Найти машины по параметру", чтобы найти все машины с указанной характеристикой
    Введите "Посмотреть всё", чтобы посмотреть все машины и все их характеристики
    Введите "Добавить машину", чтобы добавить новую машину в список
    Введите "Удалить машину", чтобы удалить машину из списка
    Введите "Изменить значение", чтобы изменить значение ячейки
    Введите "Задать СДЗ", чтобы задать список допустимых значений
    Введите "Удалить СДЗ", чтобы удалить список допустимых значений
    Введите "Стоп", чтобы завершить работу программы
    """


def read(n):
    with open(n, 'r', encoding='UTF-8') as file:
        return file.readlines()


def save(m, n):
    with open(m, 'w', encoding='UTF-8') as file:
        file.writelines(n)


def check_parameter(parameter_name):
    out = "Неверно указан параметр! Попробуйте снова"
    for key in translator.keys():
        if key == parameter_name:
            out = "ОК"
    return out


def check_value(parameter_name, parameter_value):
    with open("sdz.txt", "r", encoding="UTF-8") as sdzfile:
        sdz = sdzfile.readlines()
        flag = 0
        for line in sdz:
            values = line[:-1].split(",")
            if values[0] == parameter_name:
                flag = 1
                for value in range(1, len(values)):
                    if values[value] == parameter_value:
                        return None
        if flag == 0:
            return None
    return "Нельзя задать это значение!"


def main():
    while True:
        print(menu())
        command = input()
        if command == "Посмотреть всё":
            print(Car.show_all())
        elif command == "Найти машины по параметру":
            while True:
                print("Введите параметр и значение через запятую", end=": ")
                inputs = input().split(",")
                if len(inputs) != 2:
                    print("Ошибка, научитесь читать")
                else:
                    parameter_name = inputs[0]
                    parameter_value = inputs[1]
                    cars = load_data("oop.txt")
                    car = Car.search(parameter_name, parameter_value, cars)
                    if type(car) == list:
                        table = [["Номер", "Производитель", "Модель", "Госномер", "Цвет", "Мощность двигателя(л.с.)",
                                  "Тип топлива", "Объём бака(л)", "Пробег(км)", "Привод", "Коробка передач\n"], car]
                        table = tabulate(table, headers="firstrow", tablefmt="fancy_grid")
                        print(table)
                        break
                    else:
                        print(car)
        elif command == "Добавить машину":
            print(Car.add_car())
        elif command == "Удалить машину":
            print("Введите госномер", end=": ")
            while True:
                car_license = input()
                cars = load_data("oop.txt")
                result = Car.delete_car(car_license, cars)
                print(result)
                if result == "Машина успешно удалена":
                    save_data(cars, "oop.txt")
                    break
        elif command == "Изменить значение":
            cars = load_data("oop.txt")
            while True:
                print("Введите госномер машины", end=": ")
                car_license = input()
                flag = 0
                for car in cars:
                    if car.car_license == car_license:
                        flag = 1
                        while True:
                            print("Введите параметр машины и его значение через запятую:")
                            inputs = input().split(",")
                            if len(inputs) != 2:
                                print("Ошибка, научитесь читать")
                            else:
                                parameter_name = inputs[0]
                                parameter_value = inputs[1]
                                result = car.edit_car(parameter_name, parameter_value)
                                print(result)
                                if result == "Успешно изменено":
                                    save_data(cars, "oop.txt")
                                    break
                if flag == 0:
                    print("Нет машиины с таким госномером!")
                else:
                    break
        elif command == "Задать СДЗ":
            print('Введите параметр', end=': ')
            while True:
                parameter_name = input()
                if check_parameter(parameter_name) == "ОК":
                    break
                else:
                    print(check_parameter(parameter_name))
            sdz = read('sdz.txt')
            print('Введите допустимые значения через запятую', end=': ')
            new_string = parameter_name + ',' + input() + '\n'
            for line in range(len(sdz)):
                string = sdz[line][:-1].split(',')
                if string[0] == parameter_name:
                    sdz[line] = new_string
                else:
                    sdz.append(new_string)
            save('sdz.txt', sdz)
            print(f"СДЗ для параметра {parameter_name} успешно задана")
        elif command == 'Удалить СДЗ':
            print('Введите параметр', end=': ')
            while True:
                parameter_name = input()
                if check_parameter(parameter_name) == "ОК":
                    break
                else:
                    print(check_parameter(parameter_name))
            sdz = read('sdz.txt')
            flag = 0
            for line in range(len(sdz)):
                string = sdz[line][:-1].split(',')
                if string[0] == parameter_name:
                    number_of_string = line
                    flag = 1
            if flag == 1:
                del sdz[number_of_string]
            save('sdz.txt', sdz)
            print(f"СДЗ для параметра {parameter_name} успешно удалена")
        elif command == "Стоп":
            print("Работа программы завершена")
            break
        else:
            print("Неверная команда!")


translator = {'Номер': 'number', 'Производитель': 'firm', 'Модель': 'model',
              'Госномер': 'car_license', 'Цвет': 'colour', 'Мощность двигателя': 'engine_power',
              'Топливо': 'fuel', 'Объём': 'volume', 'Пробег': 'mileage',
              'Привод': 'drive', 'Коробка передач': 'transmission'}

if __name__ == "__main__":
    main()
