from flask import Flask
from flask import request, render_template, redirect
from config import Config
from extensions import db
from models import Camilla, Mantenimiento, Baja

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route("/")
    def index():
        return redirect("/menu")

    @app.route("/menu")
    def menu_principal():
        return render_template("menu.html")

    @app.route("/registrar", methods=["GET", "POST"])
    def registrar_camilla():
        mensaje = None
        if request.method == "POST":
            placa = request.form.get("placa")
            if placa:
                existente = Camilla.query.filter_by(placa=placa).first()
                if existente:
                    mensaje = "Ya existe una camilla con esa placa."
                else:
                    nueva = Camilla(placa=placa)
                    db.session.add(nueva)
                    db.session.commit()
                    mensaje = "Camilla registrada correctamente."
            else:
                mensaje = "La placa es obligatoria."
        return render_template("registrar_camilla.html", mensaje=mensaje)

    @app.route("/camillas")
    def listar_camillas():
        camillas = Camilla.query.all()
        return render_template("listar_camillas.html", camillas=camillas)

    @app.route("/mantenimiento", methods=["GET", "POST"])
    def ingresar_mantenimiento():
        mensaje = None
        camillas = Camilla.query.filter(Camilla.estado != "baja").all()

        if request.method == "POST":
            camilla_id = request.form.get("camilla_id")
            descripcion = request.form.get("descripcion")

            if camilla_id and descripcion:
                camilla = Camilla.query.get(camilla_id)
                if camilla:
                    camilla.estado = "mantenimiento"
                    mantenimiento = Mantenimiento(
                        camilla_id=camilla.id,
                        descripcion=descripcion
                    )
                    db.session.add(mantenimiento)
                    db.session.commit()
                    mensaje = "Camilla ingresada a mantenimiento correctamente."
                else:
                    mensaje = "Camilla no encontrada."
            else:
                mensaje = "Todos los campos son obligatorios."

        return render_template("mantenimiento.html", camillas=camillas, mensaje=mensaje)

    from datetime import datetime

    from datetime import datetime

    @app.route("/cerrar-mantenimiento", methods=["GET", "POST"])
    def cerrar_mantenimiento():
        mensaje = None
        camillas = Camilla.query.filter_by(estado="mantenimiento").all()

        if request.method == "POST":
            camilla_id = request.form.get("camilla_id")
            camilla = Camilla.query.get(camilla_id)

            if camilla:
                mantenimiento_abierto = Mantenimiento.query.filter_by(
                    camilla_id=camilla.id, fecha_fin=None
                ).order_by(Mantenimiento.fecha_inicio.desc()).first()

                if mantenimiento_abierto:
                    mantenimiento_abierto.fecha_fin = datetime.utcnow()
                    camilla.estado = "producción"
                    db.session.commit()
                    mensaje = "Mantenimiento cerrado correctamente."
                else:
                    mensaje = "No hay mantenimiento abierto para esta camilla."
            else:
                mensaje = "Camilla no encontrada."

        return render_template("cerrar_mantenimiento.html", camillas=camillas, mensaje=mensaje)


    @app.route("/dar-baja", methods=["GET", "POST"])
    def dar_baja_camilla():
        mensaje = None
        camillas = Camilla.query.filter(Camilla.estado != "baja").all()

        if request.method == "POST":
            camilla_id = request.form.get("camilla_id")
            motivo = request.form.get("motivo", "")

            camilla = Camilla.query.get(camilla_id)
            if camilla:
                camilla.estado = "baja"
                camilla.motivo_baja = motivo

            # Registrar en historial
                baja = Baja(
                    camilla_id=camilla.id,
                    motivo=motivo
                )
                db.session.add(baja)

                db.session.commit()
                mensaje = "Camilla dada de baja correctamente."
            else:
                mensaje = "Camilla no encontrada."

        return render_template("dar_baja.html", camillas=camillas, mensaje=mensaje)

    @app.route("/historial-bajas")
    def historial_bajas():
        bajas = Baja.query.order_by(Baja.fecha.desc()).all()
        return render_template("historial_bajas.html", bajas=bajas)


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


