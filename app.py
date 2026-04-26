# ============================================================
#  app.py  —  Sistem Pakar Konsentrasi Informatika
#  Backend: Flask + Forward Chaining Engine (Python)
#  Jalankan : python app.py
#  API      : POST /api/infer  →  { "facts": [...] }
# ============================================================

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # izinkan request dari frontend (HTML yang dibuka via file:// atau port berbeda)


# ════════════════════════════════════════════════════════════
#  1.  KNOWLEDGE BASE — RULES
#  Setiap rule: kondisi (list fakta) + bobot + konsentrasi
# ════════════════════════════════════════════════════════════

RULES = [
    # ── Software Engineering ─────────────────────────────
    {"conditions": ["suka_logika_pemrograman"],                              "weight": 3, "conclusion": "SE"},
    {"conditions": ["lebih_suka_coding_dari_desain"],                        "weight": 3, "conclusion": "SE"},
    {"conditions": ["tertarik_arsitektur_sistem"],                           "weight": 4, "conclusion": "SE"},
    {"conditions": ["suka_logika_pemrograman", "tertarik_arsitektur_sistem"],"weight": 5, "conclusion": "SE"},

    # ── Data Science / AI ────────────────────────────────
    {"conditions": ["suka_matematika_statistika"],                           "weight": 3, "conclusion": "DS"},
    {"conditions": ["tertarik_pengolahan_data"],                             "weight": 3, "conclusion": "DS"},
    {"conditions": ["ingin_belajar_ml"],                                     "weight": 4, "conclusion": "DS"},
    {"conditions": ["suka_matematika_statistika", "ingin_belajar_ml"],       "weight": 5, "conclusion": "DS"},
    {"conditions": ["tertarik_pengolahan_data", "ingin_belajar_ml"],         "weight": 5, "conclusion": "DS"},

    # ── Jaringan & Cyber Security ────────────────────────
    {"conditions": ["suka_hardware_jaringan"],                               "weight": 3, "conclusion": "NET"},
    {"conditions": ["tertarik_keamanan_siber"],                              "weight": 4, "conclusion": "NET"},
    {"conditions": ["lebih_suka_infra_dari_aplikasi"],                       "weight": 3, "conclusion": "NET"},
    {"conditions": ["suka_hardware_jaringan", "tertarik_keamanan_siber"],    "weight": 5, "conclusion": "NET"},

    # ── Multimedia & UI/UX ───────────────────────────────
    {"conditions": ["suka_desain_visual"],                                   "weight": 3, "conclusion": "MM"},
    {"conditions": ["peduli_ux"],                                            "weight": 4, "conclusion": "MM"},
    {"conditions": ["tertarik_multimedia_game"],                             "weight": 3, "conclusion": "MM"},
    {"conditions": ["suka_desain_visual", "peduli_ux"],                      "weight": 5, "conclusion": "MM"},
    {"conditions": ["peduli_ux", "tertarik_multimedia_game"],                "weight": 4, "conclusion": "MM"},
]


# ════════════════════════════════════════════════════════════
#  2.  CONCENTRATION METADATA
# ════════════════════════════════════════════════════════════

