import functools

from flask import Flask, render_template, request, flash, redirect, session, g

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import db
import forms
import os
import utils
import yagmail

app = Flask(__name__)

app.secret_key = os.urandom(15)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.User()
    try:
        if g.user:
            return redirect('/logout')
        if request.method == 'POST':
            database = db.get_db()
            username = form.name.data
            password = form.password.data

            user = database.execute('SELECT * FROM USER WHERE username=? AND password=?',
                                    (username, password)).fetchone()

            if user is None:
                database.close()
                return render_template("login.html", form=form)
            elif password=="GrupoD1234":
            #elif check_password_hash(user[3], password):
                print(generate_password_hash(password))
                session.clear()
                session['user_id'] = user[0]
                session['role'] = user[1]
                database.close()
                if session.get('role') == 1:
                    return redirect("/admin")
                elif session.get('role') == 2:
                    return redirect("/employee")
            else:
                print("Error inesperado")
        return render_template("login.html", form=form)
    except TypeError as e:
        print("Ocurrio un error:", e)
        return render_template('login.html', form=form)


def login_required(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( "/login" )
        return view( **kwargs )

    return wrapped_view


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")


@app.before_request
def load_logged_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.get_db().execute(
            'SELECT * FROM USER WHERE usr_id=?', (user_id,)
        ).fetchone()
        db.close_db()


@app.route('/admin')
@login_required
def admin():
    return render_template('principalAdmin.html')


@app.route('/employee')
@login_required
def employee():
    return render_template('principalEmpleado.html')


@app.route('/admin/product')
@login_required
def product():
    return render_template('producto.html')


@app.route('/admin/add-employee', methods=("GET", "POST"))
@login_required
def add_employee():
    form = forms.User()
    try:
        if form.validate_on_submit():
            emp_user = form.name.data
            emp_pass = form.password.data
            emp_email = form.email.data
            emp_role = form.role.data
            role_dict = {"Administrador": 1, "Empleado": 2}
            error = None

            if not utils.isUsernameValid(emp_user):
                error = "El usuario debe ser alfanumerico"
                flash(error)
                print(error)
                return render_template('agregarUsuario.html', form=form)

            if not utils.isEmailValid(emp_email):
                error = 'Correo inválido'
                flash(error)
                print(error)
                return render_template('agregarUsuario.html', form=form)

            if not utils.isPasswordValid(emp_pass):
                error = 'La contraseña debe tener por los menos una mayúcscula y una mínuscula y 8 caracteres'
                flash(error)
                print(error)
                return render_template('agregarUsuario.html', form=form)

            hashpass = generate_password_hash(emp_pass)

            database = db.get_db()

            query = 'INSERT INTO USER (username,password,email,usr_type,creation_date)' \
                    ' VALUES (?,?,?,?,?)', (emp_user, hashpass, emp_email, role_dict.get(emp_role),
                                            datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
            print(query)

            database.execute('INSERT INTO USER (username,password,email,usr_type,creation_date) '
                             'VALUES (?,?,?,?,?)', (emp_user, hashpass, emp_email, role_dict.get(emp_role),
                                                    datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
                             )
            database.commit()

            serverEmail = yagmail.SMTP('misiontic.2020.grupod@gmail.com', 'Karen.1234')

            serverEmail.send(to=emp_email, subject='Activa tu cuenta',
                             contents='Bienvenido, usa este link para activar tu cuenta')

            return redirect("/admin")
        else:
            return render_template('agregarUsuario.html', form=form)
    except Exception:
        return render_template('agregarUsuario.html', form=form)


@app.route('/admin/product/add', methods=("GET", "POST"))
@login_required
def add_product():
    form = forms.Product()
    try:
        if form.validate_on_submit():
            prod_id = form.id.data
            prod_name = form.name.data
            prod_quantity = form.quantity.data
            prod_description = form.desc.data
            prod_image = form.img.data
            prod_status = True

            database = db.get_db()

            if database.execute('SELECT * FROM PRODUCT WHERE prd_id=?', [prod_id]).fetchone() is not None:
                error = 'El producto ya existe'
                flash(error)
                return render_template('agregarProducto.html', form=form)

            database.execute('INSERT INTO PRODUCT (prd_id,name,description,inventory,active) '
                             'VALUES (?,?,?,?,?)', (prod_id, prod_name, prod_description, prod_quantity,
                                                    prod_status)
                             )
            database.commit()
            return redirect("/admin/product")
        return render_template('agregarProducto.html', form=form)
    except Exception:
        return render_template('agregarProducto.html', form=form)


@app.route('/admin/product/mod', methods=("GET", "POST"))
@login_required
def mod_product():
    form = forms.Product()
    try:
        if form.validate_on_submit():
            prod_mod_id = form.id.data
            prod_mod_name = form.name.data
            prod_mod_quantity = form.quantity.data
            prod_mod_description = form.desc.data
            prod_mod_image = form.img.data

            database = db.get_db()
            database.execute('UPDATE PRODUCT SET name=?, quantity=?, description=? WHERE prd_id=?',
                             (prod_mod_name, prod_mod_description, prod_mod_quantity, prod_mod_id)
                             )
            database.commit()
            return redirect("/admin/product")
        return render_template('modificarProducto.html', form=form)
    except Exception:
        return render_template('modificarProducto.html', form=form)
'''
        return redirect("/product", form=form)
        else:
            render_template("modificarProducto.html", form=form)
    except Exception as e:
        return render_template('modificarProducto.html', form=form)'''


@app.route('/employee/product-id')
@login_required
def inventory():
    return render_template('editarCantidadProducto.html')


@app.route('/forgot', methods=('POST', 'GET'))
def forgot():
    form = forms.User()
    try:
        if g.user:
            return redirect('/logout')
        if form.validate_on_submit():
            email = form.email.data
            error = None

            if not utils.isEmailValid(email):
                error = 'Correo inválido'
                flash(error)
                return render_template('forgot.html', form=form)

            serverEmail = yagmail.SMTP('misiontic.2020.grupod@gmail.com', 'Karen.1234')

            serverEmail.send(to=email, subject='Recuperar contraseña',
                             contents='Hola! haz olvidado tu contraseña..... Esta es tu contraseña:')

            flash('Revisa tu correo para activar tu cuenta')

            return redirect("/login")
        return render_template('forgot.html', form=form)
    except Exception:
        return render_template('forgot.html', form=form)


if __name__ == '__main__':
    app.run()
