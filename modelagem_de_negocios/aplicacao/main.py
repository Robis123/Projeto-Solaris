from flask import Flask, render_template, session, flash, url_for, redirect
from modelagem_de_negocios.persistencia import login, cadastro
from modelagem_de_negocios.util import pathing
from modelagem_de_negocios.aplicacao import algoritmo

'''
set FLASK_DEBUG=1
set FLASK_ENV=development
set FLASK_APP=modelagem_de_negocios.aplicacao.main.py
flask run
'''

rota = pathing.Path()
app = Flask(__name__, template_folder=rota.templateWay(), static_folder=rota.staticWay())
app.secret_key = 'ventodonorte'


@app.route('/')
def index():
    session['usuario_logado'] = None
    return render_template('index.html')


@app.route('/index')
def indexlogado():
    if session['usuario_logado'] != None:
        return redirect(url_for('indexcliente'))
    elif session['empresa_logada'] != None:
        return render_template('indexempresa.html')

    return redirect(url_for('index'))


# ---FUNCIONALIDADES---
@app.route('/quemsomos')
def quemSomos():
    return render_template('quemsomos.html')


# ---PROPOSTA---
@app.route('/proposta')
def proposta():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Voce deve estar logado para acessar esta função')
        return redirect(url_for('formLogin'))
    return render_template('algoritmo.html')


@app.route('/geraproposta', methods=['POST'])
def geraProposta():
    proposta = algoritmo.Proposta()
    res = proposta.calculo(session['cep'])
    validacao = proposta.validacaoCEP(session['cep'])
    sgl = validacao[1]
    empresas = proposta.getEmpresas(sgl)
    return render_template('proposta.html', rep=res, empresas=empresas)


# ---CADASTRO---
@app.route('/cadastro')
def formCadastro():
    return render_template('cadastro.html')


@app.route('/cadastracliente', methods=['POST'])
def cadastraCliente():
    cad_c = cadastro.ContaCliente()
    if cad_c.cadastra() == 'usuario_invalido':
        flash('Usuário informado já existe!')
        return redirect(url_for('formCadastro'))

    elif cad_c.cadastra() == 'senha_invalida':
        flash('Senha inválida! A senha deve conter:'
              '* Ao menos 8 caracteres;'
              '* Ao menos uma letra;'
              '* Ao menos um número;'
              '* Ao menos um caractere especial (_, @, $)')
        return redirect(url_for('formCadastro'))

    flash('Cliente cadastrado com sucesso!')
    return redirect(url_for('formLogin'))


@app.route('/cadastraempresa', methods=['POST'])
def cadastraEmpresa():
    cad_e = cadastro.ContaEmpresa()

    if cad_e.cadastra() == 'usuario_invalido':
        flash('Usuário informado já existe!')
        return redirect(url_for('formCadastro'))

    elif cad_e.cadastra() == 'senha_invalida':
        flash('Senha inválida! A senha deve conter:'
              '* Ao menos 8 caracteres;'
              '* Ao menos uma letra;'
              '* Ao menos um número;'
              '* Ao menos um caractere especial (_, @, $)')
        return redirect(url_for('formCadastro'))

    flash('Empresa cadastrada com sucesso!')
    return redirect(url_for('formLogin'))


# ---LOGIN---
@app.route('/login')
def formLogin():
    return render_template('login.html')


@app.route('/logincliente', methods=['POST'])
def loginCliente():
    log_c = login.LoginCliente()

    if log_c.loga():
        session['usuario_logado'] = log_c.getDados('id')
        session['cep'] = int(log_c.getDados('cep'))
        session['user'] = log_c.getDados('user')
        flash(f"Olá, {session['user']}! Login efetuado com sucesso!")
        return render_template('indexcliente.html')

    flash('Usuário ou senha incorretos, tente novamente')
    return redirect(url_for('formLogin'))


@app.route('/loginempresa', methods=['POST'])
def loginEmpresa():
    log_e = login.LoginEmpresa()

    if log_e.loga():
        session['empresa_logada'] = log_e.getDados('id')
        session['user'] = log_e.getDados('user')
        flash(f"Olá, {session['user']}! Login efetuado com sucesso!")
        return render_template('indexempresa.html')

    flash(f'Usuário ou senha incorretos, tente novamente')
    return redirect(url_for('formLogin'))


# ---LOGOUT---
@app.route('/logout')
def logout():
    if session['usuario_logado'] == None or session['empresa_logada'] == None:
        flash('Atualmente você não se encontra em nenhuma sessão')
        return redirect(url_for('index'))

    session['usuario_logado'] = None
    session['empresa_logada'] = None
    session['cep'] = None
    session['user'] = None
    flash('Usuário deslogado, faça o login novamente para ter acesso a todas funcionalidades do site')

    return redirect(url_for('index'))


# ---ALTERAR---
@app.route('/alterar')
def alterar():

    proposta = algoritmo.Proposta()
    empresa = proposta.get_uma_empresa(session['empresa_logada'])
    return render_template('alterar.html', empresa=empresa)


@app.route('/alterarinformacoes', methods=['POST'])
def alterardados():
    proposta = algoritmo.Proposta()
    msg = proposta.updateDados(session['empresa_logada'])
    if session['empresa_logada'] == None:
        flash('Atualmente você não se encontra em nenhuma sessão')
        return redirect(url_for('index'))
    flash(msg)
    return render_template('indexempresa.html')


app.run()
