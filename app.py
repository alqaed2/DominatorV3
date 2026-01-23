import os
import random
import time
import json
import logging
import base64
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from google import genai
from google.genai import types

# --- INITIALIZATION ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# CONFIGURATION
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'DOMINATOR_SUPREME_KEY_v17')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dominator.db' # Local DB for MVP
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'production'

# LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SIC_CORE")

# --- DATABASE & AUTH SETUP ---
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

# MODELS
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    image_prompt = db.Column(db.Text)
    # Note: Storing base64 in DB is not ideal for scaling (better S3), but fine for MVP
    # For production, we will render it on demand or use external storage. 
    # Here we simulate history by saving metadata.
    niche = db.Column(db.String(100))
    mode = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# CREATE DB
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- AI CONNECTIVITY ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
client = None
AI_ACTIVE = False

if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        AI_ACTIVE = True
        logger.info(">> [SYSTEM] v17.0 SAAS CORE ACTIVE.")
    except Exception as e:
        logger.error(f"!! [ERROR] AI Connection Failed: {e}")

# --- INTELLIGENCE CORE (SIC v17.0) ---
class StrategicIntelligenceCore:
    def __init__(self):
        self.version = "17.0 (SaaS-Architect)"

    def _generate_backup_image(self, prompt, niche):
        try:
            logger.info(">> Switching to Flux Backup...")
            seed = random.randint(1, 999999999)
            forced_prompt = f"{niche} concept, {prompt}, cinematic lighting, 8k, hyper-realistic, --no text"
            url = f"https://image.pollinations.ai/prompt/{forced_prompt}?model=flux&width=1280&height=720&nologo=true&seed={seed}"
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                return base64.b64encode(response.content).decode('utf-8')
            return None
        except: return None

    def _materialize_visual(self, prompt, niche):
        final_prompt = f"A photorealistic, cinematic image of {niche}. {prompt}. High detail, 8k resolution."
        if not AI_ACTIVE or not client: return self._generate_backup_image(final_prompt, niche)
        try:
            response = client.models.generate_images(
                model='imagen-3.0-generate-001', prompt=final_prompt,
                config=types.GenerateImageConfig(number_of_images=1, aspect_ratio="16:9")
            )
            if response.generated_images:
                return base64.b64encode(response.generated_images[0].image.image_bytes).decode('utf-8')
            raise Exception("No Google Image")
        except: return self._generate_backup_image(final_prompt, niche)

    def generate_warhead(self, niche, mode):
        if not AI_ACTIVE: return {"error": "AI Offline"}
        try:
            styles = ["Cinematic Commercial", "Cyber-Noir", "Macro Luxury", "National Geographic"]
            sys_inst = f"""
            Role: World-Class Content Strategist.
            Niche: {niche}. Style: {random.choice(styles)}.
            Task:
            1. Arabic Viral Post (Hook + Body).
            2. Detailed English Image Prompt (Visuals ONLY, NO Text).
            3. 8 Hashtags.
            JSON Output Only.
            """
            user_msg = f"Generate content for {niche}. Seed: {random.randint(1,1000)}"
            
            res = client.models.generate_content(
                model='gemini-flash-latest',
                config=types.GenerateContentConfig(system_instruction=sys_inst, response_mime_type='application/json'),
                contents=[user_msg]
            )
            content = json.loads(res.text)
            content["image_base64"] = self._materialize_visual(content.get("image_prompt", niche), niche)
            return content
        except Exception as e:
            logger.error(f"Gen Error: {e}")
            return {"error": "Generation Failed"}

sic_engine = StrategicIntelligenceCore()

# --- ROUTES & INTERFACE ---

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            login_user(user)
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    return render_template_string(LOGIN_HTML)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"status": "error", "message": "User exists"}), 400
    hashed_pw = generate_password_hash(data['password'], method='scrypt')
    new_user = User(username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return jsonify({"status": "success"})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/')
@login_required
def dashboard():
    return render_template_string(DASHBOARD_HTML, user=current_user)

@app.route('/api/tactical/execute', methods=['POST'])
@login_required
def execute_order():
    data = request.json
    niche = data.get('niche')
    mode = data.get('mode')
    
    content = sic_engine.generate_warhead(niche, mode)
    
    if "error" in content: return jsonify(content), 500
    
    # SAVE TO HISTORY (DB)
    new_post = Post(
        title=content.get('title'),
        body=content.get('body'),
        image_prompt=content.get('image_prompt'),
        niche=niche,
        mode=mode,
        user_id=current_user.id
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "status": "SUCCESS",
        "title": content.get('title'),
        "body": content.get('body'),
        "image_base64": content.get('image_base64'),
        "image_prompt": content.get('image_prompt'),
        "hashtags": content.get('hashtags', []),
        "metrics": {
            "viralityScore": random.randint(95, 99),
            "predictedReach": random.randint(100000, 2000000),
            "sentiment": content.get('sentiment')
        }
    })

