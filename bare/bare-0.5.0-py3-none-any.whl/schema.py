class Time(bare.String):
    pass


class PublicKey(bare.Data):
    __size__ = 128


class Department(Enum):
    pass


class Customer(bare.Type):
    name = bare.String()
    email = bare.String()
    address = bare.String()
    orders = bare.Array()
    metadata = bare.Map(bare.String, bare.Data)


class Employee(bare.Type):
    name = bare.String()
    email = bare.String()
    address = bare.String()
    department = bare.Enum(Department)
    hireDate = Time()
    publicKey = PublicKey(required=False)
    metadata = bare.Map(bare.String, bare.Data)


class Person(bare.Union):
    __union__ = [Customer, Employee]


class Address(bare.Type):
    address = bare.Array(bare.String, count=4)
    city = bare.String()
    state = bare.String()
    country = bare.String()
