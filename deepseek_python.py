import pandas as pd
import psycopg2
import json
from datetime import datetime

# --- ВАШ КЛАСС С ИСПРАВЛЕНИЯМИ ---
class SimulationDataTransformer:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cur = self.conn.cursor()
    
    def load_and_transform_data(self, csv_file_path):
        print(f"Загрузка данных из {csv_file_path}...")
        df = pd.read_csv(csv_file_path)
        print("Данные из CSV успешно загружены.")
        
        print("Начинаю трансформацию и вставку данных в БД...")
        self._extract_players(df)
        self._extract_sessions(df)
        self._extract_simulation_results(df)
        self._extract_game_events(df)
        self._extract_behavior_metrics(df)
        
        print("Сохраняю изменения в БД (commit)...")
        self.conn.commit()
    
    def _extract_players(self, df):
        players_data = df[['player_id']].drop_duplicates()
        for _, row in players_data.iterrows():
            self.cur.execute("""
                INSERT INTO players (player_id, registration_date, experience_level)
                VALUES (%s, %s, %s) ON CONFLICT (player_id) DO NOTHING
            """, (
                int(row['player_id']), # <-- ИСПРАВЛЕНО
                datetime.now().date(), 
                'medium'
            ))
    
    def _extract_sessions(self, df):
        sessions_data = df[['session_id', 'player_id', 'game_version']].drop_duplicates()
        for _, row in sessions_data.iterrows():
            self.cur.execute("""
                INSERT INTO game_sessions (session_id, player_id, game_version, start_time)
                VALUES (%s, %s, %s, %s) ON CONFLICT (session_id) DO NOTHING
            """, (
                int(row['session_id']), # <-- ИСПРАВЛЕНО
                int(row['player_id']),  # <-- ИСПРАВЛЕНО
                row['game_version'], 
                datetime.now()
            ))
    
    def _extract_simulation_results(self, df):
        for _, row in df.iterrows():
            self.cur.execute("""
                INSERT INTO simulation_results 
                (session_id, simulation_time, player_level, simulation_timestamp)
                VALUES (%s, %s, %s, %s)
            """, (
                int(row['session_id']),        # <-- ИСПРАВЛЕНО
                float(row['simulation_time']), # <-- ИСПРАВЛЕНО
                int(row['player_level']),       # <-- ИСПРАВЛЕНО
                row['simulation_timestamp']
            ))
    
    def _extract_game_events(self, df):
        for _, row in df.iterrows():
            self.cur.execute("""
                INSERT INTO game_events (session_id, event_type, event_value, parameters)
                VALUES (%s, %s, %s, %s)
            """, (
                int(row['session_id']),          # <-- ИСПРАВЛЕНО
                'resource_gather', 
                int(row['resources_gathered']), # <-- ИСПРАВЛЕНО
                json.dumps({'auto_gathered': False})
            ))
            self.cur.execute("""
                INSERT INTO game_events (session_id, event_type, event_value, parameters)
                VALUES (%s, %s, %s, %s)
            """, (
                int(row['session_id']),        # <-- ИСПРАВЛЕНО
                'combat', 
                int(row['enemies_defeated']), # <-- ИСПРАВЛЕНО
                json.dumps({'combat_type': 'pve'})
            ))
            self.cur.execute("""
                INSERT INTO game_events (session_id, event_type, event_value, parameters)
                VALUES (%s, %s, %s, %s)
            """, (
                int(row['session_id']),         # <-- ИСПРАВЛЕНО
                'quest', 
                int(row['quests_completed']),  # <-- ИСПРАВЛЕНО
                json.dumps({'quest_type': 'main'})
            ))
    
    def _extract_behavior_metrics(self, df):
        for _, row in df.iterrows():
            self.cur.execute("""
                INSERT INTO behavior_metrics 
                (session_id, decision_making_time, strategy_type)
                VALUES (%s, %s, %s)
            """, (
                int(row['session_id']),             # <-- ИСПРАВЛЕНО
                float(row['decision_making_time']),# <-- ИСПРАВЛЕНО
                row['strategy_type']
            ))

# --- Ниже код без изменений ---
def transform_simulation_data():
    conn = None
    try:
        print("Подключаюсь к базе данных...")
        conn = psycopg2.connect(
            host="localhost",
            database="game_research",
            user="postgres",
            password="postgres"
        )
        print("Подключение успешно.")
        
        transformer = SimulationDataTransformer(conn)
        transformer.load_and_transform_data('simulation_results.csv')
        
        print("Трансформация данных успешно завершена!")

    except psycopg2.Error as e:
        print("--- ОШИБКА БАЗЫ ДАННЫХ ---")
        print(f"Не удалось подключиться к базе данных или выполнить операцию: {e}")
        print("--- Проверьте, что PostgreSQL запущен и ПАРОЛЬ в скрипте ВЕРНЫЙ ---")
    except FileNotFoundError:
        print("--- ОШИБКА: ФАЙЛ НЕ НАЙДЕН ---")
        print("Не удалось найти файл 'simulation_results.csv'.")
        print("--- Убедитесь, что этот файл лежит в той же папке, что и скрипт ---")
    except Exception as e:
        print(f"--- Произошла непредвиденная ошибка: {e} ---")
    finally:
        if conn is not None:
            conn.close()
            print("Соединение с базой данных закрыто.")

if __name__ == "__main__":
    transform_simulation_data()