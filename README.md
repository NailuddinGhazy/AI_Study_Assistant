# 🎓 EduBot — AI Study Assistant

Proyek final ini merupakan implementasi chatbot **berbasis AI dan Streamlit** yang berfungsi sebagai asisten belajar interaktif bagi mahasiswa.  
Chatbot ini menggunakan **model Google Gemini (melalui library `google-genai`)** untuk memahami bahasa alami, menjawab pertanyaan, meringkas teks, dan membuat soal otomatis.

---

## 💡 Deskripsi Fitur

| Mode | Fungsi Utama |
|------|---------------|
| 💬 **Chat**           | Menjawab pertanyaan seputar konsep akademik secara ringkas dan jelas. |
| 📘 **Ringkasan**      | Meringkas teks panjang menjadi 3–6 kalimat dengan tambahan saran referensi. |
| 🧩 **Generate Quiz**  | Menghasilkan soal pilihan ganda lengkap dengan kunci jawaban dan pembahasan singkat. |

---

## ⚙️ Teknologi yang Digunakan
- Python 3.10+
- Streamlit
- Google GenAI API (Gemini)
- SQLite (database lokal untuk riwayat chat dan kuis)
- Regex, JSON parser

---

## 📁 Struktur Folder Project

📂 AI_Study_Assistant/
│
├── README.md               # Deskripsi lengkap proyek
├── requirements.txt        # Daftar library yang diperlukan
├── screenshot_1.png        # Tampilan halaman utama aplikasi
├── screenshot_2.png        # Tampilan saat mode Chat atau Ringkasan aktif
├── streamlit_chat_app.py   # File utama Streamlit (UI & logika chatbot)
├── study_assistant.db      # Database lokal (terbentuk otomatis)
└── study_db_tools.py       # Modul database SQLite (fungsi penyimpanan)




## 🚀 Cara Menjalankan Aplikasi

1. **Clone repositori dari GitHub**
   
   ```bash
   git clone https://github.com/<username>/AI_Study_Assistant.git
   cd AI_Study_Assistant
   
2. **Install semua dependensi**
   ```bash
   pip install -r requirements.txt

3. **Jalankan aplikasi Streamlit**
   ```bash
   streamlit run streamlit_chat_app.py

4. Masukkan Google AI API Key di sidebar kiri, lalu pilih mode:
   -💬 Chat
   -📘 Ringkasan
   -🧩 Generate Quiz

5. Masukkan Google AI API Key di sidebar kiri, lalu pilih mode:
   -💬 Chat
   -📘 Ringkasan
   -🧩 Generate Quiz

🧠 Catatan Teknis
Database lokal (study_assistant.db) akan otomatis dibuat saat pertama dijalankan.

Semua riwayat percakapan dan hasil kuis tersimpan secara lokal.

Gaya bahasa chatbot dibuat santai namun edukatif, disesuaikan dengan mahasiswa Sistem Informasi.

## 📸 Cuplikan Tampilan

| Tampilan Utama | Mode Chat |
|----------------|------------|
| ![Screenshot UI](screenshot_1.png) | ![Screenshot Chat](screenshot_2.png) |



👨‍💻 Pengembang
Nama: Nailuddin Ghazy Al Ghifari
Universitas: Universitas Negeri Surabaya (UNESA)
Tahun: 2025

🏁 Status Proyek
✅ Fungsional penuh
✅ Integrasi AI berhasil
✅ Database lokal aktif

✅ Siap diunggah ke GitHub & dikumpulkan sebagai Final Projec
