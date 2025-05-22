import streamlit as st
from influxdb_client import InfluxDBClient
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

# Configuración desde archivo local
from config import INFLUX_URL, INFLUX_TOKEN, ORG, BUCKET

# Configuración de umbrales para recomendaciones
TEMP_MIN = 18  # °C
TEMP_MAX = 28  # °C
HUMIDITY_MIN = 40  # %
HUMIDITY_MAX = 80  # %
UV_MAX = 8  # Índice UV crítico

# Función para consultar datos con manejo de errores mejorado
def query_sensor_data(measurement, field, range_minutes=60):
    """Consulta datos de un sensor específico"""
    try:
        client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
        query_api = client.query_api()

        query = f'''
        from(bucket: "{BUCKET}")
          |> range(start: -{range_minutes}m)
          |> filter(fn: (r) => r["_measurement"] == "{measurement}" and r["_field"] == "{field}")
          |> sort(columns: ["_time"])
        '''

        result = query_api.query_data_frame(query)
        if result.empty:
            return pd.DataFrame()

        # Procesar resultado
        result = result.rename(columns={"_time": "time", "_value": field})
        result["time"] = pd.to_datetime(result["time"])
        return result[["time", field]]
    
    except Exception as e:
        st.error(f"Error consultando datos de {measurement}/{field}: {str(e)}")
        return pd.DataFrame()

def query_uv_data(range_minutes=60):
    """Consulta datos UV con campos específicos"""
    try:
        client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=ORG)
        query_api = client.query_api()

        query = f'''
        from(bucket: "{BUCKET}")
          |> range(start: -{range_minutes}m)
          |> filter(fn: (r) => r["_measurement"] == "uv_sensor" and (r["_field"] == "uv_index" or r["_field"] == "uv_raw"))
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> sort(columns: ["_time"])
        '''

        result = query_api.query_data_frame(query)
        if result.empty:
            return pd.DataFrame()

        result = result.rename(columns={"_time": "time"})
        result["time"] = pd.to_datetime(result["time"])
        return result[["time", "uv_index", "uv_raw"]] if "uv_index" in result.columns else result[["time", "uv_raw"]]
    
    except Exception as e:
        st.error(f"Error consultando datos UV: {str(e)}")
        return pd.DataFrame()

def calculate_statistics(df, field):
    """Calcula estadísticas básicas de un campo"""
    if df.empty or field not in df.columns:
        return {}
    
    data = df[field].dropna()
    if data.empty:
        return {}
    
    return {
        "promedio": round(data.mean(), 2),
        "maximo": round(data.max(), 2),
        "minimo": round(data.min(), 2),
        "mediana": round(data.median(), 2),
        "desviacion": round(data.std(), 2)
    }

def generate_recommendations(temp_stats, hum_stats, uv_stats):
    """Genera recomendaciones basadas en los datos"""
    recommendations = []
    alerts = []
    
    # Recomendaciones de temperatura
    if temp_stats and temp_stats.get("promedio"):
        temp_avg = temp_stats["promedio"]
        if temp_avg < TEMP_MIN:
            alerts.append("🌡️ **ALERTA**: Temperatura muy baja")
            recommendations.append("🔥 **Acción requerida**: Considera mover las plantas a un lugar más cálido o usar calefacción adicional")
        elif temp_avg > TEMP_MAX:
            alerts.append("🌡️ **ALERTA**: Temperatura muy alta")
            recommendations.append("❄️ **Acción requerida**: Proporciona ventilación o sombra para reducir la temperatura")
        else:
            recommendations.append("🌡️ **Perfecto**: La temperatura está en rango óptimo para los microcultivos")
    
    # Recomendaciones de humedad
    if hum_stats and hum_stats.get("promedio"):
        hum_avg = hum_stats["promedio"]
        if hum_avg < HUMIDITY_MIN:
            alerts.append("💧 **ALERTA**: Humedad muy baja")
            recommendations.append("💦 **Acción requerida**: Aumenta el riego o usa un humidificador")
        elif hum_avg > HUMIDITY_MAX:
            alerts.append("💧 **ALERTA**: Humedad muy alta")
            recommendations.append("🌬️ **Acción requerida**: Mejora la ventilación para reducir la humedad")
        else:
            recommendations.append("💧 **Perfecto**: La humedad está en el rango ideal")
    
    # Recomendaciones UV
    if uv_stats and uv_stats.get("maximo"):
        uv_max = uv_stats["maximo"]
        if uv_max > UV_MAX:
            alerts.append("☀️ **ALERTA**: Radiación UV muy alta")
            recommendations.append("🏠 **Acción requerida**: Proporciona sombra o protección UV a los cultivos")
        elif uv_max < 3:
            recommendations.append("☀️ **Atención**: Baja radiación UV, considera complementar con luz artificial")
        else:
            recommendations.append("☀️ **Perfecto**: Niveles de UV adecuados para el crecimiento")
    
    return recommendations, alerts

