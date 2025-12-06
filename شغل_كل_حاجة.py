import os, sqlite3, asyncio, time
from telethon import TelegramClient, events

os.makedirs("images", exist_ok=True)

# قاعدة البيانات
conn = sqlite3.connect("posts.db")
conn.execute('''CREATE TABLE IF NOT EXISTS posts 
                (id INTEGER PRIMARY KEY, text TEXT, img TEXT, status TEXT DEFAULT 'pending')''')
conn.commit()

# تعديل النص تلقائي بدون أي مشكلة
# استبدل دالة rewrite القديمة بالكود ده كله
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def rewrite(text):
    if not text or text.strip() == "":
        return "🔥 عرض جديد من متجر محمد 🔥\nتواصل واتساب: 01023257600"

    prompt = f"""أعد كتابة النص ده بطريقة جذابة جدًا وقصيرة وتشد العميل فورًا لمتجر اسمه "محمد"
    خليه يحس إن العرض محدود ويبعت حالا
    في النهاية ضيف:
    تواصل واتساب: 01023257600

    النص الأصلي:
    {text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=250
        )
        new_text = response.choices[0].message.content.strip()
        return new_text + "\n\nتواصل واتساب: 01023257600"
    except:
        return f"💥 عرض نار من متجر محمد 💥\n\n{text.strip()}\n\nتواصل واتساب: 01023257600"
api_id = 30795092
api_hash = "7419fd41d66e1b6dd934702c479ee792"

client = TelegramClient("monitor", api_id, api_hash)

@client.on(events.NewMessage())
async def handler(event):
    if event.is_private: return
    text = event.message.message or ""
    img = None
    if event.photo:
        img = await event.download_media("images/")
    new_text = rewrite(text)
    conn.execute("INSERT INTO posts (text, img) VALUES (?, ?)", (new_text, img or ""))
    conn.commit()
    print("تم سحب منشور جديد")

print("المراقب شغال 100% دلوقتي...")
client.start()
client.run_until_disconnected()