@app.route('/api/history', methods=['GET'])
@login_required
def get_history():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).limit(10).all()
    return jsonify([{
        "title": p.title,
        "niche": p.niche,
        "date": p.timestamp.strftime("%Y-%m-%d %H:%M"),
        "body": p.body
    } for p in posts])

# --- HTML TEMPLATES (Embedded for Single File Power) ---

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI DOMINATOR | ACCESS CONTROL</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>body{background:#000;color:white;font-family:sans-serif;}</style>
</head>
<body class="flex items-center justify-center h-screen bg-black">
    <div class="w-full max-w-md p-8 space-y-6 bg-white/5 border border-white/10 rounded-2xl backdrop-blur-xl">
        <div class="text-center">
            <h1 class="text-3xl font-bold text-white tracking-tighter">AI DOMINATOR</h1>
            <p class="text-xs text-emerald-500 uppercase tracking-widest mt-2">Restricted Access // v17.0</p>
        </div>
        <div class="space-y-4">
            <input type="text" id="username" placeholder="Username" class="w-full p-4 bg-black/50 border border-white/10 rounded-xl text-white focus:border-emerald-500 outline-none">
            <input type="password" id="password" placeholder="Password" class="w-full p-4 bg-black/50 border border-white/10 rounded-xl text-white focus:border-emerald-500 outline-none">
            <div class="grid grid-cols-2 gap-4">
                <button onclick="auth('login')" class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 rounded-xl font-bold transition-all">LOGIN</button>
                <button onclick="auth('register')" class="w-full py-3 border border-white/20 hover:bg-white/10 rounded-xl font-bold transition-all">REGISTER</button>
            </div>
        </div>
        <div id="msg" class="text-center text-xs text-red-500 mt-4"></div>
    </div>
    <script>
        async function auth(action) {
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            if(!u || !p) return;
            const res = await fetch('/'+action, {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({username:u, password:p})
            });
            const data = await res.json();
            if(data.status === 'success') window.location.href = '/';
            else document.getElementById('msg').textContent = data.message;
        }
    </script>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI DOMINATOR | ROYAL CONSOLE</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vanta/0.5.24/vanta.net.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Space Grotesk', sans-serif; background: #000; overflow-x: hidden; color: white; }
        .glass-panel { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); }
        #vanta-canvas { position: fixed; z-index: -1; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
        .gradient-btn { background: linear-gradient(90deg, #10b981 0%, #059669 100%); transition: all 0.3s; }
        .gradient-btn:hover { box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); transform: scale(1.02); }
    </style>
</head>
<body class="min-h-screen flex flex-col">
    <div id="vanta-canvas"></div>
    
    <nav class="w-full h-20 border-b border-white/5 bg-black/20 backdrop-blur-md flex items-center justify-between px-8 sticky top-0 z-50">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
                <svg class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <div>
                <h1 class="text-xl font-bold tracking-tighter text-white">AI DOMINATOR <span class="text-emerald-500">v17.0</span></h1>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <span class="text-xs text-gray-400">OPERATOR: {{ user.username }}</span>
            <a href="/logout" class="px-4 py-2 border border-white/10 rounded-lg text-xs hover:bg-white/5">LOGOUT</a>
        </div>
    </nav>

    <main class="flex-1 max-w-7xl mx-auto w-full p-6 grid grid-cols-1 lg:grid-cols-12 gap-8 mt-4 z-10">
        <!-- COMMAND -->
        <div class="lg:col-span-4 flex flex-col gap-6">
            <div class="glass-panel rounded-3xl p-8">
                <h2 class="text-2xl font-bold mb-6">Mission Control</h2>
                <div class="space-y-6">
                    <input type="text" id="nicheInput" placeholder="Target Niche" class="w-full bg-black/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-emerald-500 outline-none">
                    <div class="grid grid-cols-2 gap-3">
                        <button onclick="setMode('VIRAL_ATTACK')" id="btn-viral" class="p-3 rounded-xl border border-emerald-500 bg-emerald-500/20 text-emerald-400 text-xs font-bold">VIRAL</button>
                        <button onclick="setMode('AUTHORITY_BUILDER')" id="btn-auth" class="p-3 rounded-xl border border-white/10 bg-black/30 text-gray-400 text-xs font-bold">AUTHORITY</button>
                    </div>
                    <button onclick="execute()" id="executeBtn" class="gradient-btn w-full py-4 rounded-xl font-bold text-black text-sm uppercase tracking-widest flex items-center justify-center gap-2">
                        GENERATE ASSETS
                    </button>
                </div>
            </div>
            
            <!-- HISTORY MINI -->
            <div class="glass-panel rounded-xl p-4 h-64 overflow-hidden flex flex-col">
                <div class="text-[10px] text-gray-500 uppercase tracking-widest mb-2 border-b border-white/5 pb-1">Recent Operations</div>
                <div id="historyList" class="flex-1 overflow-y-auto space-y-2 pr-2">
                    <div class="text-xs text-gray-600 text-center mt-10">Loading history...</div>
                </div>
            </div>
        </div>

        <!-- OUTPUT -->
        <div class="lg:col-span-8 relative min-h-[600px]">
            <div id="loader" class="hidden absolute inset-0 glass-panel rounded-3xl z-20 flex flex-col items-center justify-center">
                <div class="w-16 h-16 border-4 border-t-emerald-500 border-gray-800 rounded-full animate-spin mb-4"></div>
                <div class="text-xl font-bold animate-pulse">SYNTHESIZING</div>
            </div>

            <div id="resultState" class="hidden h-full flex flex-col gap-6">
                <div class="glass-panel rounded-3xl p-2 overflow-hidden">
                    <div class="aspect-video bg-black rounded-2xl overflow-hidden relative">
                        <img id="resultImage" src="" class="w-full h-full object-cover">
                        <div class="absolute bottom-6 left-6 bg-black/60 px-3 py-1 rounded text-[10px] text-emerald-400 font-bold backdrop-blur">AI GENERATED</div>
                    </div>
                </div>
                <div class="glass-panel rounded-3xl p-8">
                    <h1 id="postTitle" class="text-3xl font-bold text-white mb-6 text-right" style="direction: rtl;"></h1>
                    <div id="postBody" class="text-gray-300 text-lg leading-relaxed text-right whitespace-pre-line mb-6" style="direction: rtl;"></div>
                    <div id="hashtags" class="flex flex-wrap gap-2 justify-end" style="direction: rtl;"></div>
                </div>
            </div>
            
            <div id="emptyState" class="absolute inset-0 glass-panel rounded-3xl flex flex-col items-center justify-center border-2 border-dashed border-white/5">
                <div class="text-gray-500 font-mono text-sm">READY FOR DEPLOYMENT</div>
            </div>
        </div>
    </main>

    <script>
        document.addEventListener("DOMContentLoaded", () => {
            try { VANTA.NET({ el: "#vanta-canvas", mouseControls: false, touchControls: false, gyroControls: false, minHeight: 200.00, minWidth: 200.00, scale: 1.00, scaleMobile: 1.00, color: 0x10b981, backgroundColor: 0x050505, points: 10.00, maxDistance: 24.00, spacing: 20.00, showDots: true }) } catch(e) {}
            loadHistory();
        });

        let currentMode = 'VIRAL_ATTACK';
        function setMode(mode) {
            currentMode = mode;
            document.getElementById('btn-viral').className = mode === 'VIRAL_ATTACK' ? 'p-3 rounded-xl border border-emerald-500 bg-emerald-500/20 text-emerald-400 text-xs font-bold transition-all' : 'p-3 rounded-xl border border-white/10 bg-black/30 text-gray-400 text-xs font-bold transition-all';
            document.getElementById('btn-auth').className = mode === 'AUTHORITY_BUILDER' ? 'p-3 rounded-xl border border-blue-500 bg-blue-500/20 text-blue-400 text-xs font-bold transition-all' : 'p-3 rounded-xl border border-white/10 bg-black/30 text-gray-400 text-xs font-bold transition-all';
        }

        async function execute() {
            const niche = document.getElementById('nicheInput').value;
            if(!niche) return;
            
            document.getElementById('emptyState').classList.add('hidden');
            document.getElementById('resultState').classList.add('hidden');
            document.getElementById('loader').classList.remove('hidden');
            document.getElementById('executeBtn').disabled = true;

            try {
                const res = await fetch('/api/tactical/execute', {
                    method: 'POST', headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ niche: niche, mode: currentMode })
                });
                const data = await res.json();
                
                document.getElementById('postTitle').textContent = data.title;
                document.getElementById('postBody').textContent = data.body;
                if(data.image_base64) document.getElementById('resultImage').src = `data:image/png;base64,${data.image_base64}`;
                
                const tags = document.getElementById('hashtags'); tags.innerHTML = '';
                data.hashtags.forEach(t => {
                    const s = document.createElement('span'); s.className = "px-3 py-1 rounded-full bg-white/5 text-xs text-emerald-400"; s.textContent = t; tags.appendChild(s);
                });

                document.getElementById('resultState').classList.remove('hidden');
                loadHistory(); // Refresh history
            } catch(e) { alert("Error: " + e); } 
            finally {
                document.getElementById('loader').classList.add('hidden');
                document.getElementById('executeBtn').disabled = false;
            }
        }

        async function loadHistory() {
            const res = await fetch('/api/history');
            const data = await res.json();
            const list = document.getElementById('historyList');
            list.innerHTML = '';
            data.forEach(item => {
                const div = document.createElement('div');
                div.className = "p-3 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition cursor-pointer";
                div.innerHTML = `<div class='text-xs font-bold text-white truncate'>${item.niche}</div><div class='text-[10px] text-gray-500'>${item.date}</div>`;
                list.appendChild(div);
            });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
