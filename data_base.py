import sqlite3
import json
from gramm_tests import test_presens_question, test_preteritum_question

# path to JSON 
json_file_path = r'C:\Users\tr211\Documents\learnBook\word_json.json'

# path to data base SQLite
db_file_path = r'C:\Users\tr211\Documents\learnBook\norwegian_language.db'

def load_verb_forms_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Ошибка при чтении JSON файла: {e}")
        return {}

def insert_verb_forms_to_db(db_path, verb_forms):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Clear table if exist
        cursor.execute('DROP TABLE IF EXISTS verb_forms')
        
        # Create table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS verb_forms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            verb TEXT UNIQUE,
            Presens TEXT,
            Preteritum TEXT,
            "Pres. perfektum" TEXT,
            english TEXT
        )
        ''')
        
        # Insert data
        for verb, forms in verb_forms.items():
            # Right value "Pres. perfektum"
            pres_perfektum = forms.get("Pres. perfektum") or forms.get("Pres. perfektum ")

            cursor.execute('''
            INSERT INTO verb_forms (verb, Presens, Preteritum, "Pres. perfektum", english)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                verb,
                forms.get("Presens"),
                forms.get("Preteritum"),
                pres_perfektum,
                ', '.join(forms.get("english", []))  # Eng value in str
            ))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")

# Create and connect
try:
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Update if exisi
    cursor.execute('DROP TABLE IF EXISTS themes')
    cursor.execute('DROP TABLE IF EXISTS texts')
    cursor.execute('DROP TABLE IF EXISTS tests')

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS themes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme_id INTEGER,
        content TEXT,
        FOREIGN KEY (theme_id) REFERENCES themes (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        correct_answer TEXT,
        options TEXT,
        test_type TEXT,
        theme_id INTEGER,
        FOREIGN KEY (theme_id) REFERENCES themes (id)
    )
    ''')

    # Insert tests
    cursor.executemany(
        'INSERT INTO tests (question, correct_answer, options, test_type, theme_id) VALUES (?, ?, ?, ?, ?)',
        test_presens_question
    )
    cursor.executemany(
        'INSERT INTO tests (question, correct_answer, options, test_type, theme_id) VALUES (?, ?, ?, ?, ?)',
        test_preteritum_question
    )
    
    conn.commit()
except sqlite3.Error as e:
    print(f"Ошибка при работе с базой данных: {e}")
finally:
    conn.close()

# Add from ... to data base
verb_forms = load_verb_forms_from_json(json_file_path)
insert_verb_forms_to_db(db_file_path, verb_forms)

print(f"Succeful addet '{db_file_path}'.")
