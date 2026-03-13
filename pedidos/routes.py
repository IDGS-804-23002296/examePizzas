from . import pedidos
from flask import render_template, request, redirect, url_for, flash, session
from models import db, Cliente, Pedido, DetallePedido, Pizza
import forms
from datetime import date

@pedidos.route("/pedidos", methods=['GET', 'POST'])
def index():
    form_cliente = forms.PedidoFinalForm()
    form_pizza = forms.PizzaForm()
    hoy = date.today()

    if 'carrito' not in session:
        session['carrito'] = []

    if request.method == 'GET':
        if 'cliente_datos' in session:
            form_cliente.nombre.data = session['cliente_datos'].get('nombre')
            form_cliente.direccion.data = session['cliente_datos'].get('direccion')
            form_cliente.telefono.data = session['cliente_datos'].get('telefono')
            fecha_str = session['cliente_datos'].get('fecha')
            form_cliente.fecha.data = date.fromisoformat(fecha_str) if fecha_str else hoy
        else:
            form_cliente.fecha.data = hoy

    if request.method == 'POST':
        if 'submit' in request.form:
            p_valida = form_pizza.validate()
            c_valida = form_cliente.validate()

            if p_valida and c_valida:
                session['cliente_datos'] = {
                    'nombre': form_cliente.nombre.data,
                    'direccion': form_cliente.direccion.data,
                    'telefono': form_cliente.telefono.data,
                    'fecha': form_cliente.fecha.data.isoformat()
                }

                precios = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
                subtotal_base = precios.get(form_pizza.tamano.data, 0)
                ingredientes = []
                extras = 0
                
                if form_pizza.jamon.data: 
                    ingredientes.append("Jamón")
                    extras += 10
                if form_pizza.pina.data: 
                    ingredientes.append("Piña")
                    extras += 10
                if form_pizza.champinones.data: 
                    ingredientes.append("Champiñones")
                    extras += 10
                    
                precio_u = subtotal_base + extras
                subtotal = precio_u * form_pizza.num_pizzas.data
                
                carrito = session['carrito']
                carrito.append({
                    'tamano': form_pizza.tamano.data,
                    'ingredientes': ", ".join(ingredientes),
                    'cantidad': form_pizza.num_pizzas.data,
                    'subtotal': subtotal,
                    'precio_u': precio_u
                })
                session['carrito'] = carrito
                session.modified = True
                flash(f"Pizza {form_pizza.tamano.data} añadida")
                return redirect(url_for('.index'))

        if 'confirmar' in request.form:
            if form_cliente.validate():
                if not session.get('carrito'):
                    flash("Carrito vacío")
                    return redirect(url_for('.index'))

                total_p = sum(item['subtotal'] for item in session['carrito'])
                try:
                    c = Cliente(nombre=form_cliente.nombre.data, direccion=form_cliente.direccion.data, telefono=form_cliente.telefono.data)
                    db.session.add(c)
                    db.session.flush()
                    
                    ped = Pedido(id_cliente=c.id_cliente, fecha=form_cliente.fecha.data, total=total_p)
                    db.session.add(ped)
                    db.session.flush()

                    for i in session['carrito']:
                        piz = Pizza(tamano=i['tamano'], ingredientes=i['ingredientes'], precio=i['precio_u'])
                        db.session.add(piz)
                        db.session.flush()
                        db.session.add(DetallePedido(id_pedido=ped.id_pedido, id_pizza=piz.id_pizza, cantidad=i['cantidad'], subtotal=i['subtotal']))

                    db.session.commit()
                    session.pop('carrito', None)
                    session.pop('cliente_datos', None)
                    flash("Compra terminada")
                    return redirect(url_for('.index'))
                except:
                    db.session.rollback()
                    flash("Error al procesar")

    ventas_dia = Pedido.query.filter_by(fecha=hoy).all()
    total_hoy = sum(v.total for v in ventas_dia)

    return render_template("pedidos/pedidos.html", form_cliente=form_cliente, form_pizza=form_pizza, 
                           carrito=session.get('carrito', []), ventas_dia=ventas_dia, total_ventas_hoy=total_hoy)

@pedidos.route("/quitar/<int:id>")
def quitar(id):
    carrito = session.get('carrito', [])
    if 0 <= id < len(carrito):
        item = carrito.pop(id)
        session['carrito'] = carrito
        session.modified = True
        flash(f"Se quitó la pizza {item['tamano']} del detalle")
    return redirect(url_for('.index'))