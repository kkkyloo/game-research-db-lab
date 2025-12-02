import pandas as pd
import random
from datetime import datetime, timedelta

def generate_source_csv(filename='simulation_results.csv', num_records=100):
    """Генерирует исходный CSV-файл с результатами симуляции."""
    data = []
    player_ids = list(range(1, 11))  # 10 игроков
    session_id_counter = 1

    for _ in range(num_records):
        strategy = random.choice(['Aggressive', 'Balanced', 'Defensive'])
        
        # В зависимости от стратегии меняются некоторые параметры
        if strategy == 'Aggressive':
            enemies = random.randint(10, 20)
            resources = random.randint(1, 5)
            sim_time = random.uniform(300, 600)
            level = random.randint(5, 10)
        elif strategy == 'Balanced':
            enemies = random.randint(5, 10)
            resources = random.randint(5, 10)
            sim_time = random.uniform(600, 900)
            level = random.randint(3, 8)
        else: # Defensive
            enemies = random.randint(1, 5)
            resources = random.randint(10, 20)
            sim_time = random.uniform(900, 1200)
            level = random.randint(1, 5)

        record = {
            'player_id': random.choice(player_ids),
            'session_id': session_id_counter,
            'game_version': f"v1.{random.randint(1,3)}",
            'simulation_time': round(sim_time, 2),
            'player_level': level,
            'simulation_timestamp': datetime.now() - timedelta(hours=random.randint(1, 72)),
            'resources_gathered': resources,
            'enemies_defeated': enemies,
            'quests_completed': random.randint(0, 3),
            'decision_making_time': round(random.uniform(1.5, 5.0), 2),
            'strategy_type': strategy
        }
        data.append(record)
        session_id_counter += 1

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Файл '{filename}' с {num_records} записями успешно создан.")

if __name__ == "__main__":
    generate_source_csv()