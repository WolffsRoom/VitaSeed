# VitaSeed

The newest database and catalog for PS Vita and PSTV homebrews, ports, translations, and mods.

## 🚀 Features
- **Modern Catalog:** Explore a visually stunning and fast catalog of PS Vita content.
- **Dynamic Filtering:** Search by category, title, or author instantly.
- **User Requests:** Log in to request new games and ports directly to the database.
- **Role-based Access Control (RBAC):** Admins can manage requests via a secure dashboard.
- **Mobile Friendly:** Fully responsive design that works beautifully on any screen size.

## 🛠️ Architecture & Tech Stack
VitaSeed is built on a modern, serverless architecture for maximum performance and zero maintenance:
- **Frontend:** Vanilla HTML, CSS, and JS. Deployed on Cloudflare Pages.
- **Backend API:** Cloudflare Workers.
- **Database:** Cloudflare D1 (Serverless SQLite).
- **Authentication:** Firebase Auth (Google & GitHub login).
- **Automation:** Integrated with GitHub API to automatically create Issues for approved requests.

## 🔧 Setup & Configuration

### 1. Database (Cloudflare D1)
Initialize the database schemas found in `worker/schema.sql` on your Cloudflare D1 instance. This creates the `requests` and `users` tables.

### 2. Backend (Cloudflare Workers)
Deploy the API found in `worker/index.js`. 
Ensure the following environment variables are set in the Worker:
- `DB`: Your D1 Database binding.
- `GITHUB_TOKEN`: Your GitHub Personal Access Token.
- `GITHUB_REPO`: Your repository in the format `Owner/Repo` (e.g. `WolffsRoom/VitaSeed`).
- `ADMIN_PASSWORD`: A fallback password for the admin dashboard.

### 3. Authentication (Firebase)
1. Set up a Firebase project and enable Authentication (Google and GitHub).
2. Add your domain to the authorized OAuth domains in the Firebase Console.
3. Copy your Firebase config object and paste it into `js/auth.js`.

### 4. Role Management
By default, any logged-in user is a "Viteiro" and can make requests.
To grant someone Admin access to the dashboard, manually add their email to the `users` table in your D1 database with the role `'admin'`:
```sql
INSERT INTO users (email, role) VALUES ('admin@example.com', 'admin');
```

## 📄 License
This project is open-source. Enjoy the Vita scene!
