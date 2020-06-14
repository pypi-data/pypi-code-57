from ciphers.caeser_cipher import CaeserCipher
from pytest import raises


class TestCaeser:
    def setup_class(self):
        self.default_cipher = CaeserCipher()
        self.custom_cipher = CaeserCipher(rotation=1)

    def test_caeser_cipher_encrypt_default_rotation(self):
        input_string = "some random string"
        output_string = self.default_cipher.encrypt(plain_text=input_string)
        assert output_string == "4c0> e.#qc0 4(e^#["

    def test_caeser_cipher_decrypt_default_rotation(self):
        input_string = "4c0> e.#qc0 4(e^#["
        output_string = self.default_cipher.decrypt(encrypted=input_string)
        assert output_string == "some random string"

    def test_caeser_cipher_encrypt_custom_rotation(self):
        input_string = "some random string"
        output_string = self.custom_cipher.encrypt(plain_text=input_string)
        assert output_string == ">:.3 =~/2:. >?=7/5"

    def test_caeser_cipher_decrypt_custom_rotation(self):
        input_string = ">:.3 =~/2:. >?=7/5"
        output_string = self.custom_cipher.decrypt(encrypted=input_string)
        assert output_string == "some random string"

    def test_get_rotation(self):
        assert self.custom_cipher.rotation == 1

    def test_set_rotation_invalid_input(self):
        with raises(Exception) as value_error:
            self.custom_cipher.rotation = "five"
            assert str(value_error) == "Rotation must be an integer"
