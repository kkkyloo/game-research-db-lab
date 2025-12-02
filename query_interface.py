import psycopg2
import pandas as pd

def create_connection():
    """Создает и возвращает соединение с базой данных."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="game_research",
            user="postgres",
            password="postgres" 
        )
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

def execute_query(query):
    """Выполняет SQL-запрос и возвращает результат в виде DataFrame."""
    conn = create_connection()
    if conn:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    return pd.DataFrame() # Возвращаем пустой DataFrame в случае ошибки