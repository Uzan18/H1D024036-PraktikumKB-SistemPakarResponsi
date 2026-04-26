# Sistem Pakar - Penentu Konsentrasi Informatika

Halo! Ini project responsi Praktikum Kecerdasan Buatan aku buat bikin Sistem Pakar. 
Intinya, aplikasi web ini tuh dipake buat ngebantu mahasiswa IT nentuin konsentrasi studi yang pas buat mereka (kayak Software Engineering, Data Science, Jaringan, atau Multimedia/UI UX).

Metode yang dipake di sini adalah **Forward Chaining**.

## Tools yang Dipake
- **Backend:** Python + Flask (buat ngurus logic forward chaining-nya dan nyediain API)
- **Frontend:** HTML biasa + Tailwind CSS (via CDN biar gampang stylingnya) + Vanilla JavaScript buat fetch data ke backend.

## Cara Jalaninnya di Lokal

Gampang banget kok buat nge-run project ini, yang penting udah ada Python di laptop.

1. Buka terminal/cmd terus arahin ke folder project ini.
2. Install dulu library yang dibutuhin pake command:
   ```bash
   pip install -r requirements.txt
   ```
3. Kalo udah beres, tinggal jalanin aja file utamanya:
   ```bash
   python app.py
   ```
4. Kalo ga error, di terminal bakal muncul tulisan running. Tinggal klik aja link-nya atau buka browser terus masuk ke: `http://localhost:5000`

## Cara Kerjanya Gimana?
1. Pas web dibuka, dia bakal nampilin 12 pernyataan seputar minat dan bakat IT.
2. User tinggal pilih "Ya, itu saya" atau "Tidak". Tiap jawaban "Ya" bakal dicatet sebagai **fakta**.
3. Pas udah selesai, kumpulan fakta ini bakal dikirim ke backend Python lewat API (`/api/infer`).
4. Di backend, mesin inferensi (Forward Chaining) bakal nyocokin fakta-fakta tadi sama kumpulan aturan (**Rules**) yang udah aku tulis di `app.py`.
5. Tiap kecocokan bakal dapet poin (bobot). Nah, konsentrasi yang ngumpulin poin paling gede, itu yang bakal keluar jadi hasil rekomendasinya!

Udah sih, kira-kira gitu aja konsep dan cara kerjanya. Semoga paham ya! 🚀
