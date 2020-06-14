from ciphers.cipher_helper import get_character_map, flip_dict


class VigenereCipher:
    def __init__(self, secret: str = None):
        self.default_character_map = get_character_map()
        self.flipped_default_character_map = flip_dict(
            self.default_character_map
        )
        if secret:
            secret_index = 0
            while secret_index < len(secret):
                if secret[secret_index] not in self.default_character_map:
                    secret = (
                        secret[0:secret_index] + secret[secret_index + 1:]
                    )
                secret_index += 1
            self._secret = str(secret).lower()
        else:
            self._secret = "secret"

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, secret_value):
        secret_value = str(secret_value)
        self._secret = secret_value

    def encrypt(self, plain_text):
        plain_text = plain_text.lower()
        encrypted = ""
        current_index = 0
        secret_length = len(self._secret)
        map_length = len(self.default_character_map)

        for character in plain_text:
            if character in self.default_character_map:
                value = self.default_character_map[character]
                secret_value = self.default_character_map[
                    self._secret[current_index % secret_length]
                ]
                new_value = (value + secret_value) % map_length
                encrypted += self.flipped_default_character_map[new_value]
            else:
                encrypted += character
            current_index += 1

        return encrypted

    def decrypt(self, encrypted):
        encrypted = encrypted.lower()
        plain_text = ""
        current_index = 0
        secret_length = len(self._secret)
        map_length = len(self.default_character_map)

        for character in encrypted:
            if character in self.default_character_map:
                value = self.default_character_map[character]
                secret_value = self.default_character_map[
                    self._secret[current_index % secret_length]
                ]
                new_value = (value - secret_value) % map_length
                plain_text += self.flipped_default_character_map[new_value]
            else:
                plain_text += character
            current_index += 1

        return plain_text
