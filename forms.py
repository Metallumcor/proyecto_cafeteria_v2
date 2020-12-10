from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class Product(FlaskForm):
    id = IntegerField("Referencia", validators=[DataRequired(message="Este campo es obligatorio"),
                                                NumberRange(min=0)], render_kw={"placeholder": "ds"})
    name = StringField("Nombre", validators=[Optional(True)],
                       render_kw={"placeholde": "dsa"})
    quantity = IntegerField("Referencia", validators=[DataRequired(message="Este campo es obligatorio"),
                                                      NumberRange(min=0)], render_kw={"placeholder": "ds"})
    desc = TextAreaField("Descripción", validators=[Optional(True)], render_kw={"placeholder": "sd"})
    img = FileField("Subir imagen", validators=[DataRequired(message="Este campo es obligatorio")])
    send = SubmitField("Crear producto")