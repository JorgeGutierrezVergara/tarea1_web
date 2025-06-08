import os
from flask import Flask, redirect, url_for, render_template, request, flash, abort
from datetime import datetime
from werkzeug.utils import secure_filename
from database.db import Base, engine, get_db_session, Region, Comuna, Actividad, Foto, ContactarPor, ActividadTema
from database.db import obtener_todas_las_regiones_bd, obtener_todas_las_comunas_bd, crear_tablas_bd
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
import math

app = Flask(__name__) 
app.secret_key = "secret_key"

UPLOAD_FOLDER = os.path.join(app.static_folder, 'UPLOAD_FOLDER') 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Límite 16 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    ultimas_actividades = []
    try:
        with get_db_session() as db_sess:
            query = db_sess.query(Actividad)
            query = query.options(
                joinedload(Actividad.comuna),
                joinedload(Actividad.fotos),
                joinedload(Actividad.temas_asociados)
            )
            
            ultimas_actividades = query.order_by(desc(Actividad.dia_hora_inicio)).limit(5).all()

    except Exception as e:
        print(f"Error al cargar actividades para la portada: {e}")
        flash("Hubo un error al cargar las actividades recientes.", "danger")
    
    return render_template('index.html', actividades=ultimas_actividades)

@app.route('/agregar', methods=['GET']) 
def agregar_actividad_page():
    regiones_db = []
    comunas_db_json = []
    try:
        with get_db_session() as db_sess:
            regiones_db = obtener_todas_las_regiones_bd(db_sess)
            comunas_db_json = obtener_todas_las_comunas_bd(db_sess)
    except Exception as e:
        flash(f"Error al cargar datos iniciales: {e}", "danger")

    return render_template('agregar.html',
                           regiones=regiones_db,
                           todas_las_comunas=comunas_db_json)

@app.route('/listado') 
def listado_actividades_page():   
    page = request.args.get('page', 1, type=int)
    per_page = 5 # Definimos cuántas actividades mostrar por página. 
    
    actividades_paginadas = []
    total_actividades = 0
    
    try:
        with get_db_session() as db_sess:
            total_actividades = db_sess.query(Actividad.id).count()
            
            query = db_sess.query(Actividad).options(
                joinedload(Actividad.comuna),
                joinedload(Actividad.fotos),
                joinedload(Actividad.temas_asociados)
            ).order_by(desc(Actividad.dia_hora_inicio))
            
            actividades_paginadas = query.offset((page - 1) * per_page).limit(per_page).all()

    except Exception as e:
        print(f"Error al cargar el listado de actividades: {e}")
        flash("Hubo un error al cargar el listado.", "danger")

    total_pages = math.ceil(total_actividades / per_page)

    return render_template('listado.html', 
                           actividades=actividades_paginadas,
                           page=page,
                           total_pages=total_pages)

@app.route('/actividad/<int:actividad_id>')
@app.route('/actividad/<int:actividad_id>')
def detalle_actividad_page(actividad_id):
    try:
        with get_db_session() as db_sess:
            # 1. Buscamos la actividad principal
            actividad = db_sess.query(Actividad).filter(Actividad.id == actividad_id).first()
            
            if not actividad:
                abort(404)
            
            # 2. EXTRAEMOS TODOS LOS DATOS RELACIONADOS MIENTRAS LA SESIÓN ESTÁ ABIERTA
            nombre_comuna = actividad.comuna.nombre
            nombre_region = actividad.comuna.region.nombre
            lista_fotos = list(actividad.fotos) # Convertimos a lista normal
            lista_temas = list(actividad.temas_asociados)
            lista_contactos = list(actividad.contactos)

    except Exception as e:
        print(f"--- ¡ERROR EN DETALLE DE ACTIVIDAD! ---")
        print(f"ERROR: {e}")
        print(f"---------------------------------------")
        flash("Hubo un error al cargar los detalles de la actividad.", "danger")
        return redirect(url_for('listado_actividades_page'))

    # 3. PASAMOS TODO POR SEPARADO A LA PLANTILLA
    return render_template('detalle_actividad.html', 
                           actividad=actividad,
                           nombre_comuna=nombre_comuna,
                           nombre_region=nombre_region,
                           fotos=lista_fotos,
                           temas=lista_temas,
                           contactos=lista_contactos)
                           
