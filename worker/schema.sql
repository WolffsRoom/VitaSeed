DROP TABLE IF EXISTS requests;
CREATE TABLE requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  link TEXT,
  description TEXT,
  status TEXT DEFAULT 'pending',
  ip_address TEXT,
  user_id TEXT,
  user_name TEXT,
  user_email TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
  email TEXT PRIMARY KEY,
  role TEXT DEFAULT 'viteiro',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

