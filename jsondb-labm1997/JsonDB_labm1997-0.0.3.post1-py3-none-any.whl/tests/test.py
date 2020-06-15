from JsonDB import JsonDB


class TestInstantiate:

    def test_nofile(self, tmpdir):
        """Testa se consegue instanciar de um arquivo que não existe"""
        jsonDB = JsonDB(tmpdir + "/test.json")

        assert jsonDB.getJSON() == {}

    def test_nofile_default(self, tmpdir):
        """Testa se consegue instanciar de um arquivo que não existe e retornar o JSON padrão"""
        jsonDB = JsonDB(tmpdir + "/test.json", {"chave1": "valor1", "chave2": "valor2"})

        assert jsonDB.getJSON() == {"chave1": "valor1", "chave2": "valor2"}

    def test_nofile_save(self, tmpdir):
        """Testa se está salvando o JSON depois do flush"""
        jsonDB = JsonDB(tmpdir + "/test.json", {"chave1": "valor1", "chave2": "valor2"})

        json = jsonDB.getJSON()
        json["chave1"] = "novovalor1"

        jsonDB.flush()

        jsonDB_new = JsonDB(tmpdir + "/test.json", {"chave1": "valor1", "chave2": "valor2"})
        assert jsonDB_new.getJSON() == {"chave1": "novovalor1", "chave2": "valor2"}

    def test_default_with_more_params(self, tmpdir):
        """Testa se novas chaves em default são criadas, mesmo que o arquivo já tenha sido gerado"""
        jsonDB_old = JsonDB(tmpdir + "/test.json", {"chave1": "valor1", "chave2": "valor2"})

        jsonDB_new = JsonDB(tmpdir + "/test.json", {"chave1": "valor1", "chave2": "valor2", "chave3": "valor3"})
        assert jsonDB_new.getJSON() == {"chave1": "valor1", "chave2": "valor2", "chave3": "valor3"}

    def test_default_with_less_params(self, tmpdir):
        """Testa se chaves em retiradas default são removidas, mesmo que o arquivo já tenha sido gerado"""
        jsonDB_old = JsonDB(tmpdir + "/test.json", {"chave1": "valor1", "chave2": "valor2"})

        jsonDB_new = JsonDB(tmpdir + "/test.json", {"chave1": "valor1"})
        assert jsonDB_new.getJSON() == {"chave1": "valor1"}

    def test_flush_all(self, tmpdir):
        """Se salva todos os DBs abertos com flushAll"""
        jsonDB1 = JsonDB(tmpdir + "/test1.json", {"chave1": "valor1", "chave2": "valor2"})
        jsonDB2 = JsonDB(tmpdir + "/test2.json", {"chave3": "valor3", "chave4": "valor4"})

        jsonDB1.getJSON()["chave1"] = "novovalor1"
        jsonDB2.getJSON()["chave4"] = "novovalor4"

        JsonDB.flushAll()

        jsonDB1_new = JsonDB(tmpdir + "/test1.json", {"chave1": "valor1", "chave2": "valor2"})
        jsonDB2_new = JsonDB(tmpdir + "/test2.json", {"chave3": "valor3", "chave4": "valor4"})

        assert jsonDB1_new.getJSON() == {"chave1": "novovalor1", "chave2": "valor2"}
        assert jsonDB2_new.getJSON() == {"chave3": "valor3", "chave4": "novovalor4"}