def create_metric_card(title, value, unit, delta=None, help_text=None):
    """Crear tarjeta de métrica personalizada"""
    if delta:
        st.metric(
            label=title,
            value=f"{value} {unit}",
            delta=f"{delta:+.1f}",
            help=help_text
        )
    else:
        st.metric(
            label=title,
            value=f"{value} {unit}" if value is not None else "Sin datos",
            help=help_text
        )

def create_combined_chart(temp_df, hum_df, uv_df):
    """Crear gráfico combinado con múltiples ejes Y"""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('🌡️ Temperatura (°C)', '💧 Humedad (%)', '☀️ Índice UV'),
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    # Temperatura
    if not temp_df.empty:
        fig.add_trace(
            go.Scatter(
                x=temp_df['time'], 
                y=temp_df['temperature'],
                mode='lines+markers',
                name='Temperatura',
                line=dict(color='#FF6B6B', width=2),
                marker=dict(size=4)
            ),
            row=1, col=1
        )
    
    # Humedad
    if not hum_df.empty:
        fig.add_trace(
            go.Scatter(
                x=hum_df['time'], 
                y=hum_df['humidity'],
                mode='lines+markers',
                name='Humedad',
                line=dict(color='#4ECDC4', width=2),
                marker=dict(size=4)
            ),
            row=2, col=1
        )
    
    # UV
    if not uv_df.empty and 'uv_index' in uv_df.columns:
        fig.add_trace(
            go.Scatter(
                x=uv_df['time'], 
                y=uv_df['uv_index'],
                mode='lines+markers',
                name='UV Index',
                line=dict(color='#FFE66D', width=2),
                marker=dict(size=4)
            ),
            row=3, col=1
        )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        title_text="📊 Monitoreo Integral de Sensores",
        title_x=0.5,
        font=dict(size=12)
    )
    
    return fig

