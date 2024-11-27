import tkinter as tk
from tkinter import ttk, messagebox
from modelo_orm import Obra
from PIL import Image, ImageTk


class ObrasUrbanasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Obras Urbanas")
        self.root.geometry("800x600")
        image_path = "Buenos Aires.jpeg"
        #hasta aca es la creacion de la ventana principal
        try:
            self.background_image = Image.open(image_path)
            self.background_image = self.background_image.resize((800, 600), Image.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(self.background_image)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
            return

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        #hasta aca carga la imagen de fondo en la pantalla principal

        self.canvas.create_rectangle(150, 20, 650, 80, fill="#000000", outline="")
        self.canvas.create_text(400, 50, text="Obras Urbanas en CABA", font=("Arial", 26, "bold"), fill="white")
        self.canvas.create_rectangle(100, 180, 700, 480, fill="#ffffff", outline="")

        self.frame_lista = tk.Frame(self.canvas, bg="white", relief="flat", bd=0)
        self.frame_lista.place(relx=0.5, rely=0.55, anchor="center", width=580, height=240) 
        style = ttk.Style()
        style.configure("Treeview", background="#f7f7f7", foreground="black", rowheight=25, fieldbackground="#f7f7f7")
        style.map("Treeview", background=[("selected", "#4287f5")])
        # hasta aca es el diseño de la pantalla de busqueda


        self.tree = ttk.Treeview(self.frame_lista, columns=("ID", "Nombre", "Tipo Obra", "Estado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Tipo Obra", text="Tipo de Obra")
        self.tree.heading("Estado", text="Estado")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=250, anchor="w")
        self.tree.column("Tipo Obra", width=150, anchor="w")
        self.tree.column("Estado", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        # diseño de la tabla interior de busqueda

        self.cargar_obras()
        self.tree.bind("<<TreeviewSelect>>", self.mostrar_popup) #esto hace que se cree el pop up cuando seleccionas la obra

    def cargar_obras(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for obra in Obra.select():
            self.tree.insert("", "end", values=(
                str(obra.idObra).capitalize(),
                obra.nombre.capitalize() if obra.nombre else "N/A",
                obra.tipoObra.nombre.capitalize() if obra.tipoObra and obra.tipoObra.nombre else "N/A",
                obra.etapa.nombre.capitalize() if obra.etapa and obra.etapa.nombre else "N/A"
            ))
    #esto carga las obras en la tabla
    
    def mostrar_popup(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        obra_id = self.tree.item(selected_item)["values"][0]
        try:
            obra = Obra.get_by_id(obra_id)
            popup = tk.Toplevel(self.root)
            popup.title(f"Detalles de la Obra: {obra.nombre}")
            popup.geometry("600x700")
            popup_image_path = "Buenos Aires.jpeg"

            try:
                popup_image = Image.open(popup_image_path)
                popup_image = popup_image.resize((600, 700), Image.LANCZOS)
                popup_background = ImageTk.PhotoImage(popup_image)
                canvas = tk.Canvas(popup, width=600, height=700)
                canvas.pack(fill="both", expand=True)
                canvas.create_image(0, 0, image=popup_background, anchor="nw")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo del popup: {e}")
                return
            detalles_frame = tk.Frame(canvas, bg="#ffffff", relief="flat", bd=0)
            detalles_frame.place(relx=0.5, rely=0.5, anchor="center", width=550, height=650)
            lbl_titulo = tk.Label(detalles_frame, text="Detalles de la Obra", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333")

            lbl_titulo.pack(pady=10)
            lbl_info_general = tk.Label(detalles_frame, text="Información General", font=("Arial", 14, "bold"), bg="#ffffff", fg="#555")
            lbl_info_general.pack(anchor="w", pady=(10, 5))
            #hasta aca es el diseño de la ventana de popup

            info_general = f"""
            ID: {obra.idObra}
            Nombre: {obra.nombre}
            Tipo de Obra: {obra.tipoObra.nombre if obra.tipoObra else "N/A"}
            Estado: {obra.etapa.nombre if obra.etapa else "N/A"}
            """

            lbl_info_general_valores = tk.Label(detalles_frame, text=info_general.strip(), justify="left", font=("Arial", 11), bg="#ffffff", fg="#333")
            lbl_info_general_valores.pack(anchor="w", pady=5)
            lbl_descripcion = tk.Label(detalles_frame, text="Descripción", font=("Arial", 14, "bold"), bg="#ffffff", fg="#555")

            lbl_descripcion.pack(anchor="w", pady=(10, 5))
            descripcion_formateada = obra.descripcion if obra.descripcion else "Sin descripción"
            lbl_descripcion_valores = tk.Label(detalles_frame, text=descripcion_formateada, justify="left", font=("Arial", 11), bg="#ffffff", fg="#333", wraplength=500)
            lbl_descripcion_valores.pack(anchor="w", pady=5)

            lbl_ubicacion = tk.Label(detalles_frame, text="Ubicación", font=("Arial", 14, "bold"), bg="#ffffff", fg="#555")
            lbl_ubicacion.pack(anchor="w", pady=(10, 5))

            ubicacion_info = f"""
            Dirección: {obra.ubicacion.direccion if obra.ubicacion else "N/A"}
            Barrio: {obra.ubicacion.barrio.nombre if obra.ubicacion and obra.ubicacion.barrio else "N/A"}
            Comuna: {obra.ubicacion.barrio.comuna if obra.ubicacion and obra.ubicacion.barrio else "N/A"}
            Latitud: {obra.ubicacion.latitud if obra.ubicacion else "N/A"}
            Longitud: {obra.ubicacion.longitud if obra.ubicacion else "N/A"}
            """
            lbl_ubicacion_valores = tk.Label(detalles_frame, text=ubicacion_info.strip(), justify="left", font=("Arial", 11), bg="#ffffff", fg="#333")
            lbl_ubicacion_valores.pack(anchor="w", pady=5)

            lbl_financiera = tk.Label(detalles_frame, text="Financiera", font=("Arial", 14, "bold"), bg="#ffffff", fg="#555")
            lbl_financiera.pack(anchor="w", pady=(10, 5))

            financiera_info = f"""
            Monto Contrato: ${obra.montoContrato if obra.montoContrato else "N/A"}
            Mano de Obra: {obra.manoObra if obra.manoObra else "N/A"}
            Porcentaje Avance: {obra.porcentajeAvance if obra.porcentajeAvance else "N/A"}%
            """

            lbl_financiera_valores = tk.Label(detalles_frame, text=financiera_info.strip(), justify="left", font=("Arial", 11), bg="#ffffff", fg="#333")
            lbl_financiera_valores.pack(anchor="w", pady=5)
            
            btn_cerrar = tk.Button(detalles_frame, text="Cerrar", command=popup.destroy, bg="#ddd", fg="#333", font=("Arial", 10))
            btn_cerrar.pack(pady=20)
            #Hasta aca carga de informacion y fuentes de los detalles de la obra
            popup.image = popup_background #esto evita que desapareezca la imagen de fondo

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la obra: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ObrasUrbanasApp(root)
    root.mainloop()
