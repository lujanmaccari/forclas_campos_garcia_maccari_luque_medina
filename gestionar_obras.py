import peewee as pw
from modelo_orm import sqlite_crear, Obra, Empresa, Etapa, Ubicacion, AreaResponsable, TipoObra, EmpresaObra
import pandas as pd
from abc import ABC 
from abc import abstractmethod


class GestionarObra(ABC):
    
    @classmethod
    def extraer_datos(cls, ruta_dataset):
        try:
            df = pd.read_csv("observatorio-de-obras-urbanas.csv", sep=";", encoding="latin-1")
            print("Datos extraídos con éxito.")
            return df
        except FileNotFoundError as e:
            print(f"Error: El archivo {ruta_dataset} no se encuentra. Verifique la ruta.")
            return None
        except pd.errors.EmptyDataError as e:
            print(f"Error: El archivo está vacío.")
            return None
        except pd.errors.ParserError as e:
            print(f"Error: El archivo no puede ser analizado correctamente. Verifique el formato.")
            return None
        except Exception as e:
            print(f"Error inesperado al extraer los datos: {e}")
            return None

    @classmethod
    def conectar_db(cls):
        try:
            cls.db = pw.SqliteDatabase('obras_urbanas.db')
            cls.db.connect()
            print("Conexión a la base de datos exitosa.")
        except pw.OperationalError as e:
            print(f"Error de conexión a la base de datos: {e}")
        except Exception as e:
            print(f"Error inesperado al conectar a la base de datos: {e}")

    @classmethod
    def mapear_orm(cls):
        try:
            sqlite_crear.create_tables([Etapa, Empresa, Ubicacion, TipoObra, AreaResponsable, Obra, EmpresaObra])
            print("Tablas creadas exitosamente.")
        except pw.OperationalError as e:
            print(f"Error al crear las tablas: {e}")
    
    @classmethod
    def limpiar_datos(cls):
        try:
            df = pd.read_csv("observatorio-de-obras-urbanas.csv", sep=";", encoding="latin-1")            
            columnasAEliminar = ['ba_elige','link_interno','pliego_descarga', 'imagen_1', 'imagen_2', 'imagen_3', 'imagen_4']
            
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            df = df.drop(columns=columnasAEliminar, axis=1)
            
            df = df.dropna(subset=['entorno', 'nombre', 'etapa', 'tipo', 'area_responsable', 'descripcion', 'monto_contrato', 'comuna', 'barrio', 'direccion', 'lat', 'lng', 'fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance', 'licitacion_oferta_empresa', 'licitacion_anio', 'contratacion_tipo', 'nro_contratacion', 'cuit_contratista', 'beneficiarios', 'mano_obra', 'compromiso', 'destacada', 'expediente-numero', 'estudio_ambiental_descarga', 'financiamiento'], axis=0, how='all')
  
            print("Datos limpios (primeras 10 filas):", df.columns)
            return df
        except Exception as e:
            print(f"Error al limpiar los datos: {e}")
            
    @classmethod
    def cargar_datos():
        pass    
    
    @classmethod
    def nueva_obra():
        pass
    
    @classmethod
    def obtener_indicadores():
        pass
    

prueba = GestionarObra()
prueba.limpiar_datos()