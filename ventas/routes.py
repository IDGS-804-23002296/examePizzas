from . import ventas
from flask import render_template, request, flash
from models import db, Pedido, DetallePedido
import forms
from sqlalchemy import extract

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, 
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}

DIAS = {
    "lunes": 0, "martes": 1, "miercoles": 2, "miércoles": 2,
    "jueves": 3, "viernes": 4, "sabado": 5, "sábado": 5, "domingo": 6
}

@ventas.route("/ventas", methods=['GET', 'POST'])
def index():
    form_dia = forms.VentasDiaForm()
    form_mes = forms.VentasMesForm()
    pedidos_resultados = []
    total_acumulado = 0

    if request.method == 'POST':
        if 'consulta_dia' in request.form:
            form_dia = forms.VentasDiaForm(request.form)
            if form_dia.validate():
                dia_buscado = form_dia.dia.data.lower().strip()
                numero_dia = DIAS.get(dia_buscado)
                
                if numero_dia is not None:
                    todos = Pedido.query.all()
                    pedidos_resultados = [p for p in todos if p.fecha.weekday() == numero_dia]
                    if pedidos_resultados:
                        flash(f"Se encontraron {len(pedidos_resultados)} ventas para el día {dia_buscado}")
                    else:
                        flash(f"No hay ventas registradas para el día {dia_buscado}")
                else:
                    form_dia.dia.errors.append("Día no válido (Ej: Lunes, Martes...)")
                    flash("Error en la consulta por día")

        elif 'consulta_mes' in request.form:
            form_mes = forms.VentasMesForm(request.form)
            if form_mes.validate():
                mes_nombre = form_mes.mes.data.lower().strip()
                mes_numero = MESES.get(mes_nombre)
                
                if mes_numero:
                    pedidos_resultados = Pedido.query.filter(
                        extract('month', Pedido.fecha) == mes_numero
                    ).all()
                    if pedidos_resultados:
                        flash(f"Consulta exitosa: {len(pedidos_resultados)} ventas en {mes_nombre}")
                    else:
                        flash(f"No se encontraron ventas para el mes de {mes_nombre}")
                else:
                    form_mes.mes.errors.append("Mes no válido (Ej: Enero, Febrero...)")
                    flash("Error en la consulta por mes")

    total_acumulado = sum(p.total for p in pedidos_resultados)

    return render_template(
        "ventas/ventas.html",
        form_dia=form_dia,
        form_mes=form_mes,
        ventas=pedidos_resultados,
        total_acumulado=total_acumulado
    )

@ventas.route("/ventas/detalle/<int:id>")
def detalle(id):
    pedido = Pedido.query.get_or_404(id)
    detalles = DetallePedido.query.filter_by(id_pedido=id).all()
    return render_template("ventas/detalle.html", pedido=pedido, detalles=detalles)