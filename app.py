from flask import Flask, render_template, request, flash

app = Flask(__name__)


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


@app.route('/admin/product/add')
def add_product():
    return render_template('agregarProducto.html')


@app.route('/admin/product/mod')
def mod_product():
    return render_template('modificarProducto.html')


@app.route('/employee/product-id')
def inventory():
    return render_template('editarCantidadProducto.html')


if __name__ == '__main__':
    app.run()
