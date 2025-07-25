#!/usr/bin/env python3
"""
Sample data initialization script for KYC PLDFT system
This script creates sample data to test the system functionality
"""

from datetime import datetime, date, timedelta
from database import (
    get_session, Persona, Documento, Rol, Transaccion, Alerta, PEPRelacion,
    KYCAutomations
)

def init_sample_data():
    """Initialize database with sample data"""
    session = get_session()
    automations = KYCAutomations(session)
    
    try:
        # Clear existing data (for testing)
        session.query(PEPRelacion).delete()
        session.query(Alerta).delete()
        session.query(Rol).delete()
        session.query(Documento).delete()
        session.query(Transaccion).delete()
        session.query(Persona).delete()
        session.commit()
        
        print("Creating sample personas...")
        
        # Sample Personas
        personas_data = [
            {
                'tipo_persona': 'PF',
                'nombre_razon_social': 'Juan Carlos Pérez García',
                'rfc': 'PEGJ850315ABC',
                'curp': 'PEGJ850315HDFRZN01',
                'nacionalidad': 'MEX',
                'fecha_nac_constitucion': date(1985, 3, 15),
                'domicilio_completo': 'Av. Reforma 123, Col. Centro, CDMX',
                'telefono': '5555551234',
                'correo': 'juan.perez@email.com',
                'actividad_economica_giro': 'Comerciante',
                'pep': False,
                'pariente_pareja_pep': False,
                'jurisdiccion_alto_riesgo': False,
                'estatus_expediente': 'Completo',
                'roles_activos': 'CL'
            },
            {
                'tipo_persona': 'PM',
                'nombre_razon_social': 'Desarrollos Inmobiliarios del Norte SA de CV',
                'rfc': 'DIN920401XYZ',
                'curp': None,
                'nacionalidad': 'MEX',
                'fecha_nac_constitucion': date(1992, 4, 1),
                'domicilio_completo': 'Blvd. Constitución 456, Col. Industrial, Monterrey, NL',
                'telefono': '8181234567',
                'correo': 'contacto@desarrollosnorte.mx',
                'actividad_economica_giro': 'Desarrollo inmobiliario',
                'pep': False,
                'pariente_pareja_pep': False,
                'jurisdiccion_alto_riesgo': False,
                'estatus_expediente': 'Completo',
                'roles_activos': 'PR'
            },
            {
                'tipo_persona': 'PF',
                'nombre_razon_social': 'María Elena Rodríguez Sánchez',
                'rfc': 'ROSM780622DEF',
                'curp': 'ROSM780622MDFNRL05',
                'nacionalidad': 'MEX',
                'fecha_nac_constitucion': date(1978, 6, 22),
                'domicilio_completo': 'Calle Morelos 789, Col. Centro, Guadalajara, JAL',
                'telefono': '3331234567',
                'correo': 'maria.rodriguez@email.com',
                'actividad_economica_giro': 'Empresaria',
                'pep': True,  # PEP person for testing
                'pariente_pareja_pep': False,
                'jurisdiccion_alto_riesgo': False,
                'estatus_expediente': 'Bajo Revisión',
                'roles_activos': 'BF,CL'
            },
            {
                'tipo_persona': 'PF',
                'nombre_razon_social': 'Roberto Carlos Mendoza López',
                'rfc': 'MELR900815GHI',
                'curp': 'MELR900815HDFRBT02',
                'nacionalidad': 'MEX',
                'fecha_nac_constitucion': date(1990, 8, 15),
                'domicilio_completo': 'Av. Universidad 321, Col. Del Valle, CDMX',
                'telefono': '5556789012',
                'correo': 'roberto.mendoza@email.com',
                'actividad_economica_giro': 'Abogado',
                'pep': False,
                'pariente_pareja_pep': True,  # PEP relative for testing
                'jurisdiccion_alto_riesgo': False,
                'estatus_expediente': 'Incompleto',
                'roles_activos': 'RL'
            },
            {
                'tipo_persona': 'PF',
                'nombre_razon_social': 'Ana Sofía Jiménez Torres',
                'rfc': 'JITA950403JKL',
                'curp': 'JITA950403MDFRMN03',
                'nacionalidad': 'USA',
                'fecha_nac_constitucion': date(1995, 4, 3),
                'domicilio_completo': '123 Main St, Miami, FL, USA',
                'telefono': '+1-305-555-0123',
                'correo': 'ana.jimenez@email.com',
                'actividad_economica_giro': 'Inversionista',
                'pep': False,
                'pariente_pareja_pep': False,
                'jurisdiccion_alto_riesgo': True,  # High risk jurisdiction
                'estatus_expediente': 'Observado',
                'roles_activos': 'CL'
            }
        ]
        
        personas = []
        for data in personas_data:
            persona = Persona(**data)
            session.add(persona)
            personas.append(persona)
        
        session.commit()
        print(f"Created {len(personas)} personas")
        
        # Sample Documents
        print("Creating sample documents...")
        documentos_data = [
            {
                'persona_relacionada_id': personas[0].id,
                'tipo_documento': 'INE',
                'numero_folio': 'INE123456789',
                'fecha_expedicion': date(2020, 1, 15),
                'vigencia': date(2030, 1, 15),
                'estatus_documento': 'Vigente',
                'observaciones': 'Documento en buen estado'
            },
            {
                'persona_relacionada_id': personas[0].id,
                'tipo_documento': 'Comprobante Domicilio',
                'numero_folio': 'CFE202301',
                'fecha_expedicion': date(2024, 1, 1),
                'vigencia': date(2024, 4, 1),
                'estatus_documento': 'Vencido',  # Expired document for testing
                'observaciones': 'Recibo de luz vencido'
            },
            {
                'persona_relacionada_id': personas[1].id,
                'tipo_documento': 'Acta Constitutiva',
                'numero_folio': 'AC-2024-001',
                'fecha_expedicion': date(1992, 4, 1),
                'vigencia': None,  # No expiry
                'estatus_documento': 'Vigente',
                'observaciones': 'Acta constitutiva original'
            },
            {
                'persona_relacionada_id': personas[2].id,
                'tipo_documento': 'INE',
                'numero_folio': 'INE987654321',
                'fecha_expedicion': date(2019, 6, 15),
                'vigencia': date(2029, 6, 15),
                'estatus_documento': 'Vigente',
                'observaciones': 'Documento vigente'
            },
            {
                'persona_relacionada_id': personas[4].id,
                'tipo_documento': 'Pasaporte',
                'numero_folio': 'US123456789',
                'fecha_expedicion': date(2020, 5, 10),
                'vigencia': date(2025, 5, 10),
                'estatus_documento': 'Vigente',
                'observaciones': 'Pasaporte estadounidense'
            }
        ]
        
        for data in documentos_data:
            documento = Documento(**data)
            session.add(documento)
        
        session.commit()
        print(f"Created {len(documentos_data)} documents")
        
        # Sample Transactions
        print("Creating sample transactions...")
        transacciones_data = [
            {
                'proyecto_unidad': 'Torre Reforma - Depto 1501',
                'tipo_operacion': 'Compra',
                'monto_mxn': 2500000.00,  # High amount to trigger UIF alert
                'forma_pago': 'Transferencia',
                'fecha_operacion': date.today() - timedelta(days=30),
                'origen_recursos': 'Ahorros personales y crédito hipotecario',
                'destino_recursos': 'Adquisición de vivienda',
                'estatus_aviso': 'No Aplica'
            },
            {
                'proyecto_unidad': 'Residencial Los Pinos - Casa 15',
                'tipo_operacion': 'Venta',
                'monto_mxn': 1800000.00,
                'forma_pago': 'Mixto',
                'fecha_operacion': date.today() - timedelta(days=15),
                'origen_recursos': 'Venta de inmueble',
                'destino_recursos': 'Cuenta bancaria empresarial',
                'estatus_aviso': 'No Aplica'
            },
            {
                'proyecto_unidad': 'Plaza Comercial Norte - Local 23',
                'tipo_operacion': 'Renta',
                'monto_mxn': 45000.00,
                'forma_pago': 'Transferencia',
                'fecha_operacion': date.today() - timedelta(days=5),
                'origen_recursos': 'Ingresos por negocio',
                'destino_recursos': 'Renta mensual',
                'estatus_aviso': 'No Aplica'
            },
            {
                'proyecto_unidad': 'Condominios del Valle - Torre B Piso 8',
                'tipo_operacion': 'Compra',
                'monto_mxn': 950000.00,  # Amount that might trigger UIF threshold
                'forma_pago': 'Efectivo',
                'fecha_operacion': date.today() - timedelta(days=2),
                'origen_recursos': 'Liquidación de inversiones',
                'destino_recursos': 'Adquisición inmobiliaria',
                'estatus_aviso': 'Pendiente'
            }
        ]
        
        transacciones = []
        for data in transacciones_data:
            transaccion = Transaccion(**data)
            session.add(transaccion)
            transacciones.append(transaccion)
        
        session.commit()
        print(f"Created {len(transacciones)} transactions")
        
        # Sample PEP Relations
        print("Creating sample PEP relations...")
        pep_relaciones_data = [
            {
                'persona_id': personas[2].id,  # María Elena (PEP)
                'nombre_pep': 'María Elena Rodríguez Sánchez',
                'parentesco': 'Pareja',
                'puesto_destacado': 'Diputada Federal',
                'dependencia_entidad': 'Cámara de Diputados',
                'ano_ejercicio': 2021,
                'ano_fin': 2024
            },
            {
                'persona_id': personas[3].id,  # Roberto (pariente PEP)
                'nombre_pep': 'Elena Rodríguez Vázquez',
                'parentesco': 'Hermano/Hermana',
                'puesto_destacado': 'Secretaria de Estado',
                'dependencia_entidad': 'Gobierno Estatal',
                'ano_ejercicio': 2019,
                'ano_fin': 2025
            }
        ]
        
        for data in pep_relaciones_data:
            pep_rel = PEPRelacion(**data)
            session.add(pep_rel)
        
        session.commit()
        print(f"Created {len(pep_relaciones_data)} PEP relations")
        
        # Trigger automations to create alerts
        print("Triggering automations...")
        
        # Check PEP flags
        for persona in personas:
            automations.check_pep_flag(persona.id)
        
        # Check document expiration
        documentos = session.query(Documento).all()
        for doc in documentos:
            automations.check_documento_vencido(doc.id)
        
        # Check UIF thresholds
        for trans in transacciones:
            automations.check_umbral_uif(trans.id)
        
        # Create some manual alerts for testing
        alertas_manuales = [
            {
                'tipo_alerta': 'Operación Inusual',
                'persona_id': personas[4].id,
                'descripcion': 'Cliente extranjero con múltiples transacciones en efectivo',
                'responsable': 'Oficial de Cumplimiento',
                'estatus': 'Pendiente'
            },
            {
                'tipo_alerta': 'Riesgo Alto',
                'persona_id': personas[4].id,
                'descripcion': 'Cliente de jurisdicción de alto riesgo',
                'responsable': 'Analista Senior',
                'estatus': 'En Revisión'
            }
        ]
        
        for data in alertas_manuales:
            alerta = Alerta(**data)
            session.add(alerta)
        
        session.commit()
        
        # Final counts
        total_personas = session.query(Persona).count()
        total_documentos = session.query(Documento).count()
        total_transacciones = session.query(Transaccion).count()
        total_alertas = session.query(Alerta).count()
        total_pep_rel = session.query(PEPRelacion).count()
        
        print("\n" + "="*50)
        print("SAMPLE DATA INITIALIZATION COMPLETE")
        print("="*50)
        print(f"Personas created: {total_personas}")
        print(f"Documents created: {total_documentos}")
        print(f"Transactions created: {total_transacciones}")
        print(f"Alerts created: {total_alertas}")
        print(f"PEP Relations created: {total_pep_rel}")
        print("="*50)
        
        print("\nSample data includes:")
        print("- PEP persons and relatives")
        print("- Expired documents")
        print("- High-value transactions")
        print("- Foreign nationals")
        print("- Various document types")
        print("- Automated alerts")
        print("\nYou can now run the Streamlit app to test the system!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_sample_data()