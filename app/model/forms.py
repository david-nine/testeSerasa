from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

'''
Este arquivo contém os formulários para adiconar uma empresa e para
adicionar notas e débitos uma empresa
'''

class formEmpresa(FlaskForm):
    '''Formulário para adicionar empresas manualmente no banco

    Atributes
    ---------
    nome : str
        Campo para adicionar o nome da empresa a se adicionar
    submit : boolean
        Botão para enviar o formulário 
    '''
    nome = StringField("Nome da empresa", validatos=[Required("colque o nome da empresa")])
    submit = SubmitField("Confirmar")

class formNotaDebito(FlaskForm):
    '''Formulário para adicionar notas e débitos a uma empresa

    Atributes
    ---------
    notas : int
        Campo para adicionar a quantidade de notas emitidas pela empresa
    debitos : int
        Campo para adicionar a quantidade de débitos emitidos pela empresa
    submit : boolean
        Botão para enviar o formulário
    '''
    notas = IntegerField("Quantidade de notas")
    debitos = IntegerField("Quantidade de débitos")
    submit = SubmitField("Confirmar")