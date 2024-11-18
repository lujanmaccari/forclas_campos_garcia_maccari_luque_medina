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
            
            columnasAEliminar = ['ba_elige', 'link_interno', 'pliego_descarga', 'imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'estudio_ambiental_descarga', 'entorno', 'compromiso', 'destacada', 'financiamiento']
            
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df = df.drop(columns=columnasAEliminar, axis=1)
            
            df.fillna({'tipo_obra': 'Salud'}, inplace=True)            
            df.fillna({'descripcion': 'Obra en ejecucion'}, inplace=True)            
            df.fillna({'monto_contrato': '300.000.000'}, inplace=True)            
            df.fillna({'porcentaje_avance': '0'}, inplace=True)            
            df.fillna({'fecha_fin_inicial': '31/12/2024'}, inplace=True)            
            df.fillna({'expediente-numero': '46213850'}, inplace=True)            
            df.fillna({'mano_obra': '10'}, inplace=True)            
            df.fillna({'nro_contratacion': '1816/SIGAF/2014'}, inplace=True)            
            df.fillna({'cuit_contratista': '30505454436'}, inplace=True)            
            df.fillna({'beneficiarios': 'vecinos'}, inplace=True)            
            df.fillna({'contratacion_tipo': 'Licitación Pública'}, inplace=True)
            df.fillna({'licitacion_anio': '2024'}, inplace=True)            
            
            columnas_verificables = [col for col in df.columns if col not in columnasAEliminar]
            
            df = df.dropna(subset=columnas_verificables, how='any')
            
            df.to_csv("datos_limpios_obras_urbanas.csv", sep=";", encoding="utf8", index=False)
                        
            print("Datos limpios guardados en 'datos_limpios_obras_urbanas.csv'.", df)
            return df
        except Exception as e:
            print(f"Error al limpiar los datos: {e}")
            
    @classmethod
    def cargar_datos(cls):
        df = GestionarObra.limpiar_datos()    

        # datosTipoObra = list(df['tipo'].unique())
        # for tipo in datosTipoObra:
        #     #Agregue un if para evitar duplicados
        #     if not TipoObra.select().where(TipoObra.nombre == tipo).exists():
        #         tipo_obra = TipoObra.create(nombre=tipo)
        #         tipo_obra.save()

        # datosEtapa = list(df['etapa'].unique())
        # for etapa in datosEtapa:
        #     etapa = Etapa.create(nombre=etapa)
        #     etapa.save()
       
        #   #hasta aca es lo que hicimos antes ------
        # for _, row in df[['barrio', 'comuna']].drop_duplicates().iterrows():
        #     try:
        #         if not Barrio.select().where(Barrio.nombre == row['barrio']).exists():
        #             Barrio.create(nombre=row['barrio'], comuna=row['comuna'])
        #     except Exception as e:
        #         print(f"Error al insertar barrio {row['barrio']}: {e}")

        # for area in df['area_responsable'].unique():
        #     try:
        #         if not AreaResponsable.select().where(AreaResponsable.nombre == area).exists():
        #             AreaResponsable.create(nombre=area)
        #     except Exception as e:
        #         print(f"Error al insertar área responsable {area}: {e}")
        
        # for _, row in df[['barrio', 'direccion', 'lat', 'lng']].drop_duplicates().iterrows():
        #     try:
        #         barrio = Barrio.get(Barrio.nombre == row['barrio'])
        #         Ubicacion.create(
        #         idBarrio=barrio,direccion=row['direccion'],latitud=float(row['lat'].replace(',', '.')),longitud=float(row['lng'].replace(',', '.'))            )
        #     except Barrio.DoesNotExist:
        #         print(f"Error: El barrio '{row['barrio']}' no existe en la base de datos. Verifica los datos.")
        #     except Exception as e:
        #         print(f"Error inesperado al procesar la ubicación: {e}")
        
       
        try:
            datos_empresas = df[['licitacion_oferta_empresa','licitacion_anio', 'cuit_contratista', 'nro_contratacion', 'contratacion_tipo', 'area_responsable']].drop_duplicates()
            for _, row in datos_empresas.iterrows():
                try:
                    area_responsable = AreaResponsable.get(AreaResponsable.nombre==row['area_responsable'])
                    if not Empresa.select().where(Empresa.cuitContratista == row['cuit_contratista']).exists():
                        Empresa.create(
                            licitacionOfertaEmpresa=row['licitacion_oferta_empresa'],
                            licitacionAnio=row.get('licitacion_anio', 0),
                            tipoContratacion=row.get('contratacion_tipo', 'Desconocido'),
                            cuitContratista=str(row['cuit_contratista'])[:13],
                            areaContratacion=area_responsable,
                            numeroContratacion=(row['nro_contratacion'])
                        )
                except KeyError as ke:
                    print(f"Error: Falta una columna clave en el DataFrame. Detalles: {ke}")
                except ValueError as ve:
                    print(f"Error de valor: Datos inválidos al crear Empresa. Detalles: {ve}")
                except pw.IntegrityError as ie:
                    print(f"Error de integridad: {ie}")
                except Exception as e:
                    print(f"Error inesperado al insertar empresa: {row.get('licitacion_oferta_empresa', 'Desconocido')}, {e}")
        except KeyError as ke:
            print(f"Error: Falta una columna clave en el DataFrame principal. Detalles: {ke}")
        except ValueError as ve:
            print(f"Error de valor general al procesar datos de empresas. Detalles: {ve}")
        except Exception as e:
            print(f"Error inesperado al procesar datos de empresas: {e}")

        
        #Recorrer el archivo registro por registro y dentro del for pasamos los dtos dl archivo a objetos
        #si es necesario, instanciar una obra y guardarla.Esto podria hacerse en un metodo aparte     
        
        print("Datos cargados exitosamente.")
        
       

    @classmethod
    def nueva_obra():
        pass
    
    @classmethod
    def obtener_indicadores():
        pass
    

prueba = GestionarObra()
# prueba.limpiar_datos()
# GestionarObra.conectar_db()

# #mapeo el ORM 
# GestionarObra.mapear_orm()
prueba.cargar_datos()