CONCENTRATIONS = {
    "SE": {
        "label": "Software Engineering",
        "color": "#3fb950",
        "badgeBg": "rgba(63,185,80,.12)",
        "badgeBorder": "rgba(63,185,80,.35)",
        "icon": "⚙️",
        "description": (
            "Kamu adalah seorang pembangun sistem. Kamu berpikir dalam struktur, "
            "arsitektur, dan efisiensi. Software Engineering adalah tempatmu berkembang — "
            "merancang aplikasi yang skalabel, menulis kode yang bersih, dan memodelkan "
            "sistem yang kompleks menjadi solusi elegan."
        ),
        "reasons": [
            "Kamu menikmati proses berpikir logis & algoritmik.",
            "Arsitektur sistem (API, database, microservices) menarik minatmu.",
            "Kamu lebih suka coding logika backend daripada aspek desain.",
            "Pemecahan masalah teknis memberimu kepuasan.",
        ],
        "courses": [
            "Algoritma & Struktur Data", "Rekayasa Perangkat Lunak",
            "Pemrograman Berorientasi Objek", "Arsitektur Sistem",
            "Pemrograman Web Lanjut", "DevOps & CI/CD",
            "Database System", "Design Patterns",
        ],
        "maxWeight": 15,
    },
    "DS": {
        "label": "Data Science / AI",
        "color": "#58a6ff",
        "badgeBg": "rgba(88,166,255,.12)",
        "badgeBorder": "rgba(88,166,255,.35)",
        "icon": "🤖",
        "description": (
            "Kamu adalah seorang penjelajah data dan pembangun kecerdasan. "
            "Dengan fondasi matematika yang kuat dan rasa ingin tahu terhadap data, "
            "kamu siap mengeksplorasi Machine Learning, membangun model prediktif, "
            "dan menciptakan sistem AI yang memecahkan masalah nyata."
        ),
        "reasons": [
            "Matematika dan statistika adalah kekuatan utamamu.",
            "Kamu senang menggali pola tersembunyi dalam data besar.",
            "Machine Learning dan cara kerja AI sangat menarik bagimu.",
            "Kamu berpikir secara analitis dan berbasis data.",
        ],
        "courses": [
            "Statistika & Probabilitas", "Machine Learning", "Deep Learning",
            "Pengolahan Data (Pandas/NumPy)", "Visualisasi Data",
            "Natural Language Processing", "Computer Vision", "Big Data Analytics",
        ],
        "maxWeight": 17,
    },
    "NET": {
        "label": "Jaringan & Cyber Security",
        "color": "#e3b341",
        "badgeBg": "rgba(227,179,65,.12)",
        "badgeBorder": "rgba(227,179,65,.35)",
        "icon": "🛡️",
        "description": (
            "Kamu adalah penjaga benteng digital. Dengan ketertarikan pada infrastruktur "
            "jaringan dan hasrat untuk melindungi sistem dari ancaman, kamu cocok menjadi "
            "security engineer, network architect, atau ethical hacker yang dibutuhkan "
            "di era keamanan siber ini."
        ),
        "reasons": [
            "Kamu suka mengkonfigurasi dan memahami perangkat jaringan.",
            "Keamanan sistem dan ethical hacking membuatmu penasaran.",
            "Mengelola infrastruktur lebih menarik bagimu daripada membuat aplikasi.",
            "Kamu suka memahami cara kerja sistem di level rendah.",
        ],
        "courses": [
            "Jaringan Komputer", "Keamanan Informasi",
            "Ethical Hacking & Penetration Testing", "Kriptografi",
            "Linux & Server Administration", "Forensik Digital",
            "Cloud Security", "Protokol Jaringan",
        ],
        "maxWeight": 12,
    },
    "MM": {
        "label": "Multimedia & UI/UX",
        "color": "#bc8cff",
        "badgeBg": "rgba(188,140,255,.12)",
        "badgeBorder": "rgba(188,140,255,.35)",
        "icon": "🎨",
        "description": (
            "Kamu adalah kreator pengalaman digital. Kepedulianmu pada estetika, "
            "empati terhadap pengguna, dan minat pada aset visual menjadikanmu calon "
            "UI/UX designer, creative developer, atau game developer yang mampu "
            "menggabungkan seni dan teknologi."
        ),
        "reasons": [
            "Desain visual dan estetika antarmuka adalah passionmu.",
            "Kamu sangat peduli pada pengalaman dan kenyamanan pengguna (UX).",
            "Pembuatan aset digital, animasi, atau game menarik minatmu.",
            "Kamu berpikir dari sudut pandang manusia, bukan hanya mesin.",
        ],
        "courses": [
            "Desain Interaksi (UI/UX)", "Grafika Komputer", "Animasi Digital",
            "Human-Computer Interaction", "Game Development", "Design Thinking",
            "Figma & Prototyping", "Motion Design",
        ],
        "maxWeight": 16,
    },
}


# ════════════════════════════════════════════════════════════
#  3.  FORWARD CHAINING ENGINE
# ════════════════════════════════════════════════════════════

def forward_chaining(facts: list[str]) -> dict:
    """
    Jalankan Forward Chaining:
      - facts   : list fakta yang dikumpulkan dari jawaban user
      - return  : dict berisi skor per konsentrasi + rules yang aktif
    """
    fact_set    = set(facts)
    scores      = {key: 0 for key in CONCENTRATIONS}
    fired_rules = []

    for rule in RULES:
        # Cek apakah SEMUA kondisi rule terpenuhi
        if all(cond in fact_set for cond in rule["conditions"]):
            scores[rule["conclusion"]] += rule["weight"]
            fired_rules.append(rule)

    return {"scores": scores, "fired_rules": fired_rules}


# ════════════════════════════════════════════════════════════
#  4.  API ENDPOINTS
# ════════════════════════════════════════════════════════════

@app.route("/api/infer", methods=["POST"])
def infer():
    """
    Endpoint utama inferensi.
    Request body (JSON):
      { "facts": ["suka_logika_pemrograman", "tertarik_arsitektur_sistem", ...] }
    Response (JSON):
      {
        "winner": "SE",
        "scores": { "SE": 12, "DS": 0, "NET": 0, "MM": 0 },
        "score_pct": { "SE": 80, ... },
        "fired_rules": [...],
        "concentrations": { ... }   ← metadata semua konsentrasi
      }
    """
    body  = request.get_json(silent=True) or {}
    facts = body.get("facts", [])

    if not isinstance(facts, list):
        return jsonify({"error": "Field 'facts' harus berupa array string."}), 400

    result      = forward_chaining(facts)
    scores      = result["scores"]
    fired_rules = result["fired_rules"]

    # Tentukan pemenang (skor tertinggi)
    winner = max(scores, key=lambda k: scores[k])

    # Hitung persentase kesesuaian
    score_pct = {
        key: round((scores[key] / CONCENTRATIONS[key]["maxWeight"]) * 100)
        for key in scores
    }

    return jsonify({
        "winner":        winner,
        "scores":        scores,
        "score_pct":     score_pct,
        "fired_rules":   fired_rules,
        "concentrations": CONCENTRATIONS,
    })


