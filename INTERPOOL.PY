import tkinter as tk
import mysql.connector
from tkinter import messagebox

class Persona:
    def __init__(self, nombre, apellido_paterno, apellido_materno, curp):
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.curp = curp

class Visitante(Persona):
    def __init__(self, nombre, apellido_paterno, apellido_materno, curp, direccion, correo):
        super().__init__(nombre, apellido_paterno, apellido_materno, curp)
        self.direccion = direccion
        self.correo = correo

class Empleado(Persona):
    def __init__(self, nombre, apellido_paterno, apellido_materno, area):
        super().__init__(nombre, apellido_paterno, apellido_materno, "")
        self.area = area

class Area:
    def __init__(self, nombre, ubicacion):
        self.nombre = nombre
        self.ubicacion = ubicacion

def guardar_datos(tabla, data):
    try:
        miConexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='empresa'
        )

        cursor = miConexion.cursor()
        query = f"INSERT INTO {tabla} VALUES ({', '.join(['%s']*len(data))})"
        cursor.execute(query, data)

        miConexion.commit()
        cursor.close()
        miConexion.close()

        tk.messagebox.showinfo("Éxito", "Datos guardados en la base de datos.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Error al guardar datos en la base de datos: {str(e)}")

def abrir_formulario_registro(tipo_registro):
    form = tk.Toplevel(root)
    form.title(f"Registrar {tipo_registro}")

    tk.Label(form, text="Nombre:").pack()
    nombre = tk.Entry(form)
    nombre.pack()

    tk.Label(form, text="Apellido Paterno:").pack()
    apellido_paterno = tk.Entry(form)
    apellido_paterno.pack()

    tk.Label(form, text="Apellido Materno:").pack()
    apellido_materno = tk.Entry(form)
    apellido_materno.pack()

    if tipo_registro == "Visitante":
        tk.Label(form, text="CURP:").pack()
        curp = tk.Entry(form)
        curp.pack()

        tk.Label(form, text="Dirección:").pack()
        direccion = tk.Entry(form)
        direccion.pack()

        tk.Label(form, text="Correo Electrónico:").pack()
        correo = tk.Entry(form)
        correo.pack()

        def guardar_datos_visitante():
            data = (nombre.get(), apellido_paterno.get(), apellido_materno.get(), curp.get(), direccion.get(), correo.get())
            guardar_datos("visitantes", data)
            form.destroy()

        tk.Button(form, text="Guardar", command=guardar_datos_visitante).pack()

    elif tipo_registro == "Empleado":
        tk.Label(form, text="Área:").pack()
        area = tk.Entry(form)
        area.pack()

        def guardar_datos_empleado():
            data = (nombre.get(), apellido_paterno.get(), apellido_materno.get(), area.get())
            guardar_datos("empleados", data)
            form.destroy()

        tk.Button(form, text="Guardar", command=guardar_datos_empleado).pack()

    elif tipo_registro == "Area":
        tk.Label(form, text="Ubicación:").pack()
        ubicacion = tk.Entry(form)
        ubicacion.pack()

        def guardar_datos_area():
            data = (nombre.get(), ubicacion.get())
            guardar_datos("areas", data)
            form.destroy()

        tk.Button(form, text="Guardar", command=guardar_datos_area).pack()

# Crear ventana principal
root = tk.Tk()
root.title("ALPHA - Sistema de Registro")

frame = tk.Frame(root, bg="lightblue")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Botones e imágenes
botones = [
    {"text": "Registrar Visitante", "image_path": "area.png", "command": lambda: abrir_formulario_registro("Visitante")},
    {"text": "Registrar Empleado", "image_path": "area.png", "command": lambda: abrir_formulario_registro("Empleado")},
    {"text": "Registrar Área", "image_path": "area.png", "command": lambda: abrir_formulario_registro("Area")},
]

for i, boton_info in enumerate(botones):
    label_text = boton_info["text"]
    label = tk.Label(frame, text=label_text)
    label.grid(row=i, column=0)

    image = tk.PhotoImage(file=boton_info["image_path"])
    button = tk.Button(frame, text=label_text, image=image, command=boton_info["command"])
    button.image = image
    button.grid(row=i, column=1)

frame.update_idletasks()
frame_width = frame.winfo_width()
frame_height = frame.winfo_height()
extra_width = 150
extra_height = 150

root.geometry(f"{frame_width + extra_width}x{frame_height + extra_height}")

root.mainloop()
