import Conexion
import sys

# Crear un cursor
conexion = Conexion.establecer_conexion()
cursor = conexion.cursor()

print("-------------------------------------------------------------")
print("Bienvenido al identificador de sintaxis de oraciones SintaxPy")
print("-------------------------------------------------------------")

# Menú principal
def menu_principal():
    print("1. Ingresar con una cuenta existente")
    print("2. Registrarse")
    print("3. Salir")

# Menú usuario
def menu_usuario():
    print("-------------------------------------------------------------")
    print("1. Verificar si una oración esta en voz activa o pasiva")
    print("2. Ver oraciones guardadas")
    print("3. Salir")

# Registrar usuario nuevos
def registro_usuario():
    nombre = input("Ingresar nombre: ")
    apellido = input("Ingresar apellido(s): ")
    fecha_nacimiento = input("Ingresar fecha de nacimiento: ")
    nacionalidad = input("Ingresar nacionalidad: ")
    nombre_user = input("Ingresar el nombre con el que ingresará a la app: ")
    contraseña = input("Ingresar contraseña: ")

    # Guardar datos del usuario en la base de datos
    query = "INSERT INTO usuario(nombre, apellido, fecha_nacimiento, nacionalidad, nombre_user, contraseña) VALUES (%s, %s, %s, %s, %s, %s)"
    datos_user = (nombre, apellido, fecha_nacimiento, nacionalidad, nombre_user, contraseña)

    cursor.execute(query, datos_user)
    conexion.commit()
    print("Registro exitoso.")

# Ingresar a la aplicación
def autenticar_usuario():
    global resultado_usuario
    user = input("Ingrese su usuario: ")
    password = input("Ingrese su contraseña: ")

    # Consulta parametrizada para verificar las credenciales
    query_usuario = "SELECT * FROM usuario WHERE nombre_user = %s AND contraseña = %s"
    datos_usuario = (user, password)

    cursor.execute(query_usuario, datos_usuario)

    # Procesar el resultado de la consulta
    resultado_usuario = cursor.fetchone()

    if resultado_usuario:
        print("Inicio de sesión exitoso.")
        print("Bienvenido nuevamente.")
    else:
        print("Credenciales incorrectas.")

# Ver oraciones guardadas
def ver_oraciones_guardadas():
    if resultado_usuario:
        # Obtener el ID del usuario autenticado
        id_usuario_autenticado = resultado_usuario[0]
        
        # Consulta para obtener las oraciones guardadas por el usuario actual
        query_oraciones = "SELECT texto FROM sintaxis WHERE id_usuario = %s"
        cursor.execute(query_oraciones, (id_usuario_autenticado,))
        
        # Obtener todas las oraciones del resultado
        oraciones_guardadas = cursor.fetchall()

        if oraciones_guardadas:
            print("Oraciones guardadas:")
            for oracion in oraciones_guardadas:
                print(oracion[0])
        else:
            print("No hay oraciones guardadas.")
    else:
        print("Debe iniciar sesión para ver las oraciones guardadas.")