@app.route('/estadisticas') 
def estadisticas_page():
    return render_template('estadisticas.html')

@app.route('/procesar_actividad', methods=['POST'])
def procesar_nueva_actividad():
    print("--- DENTRO DE procesar_nueva_actividad ---") 
    #
    print("\n---[ DEBUG: DATOS RECIBIDOS DEL FORMULARIO ]---")
    print(f"Nombre: {request.form.get('nombre')}")
    print(f"Email: {request.form.get('email')}")
    print(f"ID Región: {request.form.get('select-region')}")
    print(f"ID Comuna: {request.form.get('comuna')}")
    print(f"Temas seleccionados: {request.form.getlist('tema_opcion')}")
    print(f"Checkbox 'Otro Tema': {request.form.get('tema_opcion_otro_checkbox')}")
    print(f"Texto 'Otro Tema': {request.form.get('otra_tema_texto')}")
    print(f"Archivos recibidos: {request.files.getlist('fotos_actividad[]')}")
    print("--------------------------------------------------\n")
    #
    errores_servidor = []
    datos_previos = request.form 
    nombres_archivos_guardados = []

    nombre_organizador = datos_previos.get('nombre', '').strip() 
    email_organizador = datos_previos.get('email', '').strip()
    region_seleccionada = datos_previos.get('select-region', '').strip()
    comuna_seleccionada = datos_previos.get('comuna', '').strip()
    sector = datos_previos.get('sector', '').strip()
    telefono = datos_previos.get('telefono', '').strip()
    
    temas_seleccionados = datos_previos.getlist('tema_opcion') 
    tema_otro_checkbox_marcado = datos_previos.get('tema_opcion_otro_checkbox') 
    texto_otro_tema = datos_previos.get('otra_tema_texto', '').strip()

    contactos_chk_seleccionados = datos_previos.getlist('contactar_opcion_chk')


    if not nombre_organizador:
        errores_servidor.append("El nombre del organizador es obligatorio.")
    elif len(nombre_organizador) > 200:
        errores_servidor.append("El nombre del organizador no puede exceder los 200 caracteres.")

    if not email_organizador:
        errores_servidor.append("El email del organizador es obligatorio.")
    elif "@" not in email_organizador or "." not in email_organizador.split('@')[-1] or len(email_organizador.split('@')[-1].split('.')) < 2 or email_organizador.split('@')[-1].split('.')[-1] == "":
        errores_servidor.append("El formato del email del organizador no es válido.")

    if not region_seleccionada:
        errores_servidor.append("Debe seleccionar una región.")

    if not comuna_seleccionada:
        errores_servidor.append("Debe seleccionar una comuna.")
        
    if sector and len(sector) > 100:
        errores_servidor.append("El sector no puede exceder los 100 caracteres.")

    if telefono: 
        import re 
        patron_telefono = r"^\+\d{3}\.\d{8}$"
        if not re.match(patron_telefono, telefono):
            errores_servidor.append("El formato del teléfono no es válido (ej: +569.12345678).")
            
    total_temas_seleccionados = len(temas_seleccionados)
    tema_otro_valido = False
    if tema_otro_checkbox_marcado:
        total_temas_seleccionados += 1
        if texto_otro_tema and 3 <= len(texto_otro_tema) <= 15:
            tema_otro_valido = True
        else:
            errores_servidor.append("Si seleccionas 'Otro' tema, la descripción debe tener entre 3 y 15 caracteres.")
            
    if total_temas_seleccionados == 0:
        errores_servidor.append("Debes seleccionar al menos un tema.")
    elif tema_otro_checkbox_marcado and not texto_otro_tema and not tema_otro_valido:
         if not any("descripción debe tener entre 3 y 15 caracteres" in err for err in errores_servidor):
            errores_servidor.append("Si seleccionas 'Otro' tema, debes proveer la descripción.")


    MAX_METODOS_CONTACTO = 5 
    total_contactos_seleccionados = 0
    
    for chk_value in contactos_chk_seleccionados:
        total_contactos_seleccionados +=1
        nombre_input_texto_asociado = ""
        es_otro_contacto = False

        if chk_value == "otro_contacto": 
            nombre_input_texto_asociado = "otra_contacto_texto"
            es_otro_contacto = True
        else: 
            nombre_input_texto_asociado = f"contactar_valor_{chk_value}" 

        valor_texto_contacto = datos_previos.get(nombre_input_texto_asociado, '').strip()
        
        if not valor_texto_contacto:
            errores_servidor.append(f"Debe ingresar el detalle para el método de contacto '{chk_value}'.")
        elif len(valor_texto_contacto) < 4 or len(valor_texto_contacto) > 50:
            errores_servidor.append(f"El detalle para '{chk_value}' debe tener entre 4 y 50 caracteres.")

    if total_contactos_seleccionados > MAX_METODOS_CONTACTO:
        errores_servidor.append(f"Puedes seleccionar un máximo de {MAX_METODOS_CONTACTO} formas de contacto.")
      
    # Listas las validaciones. Ahora se intenta enviar

    if errores_servidor:
        flash('Por favor, corrige los errores indicados en el formulario.', 'danger')
        
        with get_db_session() as db_sess:
            regiones_db = obtener_todas_las_regiones_bd(db_sess)
            comunas_db_json = obtener_todas_las_comunas_bd(db_sess)

        return render_template('agregar.html', 
                            errores_servidor=errores_servidor, 
                            datos_previos=datos_previos,
                            regiones=regiones_db,
                            todas_las_comunas=comunas_db_json)
    else:
        try:
            archivos_subidos = request.files.getlist('fotos_actividad[]')
            if not any(f.filename for f in archivos_subidos):
                raise ValueError("No se subió ninguna foto válida.")

            with get_db_session() as db_sess:
                nueva_actividad = Actividad(
                    comuna_id=int(datos_previos.get('comuna')),
                    sector=datos_previos.get('sector', '').strip(),
                    nombre=datos_previos.get('nombre', '').strip(),
                    email=datos_previos.get('email', '').strip(),
                    celular=datos_previos.get('telefono', '').strip() or None,
                    dia_hora_inicio=datetime.fromisoformat(datos_previos.get('inicio')),
                    dia_hora_termino=datetime.fromisoformat(datos_previos.get('final')) if datos_previos.get('final') else None,
                    descripcion=datos_previos.get('descripcion_actividad', '').strip()
                )
                db_sess.add(nueva_actividad)
                for file_storage in archivos_subidos:
                    if file_storage and allowed_file(file_storage.filename):
                        filename_seguro = secure_filename(file_storage.filename)
                        filename_unico = datetime.now().strftime("%Y%m%d%H%M%S%f_") + filename_seguro
                        
                        ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], filename_unico)
                        file_storage.save(ruta_guardado)
                        print(f"Archivo '{filename_unico}' guardado en disco.")

                        foto_db = Foto(
                            ruta_archivo=filename_unico,
                            nombre_archivo=filename_seguro,
                            actividad_obj=nueva_actividad 
                        )
                        db_sess.add(foto_db)
                        print(f"Registro para '{filename_unico}' añadido a la sesión de la BD.")
                
                for tema in temas_seleccionados:
                    tema_db = ActividadTema(tema=tema, actividad_obj=nueva_actividad)
                    db_sess.add(tema_db)
                if tema_otro_checkbox_marcado:
                    tema_otro_db = ActividadTema(
                        tema='otro',
                        glosa_otro=texto_otro_tema,
                        actividad_obj=nueva_actividad
                    )
                    db_sess.add(tema_otro_db)

                for chk_value in contactos_chk_seleccionados:
                    nombre_input = f"contactar_valor_{chk_value}"
                    if chk_value == "otro_contacto":
                        nombre_input = "otra_contacto_texto"
                    valor_contacto = datos_previos.get(nombre_input, '').strip()
                    nombre_enum = chk_value.replace('_contacto', '')
                    if nombre_enum == "x": nombre_enum = "X"    
                    contacto_db = ContactarPor(
                        nombre=nombre_enum,
                        identificador=valor_contacto,
                        actividad_obj=nueva_actividad
                    )
                    db_sess.add(contacto_db)

            flash('¡Actividad GUARDADA con todos sus datos en la Base de Datos!', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            print(f"---¡ERROR AL GUARDAR EN LA BD!---")
            print(f"ERROR: {e}")
            print("---------------------------------")
            flash(f"Error interno al guardar la actividad: {e}", "danger")
            return redirect(url_for('agregar_actividad_page'))

if __name__ == "__main__":
    crear_tablas_bd()
    app.run(debug = True)