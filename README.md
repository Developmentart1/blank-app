# 🏢 KYC PLDFT - Sistema de Desarrollo Inmobiliario

Sistema integral de **Know Your Customer (KYC)** y **Prevención de Lavado de Dinero y Financiamiento al Terrorismo (PLDFT)** diseñado específicamente para empresas de desarrollo inmobiliario en México.

## 📋 Características Principales

### 🔐 Gestión de Personas
- **Personas Físicas (PF)** y **Personas Morales (PM)**
- Validación automática de RFC y CURP
- Control de estatus de expedientes
- Gestión de roles (Propietario Real, Beneficiario Final, Representante Legal, Cliente)
- Identificación automática de **PEP (Personas Expuestas Políticamente)**
- Control de jurisdicciones de alto riesgo

### 📄 Gestión de Documentos
- Múltiples tipos de documentos (INE, Pasaporte, Acta Constitutiva, etc.)
- Control de vigencia automático
- Alertas por documentos vencidos
- Gestión de archivos adjuntos

### 💳 Gestión de Transacciones
- Registro de operaciones inmobiliarias
- **Control automático de umbrales UIF** (8,025 UMA)
- Seguimiento de origen y destino de recursos
- Generación automática de avisos

### 🚨 Sistema de Alertas
- Alertas automáticas por:
  - Documentos vencidos
  - Operaciones que superan umbral UIF
  - Personas PEP
  - Operaciones inusuales
  - Jurisdicciones de alto riesgo

### 📊 Reportes y Analytics
- Dashboard ejecutivo con KPIs
- Reportes regulatorios (PEP, UIF)
- Métricas de cumplimiento
- Exportación a CSV
- Gráficos interactivos

### 🔒 Control de Acceso
- **Representante de Cumplimiento**: Acceso completo
- **Equipo de Ventas**: Acceso limitado a personas
- **Auditoría**: Solo lectura

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python + SQLAlchemy
- **Base de Datos**: SQLite
- **Visualizaciones**: Plotly
- **Validaciones**: Regex para RFC/CURP
- **UI Components**: streamlit-option-menu, streamlit-aggrid

## 📦 Instalación

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd kyc-pldft-desarrollo-inmobiliario
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Inicializar la base de datos con datos de prueba**
```bash
python init_sample_data.py
```

4. **Ejecutar la aplicación**
```bash
streamlit run streamlit_app.py
```

5. **Acceder a la aplicación**
```
http://localhost:8501
```

## 🏗️ Estructura del Proyecto

```
kyc-pldft/
├── streamlit_app.py          # Aplicación principal
├── database.py               # Modelos de base de datos
├── init_sample_data.py       # Script de datos de prueba
├── requirements.txt          # Dependencias
├── README.md                # Documentación
├── kyc_pldft.db             # Base de datos SQLite (se crea automáticamente)
└── .gitignore               # Archivos ignorados por Git
```

## 📊 Modelo de Datos

### Tablas Principales

#### 👥 Personas
- Información básica (nombre, RFC, CURP, nacionalidad)
- Datos de contacto y domicilio
- Clasificación PEP y jurisdicciones de riesgo
- Control de estatus de expediente

#### 📄 Documentos
- Vinculación con personas
- Control de vigencia
- Tipos de documento estandarizados
- Gestión de archivos

#### 💰 Transacciones
- Operaciones inmobiliarias
- Control de montos y umbrales
- Trazabilidad de recursos
- Estatus de avisos UIF

#### 🚨 Alertas
- Sistema automatizado de alertas
- Clasificación por tipo y prioridad
- Seguimiento de resolución
- Asignación de responsables

#### 👑 PEP_Relaciones
- Registro de vínculos con PEP
- Información del cargo público
- Períodos de ejercicio
- Tipo de parentesco

## ⚙️ Configuración

### Umbrales UIF
- **Umbral actual**: 8,025 UMA (≈ $871,000 MXN en 2024)
- **UMA 2024**: $108.57 pesos
- Configuración automática de alertas

### Validaciones
- **RFC**: Formato estándar mexicano
- **CURP**: Solo para personas físicas
- **Email**: Validación de formato
- **Fechas**: Control de vigencia

### Automatizaciones

#### 🤖 Triggers Automáticos

