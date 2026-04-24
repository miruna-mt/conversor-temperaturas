# conversor_streamlit.py - Convertidor de temperaturas (versión web)
import streamlit as st
# Configurar la página
st.set_page_config(
    page_title="Conversor de Temperaturas",
    page_icon="🌡️",
    layout="centered"
)

# ============ FUNCIONES DE CONVERSIÓN ============

def celsius_a_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def celsius_a_kelvin(celsius):
    return celsius + 273.15

def fahrenheit_a_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def fahrenheit_a_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_a_celsius(kelvin):
    return kelvin - 273.15

def kelvin_a_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def obtener_simbolo(unidad):
    if unidad == "Celsius":
        return "°C"
    elif unidad == "Fahrenheit":
        return "°F"
    elif unidad == "Kelvin":
        return "K"
    return ""

def validar_cero_absoluto(valor, unidad):
    """Verifica que la temperatura no sea menor al cero absoluto"""
    cero_absoluto = -273.15
    if unidad == "Celsius":
        temp_celsius = valor
    elif unidad == "Fahrenheit":
        temp_celsius = fahrenheit_a_celsius(valor)
    else:
        temp_celsius = kelvin_a_celsius(valor)
    return temp_celsius >= cero_absoluto

def convertir_temperatura(valor, unidad_origen, unidad_destino):
    # Convertir a Celsius primero
    if unidad_origen == "Celsius":
        celsius = valor
    elif unidad_origen == "Fahrenheit":
        celsius = fahrenheit_a_celsius(valor)
    elif unidad_origen == "Kelvin":
        celsius = kelvin_a_celsius(valor)
    else:
        return None
    
    # Convertir desde Celsius a destino
    if unidad_destino == "Celsius":
        return celsius
    elif unidad_destino == "Fahrenheit":
        return celsius_a_fahrenheit(celsius)
    elif unidad_destino == "Kelvin":
        return celsius_a_kelvin(celsius)
    else:
        return None

# ============ INTERFAZ DE USUARIO ============

# Título
st.title("🌡️ Conversor de Temperaturas")
st.markdown("Convierte entre Celsius, Fahrenheit y Kelvin")
st.divider()

# Columnas para entrada de datos
col1, col2, col3 = st.columns(3)

with col1:
    valor = st.number_input(
        "Temperatura a convertir:",
        value=0,
        step=1,
        format="%d"
    )

with col2:
    unidad_origen = st.selectbox(
        "Convertir DESDE:",
        ["Celsius", "Fahrenheit", "Kelvin"]
    )

with col3:
    unidad_destino = st.selectbox(
        "Convertir A:",
        ["Celsius", "Fahrenheit", "Kelvin"]
    )

# Botón de conversión
if st.button("🔄 CONVERTIR", type="primary", use_container_width=True):
    # Validar cero absoluto
    if not validar_cero_absoluto(float(valor), unidad_origen):
        st.error("❌ La temperatura está por debajo del cero absoluto")
        st.caption("El cero absoluto es -273.15°C, -459.67°F o 0K")
    else:
        resultado = convertir_temperatura(float(valor), unidad_origen, unidad_destino)
        if resultado is not None:
            simbolo_origen = obtener_simbolo(unidad_origen)
            simbolo_destino = obtener_simbolo(unidad_destino)
            
            # Mostrar resultado
            st.success(f"## {valor}{simbolo_origen} = {resultado:.2f}{simbolo_destino}")
            
            # Guardar en historial
            if "historial" not in st.session_state:
                st.session_state.historial = []
            st.session_state.historial.append({
                "valor": valor,
                "origen": unidad_origen,
                "simbolo_origen": simbolo_origen,
                "resultado": resultado,
                "destino": unidad_destino,
                "simbolo_destino": simbolo_destino
            })

# ============ HISTORIAL ============
st.divider()
st.subheader("📜 Historial de conversiones")

if "historial" in st.session_state and st.session_state.historial:
    for conv in st.session_state.historial[-10:]:
        st.write(f"• {conv['valor']}{conv['simbolo_origen']} → {conv['resultado']:.2f}{conv['simbolo_destino']}")
    
    # Botón para limpiar historial
    if st.button("🗑️ Limpiar historial"):
        st.session_state.historial = []
        st.rerun()
else:
    st.info("Aún no hay conversiones. ¡Haz clic en CONVERTIR!")

# ============ PIE DE PÁGINA ============
st.divider()
st.caption("Versión web - Convertidor de Temperaturas 🌡️")