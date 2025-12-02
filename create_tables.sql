-- Таблица игроков
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(10),
    gaming_experience VARCHAR(20)
);

-- Таблица игровых сессий
CREATE TABLE game_sessions (
    session_id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(player_id),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    game_version VARCHAR(10)
);

-- Таблица игровых событий
CREATE TABLE game_events (
    event_id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES game_sessions(session_id),
    event_type VARCHAR(50),
    timestamp TIMESTAMP,
    parameters JSONB
);