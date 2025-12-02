-- Удаляем старые таблицы в правильном порядке, чтобы избежать ошибок с внешними ключами
DROP TABLE IF EXISTS behavior_metrics;
DROP TABLE IF EXISTS game_events;
DROP TABLE IF EXISTS simulation_results;
DROP TABLE IF EXISTS game_sessions;
DROP TABLE IF EXISTS players;

-- 1. Таблица Игроки
CREATE TABLE players (
    player_id INT PRIMARY KEY,
    registration_date DATE,
    experience_level VARCHAR(50)
);

-- 2. Таблица Игровые сессии
CREATE TABLE game_sessions (
    session_id INT PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    game_version VARCHAR(10),
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- 3. Таблица Результаты симуляций (основные данные о сессии)
CREATE TABLE simulation_results (
    result_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES game_sessions(session_id),
    simulation_time REAL, -- продолжительность в секундах
    player_level INT,
    simulation_timestamp TIMESTAMP -- время окончания симуляции
);

-- 4. Таблица Игровые события (детализированные действия)
CREATE TABLE game_events (
    event_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES game_sessions(session_id),
    event_type VARCHAR(50), -- 'resource_gather', 'combat', 'quest'
    event_value INT,
    parameters JSONB
);

-- 5. Таблица Поведенческие метрики (стратегия, скорость принятия решений)
CREATE TABLE behavior_metrics (
    metric_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES game_sessions(session_id) UNIQUE, -- Одна запись на сессию
    decision_making_time REAL, -- среднее время на решение в секундах
    strategy_type VARCHAR(50), -- 'Aggressive', 'Balanced', 'Defensive'
    risk_tolerance REAL
);

-- Комментарии для ясности
COMMENT ON TABLE simulation_results IS 'Хранит высокоуровневые результаты каждой симуляции/сессии.';
COMMENT ON TABLE game_events IS 'Детализированный лог событий внутри сессии.';
COMMENT ON TABLE behavior_metrics IS 'Агрегированные поведенческие метрики для каждой сессии.';