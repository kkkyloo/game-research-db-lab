import psycopg2
import random
import json
from datetime import datetime, timedelta

# !!! ВАЖНО: Впишите сюда свой пароль, который вы задали при установке PostgreSQL !!!
DB_CONFIG = {
    "host": "localhost",
    "database": "game_research",
    "user": "postgres",
    "password": "postgres"  # Например: "12345" или "postgres"
}

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    return psycopg2.connect(**DB_CONFIG)

def generate_test_data():
    """Основная функция для генерации и вставки данных."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # --- 1. Добавление игроков ---
        print("Generating players...")
        player_ids = []
        for _ in range(20): # Создадим 20 игроков
            age = random.randint(18, 45)
            gender = random.choice(['Male', 'Female'])
            experience = random.choice(['Beginner', 'Intermediate', 'Expert'])
            cur.execute(
                "INSERT INTO players (age, gender, gaming_experience) VALUES (%s, %s, %s) RETURNING player_id;",
                (age, gender, experience)
            )
            player_id = cur.fetchone()[0]
            player_ids.append(player_id)

        # --- 2. Добавление игровых сессий ---
        print("Generating game sessions...")
        session_ids = []
        for player_id in player_ids:
            num_sessions = random.randint(2, 5) # От 2 до 5 сессий на игрока
            for _ in range(num_sessions):
                start_time = datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
                end_time = start_time + timedelta(minutes=random.randint(10, 120))
                game_version = f"v{random.randint(1, 2)}.0"
                cur.execute(
                    "INSERT INTO game_sessions (player_id, start_time, end_time, game_version) VALUES (%s, %s, %s, %s) RETURNING session_id;",
                    (player_id, start_time, end_time, game_version)
                )
                session_id = cur.fetchone()[0]
                session_ids.append(session_id)

        # --- 3. Добавление игровых событий ---
        print("Generating game events...")
        for session_id in session_ids:
            num_events = random.randint(5, 20) # От 5 до 20 событий на сессию
            for _ in range(num_events):
                event_type = "click"
                timestamp = datetime.now() 
                params = {
                    "x": round(random.uniform(-10, 10), 3),
                    "y": round(random.uniform(-10, 10), 3),
                    "reaction_time": round(random.uniform(0.1, 5.0), 3)
                }
                cur.execute(
                    "INSERT INTO game_events (session_id, event_type, timestamp, parameters) VALUES (%s, %s, %s, %s);",
                    (session_id, event_type, timestamp, json.dumps(params))
                )

        # --- Завершение ---
        conn.commit()
        cur.close()
        print("Database populated successfully!")
    except psycopg2.Error as e:
        print(f"Ошибка при работе с PostgreSQL: {e}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    generate_test_data()