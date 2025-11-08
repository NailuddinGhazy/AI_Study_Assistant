# streamlit_chat_app.py
"""
AI Study Assistant (Streamlit) — versi akhir rapi
Sekarang database dikelola lewat file terpisah: study_db_tools.py
"""

import streamlit as st
import json
import re
from google import genai  # gunakan library google-genai
from study_db_tools import init_db, save_chat, get_recent_chats, save_quiz  # <- pakai file eksternal
from datetime import datetime

# -----------------------
# --- Helper Functions ---
# -----------------------

def extract_json_from_text(text: str):
    """Try to extract a JSON object from a model output."""
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, flags=re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


# -----------------------
# --- Streamlit UI ------
# -----------------------

st.set_page_config(page_title="EduBot — AI Study Assistant", page_icon="🎓", layout="centered")
st.title("🎓 EduBot — AI Study Assistant")
st.caption("Asisten belajar: jelaskan konsep, ringkas teks, dan buat soal latihan. (Gunakan Google AI API Key)")

# Sidebar settings
with st.sidebar:
    st.subheader("Pengaturan")
    google_api_key = st.text_input("Google AI API Key", type="password", help="Masukkan API Key Google (Gemini)")
    model_choice = st.selectbox("Model", ["gemini-2.5-flash", "gemini-1.5-pro"], index=0)
    st.markdown("---")
    st.markdown("Mode: pilih **Chat** untuk percakapan, **Ringkasan** untuk meringkas teks, atau **Generate Quiz** untuk membuat soal.")
    if st.button("Hapus riwayat lokal"):
        import sqlite3
        conn = sqlite3.connect("study_assistant.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM chat_history")
        cur.execute("DELETE FROM quiz_history")
        conn.commit()
        conn.close()
        st.success("✅ Riwayat lokal dihapus.")

# Pastikan API key diisi
if not google_api_key:
    st.info("Masukkan Google AI API Key di sidebar untuk mulai.", icon="🗝️")
    st.stop()

# --- Inisialisasi Google AI client ---
if ("genai_client" not in st.session_state) or (st.session_state.get("_last_key") != google_api_key):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state._last_key = google_api_key
        st.session_state.pop("chat_obj", None)
        st.session_state.pop("messages", None)
    except Exception as e:
        st.error("Gagal inisialisasi Google AI Client: " + str(e))
        st.stop()

client = st.session_state.genai_client

# --- Inisialisasi DB dan pesan ---
init_db()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Tampilkan riwayat lokal ---
with st.expander("🕓 Riwayat percakapan (lokal)"):
    rows = get_recent_chats(10)
    if rows:
        for r in rows:
            ts = r.get("created_at")
            st.markdown(f"**[{ts}] User:** {r['user_message']}")
            st.markdown(f"**Bot:** {r['bot_reply']}")
            st.markdown("---")
    else:
        st.write("Belum ada riwayat tersimpan.")

# --- Pilih mode utama ---
mode = st.radio("Pilih mode:", ["Chat", "Ringkasan", "Generate Quiz"], horizontal=True)


# -----------------------
# --- Fungsi Prompt ---
# -----------------------
def build_system_prompt(mode_selected: str):
    if mode_selected == "Chat":
        return "Kamu adalah asisten belajar santai, jelas, dan membantu mahasiswa Sistem Informasi. Jawaban ringkas jika diminta singkat."
    if mode_selected == "Ringkasan":
        return "Kamu membantu merangkum teks: buat ringkasan 3–6 kalimat dan berikan satu saran referensi tambahan."
    if mode_selected == "Generate Quiz":
        return "Buat kuis pilihan ganda (4 opsi) dengan kunci jawaban dan pembahasan singkat. Keluarkan dalam format JSON."


# -----------------------
# --- Mode CHAT ---
# -----------------------
if mode == "Chat":
    st.write("Mode: Chat — tanyakan konsep, minta contoh, atau langkah penyelesaian soal.")
    prompt = st.chat_input("Tulis pertanyaanmu...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            system_msg = build_system_prompt("Chat")
            if "chat_obj" not in st.session_state:
                st.session_state.chat_obj = client.chats.create(model=model_choice)
            response = client.models.generate_content(
                model=model_choice,
                contents=f"{system_msg}\n\nUser: {prompt}"
            )
            answer = response.text


            answer = response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            answer = f"Terjadi error saat memanggil API: {e}"

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        save_chat(prompt, answer, mode="chat")


# -----------------------
# --- Mode RINGKASAN ---
# -----------------------
elif mode == "Ringkasan":
    st.write("Mode: Ringkasan — tempel teks yang ingin kamu ringkas.")
    text = st.text_area("Tempel teks di sini (maks ~2000 kata):", height=300)
    if st.button("Ringkas"):
        if not text.strip():
            st.warning("Masukkan teks terlebih dahulu.")
        else:
            try:
                system_msg = build_system_prompt("Ringkasan")
                chat = client.chats.create(model=model_choice)
                response = client.models.generate_content(
                    model=model_choice,
                    contents=f"{system_msg}\n\nRingkas teks berikut menjadi 3–6 kalimat dan beri 1 saran referensi:\n\n{text}"
                )
                summary = response.text


                summary = response.text if hasattr(response, "text") else str(response)
            except Exception as e:
                summary = f"Terjadi error: {e}"

            st.subheader("📘 Ringkasan")
            st.write(summary)
            save_chat(text[:1000], summary, mode="summary")


# -----------------------
# --- Mode GENERATE QUIZ ---
# -----------------------
elif mode == "Generate Quiz":
    st.write("Mode: Generate Quiz — buat soal latihan otomatis dari topik.")
    topic = st.text_input("Topik (contoh: Normalisasi database):")
    num_q = st.number_input("Jumlah soal", min_value=1, max_value=10, value=5)

    if st.button("Buat Kuis"):
        if not topic.strip():
            st.warning("Isi topik terlebih dahulu.")
        else:
            try:
                system_msg = build_system_prompt("Generate Quiz")
                prompt = (
                    f"Buat {num_q} soal pilihan ganda (4 opsi) disertai kunci jawaban dan pembahasan singkat. "
                    f"Topik: {topic}. Keluarkan dalam format JSON: "
                    '{"quiz": [{"question": "...", "options": ["a","b","c","d"], "answer": "b", "explanation": "..."}]}'
                )
                response = client.models.generate_content(
                    model=model_choice,
                    contents=f"{system_msg}\n\n{prompt}"
                )
                raw = response.text


                raw = response.text if hasattr(response, "text") else str(response)
                parsed = extract_json_from_text(raw)
                quiz_json = parsed or {"error": "Gagal parse JSON dari model.", "raw": raw}
            except Exception as e:
                quiz_json = {"error": str(e)}

            st.subheader("🧩 Hasil Kuis")
            st.json(quiz_json)
            save_quiz(topic, json.dumps(quiz_json, ensure_ascii=False))

# -----------------------
# --- Footer ---
# -----------------------
st.markdown("---")
st.markdown("💡 *Versi modifikasi untuk Final Project — EduBot (AI Study Assistant)*")
