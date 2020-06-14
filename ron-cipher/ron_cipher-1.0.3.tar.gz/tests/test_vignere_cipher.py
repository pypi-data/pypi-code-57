from ciphers.vigenere_cipher import VigenereCipher


class TestVigenere:
    def setup_class(self):
        self.default_cipher = VigenereCipher()
        self.custom_cipher = VigenereCipher(secret="supersecret")

    def test_caeser_cipher_encrypt_default_rotation(self):
        input_string = "some sample text"
        output_string = self.default_cipher.encrypt(plain_text=input_string)
        assert output_string == ",[<^ k???e+ k+},"

    def test_caeser_cipher_decrypt_default_rotation(self):
        input_string = ",[<^ k???e+ k+},"
        output_string = self.default_cipher.decrypt(encrypted=input_string)
        assert output_string == "some sample text"

    def test_caeser_cipher_encrypt_custom_rotation(self):
        input_string = "some sample text"
        output_string = self.custom_cipher.encrypt(plain_text=input_string)
        assert output_string == ",i%+ ,&<6>{ m\\#,"

    def test_caeser_cipher_decrypt_custom_rotation(self):
        input_string = ",i%+ ,&<6>{ m\\#,"
        output_string = self.custom_cipher.decrypt(encrypted=input_string)
        assert output_string == "some sample text"

    def test_get_secret(self):
        assert self.custom_cipher.secret == "supersecret"

    def test_secret_handles_non_existing_characters(self):
        secret = "super secret"
        custom_cipher = VigenereCipher(secret=secret)

        assert custom_cipher.secret == "supersecret"

    def test_set_secret(self):
        self.custom_cipher.secret = "funtimeswithsecrets"
        assert self.custom_cipher.secret == "funtimeswithsecrets"
