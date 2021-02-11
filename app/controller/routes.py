from app import app
from flask import render_template, redirect
from app.model.models import EmpresaModel
from app.model.forms import formEmpresa, formNotaDebito
from app import db
'''
Este arquivo contém as rotas de cada uma das páginas do sistema web  
com as suas funçõs e renderiza o template (arquivo .html) para a rota. 
'''

@app.route("/", methods=["get", "post"])
@app.route("/index", methods=["get", "post"])
def index():
    lista_empresas = []
    empresas = EmpresaModel.query.all()
    if empresas:
        lista_empresas = empresas
    return render_template("index.html", empresas=lista_empresas)

@app.route("/cadastrar_empresa", methods=["get", "post"])
def cadastrar_empresa():
    form = formEmpresa()
    if form.validade_on_submit():
        empresa = EmpresaModel(nome=form.nome.data)
        db.session.add(empresa)
        db.session.commit()
        return redirect("/index")
    return render_template("cadastrar_empresa.html", 
                           form=form)

@app.route("/adicionar_notas_debitos/<nome>", methods=["post", "get"])
def adicionar_notas_debitos(nome):
    form = formNotaDebito()
    empresa = EmpresaModel.query.filter_by(nome=nome)
    if form.validade_on_submit():
        notas = form.notas.data
        debitos = form.debito.data
        indice = empresa.indice
        if notas != 0:
            indice = indice * ((1 + 0.02)**notas)
        if debito != 0:
            indice = indice * ((1 + 0.02)**debitos)
        empresa_atualizada = EmpresaModel(indice=indice, 
                                          notas=notas,
                                          debitos=debitos)
        db.session.add(empresa_atualizada)
        db.session.commit()
        return redirect("/index")
    return render_template("add_notas_debitos.html", 
                           form=form,
                           nome=nome)