from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, make_response
from markupsafe import Markup
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from app import app, db, bcrypt, login_manager, mail
from werkzeug.security import generate_password_hash
from app.models import Ingresso_registrado6, Comprador_registrado3
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

# Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return Comprador_registrado3.query.get(int(user_id))

# Decorador para garantir que somente administradores possam acessar
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Você precisa estar logado para acessar esta página.')
            return redirect(url_for('login_adm'))

        if not current_user.is_admin:
            flash('Acesso negado. Você não tem permissões de administrador.')
            return redirect(url_for('login_adm'))

        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    logado = current_user.is_authenticated
    return render_template('index.html', logado=logado)

# Cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        name = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cpf = request.form['cpf']
        numero = request.form['numero']
        confirmar_senha = request.form['confirmar_senha']

        # Verificar se as senhas coincidem
        if senha != confirmar_senha:
            return "Senhas não coincidem", 400

        # Verificar se o e-mail ou cpf já estão registrados
        if Comprador_registrado3.query.filter_by(email=email).first():
            return 'Esse email já existe'
        if Comprador_registrado3.query.filter_by(cpf=cpf).first():
            return 'Esse CPF já existe'
        
        # Criar novo usuário
        novo_user = Comprador_registrado3(
            name=name,
            email=email,
            senha=bcrypt.generate_password_hash(senha).decode('utf-8'),
            cpf=cpf,
            numero=numero
        )
        db.session.add(novo_user)
        db.session.commit()

        # Login automático do novo usuário
        login_user(novo_user)
        return redirect(url_for('index'))

    return render_template('cadastro.html')

# Login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(Markup('Você já está conectado, que tal <a href="/add_ingressos">comprar um ingresso?</a>'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Comprador_registrado3.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos')
    
    return render_template('login.html')

# Login de administradores
@app.route('/login_adm', methods=['GET', 'POST'])
def login_adm():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Comprador_registrado3.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.senha, senha):
            if user.is_admin:
                login_user(user)
                return redirect(url_for('list_adm'))
            else:
                flash('Acesso negado. Você não tem permissões de administrador.')
        else:
            flash('Email ou senha incorretos')
    
    return render_template('login_adm.html')

# Compra de ingressos
@app.route('/add_ingressos', methods=['GET', 'POST'])
@login_required
def add_ingressos():
    # Limpar dados da sessão, se houver
    session.pop('ingressos', None)  # Caso tenha algum dado da sessão

    users = 100 - Ingresso_registrado6.query.count()
    nome_do_comprador = current_user.name

    if users <= 0:
        flash('Número de ingressos passou do limite, lamento')
        return render_template('add_ingressos.html', nome_do_comprador=nome_do_comprador, users=users)

    if request.method == 'POST':
        ticket_count = 0
        total_valor = 0

        # Valores de ingresso para adulto e infantil
        preco_adulto = 120.00
        preco_infantil = 60.00

        while f'titular-{ticket_count+1}' in request.form:
            ticket_count += 1

        if ticket_count == 0:
            flash('Por favor, adicione pelo menos um ingresso.')
            return render_template('add_ingressos.html', nome_do_comprador=nome_do_comprador, users=users)

        for i in range(ticket_count):
            titular = request.form[f'titular-{i+1}']
            email_contato = request.form[f'email_contato-{i+1}']
            telefone = request.form[f'telefone-{i+1}']
            restricoes_alimentares = request.form.get(f'restricoes_alimentares-{i+1}', '')
            comprador_id = current_user.id
            pago = False
            tipo_verificado = request.form[f'tipo-{i+1}']
            tipo = tipo_verificado == 'infantil'

            # Calcular o valor do ingresso
            if tipo:
                total_valor += preco_infantil
            else:
                total_valor += preco_adulto

            novo_ingresso = Ingresso_registrado6(
                comprador_id=comprador_id,
                titular=titular,
                email_contato=email_contato,
                telefone=telefone,
                restricoes_alimentares=restricoes_alimentares,
                pago=pago,
                tipo=tipo
            )

            db.session.add(novo_ingresso)
        
        db.session.commit()
        flash('Obrigado pela compra! Por favor, realize o pagamento')
        return redirect(url_for('pagamento', total_valor=total_valor))

    # Renderiza a página sem cache
    response = make_response(render_template('add_ingressos.html', nome_do_comprador=nome_do_comprador, users=users))
    
    # Adiciona cabeçalhos para evitar cache
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1
    response.headers['Pragma'] = 'no-cache'  # HTTP 1.0
    response.headers['Expires'] = '0'  # Proxies

    return response


# Página de pagamento
@app.route('/pagamento')
@login_required
def pagamento():
    valor_total = Ingresso_registrado6.valor_total(current_user.id)
    ingressos = Ingresso_registrado6.query.filter_by(comprador_id=current_user.id, pago=False).all()
    
    return render_template('pagamento.html', ingressos=ingressos, nome_usuario=current_user.name, valor_total=valor_total)

# Listagem de ingressos do usuário
@app.route('/list_ingressos_usuario')
@login_required
def list_ingressos_usuario():
    nome_usuario = current_user.name
    comprador = Comprador_registrado3.query.filter_by(id=current_user.id).first()
    ingressos = Ingresso_registrado6.query.filter_by(comprador_id=current_user.id).all()

    if not comprador:
        flash('Comprador não encontrado.')
        return redirect(url_for('index'))

    return render_template('list_ingressos_usuario.html', ingressos=ingressos, nome_usuario=nome_usuario, comprador=comprador)

# Lista de administradores
@app.route('/list_adm', methods=['GET', 'POST'])
@admin_required
def list_adm():
    users = Comprador_registrado3.query.order_by(Comprador_registrado3.id).all()
    ingressos = Ingresso_registrado6.query.order_by(Ingresso_registrado6.id).all()
    compradores = sorted(set(ingresso.comprador for ingresso in ingressos), key=lambda c: c.id)
   

    for key, value in request.form.items():
        if key.startswith('pagamento_'):
            id_ingresso = key.replace('pagamento_', '')
            ingresso = Ingresso_registrado6.query.get(id_ingresso)
            if ingresso:
                ingresso.pago = value == 'pago'
                db.session.commit()

    return render_template('list_adm.html', users=users, compradores=compradores, ingressos=ingressos)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Recuperar senha
@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email_contato = request.form.get('email_contato')
        user = Comprador_registrado3.query.filter_by(email=email_contato).first()

        if user:
            token = s.dumps(user.email_contato, salt='recover-salt')
            reset_url = url_for('redefinir_senha', token=token, _external=True)

            msg = Message('Redefinir Senha', recipients=[email_contato])
            msg.body = f'Clique no link para redefinir sua senha: {reset_url}'
            try:
                mail.send(msg)
                flash('Um e-mail de redefinição de senha foi enviado.', 'success')
            except Exception as e:
                flash(f'Ocorreu um erro ao enviar o e-mail: {str(e)}', 'danger')

            return redirect(url_for('login'))

        flash('E-mail não encontrado.', 'danger')

    return render_template('recuperar_senha.html')

@app.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    try:
        email_contato = s.loads(token, salt='recover-salt', max_age=3600)
    except:
        flash('O link de redefinição de senha expirou ou é inválido.', 'danger')
        return redirect(url_for('recuperar_senha'))

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha')
        user = Comprador_registrado3.query.filter_by(email=email_contato).first()
        user.senha = bcrypt.generate_password_hash(nova_senha).decode('utf-8')

        db.session.commit()

        flash('Sua senha foi redefinida com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('redefinir_senha.html')
