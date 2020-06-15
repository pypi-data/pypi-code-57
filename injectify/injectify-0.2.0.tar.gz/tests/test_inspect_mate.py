from injectify.inspect_mate import (
    is_attribute, is_property_method, is_regular_method, is_static_method,
    is_class_method, get_attributes, get_property_methods, get_regular_methods,
    get_static_methods, get_class_methods, get_all_attributes, get_all_methods,
)


class Base:
    attribute = 'attribute'

    @property
    def property_method(self):
        return 'property_method'

    def regular_method(self):
        return 'regular_method'

    @staticmethod
    def static_method():
        return 'static_method'

    @classmethod
    def class_method(cls):
        return 'class_method'


class MyClass(Base):
    pass


def test_is_attribute_property_method_regular_method_static_method_class_method():
    assert is_attribute(MyClass, 'attribute', MyClass.attribute)
    assert is_property_method(
        MyClass, 'property_method', MyClass.property_method)
    assert is_regular_method(
        MyClass, 'regular_method', MyClass.regular_method)
    assert is_static_method(
        MyClass, 'static_method', MyClass.static_method)
    assert is_class_method(MyClass, 'class_method', MyClass.class_method)

    attr_list = [
        (MyClass, 'attribute', MyClass.attribute),
        (MyClass, 'property_method', MyClass.property_method),
        (MyClass, 'regular_method', MyClass.regular_method),
        (MyClass, 'static_method', MyClass.static_method),
        (MyClass, 'class_method', MyClass.class_method),
    ]

    checker_list = [
        is_attribute,
        is_property_method,
        is_regular_method,
        is_static_method,
        is_class_method,
    ]

    for i, pair in enumerate(attr_list):
        klass, attr, value = pair
        for j, checker in enumerate(checker_list):
            if i == j:
                assert checker(klass, attr, value) is True
            else:
                assert checker(klass, attr, value) is False


def test_getter():
    def items_to_keys(items):
        return set([item[0] for item in items])

    assert items_to_keys(get_attributes(MyClass)) == {'attribute'}
    assert items_to_keys(
        get_property_methods(MyClass)) == {'property_method'}
    assert items_to_keys(
        get_regular_methods(MyClass)) == {'regular_method'}
    assert items_to_keys(
        get_static_methods(MyClass)) == {'static_method'}
    assert items_to_keys(
        get_class_methods(MyClass)) == {'class_method'}
    assert items_to_keys(
        get_all_attributes(MyClass)) == {'attribute', 'property_method'}
    assert items_to_keys(
        get_all_methods(MyClass)) == {'regular_method', 'static_method', 'class_method'}
