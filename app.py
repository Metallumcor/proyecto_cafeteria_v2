from flask import Flask, render_template, request, flash
import forms, os

app = Flask(__name__)

app.secret_key = os.urandom(24)
@app.route('/')
@app.route('/login')
def login():
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

            return render_template('principalAdmin.html')
    except Exception as e:
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


if __name__ == '__main__':
    app.run()
