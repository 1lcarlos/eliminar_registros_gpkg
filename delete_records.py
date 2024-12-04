import sqlite3

def eliminar_registro_con_relaciones(db_path, id_principal, mapeo):
    """
    Elimina un registro en la tabla principal y sus relaciones en cascada según el mapeo proporcionado.
    Registra logs en un archivo para conocer el estado de cada eliminación.

    :param db_path: Ruta al archivo de la base de datos SQLite.
    :param id_principal: ID del registro en la tabla principal a eliminar.
    :param mapeo: Diccionario con el mapeo de tablas y relaciones.
    """
    log_file = "eliminacion_log.txt"

    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Crear o limpiar el archivo de log
        with open(log_file, "w") as log:
            log.write("Inicio del proceso de eliminación\n")

        # Ordenar relaciones para eliminar primero las dependencias
        relaciones = mapeo["relaciones"]

        print(f"Iniciando eliminación del registro con ID {id_principal}...")

        # Eliminar registros de las tablas relacionadas
        for relacion in relaciones:
            tabla_relacionada = relacion["tabla_relacionada"]
            clave_foranea = relacion["clave_foranea"]

            try:
                print(f"Eliminando registros de la tabla '{tabla_relacionada}' donde '{clave_foranea}' = {id_principal}...")
                query = f"DELETE FROM {tabla_relacionada} WHERE {clave_foranea} = ?"
                cursor.execute(query, (id_principal,))
                registros_eliminados = cursor.rowcount

                with open(log_file, "a") as log:
                    log.write(f"Tabla: {tabla_relacionada}, Registros eliminados: {registros_eliminados}\n")

                print(f"Registros eliminados en '{tabla_relacionada}': {registros_eliminados}")

            except Exception as e:
                with open(log_file, "a") as log:
                    log.write(f"Error al eliminar en '{tabla_relacionada}': {e}\n")
                print(f"Error al eliminar en '{tabla_relacionada}': {e}")

        # Eliminar el registro de la tabla principal
        tabla_principal = mapeo["tabla_principal"]
        clave_primaria = mapeo["clave_primaria"]

        try:
            print(f"Eliminando registro de la tabla principal '{tabla_principal}' con '{clave_primaria}' = {id_principal}...")
            query = f"DELETE FROM {tabla_principal} WHERE {clave_primaria} = ?"
            cursor.execute(query, (id_principal,))
            registros_eliminados = cursor.rowcount

            with open(log_file, "a") as log:
                log.write(f"Tabla principal: {tabla_principal}, Registros eliminados: {registros_eliminados}\n")

            print(f"Registro eliminado en '{tabla_principal}': {registros_eliminados}")

        except Exception as e:
            with open(log_file, "a") as log:
                log.write(f"Error al eliminar en la tabla principal '{tabla_principal}': {e}\n")
            print(f"Error al eliminar en la tabla principal '{tabla_principal}': {e}")

        # Confirmar cambios
        conn.commit()
        print("Eliminación completada con éxito. Detalles en el archivo de log.")

    except Exception as e:
        print(f"Error durante la eliminación: {e}")
        with open(log_file, "a") as log:
            log.write(f"Error general: {e}\n")

    finally:
        if 'conn' in locals():
            conn.close()

# Ejemplo de uso
mapeo = {
    "tabla_principal": "cca_predio",
    "clave_primaria": "T_Id",
    "relaciones": [
        {"tabla_relacionada": "cca_derecho", "clave_foranea": "predio"},
        {"tabla_relacionada": "cca_terreno", "clave_foranea": "predio"},
        {"tabla_relacionada": "cca_construccion", "clave_foranea": "predio"},
        {"tabla_relacionada": "cca_predio_informalidad", "clave_foranea": "cca_predio_formal"},
        {"tabla_relacionada": "cca_predio_informalidad", "clave_foranea": "cca_predio_informal"},
        {"tabla_relacionada": "cca_predio_copropiedad", "clave_foranea": "unidad_predial"},
        {"tabla_relacionada": "cca_predio_copropiedad", "clave_foranea": "matriz"},
        {"tabla_relacionada": "cca_estructuranovedadfmi", "clave_foranea": "cca_predio_novedad_fmi"},
        {"tabla_relacionada": "cca_estructuranovedadnumeropredial", "clave_foranea": "cca_predio_novedad_numeros_prediales"},
        {"tabla_relacionada": "extdireccion", "clave_foranea": "cca_predio_direccion"},
        {"tabla_relacionada": "cca_adjunto", "clave_foranea": "cca_predio_adjunto"},
        {"tabla_relacionada": "cca_ofertasmercadoinmobiliario", "clave_foranea": "predio"},
        {"tabla_relacionada": "cca_terrenohistorico", "clave_foranea": "predio"},
        {"tabla_relacionada": "cca_construccionhistorica", "clave_foranea": "predio"},
    ],
}

# Ruta a la base de datos y ID del registro a eliminar
db_path = "captura_campo_20240904.gpkg"
id_principal = input("Introduce el ID del registro a eliminar: ")

# Ejecutar la función
eliminar_registro_con_relaciones(db_path, id_principal, mapeo)