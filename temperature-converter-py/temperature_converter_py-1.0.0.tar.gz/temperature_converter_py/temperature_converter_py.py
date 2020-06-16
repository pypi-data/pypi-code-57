def celsius_to_fahrenheit(temp_in_celsius):
    temp_in_fahrenheit = 1.8 * temp_in_celsius + 32
    return temp_in_fahrenheit


def fahrenheit_to_celsius(temp_in_fahrenheit):
    temp_in_celsius = (temp_in_fahrenheit - 32) / 1.8
    return temp_in_celsius


def celsius_to_kelvin(temp_in_celsius):
    temp_in_kelvin = temp_in_celsius + 273.15
    return temp_in_kelvin


def kelvin_to_celsius(temp_in_kelvin):
    temp_in_celsius = temp_in_kelvin - 273.15
    return temp_in_celsius


# if __name__ == '__main__':
#     print('{} ºF'.format(celsius_to_fahrenheit(10)))
#     print('{} ºC'.format(fahrenheit_to_celsius(212)))
