from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import re

Base = declarative_base()

# Association table for many-to-many relationship between Personas and Transacciones
personas_transacciones = Table('personas_transacciones', Base.metadata,
    Column('persona_id', Integer, ForeignKey('personas.id')),
    Column('transaccion_id', Integer, ForeignKey('transacciones.id'))
)

class Persona(Base):
    __tablename__ = 'personas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_persona = Column(String(2))  # PF or PM
    roles_activos = Column(String(255))  # Comma-separated values
    nombre_razon_social = Column(String(255), nullable=False)
    rfc = Column(String(13))
    curp = Column(String(18))
    nacionalidad = Column(String(3))  # ISO-3166 code
    fecha_nac_constitucion = Column(DateTime)
    domicilio_completo = Column(Text)
    telefono = Column(String(20))
    correo = Column(String(255))
    actividad_economica_giro = Column(Text)
    porcentaje_participacion = Column(Float)
    pep = Column(Boolean, default=False)
    pariente_pareja_pep = Column(Boolean, default=False)
    jurisdiccion_alto_riesgo = Column(Boolean, default=False)
    estatus_expediente = Column(String(20), default='Incompleto')
    fecha_apertura_expediente = Column(DateTime, default=datetime.utcnow)
    fecha_ultima_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documentos = relationship("Documento", back_populates="persona_relacionada")
    roles = relationship("Rol", back_populates="persona")
    alertas = relationship("Alerta", back_populates="persona")
    pep_relaciones = relationship("PEPRelacion", back_populates="persona")
    transacciones = relationship("Transaccion", secondary=personas_transacciones, back_populates="personas_involucradas")
    
    def validate_rfc(self):
        """Validate RFC format"""
        if self.rfc:
            pattern = r"[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}"
            return bool(re.match(pattern, self.rfc))
        return True
    
    def validate_curp(self):
        """Validate CURP format (only for PF)"""
        if self.tipo_persona == 'PF' and self.curp:
            pattern = r"[A-Z]{4}\d{6}[HM]{1}[A-Z]{5}\d{2}"
            return bool(re.match(pattern, self.curp))
        return True

class Documento(Base):
    __tablename__ = 'documentos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    persona_relacionada_id = Column(Integer, ForeignKey('personas.id'))
    tipo_documento = Column(String(50))
    numero_folio = Column(String(100))
    fecha_expedicion = Column(DateTime)
    vigencia = Column(DateTime)
    archivo_path = Column(String(500))  # File path for attachment
    estatus_documento = Column(String(20), default='Vigente')
    observaciones = Column(Text)
    
    # Relationships
    persona_relacionada = relationship("Persona", back_populates="documentos")
    
    def check_vigencia(self):
        """Check if document is expired"""
        if self.vigencia and self.vigencia < datetime.now():
            self.estatus_documento = 'Vencido'
            return True
        return False