@app.route("/api/questions", methods=["GET"])
def get_questions():
    """
    Opsional: endpoint untuk mengambil daftar pertanyaan
    agar frontend tidak perlu hard-code pertanyaan.
    """
    questions = [
        {"id": "q1",  "category": "Logika & Pemrograman",  "text": "Aku suka memecahkan masalah dengan logika pemrograman dan algoritma.",                         "hint": "Misalnya: debugging kode, menyusun alur program, atau berpikir secara terstruktur.", "facts": ["suka_logika_pemrograman"]},
        {"id": "q2",  "category": "Logika & Pemrograman",  "text": "Aku lebih menikmati ngoding suatu fitur daripada mendesain tampilannya.",                      "hint": "Backend logic, business rules, atau struktur data lebih menarik bagimu.",           "facts": ["lebih_suka_coding_dari_desain"]},
        {"id": "q3",  "category": "Arsitektur Sistem",      "text": "Aku tertarik merancang arsitektur aplikasi skala besar (microservices, API, database schema).", "hint": "Memikirkan bagaimana komponen sistem saling terhubung secara efisien.",              "facts": ["tertarik_arsitektur_sistem"]},
        {"id": "q4",  "category": "Matematika & Statistika","text": "Matematika dan statistika adalah mata pelajaran yang aku sukai dan kuasai.",                   "hint": "Kalkulus, probabilitas, aljabar linear, atau statistika deskriptif.",               "facts": ["suka_matematika_statistika"]},
        {"id": "q5",  "category": "Pengolahan Data",        "text": "Aku senang mengeksplorasi data besar untuk menemukan pola atau wawasan tersembunyi.",          "hint": "Analisis dataset, visualisasi data, atau eksplorasi tren dalam data.",              "facts": ["tertarik_pengolahan_data"]},
        {"id": "q6",  "category": "Kecerdasan Buatan",      "text": "Aku ingin memahami cara kerja Machine Learning dan bagaimana mesin bisa 'belajar'.",           "hint": "Neural network, model prediktif, NLP, computer vision, dll.",                      "facts": ["ingin_belajar_ml"]},
        {"id": "q7",  "category": "Jaringan Komputer",      "text": "Aku suka utak-atik perangkat jaringan seperti router, switch, atau konfigurasi server.",        "hint": "Pengaturan IP, VLAN, firewall, atau topologi jaringan.",                           "facts": ["suka_hardware_jaringan"]},
        {"id": "q8",  "category": "Keamanan Siber",         "text": "Aku tertarik pada keamanan sistem — menemukan celah (ethical hacking) atau melindungi server.", "hint": "Vulnerability assessment, penetration testing, kriptografi, atau hardening sistem.", "facts": ["tertarik_keamanan_siber"]},
        {"id": "q9",  "category": "Keamanan Siber",         "text": "Aku lebih memilih mengkonfigurasi dan memantau infrastruktur daripada membuat aplikasi.",       "hint": "Sysadmin, network monitoring, atau DevOps infrastructure lebih menarik bagimu.",   "facts": ["lebih_suka_infra_dari_aplikasi"]},
        {"id": "q10", "category": "Desain Visual",          "text": "Aku menyukai desain visual — komposisi, tipografi, warna, dan estetika antarmuka.",             "hint": "Membuat mockup, memilih palet warna, atau menata layout yang enak dipandang.",     "facts": ["suka_desain_visual"]},
        {"id": "q11", "category": "Pengalaman Pengguna",    "text": "Bagi aku, pengalaman pengguna (UX) adalah inti dari sebuah produk digital yang baik.",         "hint": "User research, wireframing, usability testing, atau interaction design.",          "facts": ["peduli_ux"]},
        {"id": "q12", "category": "Multimedia & Game",      "text": "Aku tertarik membuat aset digital seperti animasi, ilustrasi, atau bahkan game.",               "hint": "Motion graphics, 3D modeling, game development, atau digital art.",                "facts": ["tertarik_multimedia_game"]},
    ]
    return jsonify(questions)


@app.route("/", methods=["GET"])
def index():
    return send_file("index.html")


# ════════════════════════════════════════════════════════════
#  5.  RUN
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 55)
    print("  Sistem Pakar - Konsentrasi Informatika")
    print("  Backend Flask  |  Forward Chaining Engine")
    print("=" * 55)
    print("  API berjalan di  ->  http://localhost:5001")
    print("  Buka index.html di browser untuk tampilan UI")
    print("=" * 55)
    app.run(debug=True, port=5001)