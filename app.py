import os
from flask import Flask, redirect, url_for, render_template, request, flash, abort, jsonify 
from datetime import datetime
from werkzeug.utils import secure_filename
from database.db import Base, engine, get_db_session, Region, Comuna, Actividad, Foto, ContactarPor, ActividadTema, Comentario 
from database.db import obtener_todas_las_regiones_bd, obtener_todas_las_comunas_bd, crear_tablas_bd
from sqlalchemy import desc, func, extract, case
from sqlalchemy.sql import and_ 
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
    per_page = 5  
    
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
def detalle_actividad_page(actividad_id):
    try:
        with get_db_session() as db_sess:
            actividad = db_sess.query(Actividad).filter(Actividad.id == actividad_id).first()
            
            if not actividad:
                abort(404)
            
            nombre_comuna = actividad.comuna.nombre
            nombre_region = actividad.comuna.region.nombre
            lista_fotos = list(actividad.fotos) 
            lista_temas = list(actividad.temas_asociados)
            lista_contactos = list(actividad.contactos)

    except Exception as e:
        flash("Hubo un error al cargar los detalles de la actividad.", "danger")
        return redirect(url_for('listado_actividades_page'))

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

            flash('Actividad GUARDADA en la Base de Datos', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            print(f"---¡ERROR AL GUARDAR EN LA BD!---")
            flash(f"Error interno al guardar la actividad: {e}", "danger")
            return redirect(url_for('agregar_actividad_page'))

@app.route('/api/actividad/<int:actividad_id>/comentarios', methods=['GET', 'POST'])
def api_comentarios(actividad_id):
    if request.method == 'GET':
     
        try:
            with get_db_session() as db_sess:
                actividad_obj = db_sess.query(Actividad).filter(Actividad.id == actividad_id).first()
                if not actividad_obj:
                    return jsonify({"error": "Actividad no encontrada."}), 404

                comentarios_data = [
                    {"nombre": c.nombre, "texto": c.texto, "fecha": c.fecha.strftime('%d-%m-%Y %H:%M')}
                    for c in actividad_obj.comentarios
                ]
                return jsonify(comentarios_data)
        except Exception as e:
            print(f"--- ¡ERROR EN API GET COMENTARIOS! ---")
            return jsonify({"error": "No se pudieron cargar los comentarios."}), 500

    if request.method == 'POST':
       
        try:
            nombre = request.form.get('nombre', '').strip()
            texto = request.form.get('texto', '').strip()
            if not (3 <= len(nombre) <= 80):
                return jsonify({"error": "El nombre debe tener entre 3 y 80 caracteres."}), 400
            if len(texto) < 5:
                return jsonify({"error": "El comentario debe tener al menos 5 caracteres."}), 400

            with get_db_session() as db_sess:
                actividad_obj = db_sess.query(Actividad).filter(Actividad.id == actividad_id).first()
                if not actividad_obj:
                    return jsonify({"error": "Actividad no encontrada."}), 404

                nuevo_comentario = Comentario(
                    nombre=nombre,
                    texto=texto,
                    fecha=datetime.now(),
                    actividad_id=actividad_id
                )
                db_sess.add(nuevo_comentario)
                db_sess.flush() 
                comentario_guardado = {
                    "nombre": nuevo_comentario.nombre,
                    "texto": nuevo_comentario.texto,
                    "fecha": nuevo_comentario.fecha.strftime('%d-%m-%Y %H:%M')
                }
                
                return jsonify(comentario_guardado), 201

        except Exception as e:
            print(f"--- ¡ERROR EN API POST COMENTARIO! ---")
            return jsonify({"error": "Ocurrió un error interno al guardar el comentario."}), 500

@app.route('/api/estadisticas/actividades_por_dia')
def api_actividades_por_dia():
    try:
        with get_db_session() as db_sess:
            resultado = db_sess.query(
                func.date(Actividad.dia_hora_inicio).label('fecha'),
                func.count(Actividad.id).label('cantidad')
            ).group_by('fecha').order_by('fecha').all()

            data_para_grafico = []
            for registro in resultado:
                fecha_python = registro.fecha
                timestamp_js = int(datetime.combine(fecha_python, datetime.min.time()).timestamp() * 1000)
                data_para_grafico.append([timestamp_js, registro.cantidad])
            return jsonify(data_para_grafico)

    except Exception as e:
        print(f"--- ¡ERROR EN API DE ESTADÍSTICAS (ACTIVIDADES POR DÍA)! ---")
        return jsonify({"error": "No se pudieron calcular los datos para el gráfico."}), 500

@app.route('/api/estadisticas/actividades_por_tipo')
def api_actividades_por_tipo():
    try:
        with get_db_session() as db_sess:
            resultado = db_sess.query(
                ActividadTema.tema.label('nombre_tema'), 
                func.count(Actividad.id).label('cantidad_actividades')
            ).join(Actividad, Actividad.id == ActividadTema.actividad_id)\
             .group_by(ActividadTema.tema)\
             .order_by(ActividadTema.tema)\
             .all()

            data_para_grafico = []
            for registro in resultado:
                data_para_grafico.append({
                    'name': registro.nombre_tema,
                    'y': registro.cantidad_actividades
                })

            return jsonify(data_para_grafico)

    except Exception as e:
        print(f"--- ¡ERROR EN API DE ESTADÍSTICAS (ACTIVIDADES POR TEMA)! ---")
        return jsonify({"error": "No se pudieron calcular los datos para el gráfico de torta."}), 500

@app.route('/api/estadisticas/actividades_por_mes_y_periodo')
def api_actividades_por_mes_y_periodo():
    try:
        with get_db_session() as db_sess:
            nombres_meses = {
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            }

            resultados_raw = db_sess.query(
                extract('month', Actividad.dia_hora_inicio).label('mes'),
                case(
                    (and_(extract('hour', Actividad.dia_hora_inicio) >= 6, extract('hour', Actividad.dia_hora_inicio) < 12), 'Mañana'),
                    (and_(extract('hour', Actividad.dia_hora_inicio) >= 12, extract('hour', Actividad.dia_hora_inicio) < 18), 'Mediodía'),
                    else_='Tarde'
                ).label('periodo_dia'),
                func.count(Actividad.id).label('cantidad')
            ).group_by('mes', 'periodo_dia')\
             .order_by('mes', 'periodo_dia')\
             .all()

            meses_ordenados = sorted(list(set([r.mes for r in resultados_raw])))

            categorias_meses = [nombres_meses[m] for m in meses_ordenados]

            data_manana = [0] * len(meses_ordenados)
            data_mediodia = [0] * len(meses_ordenados)
            data_tarde = [0] * len(meses_ordenados)

            for mes_num, periodo_dia, cantidad in resultados_raw:
                print(f"Contenido desempaquetado: mes_num={mes_num}, periodo_dia={periodo_dia}, cantidad={cantidad}")

                idx_mes = meses_ordenados.index(mes_num)
                if periodo_dia == 'Mañana':
                    data_manana[idx_mes] = cantidad
                elif periodo_dia == 'Mediodía':
                    data_mediodia[idx_mes] = cantidad
                elif periodo_dia == 'Tarde':
                    data_tarde[idx_mes] = cantidad

            series_para_grafico = [
                {'name': 'Mañana', 'data': data_manana},
                {'name': 'Mediodía', 'data': data_mediodia},
                {'name': 'Tarde', 'data': data_tarde}
            ]

            return jsonify({
                'categories': categorias_meses,
                'series': series_para_grafico
            })

    except Exception as e:
        print(f"--- ¡ERROR EN API DE ESTADÍSTICAS (ACTIVIDADES POR MES Y PERIODO)! ---")
        return jsonify({"error": "No se pudieron calcular los datos para el gráfico de barras."}), 500


if __name__ == "__main__":
    crear_tablas_bd()
    app.run(debug = True)