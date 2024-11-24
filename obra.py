from peewee import *
from datetime import datetime
from modelo_orm import Obra, Etapa, Empresa, Ubicacion, TipoObra, AreaResponsable, Barrio

class ObraManager:
    def __init__(self,obraId): 
        try:
            self.obra = Obra.select().where(Obra.idObra == obraId).get()
            print(f"Obra encontrada: {self.obra.nombre}")
        except DoesNotExist:
            raise ValueError(f"No se encontró la obra con ID {obraId}.")
    
    def nuevo_proyecto(self):
        try:
            etapa, _ = Etapa.get_or_create(nombre="Proyecto")
            self.obra.idEtapa = etapa.idEtapa
            self.obra.save()
            print(f"La obra {self.obra.nombre} fue configurada como nuevo proyecto")
        except Exception as e:
            print(f"Error al configurar la obra como nuevo proyecto {e}")
    
    def iniciar_contratacion(self):
        tipoContratacion = input("ingrese el tipo de contratacion")
        nroContratacion = input("ingrese el numero de contratacion")
        try:
            if not Empresa.select().where(Empresa.tipoContratacion == tipoContratacion).exists():
                raise ValueError(f"TipoContratacion {tipoContratacion} no existe en la base de datos.")
            
            etapa, _ = Etapa.get_or_create(nombre="Contratación")
            self.obra.idEtapa = etapa.idEtapa
            self.obra.tipoContratacion = tipoContratacion
            self.obra.numeroExpediente = nroContratacion
        
            self.obra.save()
            print(f"La contratación para la obra {self.obra.nombre} ha sido iniciada como {tipoContratacion}")
        except Exception as e:
            print(f"Error al iniciar la contratación {e}")

    def adjudicar_obra(self):
        empresaNombre = input("ingrese el nombre de la empresa")
        nroExpediente = input("Ingrese el número de expediente: ")
        try:
            
            if not Empresa.select().where(Empresa.licitacionOfertaEmpresa == empresaNombre).exists():
                raise ValueError(f"Empresa {empresaNombre} no existe en la base de datos.")

            if Obra.select().where(Obra.numeroExpediente == nroExpediente).exists():
                raise ValueError("El número de expediente ya existe en la base de datos.")
            
            etapa, _ = Etapa.get_or_create(nombre="Adjudicada")
            empresa, _ = Empresa.get_or_create(licitacionOfertaEmpresa=empresaNombre)
            self.obra.idEtapa = etapa.idEtapa
            self.obra.numeroExpediente = nroExpediente
            self.obra.idEmpresa = empresa.idEmpresa 

            self.obra.save()
            print(f"La obra {self.obra.nombre} fue adjudicada a la empresa {empresaNombre}, con el número de expediente {nroExpediente}")
        except Exception as e:
            print(f"Error al adjudicar la obra {e}")
    
    def iniciar_obra(self):
        fechaInicio = input("ingrese la fecha de inicio en formato DD/MM/YYYY")
        fechaFin = input("ingrese la fecha de fin en formato DD/MM/YYYY")
        manoObra = int(input("ingrese la mano de obra"))
        destacada = input("ingrese si es destacada")
        fuenteFinanciamiento = input("ingrese la fuente de financiamiento")
        try:
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
            self.obra.destacada = destacada
            self.obra.fechaInicio = fechaInicioFormateada
            self.obra.fechaFinIinicial = fechaFinFormateada
            self.obra.fuente_financiamiento = fuenteFinanciamiento
            self.obra.manoObra = manoObra
            self.obra.idEtapa = etapa.idEtapa
            self.obra.save()
            print(f"La obra '{self.obra.nombre}' ha iniciado su ejecución")
        except Exception as e:
            print(f"Error al iniciar la obra: {e}")

    def actualizar_porcentaje_avance(self):
        nuevoPorcentaje = float(input("Ingrese el nuevo porcentaje de avance (0-100): "))
        try:
            if not 0 <= nuevoPorcentaje <= 100:
                raise ValueError("El porcentaje debe estar entre 0 y 100")
            self.obra.porcentajeAvance =  nuevoPorcentaje
            self.obra.save()
            print(f"Porcentaje de avance actualizado a {nuevoPorcentaje}% para '{self.obra.nombre}")
        except Exception as e:
            print(f"Error al actualizar el porcentaje de avance: {e}")
            
    def incrementar_plazo(self):
        mesesExtra = int(input("Ingrese la cantidad de meses adicionales: "))
        try:
            self.obra.plazoMeses += mesesExtra
            self.obra.save()
            print(f"El plazo de la obra '{self.obra.nombre}' ha sido incrementado en {mesesExtra} ")
        except Exception as e:
            print(f"Error al incrementar el plazo: {e}")
    
    def incrementar_mano_obra(self):
        cantidadExtra = int(input("Ingrese la cantidad de mano de obra adicional: "))
        try:
            self.obra.manoObra += cantidadExtra
            self.obra.save()
            print(f"La mano de obra de '{self.obra.nombre}' aumentó a {cantidadExtra}")
        except Exception as e:
            print(f"Error al incrementar la mano de obra: {e}")

    def finalizar_obra(self):
        try:
            etapa, created = Etapa.get_or_create(nombre="Finalizada")
            self.obra.idEtapa = etapa
            self.obra.porcentajeAvance = 100
            self.obra.save()
            print(f"La obra '{self.obra.nombre}' ha sido finalizada")
        except Exception as e:
            print(f"Error al finalizar la obra {e}")

    def rescindir_obra(self):
        try:
            etapa, created = Etapa.get_or_create(nombre="Rescindida")
            self.obra.idEtapa = etapa
            self.obra.save()
            print(f"La obra '{self.obra.nombre}' ha sido rescindida")
        except Exception as e:
            print(f"Error al rescindir la obra")
            
# nuevaObra = ObraManager(1)
# nuevaObra.nuevo_proyecto()
# nuevaObra.iniciar_contratacion("Contratación Directa", "NroContratacion")
# nuevaObra.adjudicar_obra("Criba S.A.", "551592833333014")
# nuevaObra.iniciar_obra("01/03/2023", "01/08/2023", 100, True, "Criba S.A.")