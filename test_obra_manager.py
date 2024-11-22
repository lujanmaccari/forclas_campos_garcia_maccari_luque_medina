from obra import ObraManager

obra_id = 1
try:
    # Instancia de prueba
    obra_manager = ObraManager(obra_id)
    print(f"Obra encontrada: {obra_manager.obra.nombre}")
    
    # Pruebas de métodos
    obra_manager.nuevo_proyecto()
    obra_manager.iniciar_contratacion(tipo_contratacion="Licitación Pública", nro_contratacion=12345)
    obra_manager.adjudicar_obra(empresa_nombre="Construcciones S.A.", nro_expediente=67890)
    obra_manager.iniciar_obra(fecha_inicio="01/01/2023", fecha_fin="31/12/2023", mano_obra=50)
    obra_manager.actualizar_porcentaje_avance(nuevo_porcentaje=25)
    obra_manager.incrementar_plazo(meses_extra=6)
    obra_manager.incrementar_mano_obra(cantidad_extra=10)
    obra_manager.finalizar_obra()
    obra_manager.rescindir_obra()

except ValueError as e:
    print(e)
except Exception as e:
    print(f"Error inesperado: {e}")
