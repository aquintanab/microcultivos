# 🌿 Verdana - Jardín Inteligente

Sistema de monitoreo avanzado para microcultivos urbanos con tecnología IoT.

## 🚀 Características

### ✨ Interfaz Web Avanzada
- **Dashboard interactivo** con métricas en tiempo real
- **Gráficos combinados** para visualización temporal
- **Sistema de alertas** automático con códigos de color
- **Recomendaciones inteligentes** basadas en umbrales configurables
- **Actualización automática** de datos
- **Análisis estadístico** completo (promedios, máximos, mínimos, tendencias)

### 📊 Sensores Monitoreados
- **🌡️ Temperatura**: Monitoreo continuo con alertas de rango óptimo (18-28°C)
- **💧 Humedad**: Control de humedad relativa con alertas (40-80%)
- **☀️ Radiación UV**: Índice UV con recomendaciones de protección
- **🔥 Índice de Calor**: Cálculo automático basado en temperatura y humedad

### 🤖 Sistema de Recomendaciones Automatizadas

#### Temperatura
- **Muy baja (< 18°C)**: Recomienda calefacción adicional
- **Muy alta (> 28°C)**: Sugiere ventilación y sombra
- **Crítica (< 10°C o > 35°C)**: Alertas de acción inmediata

#### Humedad
- **Muy baja (< 40%)**: Recomienda riego o humidificador
- **Muy alta (> 80%)**: Sugiere mejora de ventilación
- **Crítica (< 20% o > 90%)**: Alertas de acción urgente

#### Radiación UV
- **Baja (< 3)**: Sugiere luz artificial complementaria
- **Alta (> 8)**: Recomienda protección con sombra
- **Muy alta (> 11)**: Alerta de protección inmediata

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8 o superior
- Acceso a base de datos InfluxDB
- Credenciales de InfluxDB (URL, Token, Organización, Bucket)

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd koru-garden-monitor
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar credenciales**
   - Editar `config.py` con tus credenciales de InfluxDB
   - Ajustar umbrales de alertas según tus necesidades

5. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

6. **Acceder a la aplicación**
   - Abrir navegador en `http://localhost:8501`

## ⚙️ Configuración

### Archivo `config.py`

Personaliza los siguientes parámetros:

```python
# Umbrales de temperatura
THRESHOLDS = {
    "temperature": {
        "min": 18,          # °C mínima óptima
        "max": 28,          # °C máxima óptima
        "critical_low": 10, # °C crítica baja
        "critical_high": 35 # °C crítica alta
    }
}
```

### Sensores Configurables

Añade nuevos sensores en la sección `SENSORS`:

```python
"nuevo_sensor": {
    "measurement": "nombre_medicion",
    "field": "campo_sensor", 
    "unit": "unidad",
    "icon": "🔧"
}
```

## 📈 Uso de la Aplicación

### Panel Principal
1. **Métricas en tiempo real**: Visualiza valores actuales de todos los sensores
2. **Estado general**: Indicador de salud global del sistema
3. **Alertas críticas**: Notificaciones destacadas para atención inmediata

### Controles Laterales
- **Rango de tiempo**: Selecciona período de datos (30 min - 24 horas)
- **Auto-actualización**: Configura actualización automática
- **Umbrales**: Visualiza límites configurados

### Análisis Detallado
- **Gráficos temporales**: Visualización combinada de todos los sensores
- **Estadísticas**: Cálculos automáticos de tendencias y variaciones
- **Datos crudos**: Acceso a información detallada para análisis avanzado

### Recomendaciones Automatizadas
El sistema analiza continuamente los datos y genera recomendaciones específicas:

- **🟢 Estado Óptimo**: Condiciones ideales para el crecimiento
- **🟡 Atención Requerida**: Ajustes menores necesarios
- **🔴 Acción Crítica**: Intervención inmediata requerida

## 📋 Estructura del Proyecto

```
koru-garden-monitor/
├── app.py              # Aplicación principal de Streamlit
├── config.py           # Configuración y parámetros
├── requirements.txt    # Dependencias de Python
├── README.md          # Documentación
└── assets/            # Recursos adicionales (opcional)
```

## 🔧 Personalización

### Añadir Nuevos Sensores

1. **Configurar en `config.py`**:
```python
SENSORS["mi_sensor"] = {
    "measurement": "medicion_sensor",
    "field": "campo_dato",
    "unit": "unidad",
    "icon": "🆕"
}
```

2. **Añadir umbrales**:
```python
THRESHOLDS["mi_sensor"] = {
    "min": valor_minimo,
    "max": valor_maximo
}
```

3. **Crear recomendaciones**:
```python
RECOMMENDATIONS["mi_sensor"] = {
    "too_low": "Mensaje para valor bajo",
    "too_high": "Mensaje para valor alto",
    "optimal": "Mensaje para valor óptimo"
}
```

### Modificar Apariencia

El archivo `app.py` incluye CSS personalizado que puedes modificar:

```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        # Personaliza colores, fuentes, etc.
    }
</style>
""", unsafe_allow_html=True)
```

## 🌐 Despliegue en Producción

### Streamlit Cloud
1. Sube el código a GitHub
2. Conecta tu repositorio a Streamlit Cloud
3. Configura las variables de entorno
4. Despliega automáticamente

### Docker (Opcional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔍 Solución de Problemas

### Errores Comunes

**Error de conexión a InfluxDB**:
- Verificar credenciales en `config.py`
- Comprobar conectividad de red
- Validar permisos de token

**Sin datos en gráficos**:
- Verificar nombres de measurements y fields
- Comprobar rango de tiempo seleccionado
- Revisar formato de datos en InfluxDB

**Problemas de rendimiento**:
- Reducir rango de tiempo
- Optimizar consultas en `query_sensor_data()`
- Considerar agregación de datos

### Logs y Debugging

Habilitar logs detallados:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Integración con Grafana

Para crear un dashboard en Grafana complementario:

### Consultas Flux Recomendadas

**Temperatura**:
```flux
from(bucket: "homeiot")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "airSensor" and r["_field"] == "temperature")
```

**Humedad**:
```flux
from(bucket: "homeiot")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "airSensor" and r["_field"] == "humidity")
```

**UV Index**:
```flux
from(bucket: "homeiot")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "uv_sensor" and r["_field"] == "uv_index")
```

### Configuración de Alertas en Grafana

1. **Crear reglas de alerta** basadas en los mismos umbrales
2. **Configurar notificaciones** (email, Slack, etc.)
3. **Dashboard de estado** con indicadores visuales

## 🤝 Contribuciones

### Cómo Contribuir
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con tests
4. Enviar Pull Request

### Áreas de Mejora
- [ ] Predicciones con Machine Learning
- [ ] Integración con más tipos de sensores
- [ ] API REST para acceso programático
- [ ] Notificaciones push móviles
- [ ] Histórico de recomendaciones
- [ ] Exportación de reportes PDF

### Recursos Adicionales
- [Documentación InfluxDB](https://docs.influxdata.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **InfluxData** por la base de datos de series temporales
- **Streamlit** por el framework de aplicaciones web
- **Plotly** por las visualizaciones interactivas
- **Comunidad IoT** por inspiración y mejores prácticas

---

**🌱 Verdana Jardín Inteligente** - Cuidando el futuro verde con tecnología inteligente
