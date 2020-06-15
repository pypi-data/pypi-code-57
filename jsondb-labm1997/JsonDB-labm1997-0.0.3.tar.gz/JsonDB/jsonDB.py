import json
import os.path

class JsonDB():
    instances = []
    """Instâncias de JsonDB"""

    def __init__(self, filename, default={}):
        """Inicializa o banco com base em `filename`. Recebe um JSON padrão em `default`"""

        self.filename = filename

        # Arquivo não existe
        if not os.path.isfile(filename):
            with open(filename, 'w') as outfile: json.dump(default, outfile)
        
        # Lê do arquivo
        with open(filename, 'r') as jsonfile: rawjson = json.load(jsonfile)

        # Molda o JSON com base nas chaves em default
        self.json = { k : rawjson[k] if k in rawjson else default[k] for k in default }

        # Salva a instância
        JsonDB.instances.append(self)
    
    def getJSON(self):
        """Obtém a referência para o JSON lido"""
        return self.json

    def flush(self):
        """Salva no arquivo o JSON"""
        with open(self.filename, 'w') as outfile:
            json.dump(self.json, outfile)

    def flushAll():
        """Salva em arquivos JSON todos os DBs abertos"""
        for jsonDB in JsonDB.instances: jsonDB.flush()
