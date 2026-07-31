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

CREATE TABLE IF NOT EXISTS reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id TEXT NOT NULL,
  user_email TEXT NOT NULL,
  user_name TEXT,
  user_avatar TEXT,
  rating INTEGER CHECK(rating >= 1 AND rating <= 5),
  comment TEXT,
  used_ai_tool INTEGER DEFAULT 0,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(post_id, user_email)
);

