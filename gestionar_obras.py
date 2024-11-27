import peewee as pw 
from peewee import fn
from modelo_orm import sqlite_crear, Obra, Empresa, Etapa, Ubicacion, AreaResponsable, TipoObra, Barrio, TipoContratacion
import pandas as pd
from abc import ABC 
import numpy as np
import random 
import string

class GestionarObra(ABC):
    
    @classmethod
    def extraer_datos(cls, ruta_dataset):
        try:
            df = pd.read_csv("Nueva base corregida.csv", sep=";", encoding="latin-1")
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
            sqlite_crear.create_tables([Etapa, Empresa, Ubicacion, TipoObra, AreaResponsable, Obra, Barrio, TipoContratacion])
            print("Tablas creadas exitosamente.")
        except pw.OperationalError as e:
            print(f"Error al crear las tablas: {e}")
    
    @classmethod
    def limpiar_datos(cls):
        try:
            df = GestionarObra.extraer_datos("Nueva base corregida.csv")               
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            df.fillna({'nombre': 'Area ambiental'}, inplace=True)            
            df.fillna({'tipo_obra': 'Salud'}, inplace=True)            
            df.fillna({'descripcion': 'Obra en ejecucion'}, inplace=True)            
            df.fillna({'monto_contrato': '300.000.000'}, inplace=True)            
            df.fillna({'porcentaje_avance': '0'}, inplace=True)            
            df.fillna({'fecha_fin_inicial': '31/12/2024'}, inplace=True)            
            df['expedientenumero'] = df['expedientenumero'].apply(lambda x: ''.join(random.choices(string.ascii_uppercase + string.digits, k=9)) if pd.isnull(x) else x)
            df.fillna({'mano_obra': '10'}, inplace=True)            
            df.fillna({'nro_contratacion': '1816/SIGAF/2014'}, inplace=True)            
            df.fillna({'cuit_contratista': '30505454436'}, inplace=True)            
            df.fillna({'beneficiarios': 'vecinos'}, inplace=True)            
            df.fillna({'contratacion_tipo': 'Licitación Pública'}, inplace=True)
            df.fillna({'licitacion_anio': '2024'}, inplace=True)  
            df.fillna({'destacada': 'NO'},inplace=True)          

            df = df.iloc[:1245]
            
            df.to_csv("datos_limpios_obras_urbanas.csv", sep=";", encoding="utf8", index=False)
                        
            print("Datos limpios guardados en 'datos_limpios_obras_urbanas.csv'.", df)
            return df
        except Exception as e:
            print(f"Error al limpiar los datos: {e}")
            
    @classmethod
    def cargar_datos(cls):
        df = pd.read_csv("datos_limpios_obras_urbanas.csv", sep=";", encoding="utf8")
        
        # Tabla Tipo de obra
        try:
            datosTipoObra = list(df['tipo'].unique())
            for tipo in datosTipoObra:
                try:
                    tipo_existente = TipoObra.select().where(TipoObra.nombre == tipo).first()
                    
                    if tipo_existente:
                        print(f"Tipo de obra ya existente: {tipo}")
                        continue

                    tipo_obra = TipoObra.create(nombre=tipo)
                    tipo_obra.save()
                    print(f"Tipo de obra creado: {tipo}")
                
                except Exception as e:
                    print(f"Error al procesar el tipo de obra '{tipo}': {e}")

        except Exception as e:
            print(f"Error general al cargar datos para TipoObra: {e}")
        
        # Tabla Tipo contratacion
        try:
            datosTipoContratacion = list(df['contratacion_tipo'].unique())
            for tipo_contratacion in datosTipoContratacion:
                try:
                    tipo_contratacion_existente = TipoContratacion.select().where(TipoContratacion.nombre == tipo_contratacion).first()
                    if tipo_contratacion_existente:
                        print(f"Tipo de contratación ya existente: {tipo_contratacion}")
                        continue
                    tipo_contratacion_nueva = TipoContratacion.create(nombre=tipo_contratacion)
                    tipo_contratacion_nueva.save()
                    print(f"Tipo de contratación creado: {tipo_contratacion}")
                except Exception as e:
                    print(f"Error al procesar el tipo de contratación '{tipo_contratacion}': {e}")
        except Exception as e:
            print(f"Error general al cargar datos para TipoContratacion: {e}")
            
        # Tabla Etapas
        try:
            datosEtapa = list(df['etapa'].unique())
            
            for etapa in datosEtapa:
                try:
                    etapaNormalizada = etapa.strip().lower()
                
                    if etapaNormalizada in ["en obra", "en ejecución"]:
                        etapaNormalizada = "en ejecución"

                    etapaExistente = Etapa.select().where(fn.LOWER(Etapa.nombre) == etapaNormalizada).first()
                
                    if etapaExistente:
                        print(f"Etapa ya existente: {etapaNormalizada}")
                    else:
                        nueva_etapa = Etapa.create(nombre=etapaNormalizada.title())
                        nueva_etapa.save()
                        print(f"Etapa creada: {etapaNormalizada.title()}")
                        
                except Exception as e:
                    print(f"Error al procesar la etapa '{etapa}': {e}")
                    
        except Exception as e:
                print(f"Error general al cargar datos para Etapa: {e}")
       
        # Tabla Barrios
        try:
            for _, row in df[['barrio', 'comuna']].drop_duplicates().iterrows():
                try:
                    
                    barrio = row['barrio']
                    comuna = row['comuna']
                    
                    if not barrio or not comuna:
                        print("Datos de barrio o comuna faltantes. No se puede insertar.")
                        continue
                    barrio_existente = Barrio.select().where(Barrio.nombre == barrio).first()
                    
                    if barrio_existente:
                        print(f"Barrio ya existente: {barrio} - Comuna: {barrio_existente.comuna}")
                        continue

                    Barrio.create(nombre=barrio, comuna=comuna)
                    print(f"Barrio creado: {barrio} - Comuna: {comuna}")
                
                except Exception as e:
                    print(f"Error al insertar barrio {barrio}: {e}")

        except Exception as e:
            print(f"Error general al cargar datos para Barrio: {e}")

        # Tabla Área Responsable
        try:
            for area in df['area_responsable'].unique():
                try:
                    area_existente = AreaResponsable.select().where(AreaResponsable.nombre == area).first()
                    
                    if area_existente:
                        print(f"Área responsable ya existente: {area}")
                        continue
                    AreaResponsable.create(nombre=area)
                    print(f"Área responsable creada: {area}")
                
                except Exception as e:
                    print(f"Error al insertar área responsable {area}: {e}")

        except Exception as e:
            print(f"Error general al cargar datos para Área Responsable: {e}")
        
        # Tabla Ubicación
        try:
            for _, row in df[['barrio', 'direccion', 'lat', 'lng']].drop_duplicates().iterrows():
                try:
                    barrio = Barrio.get(Barrio.nombre == row['barrio'])

                    ubicacion_existente = Ubicacion.select().where(
                        (Ubicacion.barrio == barrio) &
                        (Ubicacion.direccion == row['direccion']) &
                        (Ubicacion.latitud == row['lat']) &
                        (Ubicacion.longitud == row['lng'])
                    ).first()
                    
                    if ubicacion_existente:
                        print(f"Ubicación ya existente: {row['direccion']} en Barrio: {row['barrio']}")
                        continue

                    Ubicacion.create(
                        barrio=barrio,
                        direccion=row['direccion'],
                        latitud=row['lat'],
                        longitud=row['lng']
                    )
                    print(f"Ubicación creada: {row['direccion']} en Barrio: {row['barrio']}")
                
                except Barrio.DoesNotExist:
                    print(f"Error: El barrio '{row['barrio']}' no existe en la base de datos. Verifica los datos.")
                except Exception as e:
                    print(f"Error inesperado al procesar la ubicación '{row['direccion']}': {e}")

        except Exception as e:
            print(f"Error general al cargar datos para Ubicacion: {e}")
        
        # Tabla Empresa
        try:
            datos_empresas = df[['licitacion_oferta_empresa', 'licitacion_anio', 'cuit_contratista', 
                            # 'nro_contratacion', 'contratacion_tipo', 
                            'area_responsable']].drop_duplicates()
            for _, row in datos_empresas.iterrows():
                try:
                    area_responsable = AreaResponsable.get(AreaResponsable.nombre == row['area_responsable'])
                    empresa_existente = Empresa.select().where(
                        (Empresa.licitacionOfertaEmpresa == row['licitacion_oferta_empresa']) &
                        (Empresa.cuitContratista == str(row['cuit_contratista'])[:13]) 
                        # (Empresa.numeroContratacion == row['nro_contratacion'])
                    ).first()
                    
                    if empresa_existente:
                        print(f"Empresa ya existente: {row['licitacion_oferta_empresa']} - CUIT: {row['cuit_contratista']}")
                        continue

                    Empresa.create(
                        licitacionOfertaEmpresa=row['licitacion_oferta_empresa'],
                        licitacionAnio=row.get('licitacion_anio', 0),
                        # tipoContratacion=row.get('contratacion_tipo', 'Desconocido'),
                        cuitContratista=str(row['cuit_contratista'])[:13],
                        areaContratacion=area_responsable,
                        # numeroContratacion=row['nro_contratacion']
                    )
                    print(f"Empresa creada: {row['licitacion_oferta_empresa']} - CUIT: {row['cuit_contratista']}")
                
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
            
        # Tabla Obra
        try:
            df = pd.read_csv("datos_limpios_obras_urbanas.csv", sep=";", encoding="utf8")

            for _, row in df[['tipo', 'area_responsable', 'etapa', 'direccion', 'nombre', 'fecha_inicio',
                              'fecha_fin_inicial', 'plazo_meses', 'mano_obra', 'expedientenumero',
                              'porcentaje_avance', 'monto_contrato', 'descripcion', 'destacada',
                              'licitacion_oferta_empresa', 'contratacion_tipo', 'nro_contratacion']].drop_duplicates().iterrows():
                try:
                    tipoObra, _ = TipoObra.get_or_create(nombre=row['tipo'])
                    areaResponsable, _ = AreaResponsable.get_or_create(nombre=row['area_responsable'])
                    etapa, _ = Etapa.get_or_create(nombre=row['etapa'])
                    ubicacion, _ = Ubicacion.get_or_create(
                        direccion=row['direccion'],
                        defaults={
                            'barrio': Barrio.get_or_create(nombre='Barrio Desconocido', comuna=1)[0],
                            'latitud': 0.0,
                            'longitud': 0.0
                        }
                    )
                    empresa, _ = Empresa.get_or_create(
                        licitacionOfertaEmpresa=row['licitacion_oferta_empresa'],
                        defaults={
                            'licitacionAnio': row.get('licitacion_anio', 2024),
                            # 'tipoContratacion': row.get('contratacion_tipo', 'Desconocido'),
                            'cuitContratista': str(row.get('cuit_contratista', '00000000000'))[:11],
                            'areaContratacion': row.get('area_responsable', 'Desconocida'),
                            # 'numeroContratacion': row.get('nro_contratacion', 0)
                        }
                    )
                    tipoContratacion, _ = TipoContratacion.get_or_create(nombre=row['contratacion_tipo'])

                    if not (tipoObra and areaResponsable and etapa and ubicacion and empresa):
                        print(f"Error: Faltan dependencias para la obra '{row['nombre']}'. No se puede crear.")
                        continue
                    try:
                        montoContrato = int(row['monto_contrato'].replace('$', '').replace(',', ''))
                    except ValueError:
                        print(f"Error al convertir el monto de contrato: {row['monto_contrato']}")
                        continue
                    obraExistente = Obra.select().where(
                        (Obra.nombre == row['nombre']) &
                        (Obra.ubicacion == ubicacion) &
                        (Obra.tipoObra == tipoObra) &
                        (Obra.areaResponsable == areaResponsable) &
                        (Obra.etapa == etapa) &
                        (Obra.empresa == empresa)
                    ).first()

                    if obraExistente:
                        print(f"La obra '{row['nombre']}' ya existe en la base de datos.")
                        continue

                    nueva_obra = Obra.create(
                        nombre=row['nombre'],
                        empresa=empresa,
                        tipoObra=tipoObra,
                        areaResponsable=areaResponsable,
                        ubicacion=ubicacion,
                        tipoContratacion=tipoContratacion,
                        fechaInicio=row['fecha_inicio'],
                        fechaFinIinicial=row['fecha_fin_inicial'],
                        plazoMeses=row['plazo_meses'],
                        manoObra=row['mano_obra'],
                        etapa=etapa,
                        numeroExpediente=row['expedientenumero'],
                        porcentajeAvance=row['porcentaje_avance'],
                        montoContrato=montoContrato,
                        descripcion=row['descripcion'],
                        destacada=row['destacada'],
                        numeroContratacion=row['nro_contratacion']
                    )
                    print(f"Nueva obra creada: {nueva_obra.nombre}")

                except pw.IntegrityError as e:
                    print(f"Error de integridad al procesar la obra '{row['nombre']}': {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar la obra '{row['nombre']}': {e}")

        except FileNotFoundError:
            print("Error: El archivo 'datos_limpios_obras_urbanas.csv' no se encuentra. Verifique la ruta del archivo.")
        except pd.errors.EmptyDataError:
            print("Error: El archivo CSV está vacío.")
        except pd.errors.ParserError:
            print("Error: El archivo CSV no pudo ser leído. Verifique el formato.")
        except Exception as e:
            print(f"Error general al cargar datos para las obras: {e}")

    @classmethod
    def nueva_obra(cls):
        try:
            nombre = input("Ingresar el nombre de la nueva obra: ").strip()
            numeroContratacion = input("Ingrese el número de contratación: ").strip()
            nroDeExpediente = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
            print(f"Número de expediente generado: {nroDeExpediente}")
            while True:
                try:
                    montoDeContrato = int(input("Ingresar monto del contrato: "))
                    break
                except ValueError:
                    print("Error: El monto del contrato debe ser un número entero.")

            while True:
                manoDeObra = input("Ingresar cantidad de mano de obra: ")
                try:
                    if manoDeObra.isdigit() and int(manoDeObra) >= 0:
                        manoDeObra = int(manoDeObra)
                        break
                except ValueError:
                    print("Error: La cantidad de mano de obra es inválida.")
           
            while True:
                try:
                    tipos_obra = list(TipoObra.select())
                    if not tipos_obra:
                        print("No hay tipos de obra registrados en la base de datos.")
                        return
                    print("\nSeleccione un tipo de obra de la lista:")
                    for index, tipo in enumerate(tipos_obra, start=1):
                        print(f"{index}. {tipo.nombre}")

                    seleccion = input("Ingrese el número correspondiente al tipo de obra: ")
                    if seleccion.isdigit():
                        seleccion = int(seleccion)
                        if 1 <= seleccion <= len(tipos_obra):
                            tipoObraSeleccionado = tipos_obra[seleccion - 1]
                            break
                        else:
                            print("Selección fuera de rango. Por favor, ingrese un número válido.")
                    else:
                        print("Entrada no válida. Por favor, ingrese un número.")
                except Exception as e:
                    print(f"Error al validar el tipo de obra: {e}")
                    return
            
            while True:
                try:
                    areas_responsables = list(AreaResponsable.select())
                    if not areas_responsables:
                        print("No hay áreas responsables registradas en la base de datos.")
                        return
                    print("\nSeleccione un área responsable de la lista:")
                    for index, area in enumerate(areas_responsables, start=1):
                        print(f"{index}. {area.nombre}")

                    seleccion = input("Ingrese el número correspondiente al área responsable: ")
                    if seleccion.isdigit():
                        seleccion = int(seleccion)
                        if 1 <= seleccion <= len(areas_responsables):
                            areaResponsable = areas_responsables[seleccion - 1]
                            print(f"Ha seleccionado el área responsable: {areaResponsable.nombre}")
                            break
                        else:
                            print("Selección fuera de rango. Por favor, ingrese un número válido.")
                    else:
                        print("Entrada no válida. Por favor, ingrese un número.")
                except Exception as e:
                    print(f"Error al validar el área responsable: {e}")
                    return
            
            while True:
                direccion = input("Ingrese la dirección de la obra: ").strip()
                ubicacion = Ubicacion.get_or_none(direccion=direccion)
                
                if ubicacion:
                    print(f"La ubicación '{direccion}' ya existe.")
                    break
                else:
                    print(f"La ubicación '{direccion}' no existe en la base de datos.")
                    crear_nueva = input("¿Desea crear una nueva ubicación? (s/n): ").strip().lower()
                    
                    if crear_nueva == 's':
                        barrio_nombre = input("Ingrese el nombre del barrio: ").strip()
                        comuna = input("Ingrese la comuna: ").strip()
                        if not comuna.isdigit():
                            print("Error: La comuna debe ser un número.")
                            continue
                        
                        latitud = input("Ingrese la latitud (o presione enter para usar 0.0): ").strip() or '0.0'
                        longitud = input("Ingrese la longitud (o presione enter para usar 0.0): ").strip() or '0.0'
                        
                        try:
                            latitud = float(latitud)
                            longitud = float(longitud)
                        except ValueError:
                            print("Error: Latitud y longitud deben ser valores numéricos.")
                            continue
                        
                        barrio, created = Barrio.get_or_create(nombre=barrio_nombre, defaults={'comuna': int(comuna)})
                        if created:
                            print(f"Nuevo barrio '{barrio_nombre}' creado.")
                        ubicacion = Ubicacion.create(
                            barrio=barrio,
                            direccion=direccion,
                            latitud=latitud,
                            longitud=longitud
                        )
                        print(f"Nueva ubicación creada: {ubicacion.direccion} en Barrio: {barrio.nombre}")
                        break
                    else:
                        print("Por favor, ingrese una dirección válida existente.")
                        
            while True:
                nombre_empresa = input("Ingrese el nombre de la empresa contratista: ").strip()
                try:
                    empresa = Empresa.get_or_none(licitacionOfertaEmpresa=nombre_empresa)
                    if empresa:
                        print(f"Empresa '{nombre_empresa}' encontrada.")
                        break
                    else:
                        print(f"La empresa '{nombre_empresa}' no existe en la base de datos.")
                        crear_empresa = input("¿Desea crear una nueva empresa? (s/n): ").strip().lower()
                        if crear_empresa == 's':
                            licitacionAnio = input("Ingrese el año de la licitación : ").strip()
                            cuitContratista = input("Ingrese el CUIT de la empresa (11 dígitos): ").strip()
                            areaContratacion = input("Ingrese el área de contratación: ").strip()

                            try:
                                empresa = Empresa.create(
                                    licitacionOfertaEmpresa=nombre_empresa,
                                    licitacionAnio=int(licitacionAnio),
                                    cuitContratista=cuitContratista,
                                    areaContratacion=areaContratacion,
                                )
                                print(f"Nueva empresa '{nombre_empresa}' creada exitosamente.")
                                break
                            except ValueError:
                                print("Error: Algunos de los datos ingresados no son válidos. Por favor, intente nuevamente.")
                except Exception as e:
                    print(f"Error al validar la empresa contratista: {e}")
                    return
                
            while True:
                contratacion = list(TipoContratacion.select())
                
                if not contratacion:
                    print("No hay tipos de contratación disponibles.")
                    return
                
                print("\nSeleccione un área responsable de la lista:")
                
                for index, item in enumerate(contratacion, start=1):
                    print(f"{index}. {item.nombre}")
                
                itemSeleccionado = input("Ingrese el número del tipo de contratación: ")
                
                if itemSeleccionado.isdigit():
                        itemSeleccionado = int(itemSeleccionado)
                        if 1 <= itemSeleccionado <= len(contratacion):
                            contratacionSeleccionada = contratacion[itemSeleccionado - 1]
                            print(f"Ha seleccionado el tipo de contratación: {contratacionSeleccionada.nombre}")
                            break
                        else:
                            print("Selección fuera de rango. Por favor, ingrese un número válido.")
                else:
                        print("Entrada no válida. Por favor, ingrese un número.")
                        
            try:
                nueva_obra = Obra.create(
                    nombre=nombre,
                    empresa_id=empresa,
                    tipoObra_id=tipoObraSeleccionado,
                    areaResponsable_id=areaResponsable,
                    ubicacion_id=ubicacion,
                    fechaInicio="2024-01-01",
                    fechaFinIinicial="2025-01-01",
                    plazoMeses=12,
                    manoObra=manoDeObra,
                    etapa_id=Etapa.get_or_create(nombre="Proyecto")[0],
                    numeroExpediente=nroDeExpediente,
                    porcentajeAvance=0,
                    montoContrato=montoDeContrato,
                    descripcion="Descripción predeterminada",
                    destacada="NO",
                    tipoContratacion_id = contratacionSeleccionada,
                    numeroContratacion = numeroContratacion
                )
                
                nueva_obra.save()
                print("Obra creada exitosamente.")
            except Exception as e:
                print(f"Error al crear la nueva obra: {e}")

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    @classmethod
    def obtener_indicadores(cls):
        try:
            print("\nListado de todas las áreas responsables:")
            areas = AreaResponsable.select()
            for area in areas:
                print(f"- {area.nombre}")

            print("\nListado de todos los tipos de obra:")
            tipos_obra = TipoObra.select()
            for tipo in tipos_obra:
                print(f"- {tipo.nombre}")

            print("\nCantidad de obras por etapa:")
            etapas = Etapa.select()
            for etapa in etapas:
                cantidad = Obra.select().where(Obra.etapa == etapa).count()
                print(f"- {etapa.nombre}: {cantidad} obras")

            print("\nCantidad de obras y monto total de inversión por tipo de obra:")
            for tipo in tipos_obra:
                cantidad = Obra.select().where(Obra.tipoObra == tipo).count()
                monto_total = (
                Obra.select(fn.SUM(Obra.montoContrato))
                .where((Obra.tipoObra == tipo) & (Obra.montoContrato.is_null(False)))
                .scalar() or 0
                )
                print(f"- {tipo.nombre}: {cantidad} obras, Inversión total: ${monto_total}")
            
            print("\nListado de todos los barrios pertenecientes a las comunas 1, 2 y 3:")
            barrios = Barrio.select().where(Barrio.comuna.in_([1, 2, 3]))
            for barrio in barrios:
                print(f"- {barrio.nombre} (Comuna {barrio.comuna})")

            print("\nCantidad de obras finalizadas y su monto total de inversion en la Comuna 1")
            obras_finalizadas_comuna1 = (
                                        Obra.select()
                                        .join(Etapa, on=(Obra.etapa == Etapa.idEtapa))
                                        .join(Ubicacion, on=(Obra.ubicacion == Ubicacion.idUbicacion))
                                        .join(Barrio, on=(Ubicacion.barrio == Barrio.idBarrio))
                                        .where(
                                            (Etapa.nombre == "Finalizada") & (Barrio.comuna == 1)
                                        )
                                        )
            cantidad_finalizadas = obras_finalizadas_comuna1.count()
            monto_total_comuna1 = (
                                    Obra.select(fn.SUM(Obra.montoContrato))
                                    .join(Etapa, on=(Obra.etapa == Etapa.idEtapa))
                                    .join(Ubicacion, on=(Obra.ubicacion == Ubicacion.idUbicacion))
                                    .join(Barrio, on=(Ubicacion.barrio == Barrio.idBarrio))
                                    .where(
                                        (Etapa.nombre == "Finalizada") & (Barrio.comuna == 1)
                                    )
                                    .scalar() or 0
            )
            print(f" Obras Finalizadas en Comuna 1: {cantidad_finalizadas} obras, Inversión total: ${monto_total_comuna1}")

            print("\nCantidad de obras finalizadas en un plazo menor o igual a 24 meses")
            obras_finalizadas_24_meses = (
                Obra.select()
                .join(Etapa, on=(Obra.etapa == Etapa.idEtapa))
                .where(
                    (Etapa.nombre == 'Finalizada') & (Obra.plazoMeses <= 24)
                )
            )
            cantidad_obras_24_meses = obras_finalizadas_24_meses.count()
            print(f"Cantidad de obras finalizadas: {cantidad_obras_24_meses}")

            print("\nPorcentaje de obras finalizadas")
            total_obras = Obra.select().count()
            obras_finalizadas = Obra.select().join(Etapa, on=(Obra.etapa == Etapa.idEtapa)).where(Etapa.nombre == 'Finalizada').count()
            porcentaje_finalizadas = (obras_finalizadas / total_obras) * 100
            print(f"Porcentaje de obras finalizadas: {porcentaje_finalizadas}%")

            print("\nCantidad total de mano de obra empleada")
            mano_obra_list = [obra.manoObra for obra in Obra.select() if obra.manoObra is not None]
            mano_obra_list = [int(mano) for mano in mano_obra_list if isinstance(mano, (int, float))]
            total_mano_obra = np.sum(mano_obra_list) if mano_obra_list else 0
            print(f"- Total de mano de obra empleada: {total_mano_obra}")

            print("\nMonto total de inversión:")
            montos_list = [obra.montoContrato for obra in Obra.select() if obra.montoContrato is not None]
            montos_list = [int(monto) for monto in montos_list if isinstance(monto, (int, float, str)) and str(monto).isdigit()]
            monto_total_inversion = np.sum(montos_list) if montos_list else 0
            print(f"- Monto total de inversión: ${monto_total_inversion}")

        except Exception as e:
            print(f"Error al obtener indicadores: {e}")
            
obrasPublicas = GestionarObra()
obrasPublicas.nueva_obra()
# los nombres de las obras de prueba son "Obra de Prueba", "Segunda obra de prueba"