class Rol(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    persona_id = Column(Integer, ForeignKey('personas.id'))
    rol = Column(String(10))  # PR, BF, RL, CL, Otro
    transaccion_id = Column(Integer, ForeignKey('transacciones.id'))
    porcentaje_participacion = Column(Float)
    origen_recursos = Column(Text)
    
    # Relationships
    persona = relationship("Persona", back_populates="roles")
    transaccion = relationship("Transaccion", back_populates="roles")

class Transaccion(Base):
    __tablename__ = 'transacciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    proyecto_unidad = Column(String(255))
    tipo_operacion = Column(String(20))  # Compra, Venta, Renta
    monto_mxn = Column(Float)
    forma_pago = Column(String(20))  # Transferencia, Cheque, Efectivo, Mixto
    fecha_operacion = Column(DateTime)
    origen_recursos = Column(Text)
    destino_recursos = Column(Text)
    estatus_aviso = Column(String(20), default='No Aplica')
    
    # Relationships
    roles = relationship("Rol", back_populates="transaccion")
    alertas = relationship("Alerta", back_populates="transaccion")
    personas_involucradas = relationship("Persona", secondary=personas_transacciones, back_populates="transacciones")
    
    def check_umbral_uif(self, uma_value=108.57):  # UMA 2024 value
        """Check if transaction meets UIF reporting threshold"""
        umbral = 8025 * uma_value  # Current threshold
        return self.monto_mxn >= umbral

class Alerta(Base):
    __tablename__ = 'alertas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_alerta = Column(String(50))
    persona_id = Column(Integer, ForeignKey('personas.id'), nullable=True)
    transaccion_id = Column(Integer, ForeignKey('transacciones.id'), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    descripcion = Column(Text)
    responsable = Column(String(100))
    estatus = Column(String(20), default='Pendiente')
    
    # Relationships
    persona = relationship("Persona", back_populates="alertas")
    transaccion = relationship("Transaccion", back_populates="alertas")

class PEPRelacion(Base):
    __tablename__ = 'pep_relaciones'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    persona_id = Column(Integer, ForeignKey('personas.id'))
    nombre_pep = Column(String(255))
    parentesco = Column(String(50))  # Pareja, Padre/Madre, Hijo/Hija, Hermano/Hermana
    puesto_destacado = Column(String(255))
    dependencia_entidad = Column(String(255))
    ano_ejercicio = Column(Integer)
    ano_fin = Column(Integer)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    persona = relationship("Persona", back_populates="pep_relaciones")

# Database setup
def create_database():
    """Create database and tables"""
    engine = create_engine('sqlite:///kyc_pldft.db', echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session"""
    engine = create_database()
    Session = sessionmaker(bind=engine)
    return Session()

# Business logic for automations
class KYCAutomations:
    def __init__(self, session):
        self.session = session
    
    def update_fecha_ultima_actualizacion(self, persona_id):
        """Update last modification time for persona"""
        persona = self.session.query(Persona).get(persona_id)
        if persona:
            persona.fecha_ultima_actualizacion = datetime.utcnow()
            self.session.commit()
    
    def check_documento_vencido(self, documento_id):
        """Check and create alert for expired documents"""
        documento = self.session.query(Documento).get(documento_id)
        if documento and documento.check_vigencia():
            # Create alert
            alerta = Alerta(
                tipo_alerta="Documento Vencido",
                persona_id=documento.persona_relacionada_id,
                descripcion="Documento vencido automáticamente detectado."
            )
            self.session.add(alerta)
            self.session.commit()
    
    def check_umbral_uif(self, transaccion_id):
        """Check UIF threshold and create alert if needed"""
        transaccion = self.session.query(Transaccion).get(transaccion_id)
        if transaccion and transaccion.check_umbral_uif():
            transaccion.estatus_aviso = "Pendiente"
            
            # Create alert
            alerta = Alerta(
                tipo_alerta="Aviso Pendiente",
                transaccion_id=transaccion_id,
                descripcion="Operación alcanza umbral de aviso."
            )
            self.session.add(alerta)
            self.session.commit()
    
    def check_pep_flag(self, persona_id):
        """Check PEP status and create alert if needed"""
        persona = self.session.query(Persona).get(persona_id)
        if persona and (persona.pep or persona.pariente_pareja_pep):
            # Check if alert already exists
            existing_alert = self.session.query(Alerta).filter(
                Alerta.tipo_alerta == "PEP",
                Alerta.persona_id == persona_id
            ).first()
            
            if not existing_alert:
                alerta = Alerta(
                    tipo_alerta="PEP",
                    persona_id=persona_id,
                    descripcion="Registro marcado como PEP o pariente PEP."
                )
                self.session.add(alerta)
                self.session.commit()

# Data validation utilities
class DataValidator:
    @staticmethod
    def validate_rfc(rfc):
        """Validate RFC format"""
        if not rfc:
            return True
        pattern = r"[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}"
        return bool(re.match(pattern, rfc))
    
    @staticmethod
    def validate_curp(curp):
        """Validate CURP format"""
        if not curp:
            return True
        pattern = r"[A-Z]{4}\d{6}[HM]{1}[A-Z]{5}\d{2}"
        return bool(re.match(pattern, curp))
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email:
            return True
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

# ISO-3166 country codes (sample)
ISO_3166_COUNTRIES = {
    'MEX': 'México',
    'USA': 'Estados Unidos',
    'CAN': 'Canadá',
    'ESP': 'España',
    'FRA': 'Francia',
    'DEU': 'Alemania',
    'GBR': 'Reino Unido',
    'ITA': 'Italia',
    'BRA': 'Brasil',
    'ARG': 'Argentina',
    'COL': 'Colombia',
    'PER': 'Perú',
    'CHL': 'Chile',
    'URY': 'Uruguay',
    'ECU': 'Ecuador',
    'VEN': 'Venezuela',
    'GTM': 'Guatemala',
    'CRI': 'Costa Rica',
    'PAN': 'Panamá',
    'NIC': 'Nicaragua',
    'HND': 'Honduras',
    'SLV': 'El Salvador',
    'BLZ': 'Belice',
    'CUB': 'Cuba',
    'DOM': 'República Dominicana',
    'HTI': 'Haití',
    'JAM': 'Jamaica'
}