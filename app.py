import os
from flask import Flask, redirect, url_for, render_template, request, flash
from datetime import datetime
from werkzeug.utils import secure_filename
from database.db import Base, engine, get_db_session, Region, Comuna, Actividad 
from database.db import obtener_todas_las_regiones_bd, obtener_todas_las_comunas_bd, crear_tablas_bd

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
    return render_template('index.html')

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
    return render_template('listado.html')

@app.route('/estadisticas') 
def estadisticas_page():
    return render_template('estadisticas.html')

@app.route('/procesar_actividad', methods=['POST'])
def procesar_nueva_actividad():
    print("--- DENTRO DE procesar_nueva_actividad ---") 
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

    if not errores_servidor: 
            print("Procesando archivos")
            
            archivos_subidos = request.files.getlist('fotos_actividad[]')
            
            archivos_validos_para_guardar = []

            if not archivos_subidos or all(not f.filename for f in archivos_subidos): # Si no se envió ningún archivo o todos están vacíos
                errores_servidor.append("Debes subir al menos 1 foto.")
            else:
                num_archivos_reales = 0
                for file_storage in archivos_subidos:
                    if file_storage and file_storage.filename: 
                        num_archivos_reales += 1
                        if allowed_file(file_storage.filename):
                            archivos_validos_para_guardar.append(file_storage)
                        else:
                            errores_servidor.append(f"El archivo '{file_storage.filename}' tiene una extensión no permitida. Solo se permiten: {', '.join(ALLOWED_EXTENSIONS)}.")
                
                if num_archivos_reales < 1: 
                    if not any("Debes subir al menos 1 foto" in err for err in errores_servidor): 
                        errores_servidor.append("Debes subir al menos 1 foto.")
                elif num_archivos_reales > 5: 
                    errores_servidor.append("Puedes subir un máximo de 5 fotos.")
            
            if not errores_servidor and archivos_validos_para_guardar:
                for file_storage in archivos_validos_para_guardar:
                    filename_seguro = secure_filename(file_storage.filename) 
                    filename_seguro = datetime.now().strftime("%Y%m%d%H%M%S%f_") + filename_seguro
                    
                    ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], filename_seguro)
                    try:
                        file_storage.save(ruta_guardado)
                        nombres_archivos_guardados.append(filename_seguro) 
                        print(f"Archivo '{filename_seguro}' guardado en '{ruta_guardado}'")
                    except Exception as e:
                        print(f"Error al guardar el archivo {filename_seguro}: {e}")
                        errores_servidor.append(f"Hubo un problema al guardar el archivo: {filename_seguro}.")
            
    # --- FIN DE VALIDACIONES (POR AHORA) ---


    if errores_servidor:
        flash('Por favor, corrige los errores indicados en el formulario.', 'danger') 
        return render_template('agregar.html', 
                               errores_servidor=errores_servidor, 
                               datos_previos=datos_previos)                                                                     
    else:
        flash('¡Actividad recibida y validada (campos actuales) por el servidor! (Aún no guardada en BD)', 'success')
        return redirect(url_for('home')) 


if __name__ == "__main__":
    crear_tablas_bd()
    app.run(debug = True)