from flask import Flask, render_template, request, flash
import forms, os, utils, yagmail, jsonify

app = Flask(__name__)

app.secret_key = os.urandom(15)
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['Name']
            password = request.form['Password']

            if not username:
                error = "Debes ingresar el usuario"
                flash(error)
                return render_template('login.html')
            if not password:
                error = "Contraseña es requerida"
                flash(error)
                return render_template('login.html')

            print("usuario" + username + " clave:" + password)

            if username == "Admin" and password == "GrupoD1234":
                return render_template('principalAdmin.html')
            elif username == "Empleado" and password == "GrupoD1234":
                return render_template('principalEmpleado.html')
            else:
                error = "usuario y/o contraseña inválidos"
                flash(error)
                return render_template('login.html')

        return render_template('login.html')
    except TypeError as e:
        print("Ocurrio un error:", e)
        return render_template('login.html')


@app.route('/admin')
def admin():
    return render_template('principalAdmin.html')


@app.route('/employee')
def employee():
    return render_template('principalEmpleado.html')


@app.route('/admin/product')
def product():
    return render_template('producto.html')


@app.route('/admin/add-employee')
def add_employee():
    return render_template('agregarUsuario.html')


@app.route('/admin/add-employee-done', methods=("GET", "POST"))
def add_employee_submit():
    try:
        if request.method == 'POST':
            emp_user = request.form['Name']
            emp_pass = request.form['Password']
            emp_email = request.form['email']
            error = None

            if not utils.isUsernameValid(emp_user):
                error = "El usuario debe ser alfanumerico"
                flash(error)
                return render_template('agregarUsuario.html')

            if not utils.isEmailValid(emp_email):
                error = 'Correo inválido'
                flash(error)
                return render_template('agregarUsuario.html')

            if not utils.isPasswordValid(emp_pass):
                error = 'La contraseña debe tener por los menos una mayúcscula y una mínuscula y 8 caracteres'
                flash(error)
                return render_template('agregarUsuario.html')

            serverEmail = yagmail.SMTP('misiontic.2020.grupod@gmail.com', 'Karen.1234')

            serverEmail.send(to=emp_email, subject='Activa tu cuenta',
                             contents='Bienvenido, usa este link para activar tu cuenta')

            flash('Revisa tu correo para activar tu cuenta')

            return render_template('login.html')
        return render_template('agregarUsuario.html')
    except Exception as e:
        print("Ocurrio un eror:", e)
        return render_template('agregarUsuario.html')


@app.route('/admin/product/add')
def add_product():
    #form_add = forms.Product()
    #return render_template("agregarProducto.html", form=form_add)
    return render_template("agregarProducto.html")


@app.route('/admin/product/add-done', methods=("GET", "POST"))
def add_product_submit():
    try:
        if request.method == 'POST':
            prod_id = request.form['Id']
            prod_name = request.form['Name']
            prod_quantity = request.form['Quantity']
            prod_description = request.form['Description']
            prod_image = request.form['Image']

            return render_template('producto.html')
    except Exception as e:
        return render_template('agregarProducto.html')


@app.route('/admin/product/mod')
def mod_product():
    return render_template('modificarProducto.html')


@app.route('/admin/product/mod-done', methods=("GET", "POST"))
def mod_product_submit():
    try:
        if request.method == 'POST':
            prod_mod_id = request.form['Id']
            prod_mod_name = request.form['Name']
            prod_mod_quantity = request.form['Quantity']
            prod_mod_description = request.form['Description']
            prod_mod_image = request.form['Image']

            return render_template('producto.html')
    except Exception as e:
        return render_template('modificarProducto.html')


@app.route('/employee/product-id')
def inventory():
    return render_template('editarCantidadProducto.html')


@app.route('/forgot', methods=('POST', 'GET'))
def forgot():
    try:
        if request.method == 'POST':
            email = request.form['email']
            error = None

            if not utils.isEmailValid(email):
                error = 'Correo inválido'
                flash(error)
                return render_template('forgot.html')


            serverEmail = yagmail.SMTP('misiontic.2020.grupod@gmail.com', 'Karen.1234')

            serverEmail.send(to=email, subject='Recuperar contraseña',
                             contents='Hola! haz olvidado tu contraseña..... Esta es tu contraseña:')

            flash('Revisa tu correo para activar tu cuenta')

            return render_template('login.html')
        return render_template('forgot.html')
    except Exception as e:
        print("Ocurrio un eror:", e)
        return render_template('forgot.html')


if __name__ == '__main__':
    app.run()
