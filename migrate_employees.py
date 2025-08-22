"""
Script para migrar la tabla employees añadiendo las nuevas columnas
"""
from app import app, db
from sqlalchemy import text

def migrate_employees_table():
    with app.app_context():
        try:
            # Verificar si las columnas ya existen
            result = db.session.execute(text("PRAGMA table_info(employees)"))
            columns = [row[1] for row in result.fetchall()]
            
            print(f"Columnas actuales en employees: {columns}")
            
            # Añadir columnas faltantes una por una
            columns_to_add = [
                ("telefono", "VARCHAR(20)"),
                ("fecha_ingreso", "VARCHAR(20)"),
                ("especialidades", "TEXT"),
                ("notas", "TEXT")
            ]
            
            for column_name, column_type in columns_to_add:
                if column_name not in columns:
                    try:
                        sql_query = f"ALTER TABLE employees ADD COLUMN {column_name} {column_type}"
                        db.session.execute(text(sql_query))
                        print(f"✅ Añadida columna: {column_name}")
                    except Exception as e:
                        print(f"❌ Error añadiendo {column_name}: {e}")
                else:
                    print(f"⚠️ Columna {column_name} ya existe")
            
            db.session.commit()
            print("✅ Migración completada")
            
        except Exception as e:
            print(f"❌ Error en migración: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_employees_table()