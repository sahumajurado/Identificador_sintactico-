import mysql.connector as mysql

def establecer_conexion():
    try:
        conexion = mysql.connect(
            user='root',
            password="12345678",
            host="localhost",
            database="db_identificadorsintactico",
            port="3306"
        )
        print("Conexión exitosa:", conexion)
        return conexion

    except mysql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        print(f"Error Code: {e.errno}")
        print(f"SQL State: {e.sqlstate}")
        return None

def cerrar_conexion(conexion):
    if conexion and conexion.is_connected():
       conexion.close()

# Llama a la función para establecer la conexión
conexion = establecer_conexion()

# Finalmente, cierra la conexión cuando hayas terminado
cerrar_conexion(conexion)
