from extensions import db
from datetime import datetime

class Camilla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(50), unique=True, nullable=False)
    estado = db.Column(db.String(20), default="producción")
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    motivo_baja = db.Column(db.Text, nullable=True) 

class Mantenimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camilla_id = db.Column(db.Integer, db.ForeignKey('camilla.id'), nullable=False)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    
    camilla = db.relationship('Camilla', backref=db.backref('mantenimientos', lazy=True))

class Baja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    camilla_id = db.Column(db.Integer, db.ForeignKey('camilla.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    motivo = db.Column(db.Text, nullable=True)

    camilla = db.relationship('Camilla', backref=db.backref('bajas', lazy=True))

    
