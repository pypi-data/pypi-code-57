import re


class CaseConverter:
    def key_to_snake_case(self, key):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()

    def key_to_camel_case(self, key):
        split_key = key.split('_')
        output = []
        for index, item in enumerate(split_key):
            if index != 0:
                item = item.capitalize()

            output.append(item)

        return ''.join(output)

    def convert_to_camel_case(self, input):
        if type(input) == list:
            return [self.convert_to_camel_case(value) for value in input]

        if type(input) == dict:
            for key in input.keys():
                camel_case_key = self.key_to_camel_case(key)
                value = input.pop(key)

                if type(value) == dict or type(value) == list:
                    value = self.convert_to_camel_case(value)

                input[camel_case_key] = value

            return input

        return input

    def convert_to_snake_case(self, input):
        if type(input) == list:
            return [self.convert_to_snake_case(value) for value in input]

        if type(input) == dict:
            for key in input.keys():
                snake_case_key = self.key_to_snake_case(key)
                value = input.pop(key)

                if type(value) == dict or type(value) == list:
                    value = self.convert_to_snake_case(value)

                input[snake_case_key] = value

            return input

        return input
