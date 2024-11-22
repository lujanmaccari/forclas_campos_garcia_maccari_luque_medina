from modelo_orm import Obra, Etapa, Empresa
from datetime import datetime

class ObraManager:
    def __init__(self, obra_id):
        try:
            self.obra = Obra.get(Obra.idObra == obra_id)
        except Obra.DoesNotExist:
            raise ValueError(f"No se encontró la obra con ID {obra_id}.")
    
    def nuevo_proyecto(self):
        try:
            etapa, created = Etapa.get_or_create(nombre="Proyecto")
            self.obra.idEtapa = etapa
            self.obra.save()
            print(f"La obra '{self.obra.nombre}' fue configurada como nuevo proyecto")
        except Exception as e:
            print(f"Error al configurar la obra como nuevo proyecto {e}")
    
    def iniciar_contratacion(self, tipo_contratacion, nro_contratacion):
        try:
            etapa, created = Etapa.get_or_create(nombre="Contratación")
            self.obra.idEtapa = etapa
            self.obra.numeroExpediente = nro_contratacion
            self.obra.save()
            print(f"La contratación para la obra '{self.obra.nombre}' ha sido iniciada")
        except Exception as e:
            print(f"Error al iniciar la contratación {e}")

    def adjudicar_obra(self, empresa_nombre, nro_expediente):
        try:
            etapa, created = Etapa.get_or_create(nombre="Adjudicada")
            empresa, _ = Empresa.get_or_create(licitacionOfertaEmpresa=empresa_nombre)
            self.obra.idEtapa = etapa
            self.obra.numeroExpediente = nro_expediente
            self.obra.save()
            print(f"La obra '{self.obra.nombre}' fue adjudicada a la empresa '{empresa_nombre}'")
        except Exception as e:
            print(f"Error al adjudicar la obra {e}")
    
    def iniciar_obra(self, fecha_inicio, fecha_fin, mano_obra):
        try:
            etapa, created = Etapa.get_or_create(nombre="En ejecución")
            self.obra.fechaInicio = datetime.strptime(fecha_inicio, "%d/%m/%Y").date()
            self.obra.fechaFinIinicial = datetime.strptime(fecha_fin, "%d/%m/%Y").date()
            self.obra.manoObra = mano_obra
            self.obra.idEtapa = etapa
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