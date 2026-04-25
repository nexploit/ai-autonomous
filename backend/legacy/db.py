import sqlite3

conn = sqlite3.connect("memory.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS memory (role TEXT, content TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS tasks (task TEXT, status TEXT)")
conn.commit()

def save(role, content):
    cur.execute("INSERT INTO memory VALUES (?,?)", (role, content))
    conn.commit()

def load(limit=20):
    rows = cur.execute("SELECT role, content FROM memory").fetchall()
    return [{"role": r[0], "content": r[1]} for r in rows[-limit:]]

def add_task(task):
    cur.execute("INSERT INTO tasks VALUES (?,?)", (task, "open"))
    conn.commit()

def get_tasks():
    return cur.execute("SELECT rowid, task FROM tasks WHERE status='open'").fetchall()

def close_task(task_id):
    cur.execute("UPDATE tasks SET status='done' WHERE rowid=?", (task_id,))
    conn.commit()