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
  display_name TEXT,
  avatar_url TEXT,
  languages TEXT,
  website TEXT,
  donation_links TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS favorites (
  user_email TEXT,
  post_id TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_email, post_id)
);
