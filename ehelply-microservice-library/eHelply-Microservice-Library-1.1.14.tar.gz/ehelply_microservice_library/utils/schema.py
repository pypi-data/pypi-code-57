from pydantic import BaseModel


class eHelplySchema(BaseModel):
    """
    Extended Pydantic base model which adds helper functions for ease of use
    """

    def map(self, obj, whitelist: list = None):
        """
        Maps pydantic model values to another object.

        If whitelist is specified, it will only map those keys, otherwise, it maps all the keys

        Args:
            obj:
            whitelist:

        Returns:

        """
        my_data: dict = self.dict()
        if whitelist:
            for key in whitelist:
                if key in my_data and my_data[key] is not None:
                    setattr(obj, key, my_data[key])
        else:
            for key, value in my_data.items():
                if value is not None:
                    setattr(obj, key, value)
        return obj
