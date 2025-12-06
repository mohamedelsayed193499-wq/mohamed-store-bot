from telethon import TelegramClient
import sqlite3, asyncio, time

api_id = 30795092
api_hash = "7419fd41d66e1b6dd934702c479ee792"
target_group = -4933551180

client = TelegramClient("monitor", api_id, api_hash)
conn = sqlite3.connect("posts.db")

async def publish():
    await client.start()
    while True:
        posts = conn.execute("SELECT id, text, img FROM posts WHERE status='approved'").fetchall()
        for pid, txt, img in posts:
            await client.send_message(target_group, txt, file=img if img else None)
            conn.execute("UPDATE posts SET status='published' WHERE id=?", (pid,))
            conn.commit()
            print("تم النشر تلقائي:", pid)
        time.sleep(300)  # كل 5 دقايق

asyncio.run(publish())