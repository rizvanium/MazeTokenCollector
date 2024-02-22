DROP TABLE IF EXISTS setting;
DROP TABLE IF EXISTS solution;
DROP TABLE IF EXISTS maze;

CREATE TABLE maze (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE setting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maze_id INTEGER NOT NULL,
    brush_type TEXT NOT NULL,
    grid_size INTEGER NOT NULL,
    population_size INTEGER NOT NULL,
    generation_size INTEGER NOT NULL,
    FOREIGN KEY (maze_id) REFERENCES maze (id)
);

CREATE TABLE solution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maze_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    FOREIGN KEY (maze_id) REFERENCES maze (id)
);
