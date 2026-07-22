import re

with open('worker/index.js', 'r', encoding='utf-8') as f:
    worker = f.read()

promote_code = """
        if (user.email === 'gabrielfwchaves@gmail.com' && user.role !== 'admin') {
            await env.DB.prepare("UPDATE users SET role = 'admin' WHERE email = ?").bind(user.email).run();
            user.role = 'admin';
        }
"""

worker = worker.replace('return user;', promote_code + '\n        return user;')

with open('worker/index.js', 'w', encoding='utf-8') as f:
    f.write(worker)

print("Added auto-promote for gabrielfwchaves@gmail.com")
