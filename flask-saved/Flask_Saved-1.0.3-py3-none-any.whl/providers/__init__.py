class BaseStorage:
    
    def generate_url(self, filename):
        raise NotImplementedError

    def read(self, filename):
        raise NotImplementedError

    def save(self, f, filename):
        raise NotImplementedError

    def delete(self, filename):
        raise NotImplementedError