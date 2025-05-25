CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            contact INTEGER NOT NULL,
            date_posted DATE DATETIME DEFAULT CURRENT_TIMESTAMP
)