# Configuración de la página
st.set_page_config(
    page_title="🌿 Verdana - Jardín Inteligente",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .alert-container {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .recommendation-container {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div > select {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🌿 Verdana - Jardín Inteligente</h1>
    <p>Sistema de monitoreo avanzado para microcultivos urbanos</p>
    <p><em>Cuidando tu jardín con tecnología IoT</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar con controles
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Selector de tiempo
    range_minutes = st.selectbox(
        "📅 Rango de tiempo:",
        options=[30, 60, 120, 180, 360, 720],
        index=1,
        format_func=lambda x: f"{x} minutos ({x//60}h)" if x >= 60 else f"{x} minutos"
    )
    
    # Auto-refresh
    auto_refresh = st.checkbox("🔄 Actualización automática", value=False)
    if auto_refresh:
        refresh_rate = st.slider("⏱️ Intervalo (segundos):", 10, 60, 30)
    
    st.markdown("---")
    st.markdown("### 📊 Umbrales de Alerta")
    st.write(f"🌡️ Temperatura: {TEMP_MIN}°C - {TEMP_MAX}°C")
    st.write(f"💧 Humedad: {HUMIDITY_MIN}% - {HUMIDITY_MAX}%")
    st.write(f"☀️ UV Máximo: {UV_MAX}")

# Auto-refresh logic
if auto_refresh:
    placeholder = st.empty()
    time.sleep(refresh_rate)
    st.rerun()

# Obtener datos
with st.spinner("📡 Consultando datos de sensores..."):
    temp_df = query_sensor_data("airSensor", "temperature", range_minutes)
    hum_df = query_sensor_data("airSensor", "humidity", range_minutes)
    uv_df = query_uv_data(range_minutes)

# Calcular estadísticas
temp_stats = calculate_statistics(temp_df, "temperature")
hum_stats = calculate_statistics(hum_df, "humidity")
uv_field = "uv_index" if not uv_df.empty and "uv_index" in uv_df.columns else "uv_raw"
uv_stats = calculate_statistics(uv_df, uv_field)

# Generar recomendaciones
recommendations, alerts = generate_recommendations(temp_stats, hum_stats, uv_stats)

# Mostrar alertas importantes
if alerts:
    st.markdown("## 🚨 Alertas Críticas")
    for alert in alerts:
        st.markdown(f'<div class="alert-container">{alert}</div>', unsafe_allow_html=True)

# Métricas principales
st.markdown("## 📈 Resumen de Condiciones Actuales")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if temp_stats:
        create_metric_card(
            "🌡️ Temperatura",
            temp_stats.get("promedio", "N/A"),
            "°C",
            help_text=f"Rango: {temp_stats.get('minimo', 'N/A')}°C - {temp_stats.get('maximo', 'N/A')}°C"
        )
    else:
        st.metric("🌡️ Temperatura", "Sin datos", "°C")

with col2:
    if hum_stats:
        create_metric_card(
            "💧 Humedad",
            hum_stats.get("promedio", "N/A"),
            "%",
            help_text=f"Rango: {hum_stats.get('minimo', 'N/A')}% - {hum_stats.get('maximo', 'N/A')}%"
        )
    else:
        st.metric("💧 Humedad", "Sin datos", "%")

with col3:
    if uv_stats:
        create_metric_card(
            "☀️ Índice UV",
            uv_stats.get("promedio", "N/A"),
            "",
            help_text=f"Máximo: {uv_stats.get('maximo', 'N/A')}"
        )
    else:
        st.metric("☀️ Índice UV", "Sin datos", "")

with col4:
    # Estado general del sistema
    status = "🟢 Óptimo" if not alerts else "🟡 Atención" if len(alerts) == 1 else "🔴 Crítico"
    st.metric("📊 Estado General", status, help_text="Basado en todos los sensores")

# Gráfico combinado
st.markdown("## 📊 Tendencias Temporales")
if not temp_df.empty or not hum_df.empty or not uv_df.empty:
    fig = create_combined_chart(temp_df, hum_df, uv_df)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("🔍 No hay datos disponibles para el rango de tiempo seleccionado")

# Análisis estadístico detallado
st.markdown("## 📊 Análisis Estadístico Detallado")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌡️ Temperatura")
    if temp_stats:
        st.json(temp_stats)
    else:
        st.info("Sin datos estadísticos")

with col2:
    st.markdown("### 💧 Humedad")
    if hum_stats:
        st.json(hum_stats)
    else:
        st.info("Sin datos estadísticos")

with col3:
    st.markdown("### ☀️ Radiación UV")
    if uv_stats:
        st.json(uv_stats)
    else:
        st.info("Sin datos estadísticos")

# Recomendaciones
st.markdown("## 💡 Recomendaciones Automatizadas")
if recommendations:
    for recommendation in recommendations:
        st.markdown(f'<div class="recommendation-container">{recommendation}</div>', unsafe_allow_html=True)
else:
    st.info("🤖 El sistema está analizando los datos para generar recomendaciones...")

# Datos crudos (opcional)
with st.expander("🔍 Ver datos crudos"):
    tab1, tab2, tab3 = st.tabs(["🌡️ Temperatura", "💧 Humedad", "☀️ UV"])
    
    with tab1:
        if not temp_df.empty:
            st.dataframe(temp_df.tail(50), use_container_width=True)
        else:
            st.info("Sin datos de temperatura")
    
    with tab2:
        if not hum_df.empty:
            st.dataframe(hum_df.tail(50), use_container_width=True)
        else:
            st.info("Sin datos de humedad")
    
    with tab3:
        if not uv_df.empty:
            st.dataframe(uv_df.tail(50), use_container_width=True)
        else:
            st.info("Sin datos UV")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌱 <strong>Koru Jardín Inteligente</strong> - Tecnología IoT para el cuidado sostenible</p>
    <p>Última actualización: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
