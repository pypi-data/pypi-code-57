def to_liteaddr(ip):
    ip = ip[0].split(".")
    return "Lite|" + "_".join([int_to_lite_num(int(n)) for n in ip])


def int_to_lite_num(number):
    row = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    base = len(row)

    lite_num = [(number - (number % base)) / base, number % base]

    return "".join([list(row)[int(digit) - 1] for digit in lite_num])
