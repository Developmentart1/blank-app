import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import re
import os

# Import our database models
from database import (
    get_session, Persona, Documento, Rol, Transaccion, Alerta, PEPRelacion,
    KYCAutomations, DataValidator, ISO_3166_COUNTRIES
)

# Page configuration
st.set_page_config(
    page_title="KYC PLDFT - Desarrollo Inmobiliario",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 10px;
        margin: 10px 0;
    }
    .alert-medium {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 10px;
        margin: 10px 0;
    }
    .alert-low {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
        padding: 10px;
        margin: 10px 0;
    }
    .stSelectbox > div > div > select {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = "Representante Cumplimiento"
if 'permissions' not in st.session_state:
    st.session_state.permissions = {
        "Representante Cumplimiento": "full",
        "Equipo Ventas": {
            "Personas": ["read", "create"],
            "Documentos": ["none"],
            "Roles": ["none"],
            "Transacciones": ["none"],
            "Alertas": ["none"],
            "PEP_Relaciones": ["none"]
        },
        "Auditoria": "read"
    }

def check_permission(table, action):
    """Check if current user has permission for action on table"""
    user_perms = st.session_state.permissions.get(st.session_state.current_user, {})
    if user_perms == "full":
        return True
    if user_perms == "read" and action == "read":
        return True
    if isinstance(user_perms, dict):
        table_perms = user_perms.get(table, ["none"])
        return action in table_perms
    return False

def main():
    # Header
    st.markdown('<h1 class="main-header">🏢 KYC PLDFT - Desarrollo Inmobiliario</h1>', unsafe_allow_html=True)
    
    # User selection (for demo purposes)
    with st.sidebar:
        st.session_state.current_user = st.selectbox(
            "👤 Usuario Actual",
            ["Representante Cumplimiento", "Equipo Ventas", "Auditoria"]
        )
        st.markdown(f"**Permisos:** {st.session_state.permissions[st.session_state.current_user]}")
    
    # Navigation menu
    with st.sidebar:
        selected = option_menu(
            "Menú Principal",
            ["Dashboard", "Personas", "Documentos", "Transacciones", "Alertas", "Reportes", "Configuración"],
            icons=['speedometer2', 'people', 'file-earmark', 'credit-card', 'exclamation-triangle', 'graph-up', 'gear'],
            menu_icon="cast",
            default_index=0,
        )
    
    # Route to different pages
    if selected == "Dashboard":
        show_dashboard()
    elif selected == "Personas":
        show_personas()
    elif selected == "Documentos":
        show_documentos()
    elif selected == "Transacciones":
        show_transacciones()
    elif selected == "Alertas":
        show_alertas()
    elif selected == "Reportes":
        show_reportes()
    elif selected == "Configuración":
        show_configuracion()

def show_dashboard():
    """Main dashboard with KPIs and alerts"""
    st.header("📊 Dashboard Ejecutivo")
    
    session = get_session()
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_personas = session.query(Persona).count()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_personas}</h3>
            <p>Total Personas</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        expedientes_incompletos = session.query(Persona).filter(
            Persona.estatus_expediente != 'Completo'
        ).count()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{expedientes_incompletos}</h3>
            <p>Expedientes Incompletos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        alertas_pendientes = session.query(Alerta).filter(
            Alerta.estatus == 'Pendiente'
        ).count()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{alertas_pendientes}</h3>
            <p>Alertas Pendientes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        personas_pep = session.query(Persona).filter(
            (Persona.pep == True) | (Persona.pariente_pareja_pep == True)
        ).count()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{personas_pep}</h3>
            <p>Personas PEP</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Estatus de Expedientes")
        expedientes_data = session.query(
            Persona.estatus_expediente,
            session.query(Persona).filter(Persona.estatus_expediente == Persona.estatus_expediente).count().label('count')
        ).group_by(Persona.estatus_expediente).all()
        
        if expedientes_data:
            df_expedientes = pd.DataFrame([(row[0], session.query(Persona).filter(Persona.estatus_expediente == row[0]).count()) 
                                         for row in session.query(Persona.estatus_expediente).distinct().all()],
                                        columns=['Estatus', 'Cantidad'])
            fig_pie = px.pie(df_expedientes, values='Cantidad', names='Estatus', 
                           color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("🚨 Alertas por Tipo")
        alertas_data = session.query(Alerta.tipo_alerta).all()
        if alertas_data:
            df_alertas = pd.DataFrame([row[0] for row in alertas_data], columns=['Tipo'])
            alertas_count = df_alertas['Tipo'].value_counts().reset_index()
            alertas_count.columns = ['Tipo', 'Cantidad']
            fig_bar = px.bar(alertas_count, x='Tipo', y='Cantidad', 
                           color='Cantidad', color_continuous_scale='Reds')
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Recent alerts
    st.subheader("🔔 Alertas Recientes")
    recent_alerts = session.query(Alerta).order_by(Alerta.fecha.desc()).limit(5).all()
    
    for alert in recent_alerts:
        alert_class = "alert-high" if alert.tipo_alerta in ["PEP", "Aviso Pendiente"] else "alert-medium"
        st.markdown(f"""
        <div class="{alert_class}">
            <strong>{alert.tipo_alerta}</strong> - {alert.descripcion}<br>
            <small>Fecha: {alert.fecha.strftime('%Y-%m-%d %H:%M')} | Estatus: {alert.estatus}</small>
        </div>
        """, unsafe_allow_html=True)
    
    session.close()

def show_personas():
    """Personas management interface"""
    st.header("👥 Gestión de Personas")
    
    if not check_permission("Personas", "read"):
        st.error("No tienes permisos para acceder a esta sección")
        return
    
    session = get_session()
    automations = KYCAutomations(session)
    
    tab1, tab2, tab3 = st.tabs(["📋 Lista", "➕ Nuevo", "🔍 Buscar"])
    
    with tab1:
        st.subheader("Lista de Personas")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_tipo = st.selectbox("Tipo de Persona", ["Todos", "PF", "PM"])
        with col2:
            filter_estatus = st.selectbox("Estatus Expediente", 
                                        ["Todos", "Incompleto", "Observado", "Bajo Revisión", "Completo"])
        with col3:
            filter_pep = st.selectbox("PEP", ["Todos", "Sí", "No"])
        
        # Build query
        query = session.query(Persona)
        if filter_tipo != "Todos":
            query = query.filter(Persona.tipo_persona == filter_tipo)
        if filter_estatus != "Todos":
            query = query.filter(Persona.estatus_expediente == filter_estatus)
        if filter_pep == "Sí":
            query = query.filter((Persona.pep == True) | (Persona.pariente_pareja_pep == True))
        elif filter_pep == "No":
            query = query.filter((Persona.pep == False) & (Persona.pariente_pareja_pep == False))
        
        personas = query.all()
        
        # Display table
        if personas:
            personas_data = []
            for p in personas:
                personas_data.append({
                    'ID': p.id,
                    'Nombre/Razón Social': p.nombre_razon_social,
                    'Tipo': p.tipo_persona,
                    'RFC': p.rfc,
                    'Estatus': p.estatus_expediente,
                    'PEP': '✓' if p.pep or p.pariente_pareja_pep else '',
                    'Última Actualización': p.fecha_ultima_actualizacion.strftime('%Y-%m-%d') if p.fecha_ultima_actualizacion else ''
                })
            
            df = pd.DataFrame(personas_data)
            st.dataframe(df, use_container_width=True)
            
            # Action buttons
            if check_permission("Personas", "update"):
                selected_id = st.number_input("ID de Persona para editar", min_value=1, step=1)
                if st.button("Editar Persona"):
                    st.session_state.edit_persona_id = selected_id
                    st.rerun()
        else:
            st.info("No se encontraron personas con los filtros aplicados")
    
    with tab2:
        if check_permission("Personas", "create"):
            st.subheader("Nueva Persona")
            
            with st.form("nueva_persona"):
                col1, col2 = st.columns(2)
                
                with col1:
                    tipo_persona = st.selectbox("Tipo de Persona*", ["PF", "PM"])
                    nombre = st.text_input("Nombre/Razón Social*")
                    rfc = st.text_input("RFC")
                    if tipo_persona == "PF":
                        curp = st.text_input("CURP")
                    else:
                        curp = ""
                    nacionalidad = st.selectbox("Nacionalidad", 
                                              [""] + list(ISO_3166_COUNTRIES.keys()))
                    fecha_nac = st.date_input("Fecha Nac/Constitución")
                
                with col2:
                    domicilio = st.text_area("Domicilio Completo")
                    telefono = st.text_input("Teléfono")
                    correo = st.text_input("Correo")
                    actividad = st.text_area("Actividad Económica/Giro")
                    pep = st.checkbox("PEP")
                    pariente_pep = st.checkbox("Pariente/Pareja PEP")
                    jurisdiccion_riesgo = st.checkbox("Jurisdicción Alto Riesgo")
                
                roles_options = ["PR", "BF", "RL", "CL", "Otro"]
                roles_activos = st.multiselect("Roles Activos", roles_options)
                
                submitted = st.form_submit_button("Crear Persona")
                
                if submitted:
                    if not nombre:
                        st.error("El nombre/razón social es obligatorio")
                    elif rfc and not DataValidator.validate_rfc(rfc):
                        st.error("Formato de RFC inválido")
                    elif curp and not DataValidator.validate_curp(curp):
                        st.error("Formato de CURP inválido")
                    elif correo and not DataValidator.validate_email(correo):
                        st.error("Formato de correo inválido")
                    else:
                        nueva_persona = Persona(
                            tipo_persona=tipo_persona,
                            nombre_razon_social=nombre,
                            rfc=rfc.upper() if rfc else None,
                            curp=curp.upper() if curp else None,
                            nacionalidad=nacionalidad if nacionalidad else None,
                            fecha_nac_constitucion=fecha_nac,
                            domicilio_completo=domicilio,
                            telefono=telefono,
                            correo=correo,
                            actividad_economica_giro=actividad,
                            pep=pep,
                            pariente_pareja_pep=pariente_pep,
                            jurisdiccion_alto_riesgo=jurisdiccion_riesgo,
                            roles_activos=",".join(roles_activos)
                        )
                        
                        session.add(nueva_persona)
                        session.commit()
                        
                        # Trigger automation
                        automations.check_pep_flag(nueva_persona.id)
                        
                        st.success(f"Persona creada exitosamente con ID: {nueva_persona.id}")
                        st.rerun()
        else:
            st.error("No tienes permisos para crear personas")
    
    with tab3:
        st.subheader("Búsqueda Avanzada")
        
        search_term = st.text_input("Buscar por nombre, RFC o CURP")
        if search_term:
            search_results = session.query(Persona).filter(
                (Persona.nombre_razon_social.contains(search_term)) |
                (Persona.rfc.contains(search_term)) |
                (Persona.curp.contains(search_term))
            ).all()
            
            if search_results:
                for persona in search_results:
                    with st.expander(f"{persona.nombre_razon_social} ({persona.tipo_persona})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**ID:** {persona.id}")
                            st.write(f"**RFC:** {persona.rfc}")
                            st.write(f"**CURP:** {persona.curp}")
                            st.write(f"**Nacionalidad:** {persona.nacionalidad}")
                        with col2:
                            st.write(f"**Teléfono:** {persona.telefono}")
                            st.write(f"**Correo:** {persona.correo}")
                            st.write(f"**Estatus:** {persona.estatus_expediente}")
                            st.write(f"**PEP:** {'Sí' if persona.pep or persona.pariente_pareja_pep else 'No'}")
            else:
                st.info("No se encontraron resultados")
    
    session.close()

def show_documentos():
    """Documents management interface"""
    st.header("📄 Gestión de Documentos")
    
    if not check_permission("Documentos", "read"):
        st.error("No tienes permisos para acceder a esta sección")
        return
    
    session = get_session()
    automations = KYCAutomations(session)
    
    tab1, tab2 = st.tabs(["📋 Lista", "➕ Nuevo"])
    
    with tab1:
        st.subheader("Documentos")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            filter_tipo_doc = st.selectbox("Tipo Documento", 
                                         ["Todos", "INE", "Pasaporte", "Acta Constitutiva", 
                                          "Poder", "Comprobante Domicilio", "CFDI", "Estado de Cuenta", "Otro"])
        with col2:
            filter_estatus_doc = st.selectbox("Estatus", ["Todos", "Vigente", "Vencido", "Observado"])
        
        # Build query
        query = session.query(Documento).join(Persona)
        if filter_tipo_doc != "Todos":
            query = query.filter(Documento.tipo_documento == filter_tipo_doc)
        if filter_estatus_doc != "Todos":
            query = query.filter(Documento.estatus_documento == filter_estatus_doc)
        
        documentos = query.all()
        
        if documentos:
            docs_data = []
            for doc in documentos:
                docs_data.append({
                    'ID': doc.id,
                    'Persona': doc.persona_relacionada.nombre_razon_social,
                    'Tipo': doc.tipo_documento,
                    'Número/Folio': doc.numero_folio,
                    'Vigencia': doc.vigencia.strftime('%Y-%m-%d') if doc.vigencia else '',
                    'Estatus': doc.estatus_documento
                })
            
            df = pd.DataFrame(docs_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No se encontraron documentos")
    
    with tab2:
        if check_permission("Documentos", "create"):
            st.subheader("Nuevo Documento")
            
            personas = session.query(Persona).all()
            personas_dict = {f"{p.nombre_razon_social} (ID: {p.id})": p.id for p in personas}
            
            with st.form("nuevo_documento"):
                persona_selected = st.selectbox("Persona Relacionada*", list(personas_dict.keys()))
                tipo_doc = st.selectbox("Tipo Documento*", 
                                      ["INE", "Pasaporte", "Acta Constitutiva", "Poder", 
                                       "Comprobante Domicilio", "CFDI", "Estado de Cuenta", "Otro"])
                numero_folio = st.text_input("Número/Folio")
                fecha_expedicion = st.date_input("Fecha Expedición")
                vigencia = st.date_input("Vigencia")
                observaciones = st.text_area("Observaciones")
                
                submitted = st.form_submit_button("Crear Documento")
                
                if submitted and persona_selected:
                    persona_id = personas_dict[persona_selected]
                    
                    nuevo_doc = Documento(
                        persona_relacionada_id=persona_id,
                        tipo_documento=tipo_doc,
                        numero_folio=numero_folio,
                        fecha_expedicion=fecha_expedicion,
                        vigencia=vigencia,
                        observaciones=observaciones
                    )
                    
                    session.add(nuevo_doc)
                    session.commit()
                    
                    # Check if document is expired
                    automations.check_documento_vencido(nuevo_doc.id)
                    
                    st.success("Documento creado exitosamente")
                    st.rerun()
        else:
            st.error("No tienes permisos para crear documentos")
    
    session.close()

def show_transacciones():
    """Transactions management interface"""
    st.header("💳 Gestión de Transacciones")
    
    if not check_permission("Transacciones", "read"):
        st.error("No tienes permisos para acceder a esta sección")
        return
    
    session = get_session()
    automations = KYCAutomations(session)
    
    tab1, tab2 = st.tabs(["📋 Lista", "➕ Nueva"])
    
    with tab1:
        st.subheader("Transacciones")
        
        transacciones = session.query(Transaccion).all()
        
        if transacciones:
            trans_data = []
            for trans in transacciones:
                trans_data.append({
                    'ID': trans.id,
                    'Proyecto/Unidad': trans.proyecto_unidad,
                    'Tipo': trans.tipo_operacion,
                    'Monto MXN': f"${trans.monto_mxn:,.2f}" if trans.monto_mxn else "",
                    'Forma Pago': trans.forma_pago,
                    'Fecha': trans.fecha_operacion.strftime('%Y-%m-%d') if trans.fecha_operacion else "",
                    'Estatus Aviso': trans.estatus_aviso
                })
            
            df = pd.DataFrame(trans_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No se encontraron transacciones")
    
    with tab2:
        if check_permission("Transacciones", "create"):
            st.subheader("Nueva Transacción")
            
            with st.form("nueva_transaccion"):
                col1, col2 = st.columns(2)
                
                with col1:
                    proyecto = st.text_input("Proyecto/Unidad*")
                    tipo_operacion = st.selectbox("Tipo Operación*", ["Compra", "Venta", "Renta"])
                    monto = st.number_input("Monto MXN*", min_value=0.0, step=0.01)
                    forma_pago = st.selectbox("Forma de Pago*", 
                                            ["Transferencia", "Cheque", "Efectivo", "Mixto"])
                
                with col2:
                    fecha_operacion = st.date_input("Fecha Operación*")
                    origen_recursos = st.text_area("Origen de Recursos")
                    destino_recursos = st.text_area("Destino de Recursos")
                
                submitted = st.form_submit_button("Crear Transacción")
                
                if submitted:
                    if not all([proyecto, tipo_operacion, monto, forma_pago, fecha_operacion]):
                        st.error("Todos los campos marcados con * son obligatorios")
                    else:
                        nueva_trans = Transaccion(
                            proyecto_unidad=proyecto,
                            tipo_operacion=tipo_operacion,
                            monto_mxn=monto,
                            forma_pago=forma_pago,
                            fecha_operacion=fecha_operacion,
                            origen_recursos=origen_recursos,
                            destino_recursos=destino_recursos
                        )
                        
                        session.add(nueva_trans)
                        session.commit()
                        
                        # Check UIF threshold
                        automations.check_umbral_uif(nueva_trans.id)
                        
                        st.success("Transacción creada exitosamente")
                        st.rerun()
        else:
            st.error("No tienes permisos para crear transacciones")
    
    session.close()

def show_alertas():
    """Alerts management interface"""
    st.header("🚨 Gestión de Alertas")
    
    if not check_permission("Alertas", "read"):
        st.error("No tienes permisos para acceder a esta sección")
        return
    
    session = get_session()
    
    # Alert summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pendientes = session.query(Alerta).filter(Alerta.estatus == 'Pendiente').count()
        st.metric("Pendientes", pendientes)
    
    with col2:
        en_revision = session.query(Alerta).filter(Alerta.estatus == 'En Revisión').count()
        st.metric("En Revisión", en_revision)
    
    with col3:
        cerradas = session.query(Alerta).filter(Alerta.estatus == 'Cerrada').count()
        st.metric("Cerradas", cerradas)
    
    # Alerts list
    st.subheader("Lista de Alertas")
    
    alertas = session.query(Alerta).order_by(Alerta.fecha.desc()).all()
    
    if alertas:
        for alerta in alertas:
            with st.expander(f"🚨 {alerta.tipo_alerta} - {alerta.estatus}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**ID:** {alerta.id}")
                    st.write(f"**Fecha:** {alerta.fecha.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Tipo:** {alerta.tipo_alerta}")
                    st.write(f"**Estatus:** {alerta.estatus}")
                
                with col2:
                    if alerta.persona:
                        st.write(f"**Persona:** {alerta.persona.nombre_razon_social}")
                    if alerta.transaccion:
                        st.write(f"**Transacción:** {alerta.transaccion.proyecto_unidad}")
                    st.write(f"**Responsable:** {alerta.responsable}")
                
                st.write(f"**Descripción:** {alerta.descripcion}")
                
                if check_permission("Alertas", "update"):
                    new_status = st.selectbox(
                        "Cambiar Estatus",
                        ["Pendiente", "En Revisión", "Cerrada"],
                        index=["Pendiente", "En Revisión", "Cerrada"].index(alerta.estatus),
                        key=f"status_{alerta.id}"
                    )
                    
                    if st.button(f"Actualizar", key=f"update_{alerta.id}"):
                        alerta.estatus = new_status
                        session.commit()
                        st.success("Estatus actualizado")
                        st.rerun()
    else:
        st.info("No hay alertas registradas")
    
    session.close()

def show_reportes():
    """Reports interface"""
    st.header("📊 Reportes y Analytics")
    
    session = get_session()
    
    tab1, tab2, tab3 = st.tabs(["📈 Dashboards", "📋 Reportes", "📊 Métricas"])
    
    with tab1:
        st.subheader("Dashboards Interactivos")
        
        # Personas por tipo
        personas_tipo = session.query(Persona.tipo_persona).all()
        if personas_tipo:
            df_tipo = pd.DataFrame([row[0] for row in personas_tipo], columns=['Tipo'])
            tipo_count = df_tipo['Tipo'].value_counts().reset_index()
            tipo_count.columns = ['Tipo', 'Cantidad']
            
            fig_tipo = px.pie(tipo_count, values='Cantidad', names='Tipo', 
                            title='Distribución por Tipo de Persona')
            st.plotly_chart(fig_tipo, use_container_width=True)
        
        # Transacciones por mes
        transacciones = session.query(Transaccion).all()
        if transacciones:
            trans_data = []
            for trans in transacciones:
                if trans.fecha_operacion:
                    trans_data.append({
                        'Fecha': trans.fecha_operacion,
                        'Monto': trans.monto_mxn,
                        'Tipo': trans.tipo_operacion
                    })
            
            if trans_data:
                df_trans = pd.DataFrame(trans_data)
                df_trans['Mes'] = df_trans['Fecha'].dt.to_period('M').astype(str)
                monthly_trans = df_trans.groupby('Mes')['Monto'].sum().reset_index()
                
                fig_monthly = px.line(monthly_trans, x='Mes', y='Monto', 
                                    title='Transacciones por Mes')
                st.plotly_chart(fig_monthly, use_container_width=True)
    
    with tab2:
        st.subheader("Reportes Regulatorios")
        
        # PEP Report
        if st.button("Generar Reporte PEP"):
            personas_pep = session.query(Persona).filter(
                (Persona.pep == True) | (Persona.pariente_pareja_pep == True)
            ).all()
            
            if personas_pep:
                pep_data = []
                for p in personas_pep:
                    pep_data.append({
                        'ID': p.id,
                        'Nombre': p.nombre_razon_social,
                        'RFC': p.rfc,
                        'PEP Directo': 'Sí' if p.pep else 'No',
                        'Pariente PEP': 'Sí' if p.pariente_pareja_pep else 'No',
                        'Estatus Expediente': p.estatus_expediente
                    })
                
                df_pep = pd.DataFrame(pep_data)
                st.dataframe(df_pep, use_container_width=True)
                
                # Download button
                csv = df_pep.to_csv(index=False)
                st.download_button(
                    label="Descargar Reporte PEP",
                    data=csv,
                    file_name=f"reporte_pep_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No hay personas PEP registradas")
        
        # UIF Report
        if st.button("Generar Reporte UIF"):
            transacciones_uif = session.query(Transaccion).filter(
                Transaccion.estatus_aviso == 'Pendiente'
            ).all()
            
            if transacciones_uif:
                uif_data = []
                for t in transacciones_uif:
                    uif_data.append({
                        'ID Transacción': t.id,
                        'Proyecto': t.proyecto_unidad,
                        'Monto': t.monto_mxn,
                        'Fecha': t.fecha_operacion,
                        'Tipo': t.tipo_operacion,
                        'Forma Pago': t.forma_pago
                    })
                
                df_uif = pd.DataFrame(uif_data)
                st.dataframe(df_uif, use_container_width=True)
                
                csv = df_uif.to_csv(index=False)
                st.download_button(
                    label="Descargar Reporte UIF",
                    data=csv,
                    file_name=f"reporte_uif_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No hay transacciones pendientes de reporte UIF")
    
    with tab3:
        st.subheader("Métricas de Cumplimiento")
        
        # Completeness metrics
        total_personas = session.query(Persona).count()
        completas = session.query(Persona).filter(Persona.estatus_expediente == 'Completo').count()
        completeness_rate = (completas / total_personas * 100) if total_personas > 0 else 0
        
        st.metric("Tasa de Completitud de Expedientes", f"{completeness_rate:.1f}%")
        
        # Document expiration metrics
        docs_vencidos = session.query(Documento).filter(Documento.estatus_documento == 'Vencido').count()
        total_docs = session.query(Documento).count()
        expiration_rate = (docs_vencidos / total_docs * 100) if total_docs > 0 else 0
        
        st.metric("Tasa de Documentos Vencidos", f"{expiration_rate:.1f}%")
        
        # Alert resolution metrics
        alertas_cerradas = session.query(Alerta).filter(Alerta.estatus == 'Cerrada').count()
        total_alertas = session.query(Alerta).count()
        resolution_rate = (alertas_cerradas / total_alertas * 100) if total_alertas > 0 else 0
        
        st.metric("Tasa de Resolución de Alertas", f"{resolution_rate:.1f}%")
    
    session.close()

def show_configuracion():
    """Configuration interface"""
    st.header("⚙️ Configuración del Sistema")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Usuarios", "📋 Catálogos", "🔧 Sistema"])
    
    with tab1:
        st.subheader("Gestión de Usuarios y Permisos")
        
        st.write("**Usuarios Actuales:**")
        for user, perms in st.session_state.permissions.items():
            st.write(f"- {user}: {perms}")
    
    with tab2:
        st.subheader("Catálogos del Sistema")
        
        st.write("**Tipos de Documento:**")
        tipos_doc = ["INE", "Pasaporte", "Acta Constitutiva", "Poder", 
                    "Comprobante Domicilio", "CFDI", "Estado de Cuenta", "Otro"]
        for tipo in tipos_doc:
            st.write(f"- {tipo}")
        
        st.write("**Roles:**")
        roles = ["PR - Propietario Real", "BF - Beneficiario Final", 
                "RL - Representante Legal", "CL - Cliente", "Otro"]
        for rol in roles:
            st.write(f"- {rol}")
    
    with tab3:
        st.subheader("Configuración del Sistema")
        
        st.write("**Base de Datos:** SQLite")
        st.write("**Umbral UIF:** 8,025 UMA")
        st.write("**Respaldos:** Configurados semanalmente")
        
        if st.button("Ejecutar Respaldo Manual"):
            st.info("Funcionalidad de respaldo en desarrollo")
        
        if st.button("Verificar Integridad de Datos"):
            session = get_session()
            
            # Check data integrity
            personas_sin_nombre = session.query(Persona).filter(
                Persona.nombre_razon_social.is_(None)
            ).count()
            
            docs_sin_persona = session.query(Documento).filter(
                Documento.persona_relacionada_id.is_(None)
            ).count()
            
            st.write(f"**Personas sin nombre:** {personas_sin_nombre}")
            st.write(f"**Documentos sin persona:** {docs_sin_persona}")
            
            if personas_sin_nombre == 0 and docs_sin_persona == 0:
                st.success("✅ Integridad de datos correcta")
            else:
                st.warning("⚠️ Se encontraron inconsistencias en los datos")
            
            session.close()

if __name__ == "__main__":
    main()
