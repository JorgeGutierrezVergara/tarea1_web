import subprocess
import os

DB_USER = "cc5002"
DB_PASS = "programacionweb"
DB_NAME = "tarea2" 

SQL_DIR = os.path.join(os.path.dirname(__file__), 'database') 

sql_scripts = [
    "tarea2.sql",
    "region-comuna.sql", 
    "tabla-comentario.sql",
    "actividades.sql"
]

def run_sql_script(script_path, user, password, db_name):
    print(f"Ejecutando {script_path}...")
    try:
        command = [
            "mysql",
            f"-u{user}",
            f"-p{password}", 
            db_name,
            "--default-character-set=utf8mb4"
        ]
       
        with open(script_path, 'r', encoding='utf-8') as f: # <-- AÑADIDO: encoding='utf-8'
            process = subprocess.run(command, stdin=f, capture_output=True, text=True, check=True)
        
        if process.stdout:
            print(f"Salida de {script_path}:\n{process.stdout}")
        if process.stderr:
            print(f"Errores de {script_path}:\n{process.stderr}")
        
        print(f"Script {script_path} ejecutado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"¡ERROR al ejecutar {script_path}!")
        print(f"Código de salida: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        exit(1) # Salir si un script falla
    except FileNotFoundError:
        print(f"Error: El comando 'mysql' no se encontró. Asegúrate de que MySQL CLI esté en tu PATH.")
        exit(1)

if __name__ == "__main__":
    print("Iniciando ejecución de scripts SQL...")
    for script_name in sql_scripts:
        script_full_path = os.path.join(SQL_DIR, script_name)
        if not os.path.exists(script_full_path):
            print(f"Error: El archivo {script_full_path} no se encontró. Saltando.")
            continue
        run_sql_script(script_full_path, DB_USER, DB_PASS, DB_NAME)
    print("Todos los scripts han sido procesados.")