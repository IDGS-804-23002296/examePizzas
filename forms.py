from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, RadioField, BooleanField, DateField
from wtforms import validators

class PizzaForm(FlaskForm):
    tamano = RadioField('Tamaño Pizza', choices=[
        ('Chica', 'Chica $40'),
        ('Mediana', 'Mediana $80'),
        ('Grande', 'Grande $120')
    ], validators=[
        validators.DataRequired(message='Debe seleccionar un tamaño para la pizza')
    ])
    
    jamon = BooleanField('Jamón $10')
    pina = BooleanField('Piña $10')
    champinones = BooleanField('Champiñones $10')
    
    num_pizzas = IntegerField('Número de Pizzas', [
        validators.DataRequired(message='Indique cuántas pizzas desea'),
        validators.NumberRange(min=1, max=100, message='La cantidad debe ser entre 1 y 100')
    ])

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self, extra_validators)
        if not (self.jamon.data or self.pina.data or self.champinones.data):
            self.jamon.errors.append('Debe seleccionar al menos un ingrediente adicional')
            rv = False
        return rv
    
    submit = SubmitField('Agregar')

class PedidoFinalForm(FlaskForm):
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es obligatorio'),
        validators.Length(min=4, max=100)
    ])
    direccion = StringField('Dirección', [
        validators.DataRequired(message='La dirección es obligatoria')
    ])
    telefono = StringField('Teléfono', [
        validators.DataRequired(message='El teléfono es obligatorio')
    ])
    fecha = DateField('Fecha de compra', format='%Y-%m-%d', validators=[validators.DataRequired(message='La fecha es obligatoria')])
    submit = SubmitField('Terminar')

class VentasDiaForm(FlaskForm):
    dia = StringField('Día de la semana', [validators.DataRequired(message='El día es obligatorio')])
    submit = SubmitField('Consultar por día')

class VentasMesForm(FlaskForm):
    mes = StringField('Nombre del mes', [validators.DataRequired(message='El nombre del mes es obligatorio')])
    submit = SubmitField('Consultar por mes')