from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Comprador, Ingresso

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_comprador', methods=['GET', 'POST'])
def add_comprador():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        novo_comprador = Comprador(nome=nome, email=email)
        db.session.add(novo_comprador)
        db.session.commit()
        return redirect(url_for('list_compradores'))
    return render_template('add_comprador.html')

@app.route('/add_ingresso', methods=['GET', 'POST'])
def add_ingresso():
    compradores = Comprador.query.all()  # Buscar todos os compradores para o dropdown
    if request.method == 'POST':
        evento = request.form['evento']
        comprador_id = request.form['comprador_id']
        titular = request.form['titular']
        email_contato = request.form['email_contato']
        telefone = request.form['telefone']
        pago = 'pago' in request.form
        restricoes_alimentares = request.form.get('restricoes_alimentares', '')

        novo_ingresso = Ingresso(
            evento=evento,
            comprador_id=comprador_id,
            titular=titular,
            email_contato=email_contato,
            pago=pago,
            telefone=telefone,
            restricoes_alimentares=restricoes_alimentares
        )

        db.session.add(novo_ingresso)
        db.session.commit()
        return redirect(url_for('list_ingressos'))
    return render_template('add_ingresso.html', compradores=compradores)

@app.route('/list_compradores')
def list_compradores():
    compradores = Comprador.query.all()
    return render_template('list_compradores.html', compradores=compradores)

@app.route('/list_ingressos')
def list_ingressos():
    ingressos = Ingresso.query.all()
    return render_template('list_ingressos.html', ingressos=ingressos)
