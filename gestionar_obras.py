import peewee as pw
from modelo_orm import sqlite_crear, Obra, Empresa, Etapa, Ubicacion, AreaResponsable, TipoObra,Barrio, EmpresaObra
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
            sqlite_crear.create_tables([Etapa, Empresa, Ubicacion, TipoObra, AreaResponsable, Obra, EmpresaObra, Barrio])
            print("Tablas creadas exitosamente.")
        except pw.OperationalError as e:
            print(f"Error al crear las tablas: {e}")
    
    @classmethod
    def limpiar_datos(cls):
        try:
            df = pd.read_csv("observatorio-de-obras-urbanas.csv", sep=";", encoding="utf8")            
            columnasAEliminar = ['ba_elige','link_interno','pliego_descarga', 'imagen_1', 'imagen_2', 'imagen_3', 'imagen_4']
            
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            df = df.drop(columns=columnasAEliminar, axis=1)
            
            df = df.dropna(subset=['entorno', 'nombre', 'etapa', 'tipo', 'area_responsable', 'descripcion', 'monto_contrato', 'comuna', 'barrio', 'direccion', 'lat', 'lng', 'fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'porcentaje_avance', 'licitacion_oferta_empresa', 'licitacion_anio', 'contratacion_tipo', 'nro_contratacion', 'cuit_contratista', 'beneficiarios', 'mano_obra', 'compromiso', 'destacada', 'expediente-numero', 'estudio_ambiental_descarga', 'financiamiento'], axis=0, how='all')
  
            # print("Datos limpios (primeras 10 filas):", df.head(20))
            
            # for column in df.columns:
            #     if column == 'comuna' or column == 'barrio' or column == 'destacada':
            #         df = df.dropna(subset=[column], how='all')
            #         df = df.reset_index(drop=True)
            #         # df = df.fillna(value=1)
            #     elif column == 'monto_contrato':
            #         df[column] = pd.to_numeric(df[column], errors='coerce')
            #         df = df.reset_index(drop=True)
            #     elif column == 'fecha_inicio' or column == 'fecha_fin_inicial':
            #         df[column] = pd.to_datetime(df[column], errors='coerce')
            #         df = df.reset_index(drop=True)
            #     elif column == 'plazo_meses' or column == 'porcentaje_avance':
            #         df[column] = pd.to_numeric(df[column], errors='coerce')
            #         df = df.reset_index(drop=True)
            #     elif column == 'expediente-numero':
            #         df[column] = pd.to_numeric(df[column], errors='coerce')
            #         df = df.reset_index(drop=True)
            #     elif column == 'financiamiento':
            #         df[column] = df[column].str.replace(',', '.')
            #         df[column] = pd.to_numeric(df[column], errors='coerce')
            #         df = df.reset_index(drop=True)
            #     elif column == 'licitacion_oferta_empresa':
            #         df[column] = df[column].str.replace(',', '.')
            df.to_csv("datos_limpios_obras_urbanas.csv",sep=";",encoding="utf8" ,  index=False)
            
            print("Datos limpios guardados en 'datos_limpios_obras_urbanas.csv'.")
            
            return df
        except Exception as e:
            print(f"Error al limpiar los datos: {e}")
            
    @classmethod
    def cargar_datos(cls):
        df = GestionarObra.limpiar_datos()    
        datosAreaResponsable = list(df['area_responsable'].unique())

        # for area in datosAreaResponsable:
        #     area_responsable = AreaResponsable.create(nombre=area)
        #     area_responsable.save()
         
        datosTipoObra = list(df['tipo'].unique())
        for tipo in datosTipoObra:
            tipo_obra = TipoObra.create(nombre=tipo)
            tipo_obra.save()

        datosEtapa = list(df['etapa'].unique())
        for etapa in datosEtapa:
            etapa = Etapa.create(nombre=etapa)
            etapa.save()

        print("Datos cargados exitosamente.")

    @classmethod
    def nueva_obra():
        pass
    
    @classmethod
    def obtener_indicadores():
        pass
    

prueba = GestionarObra()
# prueba.limpiar_datos()
prueba.cargar_datos()