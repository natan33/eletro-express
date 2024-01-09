from app import app ,db
from flask import render_template,url_for,flash,redirect,request
from urllib.parse import urlparse
from flask_login import login_user,logout_user,login_required
from app.models import User, Items
from app.forms import *
from instrucoes import *

@app.route('/')
def page_home():
    titulo = "HomePage"
    return render_template('index.html',titulo=titulo)


@app.route('/sobre/<usuario>')
def page_sobre(usuario):
    titulo = "EletroExpress - Sobre"
    return render_template('sobre.html',titulo=titulo,user=usuario)



@app.route('/produtos', methods=['POST','GET'])
@login_required
def page_produtos():
    itens = Items.query.all()
    titulo = "EletroExpress - Produtos"
    return render_template('produtos.html',titulo=titulo,itens=itens)
    



@app.route('/create-produts', methods=['POST', 'GET'])
def page_cadastro_produtos():
    produto = ProductsForm()

    if produto.validate_on_submit():
        try:
            cod_barra = gerar_cod_barra()
            itens = Items(name=produto.name.data, preco=produto.price.data,
            cod_barra=cod_barra,
            description=produto.description.data)
            print(itens)
            db.session.add(itens)
            db.session.commit()
        except Exception as e:
            print(e)

        flash('Produto, foi cadastrado com sucesso! ',category='sucess')
        return redirect(url_for('page_produtos'))

    titulo = "EletroExpress - Cadastro de Produtos"
    return render_template('cadastra_produto.html',titulo=titulo,form=produto)



@app.route('/login',methods=["GET", "POST"])
def page_login():
    form = LoginForm()
    # faz a validação do login do usuario 
    if form.validate_on_submit():
        user_login = User.query.filter_by(username=form.username.data).first()
        if user_login and user_login.check_password(password_rcript=form.password.data):
            login_user(user_login)
            flash(f"Sucesso! Seu Login é: {user_login.username}", category='sucess')
            return redirect(url_for('page_produtos'))

        else:        
            flash(f'Invalid username or password',category='danger')
    titulo = "EletroExpress - Login"
    return render_template('login.html',titulo=titulo,form=form)


@app.route('/logout')
def page_logout():
    logout_user()
    flash("Você fez o logout",category="info")
    return redirect(url_for('page_home'))


@app.route('/cadastro',methods=['POST','GET'])
def page_cadastro():
    registro = RegistrationForm()
    # Cadastra o usuario no forms
    if registro.validate_on_submit():
        usuario = User(username= registro.username.data,
                       email = registro.email.data,
                        passwordcrip = registro.password.data
                        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('page_home'))
    
    # Valida se os campos foram cadastrados corretamente
    if registro.errors != {}:
        for err in registro.errors.values():
            flash(f"Erro ao cadastrar usuario {err}", category="danger") 
    titulo = "EletroExpress - Cadastre-se"
    return render_template('cadastro.html',titulo=titulo,form=registro)