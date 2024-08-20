import streamlit as st
from streamlit_ace import st_ace
from openai import OpenAI

GROQ_API_KEY = "YOUR_API_KEY"
DEEPINFRA_API_KEY = "YOUR_API_KEY"

def generate(myinput, tokens=1024):
    openai = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    response = openai.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": myinput},
        ],
        max_tokens=tokens,
        temperature=0.7,
        stream=False
    )
    print(f"Token usage: {response.usage.total_tokens}")
    return response.choices[0].message.content

def generate405(myinput, tokens=1024):
    openai = OpenAI(
        api_key=DEEPINFRA_API_KEY,
        base_url="https://api.deepinfra.com/v1/openai",
    )

    chat_completion = openai.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct",
        messages=[
            {"role": "system", "content": "Eres una terminal de Linux. Compila el código C++ proporcionado por el usuario utilizando g++ y muestra la salida. Simula la ejecución del código.  Solo muestra la salida, sin incluir comentarios. NO soluciones el código, ni muestres un ejemplo correcto. Únicamente da pistas. Si el código contiene errores, no los corrijas. Simula los errores que se producirían en la ejecución real. Prueba el código con entradas y salidas simuladas. Además, evalúa el código con una calificación del 1 al 10, según la salida esperada y la salida real obtenida."},
            {"role": "user", "content": myinput},
        ],
        max_tokens=tokens,
        temperature=0.7,
        stream=False
    )
    print(chat_completion.usage.prompt_tokens + chat_completion.usage.completion_tokens)
    out = "\n" + chat_completion.choices[0].message.content
    return(str(chat_completion.usage.prompt_tokens + chat_completion.usage.completion_tokens) + " tokens = " + str((chat_completion.usage.prompt_tokens + chat_completion.usage.completion_tokens)*0.0000027) + "€\n" + out) # Change the price per token


def save_progress(key, value):
    with open(f".{key}", "w") as f:
        f.write(str(value))

def load_progress(key, default=0):
    try:
        with open(f".{key}", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        save_progress(key, default)
        return default

def elegir_tema(level):
    temas = [
        "Introducción a C++ y su entorno",
        "Variables y tipos de datos básicos",
        "Tipos de datos fundamentales: int, float, double, char",
        "Tipos de datos compuestos: arrays, estructuras",
        "Operadores aritméticos y lógicos",
        "Operadores de comparación y asignación",
        "Expresiones y sentencias",
        "Control de flujo: condicionales (if, else, switch)",
        "Control de flujo: bucles (for, while, do-while)",
        "Funciones y modularidad",
        "Declaración y definición de funciones",
        "Paso de parámetros por valor y referencia",
        "Return y tipos de retorno",
        "Listas y tuplas: estructuras de datos básicas",
        "Declaración y manipulación de listas y tuplas",
        "Indexación y slicing",
        "Diccionarios y conjuntos: estructuras de datos avanzadas",
        "Declaración y manipulación de diccionarios y conjuntos",
        "Acceso a elementos y operaciones",
        "Manejo de archivos: lectura y escritura",
        "Tipos de archivos y modos de apertura",
        "Lectura y escritura de archivos de texto y binarios",
        "Excepciones y errores: manejo y depuración",
        "Tipos de excepciones y errores",
        "Uso de try, catch y throw",
        "Programación orientada a objetos: conceptos básicos",
        "Clases y objetos: definición y uso",
        "Constructores y destructores",
        "Herencia y polimorfismo: conceptos avanzados",
        "Herencia múltiple y virtual",
        "Sobrecarga de operadores",
        "Módulos y paquetes: organización y reutilización",
        "Declaración y uso de módulos y paquetes",
        "Uso de cabeceras y bibliotecas",
        "Bibliotecas y herramientas: uso y creación",
        "Uso de bibliotecas estándar y de terceros",
        "Creación de bibliotecas y herramientas propias",
        "Técnicas de programación: recursividad y memoización",
        "Uso de funciones recursivas",
        "Memoización y optimización de funciones",
        "Desarrollo de aplicaciones: estructura y diseño",
        "Análisis y diseño de aplicaciones",
        "Uso de patrones de diseño",
        "Interfaz gráfica de usuario: creación y manejo",
        "Uso de bibliotecas gráficas y de GUI",
        "Creación de interfaces gráficas de usuario",
        "Bases de datos: conectividad y consulta",
        "Uso de bases de datos relacionales y NoSQL",
        "Consulta y manipulación de datos",
        "Redes y sockets: comunicación y transferencia",
        "Uso de sockets y protocolos de red",
        "Comunicación y transferencia de datos",
        "Seguridad y criptografía: conceptos y técnicas",
        "Uso de técnicas de seguridad y criptografía",
        "Autenticación y autorización",
        "Uso de SSL/TLS y HTTPS"
    ]
    return temas[level % len(temas)]

def main():
    st.set_page_config(layout="wide")
    # Initialize OpenAI clients with hardcoded API keys

    level = load_progress("level")
    seed = load_progress("seed")

    st.header(f"Has alcanzado el nivel {level}")

    tema = elegir_tema(level)

    col1, col2 = st.columns(2)

    with col1:
        tab1, tab2, tab3, tab4 = st.tabs(["Enunciado", "Solución propuesta", "Pistas", "Tests"])

        with tab1:
            if 'challenge' not in st.session_state:
                challenge_prompt = f"""Crea un reto en C++ relacionado con este tema: {tema}.
                El usuario número {seed} es de nivel principiante.
                NO uses LaTeX. NO muestres un ejemplo de código.
                Solo muestra el reto, con explicaciones relativas al reto.
                NO añadas ejemplos de salida. Muestra alguna ayuda para solucionar el reto.
                NO pongas la solución."""
                st.session_state.challenge = generate(challenge_prompt)
                seed += 1
                save_progress("seed", seed)
            st.markdown(st.session_state.challenge)

        with tab2:
            if st.button("Ver solución propuesta"):
                if 'solution' not in st.session_state:
                    st.session_state.solution = generate(f"Genera código en C++ para resolver este enunciado. Debe ser simple. No lo formatees como Markdown. NO añadas ```cpp. El enunciado es:\n{st.session_state.challenge}")
                st.code(st.session_state.solution, language="cpp")

        with tab3:
            if st.button("Ver pistas"):
                if 'hints' not in st.session_state:
                    st.session_state.hints = generate(f"Genera pistas claras para resolver este enunciado en C++. Solo muestra las pistas. NO añadas ```cpp. El enunciado es:\n{st.session_state.challenge}")
                st.markdown(st.session_state.hints)

        with tab4:
            if st.button("Ver tests"):
                if 'tests' not in st.session_state:
                    st.session_state.tests = generate(f"Crea varios ejemplos de salida para probar esta solución de C++. Solo muestra los ejemplos en lenguaje coloquial. Formatéalo como Markdown. El enunciado es:\n{st.session_state.challenge}")
                st.markdown(st.session_state.tests)

    with col2:
        if 'codigo_editado' not in st.session_state:
            st.session_state.codigo_editado = "// Mi código"

        st.session_state.codigo_editado = st_ace(value=st.session_state.codigo_editado, language="c_cpp", height=500, key="code_editor")
        st.write("Recuerda guardar el progreso.")
        if st.button("Enviar", key="enviar_button"):
            st.write("Análisis del código")
            output = generate405(st.session_state.codigo_editado)
            st.markdown(output)

    if st.button("Siguiente nivel"):
        level += 1
        save_progress("level", level)
        for key in ['challenge', 'solution', 'hints', 'tests']:
            st.session_state.pop(key, None)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
