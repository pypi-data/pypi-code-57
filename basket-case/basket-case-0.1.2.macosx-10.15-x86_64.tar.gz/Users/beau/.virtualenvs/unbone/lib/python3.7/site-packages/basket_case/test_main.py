from basket_case import (
    title, find_uppercase, precede_uppercase, split_on,
    uppercase_after, camel, kebab, pythonic, constant
)

def test_camel():
    s1 = "kebab-to-camel"
    assert camel(s1) == "kebabToCamel"
    
    s2 = "snake_to_camel"
    assert camel(s2) == "snakeToCamel"
    
    s3 = "spaced to camel"
    assert camel(s3) == "spacedToCamel"
    assert camel(s3, capitalize_first=True) == "SpacedToCamel"

def test_constant():
    s1 = "some string"
    assert constant(s1) == "SOME_STRING"

def test_pythonic():
    pass

def test_title():
    s1 = "something to titlecase"
    assert title(s1) == "Something to Titlecase"

def test_find_uppercase():
    s1 = "hereIsSomeCamelCase"
    assert find_uppercase(s1) == [4, 6, 10, 15]
    
    s2 = "nouppercase"
    assert find_uppercase(s2) == []
    
    s3 = "ABC"
    assert find_uppercase(s3) == [0, 1, 2]

def test_split_on():
    s1 = "someCamelCase"
    ixs = find_uppercase(s1)
    assert split_on(s1, ixs) == ["some", "Camel", "Case"]

def test_precede_uppercase():
    s1 = "someCamelCase"
    assert precede_uppercase(s1, " ") == "some Camel Case"
    
def test_uppercase_after():
    s1 = "some-kebab-case"
    assert uppercase_after(s1, '-') == "some-Kebab-Case"
    
    s2 = "some-kebab-case"
    assert uppercase_after(s1, '-', keep_delim=False) == "someKebabCase"
