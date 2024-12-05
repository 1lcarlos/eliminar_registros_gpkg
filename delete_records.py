import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox

def eliminar_registro_con_relaciones(db_path, id_principal, mapeo):
    log_file = "eliminacion_log.txt"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(log_file, "w") as log:
            log.write("Inicio del proceso de eliminación\n")

        relaciones = mapeo["relaciones"]

        for relacion in relaciones:
            tabla_relacionada = relacion["tabla_relacionada"]
            clave_foranea = relacion["clave_foranea"]

            try:
                query = f"DELETE FROM {tabla_relacionada} WHERE {clave_foranea} = ?"
                cursor.execute(query, (id_principal,))
                registros_eliminados = cursor.rowcount

                with open(log_file, "a") as log:
                    log.write(f"Tabla: {tabla_relacionada}, Registros eliminados: {registros_eliminados}\n")

            except Exception as e:
                with open(log_file, "a") as log:
                    log.write(f"Error al eliminar en '{tabla_relacionada}': {e}\n")

        tabla_principal = mapeo["tabla_principal"]
        clave_primaria = mapeo["clave_primaria"]

        try:
            query = f"DELETE FROM {tabla_principal} WHERE {clave_primaria} = ?"
            cursor.execute(query, (id_principal,))
            registros_eliminados = cursor.rowcount

            with open(log_file, "a") as log:
                log.write(f"Tabla principal: {tabla_principal}, Registros eliminados: {registros_eliminados}\n")

        except Exception as e:
            with open(log_file, "a") as log:
                log.write(f"Error al eliminar en la tabla principal '{tabla_principal}': {e}\n")

        conn.commit()

        messagebox.showinfo("Éxito", "Eliminación completada con éxito. Revisa el archivo de log.")

    except Exception as e:
        messagebox.showerror("Error", f"Error durante la eliminación: {e}")

    finally:
        if 'conn' in locals():
            conn.close()

def ejecutar_eliminacion():
    db_path = filedialog.askopenfilename(filetypes=[("GPKG files", "*.gpkg")])
    if not db_path:
        messagebox.showwarning("Advertencia", "Debes seleccionar una base de datos.")
        return

    id_principal = id_entry.get()
    if not id_principal.isdigit():
        messagebox.showwarning("Advertencia", "Debes ingresar un ID válido.")
        return

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

    eliminar_registro_con_relaciones(db_path, id_principal, mapeo)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Eliminación de Registros SQLite")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="ID del registro a eliminar:").grid(row=0, column=0, pady=5)
id_entry = tk.Entry(frame, width=30)
id_entry.grid(row=0, column=1, pady=5)

eliminar_button = tk.Button(frame, text="Seleccionar Base de Datos y Eliminar", command=ejecutar_eliminacion)
eliminar_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
