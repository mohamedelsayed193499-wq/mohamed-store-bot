import streamlit as st, sqlite3, os
st.set_page_config(page_title="متجر محمد", layout="wide")
st.title("لوحة تحكم متجر محمد")

conn = sqlite3.connect("posts.db", check_same_thread=False)
posts = conn.execute("SELECT id, text, img FROM posts WHERE status='pending' ORDER BY id DESC").fetchall()

for pid, txt, img in posts:
    st.markdown("---")
    if img and os.path.exists(img): st.image(img, use_column_width=True)
    st.write(txt)
    c1, c2 = st.columns(2)
    if c1.button("موافقة", key=f"a{pid}"):
        conn.execute("UPDATE posts SET status='approved' WHERE id=?", (pid,))
        conn.commit()
        st.rerun()
    if c2.button("رفض", key=f"r{pid}"):
        conn.execute("DELETE FROM posts WHERE id=?", (pid,))
        conn.commit()
        st.rerun()

if not posts: st.success("لا يوجد منشورات في الانتظار")