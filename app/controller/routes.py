from app import app
from flask import render_template, redirect
from app.model.models import EmpresaModel
from app.model.forms import FormEmpresa, FormNotaDebito
from app import db
'''
Este arquivo contém as rotas de cada uma das páginas do sistema web  
com as suas funçõs e renderiza o template (arquivo .html) para a rota. 
'''

@app.route("/", methods=["get", "post"])
@app.route("/index", methods=["get", "post"])
def index():
    '''Home page do programa

    Este método chama a página index e checa se há algua empresa cadastrada,
    se tiver carrega a lista de empresas do banco em uma tabela html.
    '''
    lista_empresas = []
    empresas = EmpresaModel.query.all()
    if empresas:
        lista_empresas = empresas
    return render_template("index.html", empresas=lista_empresas)

@app.route("/cadastrar_empresa", methods=["get", "post"])
def cadastrar_empresa():
    '''Formulário de cadastro de empresas

    Um formulário para cadastrar as empresas a partir do nome delas, 
    após confirmar adiciona a empresa na tabela do banco de dados e seta
    os valores default do indice de 50. 
    '''
    form = FormEmpresa()
    if form.validate_on_submit():
        empresa = EmpresaModel(nome=form.nome.data)
        db.session.add(empresa)
        db.session.commit()
        return redirect("/index")
    return render_template("cadastrar_empresa.html", 
                           form=form)

@app.route("/adicionar_notas_debitos/<nome>", methods=["post", "get"])
def adicionar_notas_debitos(nome):
    '''Adiciona notas e débitos à empresa selecionada.

    Um formulário que adiciona débitos e notas e calcula o novo índice
    da empresa, atualizando o indice, a quantidade de notas e de débitos
    no banco.

    Parameters
    ----------
    nome : str
        nome da empresa selecionada na tela anterior 
    '''
    form = FormNotaDebito()
    empresa = EmpresaModel.query.filter_by(nome=nome).first()
    if form.validate_on_submit():
    
        notas = form.notas.data + empresa.notas
        debitos = form.debitos.data + empresa.debitos
        indice = empresa.indice
        if notas != 0:
            indice = indice * ((1 + 0.02)**notas)
        if debitos != 0:
            indice = indice * ((0.96)**debitos)
        indice = round(indice)
        if indice > 100:
            indice = 100
        elif indice < 0:
            indice = 0

        empresa_atualizada = EmpresaModel(indice=indice, 
                                          notas=notas,
                                          debitos=debitos,
                                          nome=nome)
        db.session.merge(empresa_atualizada)
        db.session.commit()
        return redirect("/index")
    return render_template("add_notas_debitos.html", 
                           form=form,
                           nome=nome)