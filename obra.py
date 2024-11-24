from peewee import *
from datetime import datetime
from modelo_orm import Obra, Etapa, Empresa, Ubicacion, TipoObra, AreaResponsable, Barrio

class ObraManager:
    def __init__(self, obra_id):
        try:
            self.obra = Obra.select().where(Obra.idObra == obra_id).get()
            print(f"Obra encontrada: {self.obra.nombre}")
        except DoesNotExist:
            raise ValueError(f"No se encontró la obra con ID {obra_id}.")
    
    def nuevo_proyecto(self):
        try:
            etapa, _ = Etapa.get_or_create(nombre="Proyecto")
            self.obra.idEtapa = etapa.idEtapa
            self.obra.save()
            print(f"La obra {self.obra.nombre} fue configurada como nuevo proyecto")
        except Exception as e:
            print(f"Error al configurar la obra como nuevo proyecto {e}")
    
    def iniciar_contratacion(self, tipo_contratacion, nro_contratacion):
        try:
            if not Empresa.select().where(Empresa.tipoContratacion == tipo_contratacion).exists():
                raise ValueError(f"TipoContratacion {tipo_contratacion} no existe en la base de datos.")
            
            etapa, _ = Etapa.get_or_create(nombre="Contratación")
            self.obra.idEtapa = etapa.idEtapa
            self.obra.tipoContratacion = tipo_contratacion
            self.obra.numeroExpediente = nro_contratacion
        
            self.obra.save()
            print(f"La contratación para la obra {self.obra.nombre} ha sido iniciada como {tipo_contratacion}")
        except Exception as e:
            print(f"Error al iniciar la contratación {e}")

    def adjudicar_obra(self, empresa_nombre, nro_expediente):
        try:
            
            if not Empresa.select().where(Empresa.licitacionOfertaEmpresa == empresa_nombre).exists():
                raise ValueError(f"Empresa {empresa_nombre} no existe en la base de datos.")

            if Obra.select().where(Obra.numeroExpediente == nro_expediente).exists():
                raise ValueError("El número de expediente ya existe en la base de datos.")
            
            etapa, _ = Etapa.get_or_create(nombre="Adjudicada")
            empresa, _ = Empresa.get_or_create(licitacionOfertaEmpresa=empresa_nombre)
            self.obra.idEtapa = etapa.idEtapa
            self.obra.numeroExpediente = nro_expediente
            self.obra.idEmpresa = empresa.idEmpresa 

            self.obra.save()
            print(f"La obra {self.obra.nombre} fue adjudicada a la empresa {empresa_nombre}, con el número de expediente {nro_expediente}")
        except Exception as e:
            print(f"Error al adjudicar la obra {e}")
    
    def iniciar_obra(self, fecha_inicio, fecha_fin, mano_obra, destacada, fuente_financiamiento ):
        try:
            if mano_obra < 0 and not isinstance(int, mano_obra):
                raise ValueError("El valor de mano debe ser un número entero positivo")
            
            if not Empresa.select().where(Empresa.licitacionOfertaEmpresa == fuente_financiamiento).exists():
             raise ValueError("La fuente de financiamiento no existe en la base de datos.")
         
            try:
                fechaInicioFormateada = datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
                fechaFinFormateada = datetime.strptime(fecha_fin, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("Las fechas deben estar en formato DD/MM/YYYY")
            
            if fechaInicioFormateada > fechaFinFormateada:
                raise ValueError("La fecha de inicio no puede ser mayor a la fecha de fin")

            etapa, _ = Etapa.get_or_create(nombre="En ejecución")
            self.obra.destacada = destacada
            self.obra.fechaInicio = fechaInicioFormateada
            self.obra.fechaFinIinicial = fechaFinFormateada
            self.obra.fuente_financiamiento = fuente_financiamiento
            self.obra.manoObra = mano_obra
            self.obra.idEtapa = etapa.idEtapa
            self.obra.save()
            print(f"La obra '{self.obra.nombre}' ha iniciado su ejecución")
        except Exception as e:
            print(f"Error al iniciar la obra: {e}")

    def actualizar_porcentaje_avance(self, nuevo_porcentaje):
        try:
            if not 0 <= nuevo_porcentaje <= 100:
                raise ValueError("El porcentaje debe estar entre 0 y 100")
            self.obra.porcentajeAvance =  nuevo_porcentaje
            self.obra.save()
            print(f"Porcentaje de avance actualizado a {nuevo_porcentaje}% para '{self.obra.nombre}")
        except Exception as e:
            print(f"Error al actualizar el porcentaje de avance: {e}")
            
    def incrementar_plazo(self, meses_extra):
        try:
            self.obra.plazoMeses += meses_extra
            self.obra.save()
            print(f"El plazo de la obra '{self.obra.nombre}' ha sido incrementado en {meses_extra} ")
        except Exception as e:
            print(f"Error al incrementar el plazo: {e}")
    
    def incrementar_mano_obra(self, cantidad_extra):
        try:
            self.obra.manoObra += cantidad_extra
            self.obra.save()
            print(f"La mano de obra de '{self.obra.nombre}' aumentó a {cantidad_extra}")
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