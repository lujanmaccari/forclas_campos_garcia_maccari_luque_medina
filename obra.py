from peewee import *
from datetime import datetime
from modelo_orm import Obra, Etapa, Empresa, TipoContratacion

class ObraManager:
    def __init__(self, obraId): 
        try:
            self.obra = Obra.select().where(Obra.idObra == obraId).get()
            print(f"Obra encontrada: {self.obra.nombre}")
        except DoesNotExist:
            raise ValueError(f"No se encontró la obra con ID {obraId}.")
    
    def nuevo_proyecto(self):
        try:
            etapa, _ = Etapa.get_or_create(nombre="Proyecto")
            self.obra.etapa_id = etapa.idEtapa
            self.obra.save()
            print(f"La obra {self.obra.nombre} fue configurada como nuevo proyecto")
        except Exception as e:
            print(f"Error al configurar la obra como nuevo proyecto {e}")
    
    def iniciar_contratacion(self):
        tipoContratacion = input("ingrese el tipo de contratacion")
        nroContratacion = input("ingrese el numero de contratacion")
        
        try:
            if not TipoContratacion.select().where(TipoContratacion.nombre == tipoContratacion).exists():
                raise ValueError(f"TipoContratacion {tipoContratacion} no existe en la base de datos.")
            
            etapa, _ = Etapa.get_or_create(nombre="Contratación")
            contratacion, _ = TipoContratacion.get_or_create(nombre=tipoContratacion)
            self.obra.etapa_id = etapa.idEtapa
            self.obra.tipoContratacion = contratacion.idTipoContratacion
            self.obra.numeroContratacion = nroContratacion
        
            self.obra.save()
            print(f"La contratación para la obra {self.obra.nombre} ha sido iniciada como {tipoContratacion}")
        except Exception as e:
            print(f"Error al iniciar la contratación {e}")

    def adjudicar_obra(self):
        nombreEmpresa = input("ingrese el nombre de la empresa")
        numeroExpediente = input("Ingrese el número de expediente: ")
        
        try:
            
            if not Empresa.select().where(Empresa.licitacionOfertaEmpresa == nombreEmpresa).exists():
                raise ValueError(f"Empresa {nombreEmpresa} no existe en la base de datos.")

            if Obra.select().where(Obra.numeroExpediente == numeroExpediente).exists():
                raise ValueError("El número de expediente ya existe en la base de datos.")
            
            etapa, _ = Etapa.get_or_create(nombre="Adjudicada")
            empresa, _ = Empresa.get_or_create(licitacionOfertaEmpresa = nombreEmpresa)
            self.obra.etapa_id = etapa.idEtapa
            self.obra.numeroExpediente = numeroExpediente
            self.obra.empresa_id = empresa.idEmpresa 

            self.obra.save()
            print(f"La obra {self.obra.nombre} fue adjudicada a la empresa {nombreEmpresa}, con el número de expediente {numeroExpediente}")
        except Exception as e:
            print(f"Error al adjudicar la obra {e}")
    
    def iniciar_obra(self):
        fechaInicio = input("ingrese la fecha de inicio en formato DD/MM/YYYY")
        fechaFin = input("ingrese la fecha de fin en formato DD/MM/YYYY")
        manoObra = int(input("ingrese la mano de obra"))
        destacada = input("ingrese si es destacada")
        fuenteFinanciamiento = input("ingrese la fuente de financiamiento")
        
        try:
            if self.obra.etapa_id == 1:
                raise ValueError("La obra está finalizada.")
            
            if manoObra < 0 and not isinstance(int, manoObra):
                raise ValueError("El valor de mano debe ser un número entero positivo")
            
            if not Empresa.select().where(Empresa.licitacionOfertaEmpresa == fuenteFinanciamiento).exists():
             raise ValueError("La fuente de financiamiento no existe en la base de datos.")
         
            try:
                fechaInicioFormateada = datetime.strptime(fechaInicio, "%d/%m/%Y").date()
                fechaFinFormateada = datetime.strptime(fechaFin, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("Las fechas deben estar en formato DD/MM/YYYY")
            
            if fechaInicioFormateada > fechaFinFormateada:
                raise ValueError("La fecha de inicio no puede ser mayor a la fecha de fin")

            etapa, _ = Etapa.get_or_create(nombre="En ejecución")
            self.obra.destacada = destacada.capitalize()
            self.obra.fechaInicio = fechaInicioFormateada
            self.obra.fechaFinIinicial = fechaFinFormateada
            self.obra.fuente_financiamiento = fuenteFinanciamiento
            self.obra.manoObra = manoObra
            self.obra.etapa_id = etapa.idEtapa
            self.obra.save()
            
            print(f"La obra '{self.obra.nombre}' ha iniciado su ejecución")
            
        except Exception as e:
            print(f"Error al iniciar la obra: {e}")

    def actualizar_porcentaje_avance(self):
        nuevoPorcentaje = int(input("Ingrese el nuevo porcentaje de avance (0-100): "))
        
        try:
            if not isinstance(nuevoPorcentaje, int):
                raise ValueError("El porcentaje debe ser un número entero")
            
            if not 0 <= nuevoPorcentaje <= 100:
                raise ValueError("El porcentaje debe estar entre 0 y 100")
            
            if self.obra.porcentajeAvance == nuevoPorcentaje:
                raise ValueError("El porcentaje de avance ya es el mismo")
            
            if self.obra.porcentajeAvance == 100:
                raise ValueError("La obra ya está finalizada")
            
            self.obra.porcentajeAvance =  nuevoPorcentaje
            self.obra.save()
            print(f"Porcentaje de avance actualizado a {nuevoPorcentaje}% para '{self.obra.nombre}")
        except Exception as e:
            print(f"Error al actualizar el porcentaje de avance: {e}")
            
    def incrementar_plazo(self):
        cantidad =  int(input("Ingrese la cantidad de meses a incrementar: "))
        
        try:
            if not isinstance(cantidad, int):
                raise ValueError("El número de meses debe ser un número entero")
            
            if cantidad < 0:
                raise ValueError("El número de meses debe ser un número entero positivo")

            if self.obra.porcentajeAvance == 100:
                raise ValueError(f"No se puede incrementar el plazo en una obra que está finalizada")
            
            self.obra.plazoMeses += cantidad
            self.obra.save()
            print(f"El plazo de la obra '{self.obra.nombre}' ha incrementado {cantidad} meses")
        except Exception as e:
            print(f"Error al incrementar el plazo: {e}")
    
    def incrementar_mano_obra(self):
        cantidad = int(input("Ingrese la cantidad de mano de obra a incrementar: "))
    
        try:
            if not isinstance(cantidad, int):
                raise ValueError("El número debe ser un número entero")
                
            if cantidad < 0:
                raise ValueError("El número debe ser un número entero positivo")

            if self.obra.porcentajeAvance == 100:
                raise ValueError(f"No se puede incrementar la mano de obra en una obra que está finalizada")
            
            self.obra.manoObra += cantidad
            self.obra.save()
            print(f"La mano de obra de '{self.obra.nombre}' aumentó {cantidad}")
        except Exception as e:
            print(f"Error al incrementar la mano de obra: {e}")

    def finalizar_obra(self):
        try:
            etapa, _ = Etapa.get_or_create(nombre="Finalizada")
            self.obra.etapa_id = etapa.idEtapa
            self.obra.porcentajeAvance = 100
            self.obra.save()
            print(f"La obra '{self.obra.nombre}' ha sido finalizada")
        except Exception as e:
            print(f"Error al finalizar la obra {e}")

    def rescindir_obra(self):
        try:
            if self.obra.porcentajeAvance == 100:
                raise ValueError("La obra no puede ser rescindida si está finalizada")
           
            etapa, _ = Etapa.get_or_create(nombre="Rescindida")
            self.obra.etapa_id = etapa
            self.obra.save()
            print(f"La obra '{self.obra.nombre}' ha sido rescindida")
        except Exception as e:
            print(f"Error al rescindir la obra {e}")

# Pruebas para modificar las obras creadas manualmente

# gestionarObraCreada = ObraManager(1245)
# gestionarObraCreada.nuevo_proyecto()
# gestionarObraCreada.iniciar_contratacion()
# gestionarObraCreada.adjudicar_obra()
# gestionarObraCreada.iniciar_obra()
# gestionarObraCreada.actualizar_porcentaje_avance()
# gestionarObraCreada.incrementar_plazo()
# gestionarObraCreada.incrementar_mano_obra()
# gestionarObraCreada.finalizar_obra()

# gestionarObraCreada = ObraManager(1246)
# gestionarObraCreada.nuevo_proyecto()
# gestionarObraCreada.iniciar_contratacion()
# gestionarObraCreada.adjudicar_obra()
# gestionarObraCreada.iniciar_obra()
# gestionarObraCreada.actualizar_porcentaje_avance()
# gestionarObraCreada.incrementar_plazo()
# gestionarObraCreada.incrementar_mano_obra()
# gestionarObraCreada.rescindir_obra()

