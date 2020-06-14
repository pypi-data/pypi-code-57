from ciphers.cipher_helper import get_character_map, flip_dict


class CaeserCipher:
    def __init__(self, rotation: int = None):
        self.default_character_map = get_character_map()
        self.flipped_default_character_map = flip_dict(
            self.default_character_map
        )

        if rotation:
            self.rotation = rotation
        else:
            self.rotation = len(self.default_character_map) // 2

        self.update_cipher_dicts()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation_value):
        try:
            rotation_value = int(rotation_value)
        except ValueError:
            raise Exception("Rotation must be an integer")

        self._rotation = rotation_value
        self.update_cipher_dicts()

    def update_cipher_dicts(self):
        # update map for new cipher
        character_map_length = len(self.default_character_map)
        self.cipher_map = {
            key: ((value + self._rotation) % character_map_length)
            for key, value in self.default_character_map.items()
        }
        self.flipped_cipher_map = flip_dict(self.cipher_map)

    def encrypt(self, plain_text):
        plain_text = plain_text.lower()

        encrypted = ""
        for character in plain_text:
            if character in self.default_character_map:
                encrypted += self.flipped_cipher_map[
                    self.default_character_map[character]
                ]
            else:
                encrypted += character

        return encrypted

    def decrypt(self, encrypted):
        encrypted = encrypted.lower()

        plain_text = ""
        for character in encrypted:
            if character in self.default_character_map:
                plain_text += self.flipped_default_character_map[
                    self.cipher_map[character]
                ]
            else:
                plain_text += character

        return plain_text
