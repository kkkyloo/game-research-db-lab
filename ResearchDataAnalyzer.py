import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# Импортируем функции из нашего второго файла
from query_interface import create_connection, execute_query

class ResearchDataAnalyzer:
    def __init__(self):
        # Проверяем соединение при инициализации
        self.conn = create_connection()
        if self.conn is None:
            raise Exception("Не удалось установить соединение с базой данных.")
        self.conn.close() # Закрываем соединение, т.к. execute_query будет открывать свое
    
    def analyze_strategy_efficiency(self):
        """Анализ эффективности стратегий"""
        print("\n--- 1. Начинаю анализ эффективности стратегий... ---")
        query = """
        SELECT 
            strategy_type,
            AVG(player_level) as avg_level,
            AVG(simulation_time) as avg_time,
            AVG(decision_making_time) as avg_decision_time
        FROM behavior_metrics bm
        JOIN simulation_results sr ON bm.session_id = sr.session_id
        GROUP BY strategy_type
        """
        
        df = execute_query(query)
        
        if df.empty:
            print("Не удалось получить данные для анализа стратегий. Пропускаю.")
            return None

        # Визуализация
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Комплексный анализ эффективности стратегий', fontsize=16)
        
        sns.barplot(data=df, x='strategy_type', y='avg_level', ax=axes[0,0])
        axes[0,0].set_title('Средний достигнутый уровень по стратегиям')
        
        sns.barplot(data=df, x='strategy_type', y='avg_time', ax=axes[0,1])
        axes[0,1].set_title('Средняя продолжительность сессии')
        
        sns.barplot(data=df, x='strategy_type', y='avg_decision_time', ax=axes[1,0])
        axes[1,0].set_title('Среднее время принятия решений')
        
        numeric_df = df[['avg_level', 'avg_time', 'avg_decision_time']]
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=axes[1,1])
        axes[1,1].set_title('Корреляция метрик')
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig('strategy_analysis.png', dpi=300, bbox_inches='tight')
        print("Графики анализа стратегий сохранены в файл 'strategy_analysis.png'")
        plt.show()
        
        return df
    
    def analyze_player_progression(self, player_id):
        """Анализ прогрессии конкретного игрока"""
        print(f"\n--- 2. Начинаю анализ прогрессии для игрока ID={player_id}... ---")
        query = f"""
        SELECT 
            sr.simulation_timestamp,
            sr.player_level,
            sr.simulation_time,
            bm.strategy_type,
            ge.event_value as resources_gathered
        FROM simulation_results sr
        JOIN game_sessions s ON sr.session_id = s.session_id
        JOIN behavior_metrics bm ON s.session_id = bm.session_id
        LEFT JOIN game_events ge ON s.session_id = ge.session_id 
            AND ge.event_type = 'resource_gather'
        WHERE s.player_id = {player_id}
        ORDER BY sr.simulation_timestamp
        """
        
        df = execute_query(query)
        
        if df.empty:
            print(f"Не найдено данных для игрока ID={player_id}. Пропускаю.")
            return None

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Анализ прогрессии игрока ID={player_id}', fontsize=16)

        axes[0,0].plot(df['simulation_timestamp'], df['player_level'], marker='o', linestyle='-')
        axes[0,0].set_title('Прогресс по уровням во времени')
        axes[0,0].set_xlabel('Дата сессии'); axes[0,0].set_ylabel('Уровень')
        axes[0,0].tick_params(axis='x', rotation=45)

        axes[0,1].plot(df['simulation_timestamp'], df['resources_gathered'].cumsum(), marker='s', linestyle='-')
        axes[0,1].set_title('Накопленные ресурсы (кумулятивно)')
        axes[0,1].set_xlabel('Дата сессии'); axes[0,1].set_ylabel('Ресурсы')
        axes[0,1].tick_params(axis='x', rotation=45)

        axes[1,0].bar(df['simulation_timestamp'], df['simulation_time'], width=0.5)
        axes[1,0].set_title('Продолжительность сессий')
        axes[1,0].set_xlabel('Дата сессии'); axes[1,0].set_ylabel('Секунды')
        axes[1,0].tick_params(axis='x', rotation=45)

        # Более наглядный график смены стратегий
        strategy_colors = {'Aggressive': 'red', 'Balanced': 'blue', 'Defensive': 'green'}
        axes[1,1].scatter(df['simulation_timestamp'], df['strategy_type'], c=df['strategy_type'].map(strategy_colors), s=100)
        axes[1,1].set_title('Используемые стратегии')
        axes[1,1].set_xlabel('Дата сессии'); axes[1,1].set_ylabel('Стратегия')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f'player_{player_id}_progression.png', dpi=300, bbox_inches='tight')
        print(f"Графики прогрессии сохранены в файл 'player_{player_id}_progression.png'")
        plt.show()
        
        return df

# --- ЭТО "КНОПКА ЗАПУСКА", КОТОРОЙ НЕ ХВАТАЛО ---
if __name__ == "__main__":
    print("Запуск анализатора данных...")
    
    # Создаем экземпляр нашего анализатора
    analyzer = ResearchDataAnalyzer()
    
    # Вызываем первый метод анализа
    analyzer.analyze_strategy_efficiency()
    
    # Вызываем второй метод анализа для конкретного игрока.
    # Можете поменять 1 на ID любого другого игрока (от 1 до 10).
    analyzer.analyze_player_progression(player_id=1)
    
    print("\nАнализ завершен.")