from flask import request
from modelagem_de_negocios.util import bd

class LoginCliente:
    def loga(self):
        username = request.form['nme_cliente']
        password = request.form['senha']
        mysql = bd.SQL('Ce5tvx5KvM', 'xq09k27yty', 'Ce5tvx5KvM')

        cmd = '''SELECT * FROM tb_conta_cliente
        WHERE nme_cliente=%s AND senha_cliente=%s;'''
        cs = mysql.consultar(cmd, [username, password])
        validaLogin = cs.fetchone()

        try:
            if username in validaLogin and password in validaLogin:
                return True
        except:
            return False

    def getDados(self, dado):
        username = request.form['nme_cliente']
        password = request.form['senha']
        mysql = bd.SQL('Ce5tvx5KvM', 'xq09k27yty', 'Ce5tvx5KvM')

        cmd = '''SELECT * FROM tb_conta_cliente
        WHERE nme_cliente=%s AND senha_cliente=%s;'''
        cs = mysql.consultar(cmd, [username, password])
        user_sessao = cs.fetchone()

        if dado == 'id':
            return user_sessao[0]
        elif dado == 'user':
            return user_sessao[1]
        elif dado == 'cep':
            cep_int = int(''.join(n for n in user_sessao[3] if n.isdecimal()))
            return cep_int

class LoginEmpresa:
    def loga(self):
        username = request.form['nme_empresa']
        password = request.form['senha']
        mysql = bd.SQL('Ce5tvx5KvM', 'xq09k27yty', 'Ce5tvx5KvM')

        cmd = '''SELECT * FROM tb_conta_empresa
        WHERE nme_empresa=%s AND senha_empresa=%s;'''
        cs = mysql.consultar(cmd, [username, password])
        validaLogin = cs.fetchone()

        try:
            if username in validaLogin and password in validaLogin:
                return True
        except:
            return False

    def getDados(self, dado):
        username = request.form['nme_empresa']
        password = request.form['senha']
        mysql = bd.SQL('Ce5tvx5KvM', 'xq09k27yty', 'Ce5tvx5KvM')

        cmd = '''SELECT * FROM tb_conta_empresa
        WHERE nme_empresa=%s AND senha_empresa=%s;'''
        cs = mysql.consultar(cmd, [username, password])
        user_sessao = cs.fetchone()

        if dado == 'id':
            return user_sessao[0]
        elif dado == 'user':
            return user_sessao[1]
        elif dado == 'cnpj':
            return user_sessao[3]