1. **Actualización de Fecha**
   - Se ejecuta al modificar personas o documentos
   - Actualiza timestamp de última modificación

2. **Control de Documentos Vencidos**
   - Verificación diaria de vigencias
   - Creación automática de alertas

3. **Umbral UIF**
   - Evaluación en tiempo real
   - Marcado automático para reporte

4. **Flag PEP**
   - Detección automática de personas PEP
   - Creación de alertas de cumplimiento

## 📈 Vistas Predefinidas

- **Expedientes Incompletos**: Personas con documentación pendiente
- **PEP & Vínculos**: Personas expuestas políticamente
- **Documentos Vencidos**: Control de vigencias
- **Avisos Pendientes**: Transacciones para reporte UIF

## 🔐 Seguridad y Cumplimiento

### Controles de Acceso
- Autenticación por roles
- Permisos granulares por tabla
- Auditoría de acciones

### Respaldos
- **Frecuencia**: Semanal
- **Formato**: CSV + archivos adjuntos
- **Almacenamiento**: S3 (configurable)
- **Encriptación**: AES-256

### Regulaciones Cumplidas
- **Ley Federal para la Prevención e Identificación de Operaciones con Recursos de Procedencia Ilícita**
- **Disposiciones de la UIF (Unidad de Inteligencia Financiera)**
- **Normativas CNBV para actividades vulnerables**

## 🚀 Uso del Sistema

### Dashboard Principal
1. **Métricas Clave**: Total personas, expedientes incompletos, alertas pendientes
2. **Gráficos**: Distribución de estatus, tipos de alertas
3. **Alertas Recientes**: Monitoreo en tiempo real

### Gestión de Personas
1. **Crear Nueva Persona**: Formulario con validaciones automáticas
2. **Búsqueda Avanzada**: Por nombre, RFC, CURP
3. **Filtros**: Tipo, estatus, clasificación PEP

### Procesamiento de Transacciones
1. **Registro**: Captura completa de operación
2. **Validación Automática**: Verificación de umbrales
3. **Generación de Avisos**: Proceso automatizado UIF

### Gestión de Alertas
1. **Monitoreo**: Dashboard de alertas activas
2. **Investigación**: Herramientas de análisis
3. **Resolución**: Workflow de cierre

## 📊 Reportes Disponibles

### Reportes Regulatorios
- **Reporte PEP**: Listado completo de personas expuestas
- **Reporte UIF**: Transacciones pendientes de aviso
- **Reporte de Cumplimiento**: Métricas de efectividad

### Analytics
- **Distribución de Clientes**: Por tipo y origen
- **Tendencias de Transacciones**: Análisis temporal
- **Métricas de Completitud**: Estatus de expedientes

## 🔧 Personalización

### Catálogos Configurables
- Tipos de documento
- Roles de personas
- Países y nacionalidades
- Tipos de alerta

### Umbrales Ajustables
- Montos UIF
- Períodos de revisión
- Criterios de riesgo

## 🆘 Soporte y Mantenimiento

### Verificación de Integridad
```bash
# Desde la interfaz web: Configuración > Sistema > Verificar Integridad
```

### Respaldo Manual
```bash
# Desde la interfaz web: Configuración > Sistema > Ejecutar Respaldo
```

### Logs del Sistema
- Eventos de alertas
- Transacciones procesadas
- Accesos de usuarios
- Errores del sistema

## 📝 Datos de Prueba

El sistema incluye datos de muestra que demuestran:
- ✅ Personas PEP y sus vínculos
- ✅ Documentos con diferentes estados de vigencia
- ✅ Transacciones que activan alertas UIF
- ✅ Clientes de jurisdicciones de alto riesgo
- ✅ Diversos tipos de documentos y roles

### Usuarios de Prueba
- **Representante Cumplimiento**: Acceso completo
- **Equipo Ventas**: Acceso limitado
- **Auditoría**: Solo lectura

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear branch para feature
3. Implementar cambios con tests
4. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo LICENSE para más detalles.

## 📞 Contacto

Para soporte técnico o consultas sobre implementación, contactar al equipo de desarrollo.

---

**Desarrollado con ❤️ para el cumplimiento regulatorio en el sector inmobiliario mexicano**
