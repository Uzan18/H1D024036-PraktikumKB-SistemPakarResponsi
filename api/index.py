import os
from flask import Flask, request, jsonify, render_template

# Set template folder path to be relative to this file agar aman saat di-deploy ke Vercel Serverless
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)

# ==========================================
# --- INFERENCE ENGINE (FORWARD CHAINING) ---
# ==========================================
# Logika Forward Chaining: 
# Sistem menerima "Fakta" (dari jawaban 'Ya' oleh user) lalu mencocokkannya 
# dengan "Rules" (Aturan) yang ada di Knowledge Base untuk menarik kesimpulan.

def forward_chaining(facts):
    """
    Menerima list fakta: misal ['suka_ngoding', 'suka_arsitektur']
    Mengembalikan string hasil konsentrasi.
    """
    # R1: Jika Suka Ngoding AND Suka Arsitektur Sistem -> Software Engineering
    if 'suka_ngoding' in facts and 'suka_arsitektur' in facts:
        return "Software Engineering"
    
    # R5: Jika Suka Ngoding AND Suka Matematika -> Data Science (Alternatif)
    if 'suka_ngoding' in facts and 'suka_matematika' in facts:
        return "Data Science"
    
    # R2: Jika Suka Matematika AND Tertarik Pengolahan Data -> Data Science
    if 'suka_matematika' in facts and 'pengolahan_data' in facts:
        return "Data Science"
    
    # R3: Jika Suka Hardware AND Tertarik Keamanan Server -> Cyber Security & Networking
    if 'suka_hardware' in facts and 'keamanan_server' in facts:
        return "Cyber Security & Networking"
    
    # R4: Jika Suka Desain Visual AND Peduli User Experience -> Multimedia & UI/UX
    if 'suka_desain' in facts and 'peduli_ux' in facts:
        return "Multimedia & UI/UX"
    
    # Fallback jika tidak ada rules yang terpenuhi secara sempurna
    return "Belum dapat ditentukan (Silakan eksplorasi minat lebih lanjut)"

# ==========================================
# --- ROUTING (API & WEB) ---
# ==========================================

@app.route('/')
def home():
    # Menampilkan halaman UI
    return render_template('index.html')

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    # Endpoint ini dipanggil oleh Fetch API dari frontend
    data = request.json
    facts = data.get('facts', [])
    
    # Jalankan mesin inferensi
    result = forward_chaining(facts)
    
    return jsonify({
        'status': 'success',
        'result': result
    })

# Untuk testing lokal
if __name__ == '__main__':
    app.run(debug=True, port=5000)
