from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    
    pedidos = db.relationship('Pedido', back_populates='cliente')

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id_pizza = db.Column(db.Integer, primary_key=True)
    tamano = db.Column(db.String(20), nullable=False)
    ingredientes = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Numeric(8, 2), nullable=False)

    detalles = db.relationship('DetallePedido', back_populates='pizza')

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    fecha = db.Column(db.Date, default=datetime.date.today)
    total = db.Column(db.Numeric(10, 2), nullable=False)

    cliente = db.relationship('Cliente', back_populates='pedidos')
    detalles = db.relationship('DetallePedido', back_populates='pedido', cascade="all, delete-orphan")

class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_pizza = db.Column(db.Integer, db.ForeignKey('pizzas.id_pizza'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    pedido = db.relationship('Pedido', back_populates='detalles')
    pizza = db.relationship('Pizza', back_populates='detalles')