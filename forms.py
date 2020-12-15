from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, FileField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, ValidationError


class User(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(message="Este campo es obligatorio"), Length(min=5, max=20)])
    password = PasswordField("Contraseña", validators=[DataRequired(message="Este campo es obligatorio"),
                                                       Length(min=8, max=20)])
    email = StringField("Correo", validators=[DataRequired(message="Este campo es obligatorio")],
                        render_kw={"placeholder": "nombre@"})
    '''img = FileField("Subir imagen", validators=[DataRequired(message="Este campo es obligatorio")],
                    render_kw={"style": "visibility: hidden"})'''
    role_choices = ["Administrador", "Empleado"]
    role = SelectField("Rol", choices=role_choices, validators=[Optional(True)])
    send_login = SubmitField("Ingreso")
    add_user = SubmitField("Agregar")
    send_forgot = SubmitField("Enviar correo")


class Product(FlaskForm):
    id = IntegerField("Referencia", validators=[DataRequired(message="Este campo es obligatorio"),
                                                NumberRange(min=0)], render_kw={"placeholder": "Eg. 123"})
    name = StringField("Nombre", validators=[Optional(True)],
                       render_kw={"placeholder": "Eg. Empanadas"})
    quantity = IntegerField("Cantidad", validators=[DataRequired(message="Este campo es obligatorio"),
                                                    NumberRange(min=0)], render_kw={"placeholder": "Eg. 11"})
    desc = TextAreaField("Descripción", validators=[Optional(True)], render_kw={"placeholder": "Eg. Con carne"})
    img = FileField("Subir imagen", validators=[DataRequired(message="Este campo es obligatorio")],
                    render_kw={"style": "visibility: hidden"})
    send = SubmitField("Crear producto")
    update_product = SubmitField("Actualizar producto")
