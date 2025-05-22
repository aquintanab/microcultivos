# Configuración de InfluxDB
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "rnRx-Nk8dXeumEsQeDT4hk78QFWNTOVim7UrH5fnYKVSoQQIkhCwKq03-UMKN-S0Nj-DbfmrMD0HUI61qRJaiw=="
ORG = "0925ccf91ab36478"
BUCKET = "homeiot"

# Configuración de umbrales para alertas y recomendaciones
THRESHOLDS = {
    "temperature": {
        "min": 18,  # °C - Temperatura mínima óptima
        "max": 28,  # °C - Temperatura máxima óptima
        "critical_low": 10,  # °C - Temperatura crítica baja
        "critical_high": 35   # °C - Temperatura crítica alta
    },
    "humidity": {
        "min": 40,  # % - Humedad mínima óptima
        "max": 80,  # % - Humedad máxima óptima
        "critical_low": 20,  # % - Humedad crítica baja
        "critical_high": 90   # % - Humedad crítica alta
    },
    "uv": {
        "low": 3,      # Índice UV bajo
        "moderate": 6,  # Índice UV moderado
        "high": 8,     # Índice UV alto
        "very_high": 11 # Índice UV muy alto
    }
}

# Configuración de sensores y mediciones
SENSORS = {
    "temperature": {
        "measurement": "airSensor", 
        "field": "temperature",
        "unit": "°C",
        "icon": "🌡️"
    },
    "humidity": {
        "measurement": "airSensor",
        "field": "humidity", 
        "unit": "%",
        "icon": "💧"
    },
    "heat_index": {
        "measurement": "airSensor",
        "field": "heat_index",
        "unit": "",
        "icon": "🔥"
    },
    "uv_index": {
        "measurement": "uv_sensor",
        "field": "uv_index",
        "unit": "",
        "icon": "☀️"
    },
    "uv_raw": {
        "measurement": "uv_sensor", 
        "field": "uv_raw",
        "unit": "",
        "icon": "📡"
    }
}

# Configuración de la interfaz
UI_CONFIG = {
    "title": "🌿 Koru - Jardín Inteligente",
    "subtitle": "Sistema de monitoreo avanzado para microcultivos urbanos",
    "description": "Cuidando tu jardín con tecnología IoT",
    "theme_color": "#667eea",
    "refresh_intervals": [10, 30, 60, 120, 300],  # segundos
    "time_ranges": [30, 60, 120, 180, 360, 720, 1440]  # minutos
}

# Mensajes de recomendaciones
RECOMMENDATIONS = {
    "temperature": {
        "too_low": "🔥 **Acción requerida**: La temperatura es muy baja. Considera mover las plantas a un lugar más cálido o usar calefacción adicional.",
        "too_high": "❄️ **Acción requerida**: La temperatura es muy alta. Proporciona ventilación o sombra para reducir la temperatura.",
        "optimal": "🌡️ **Perfecto**: La temperatura está en rango óptimo para los microcultivos.",
        "critical_low": "🚨 **CRÍTICO**: Temperatura extremadamente baja. ¡Acción inmediata requerida!",
        "critical_high": "🚨 **CRÍTICO**: Temperatura extremadamente alta. ¡Acción inmediata requerida!"
    },
    "humidity": {
        "too_low": "💦 **Acción requerida**: La humedad es muy baja. Aumenta el riego o usa un humidificador.",
        "too_high": "🌬️ **Acción requerida**: La humedad es muy alta. Mejora la ventilación para reducir la humedad.",
        "optimal": "💧 **Perfecto**: La humedad está en el rango ideal.",
        "critical_low": "🚨 **CRÍTICO**: Humedad extremadamente baja. ¡Riego inmediato necesario!",
        "critical_high": "🚨 **CRÍTICO**: Humedad extremadamente alta. ¡Ventilación urgente!"
    },
    "uv": {
        "low": "💡 **Atención**: Baja radiación UV. Considera complementar con luz artificial para el crecimiento.",
        "moderate": "☀️ **Perfecto**: Niveles de UV adecuados para el crecimiento.",
        "high": "🏠 **Acción requerida**: Radiación UV alta. Proporciona sombra parcial a los cultivos.",
        "very_high": "🚨 **CRÍTICO**: Radiación UV muy alta. ¡Protección inmediata necesaria!"
    }
}

# Configuración de colores para gráficos
CHART_COLORS = {
    "temperature": "#FF6B6B",
    "humidity": "#4ECDC4", 
    "uv_index": "#FFE66D",
    "uv_raw": "#FFA726",
    "heat_index": "#FF8A65"
}

# Configuración de alertas
ALERT_LEVELS = {
    "info": "🔵",
    "warning": "🟡", 
    "critical": "🔴",
    "success": "🟢"
}
