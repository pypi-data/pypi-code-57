from model_bakery import baker


def test_str_method():
    phone = baker.prepare('subjects.Phone', number='+49123456789', label=1)
    assert str(phone) == '+49123456789'
    assert phone.number.as_international == '+49 123456789'