# Identificador de sintaxis
def identificador():
    # Lista con conjugaciones del verbo ser/estar
    verbo_estar_ser = [
        "soy", "eres", "es", "somos", "sois", "son",  # Presente (Ser)
        "estoy", "estás", "está", "estamos", "estáis", "están",  # Presente (Estar)
        "fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron",  # Pretérito Perfecto Simple (Ser)
        "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron",  # Pretérito Perfecto Simple (Estar)
        "era", "eras", "era", "éramos", "erais", "eran",  # Pretérito Imperfecto (Ser)
        "estaba", "estabas", "estaba", "estábamos", "estabais", "estaban",  # Pretérito Imperfecto (Estar)
        "seré", "serás", "será", "seremos", "seréis", "serán",  # Futuro del Indicativo (ser)
        "estaré", "estarás", "estará", "estaremos", "estaréis", "estarán",  # Futuro del Indicativo (Estar)
        "sido",  # Pretérito Perfecto Compuesto (Ser)
        "estado",  # Pretérito Perfecto Compuesto, pretérito pluscuamperfecto (Estar)
        "sido"]  # Pretérito Pluscuamperfecto (Ser)

    # Lista de terminaciones regulares del participio regular
    terminaciones_regulares = ["ado", "ados", "ada", "adas", "idos", "ido", "idas", "idos", "idas", "idos", "iendo", "ando", "ida"]

    # Lista de terminaciones irregulares del participio irregular
    terminaciones_irregulares = ["cho", "lto", "sto", "to", "scho", "rto", "sisto", "rcho",
                                 "visto", "ccho", "chcho", "mcho", "lcho", "so", "tos", "sos",
                                 "ta", "sa", "cha", "tas", "sas", "chas"]

    # Ingresar la oración
    print("-------------------------------------------------------------")
    oracion = input("Ingresar una oración: ")
    palabras = oracion.split()

    for i in range(len(palabras) - 1):
        palabra1, palabra2 = palabras[i], palabras[i + 1]

        # Verificar si la primera palabra es un verbo de ser/estar
        if palabra1.lower() in verbo_estar_ser:

            # Verificar las terminaciones de la segunda palabra para oraciones regulares
            for terminacion_regular in terminaciones_regulares:
                if palabra2.lower().endswith(terminacion_regular) and len(palabra2) >= len(terminacion_regular):
                    print("La oración ingresada es una oración pasiva regular.")
                    respuesta = input("¿Desea guardar la oración en la base de datos? (Sí/No): ").lower()
                    if respuesta == 'si':
                        guardar_en_base_de_datos(oracion, "pasiva", "regular")
                    return

            # Verificar las terminaciones de la segunda palabra para oraciones irregulares
            for terminacion_irregular in terminaciones_irregulares:
                if palabra2.lower().endswith(terminacion_irregular) and len(palabra2) >= len(terminacion_irregular):
                    print("La oración ingresada es una oración pasiva irregular.")
                    respuesta = input("¿Desea guardar la oración en la base de datos? (Sí/No): ").lower()
                    if respuesta == 'si':
                        guardar_en_base_de_datos(oracion, "pasiva", "irregular")
                    return

    else:
        print("La oración no es una oración pasiva.")

        # Preguntar al usuario si desea guardar la oración en la base de datos
        respuesta = input("¿Desea guardar la oración en la base de datos? (Si/No): ").lower()
        if respuesta == 'si':
            guardar_en_base_de_datos(oracion, "activa", "-")  # Si la oración no es pasiva, se guarda como activa

def guardar_en_base_de_datos(oracion, voz, tipo):
    query_guardar_oracion = "INSERT INTO sintaxis (texto, voz, tipo, id_usuario) VALUES (%s, %s, %s, %s)"
    id_usuario_autenticado = resultado_usuario[0] if resultado_usuario else None
    datos_oracion = (oracion, voz, tipo, id_usuario_autenticado)

    try:
        cursor.execute(query_guardar_oracion, datos_oracion)
        conexion.commit()
        print("Oración guardada exitosamente.")
    except Exception as e:
        print(f"Error al guardar la oración: {e}")

# Salir del programa
def salir():
    cursor.close()
    Conexion.cerrar_conexion(conexion)
    sys.exit()

# Condicional para ejecutar menu_principal()
while True:
    menu_principal()
    print("-------------------------------------------------------------")
    opcion = input("Ingrese la opción deseada: ")
    print("-------------------------------------------------------------")

    if opcion == "1":
        print("-------------------------------------------------------------")
        autenticar_usuario()

        while True:
            menu_usuario()
            opcion_menu_usuario = input("Ingrese la opción deseada: ")
            print("-------------------------------------------------------------")

            if opcion_menu_usuario == "1":
                identificador()
            elif opcion_menu_usuario == "2":
                ver_oraciones_guardadas()
            elif opcion_menu_usuario == "3":
                salir()
            else:
                print("Ingrese una opción válida.")

    elif opcion == "2":
        print("-------------------------------------------------------------")
        registro_usuario()
    elif opcion == "3":
        salir()
    else:
        print("Ingrese una opción válida.")
