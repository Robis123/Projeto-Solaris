import mysql.connector

class SQL:
    def __init__(self, usuario, senha, esquema):
        self.cnx = mysql.connector.connect(user=usuario, password=senha, host='remotemysql.com', database=esquema)

    def executar(self, comando, parametros):
        cs = self.cnx.cursor()
        cs.execute(comando, parametros)
        self.cnx.commit()
        cs.close()
        return True

    def consultar(self, comando, parametros):
        cs = self.cnx.cursor()
        cs.execute(comando, parametros)
        return cs

    def __del__(self):
        self.cnx.close()