DROP TABLE IF EXISTS requests;
CREATE TABLE requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  link TEXT,
  description TEXT,
  status TEXT DEFAULT 'pending',
  ip_address TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
