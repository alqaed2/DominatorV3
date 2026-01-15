import os
import random
import time
import json
import logging
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from google import genai
from google.genai import types

# --- INITIALIZATION PROTOCOLS ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'DOMINATOR_SUPREME_KEY_v13')
app.config['ENV'] = 'production'

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SIC_CORE")

# --- AI BRAIN ACTIVATION (NEXT-GEN) ---
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
client = None
AI_ACTIVE = False

if GOOGLE_API_KEY:
    try:
        # الاتصال باستخدام المكتبة الحديثة google-genai
        client = genai.Client(api_key=GOOGLE_API_KEY)
        AI_ACTIVE = True
        logger.info(">> [SYSTEM] NEURO-LINK ESTABLISHED WITH GEMINI 2.0.")
    except Exception as e:
        logger.error(f"!! [WARNING] AI Connection Failed: {e}")
else:
    logger.warning("!! [CRITICAL] NO GOOGLE_API_KEY FOUND. SYSTEM RUNNING IN SIMULATION MODE.")

# --- THE STRATEGIC INTELLIGENCE CORE (SIC) ---
class StrategicIntelligenceCore:
    def __init__(self):
        self.version = "13.3 (Supreme-Intelligence)"

    def _generate_fallback_content(self, niche, mode):
        """خطة الطوارئ عند غياب المفتاح"""
        return {
            "title": f"⚠️ النظام يعمل بدون وقود (API KEY Missing)",
            "body": f"عذراً أيها القائد.\n\nأنت تحاول تشغيل مفاعل نووي بدون يورانيوم.\n\nيجب عليك إضافة GOOGLE_API_KEY في إعدادات Render فوراً لتفعيل الذكاء الاصطناعي الحقيقي.\n\nحالياً، أنا مجرد قالب غبي.",
            "framework": "SYSTEM_ERROR",
            "sentiment": "Critical"
        }

    def _build_expert_prompt(self, niche, mode):
        """هندسة الأوامر المتقدمة"""
        angle = random.choice([
            "Counter-Intuitive Truth (Shocking)",
            "Insider Leak (Secrets of the 1%)",
            "Framework Breakdown (Step-by-Step)",
            "Prediction 2026 (Visionary)"
        ])
        
        system_instruction = """
        You are the 'Supreme Content Architect'. You are NOT a generic AI assistant.
        You have 20 years of experience in viral marketing and psychology.
        
        STYLE RULES:
        1. NO fluff. NO generic openings like 'In the world of...'.
        2. Short, punchy sentences.
        3. Use line breaks for readability.
        4. Tone: Confident, slightly aggressive, authoritative.
        5. Language: Arabic (Mix with English technical terms).
        """
        
        user_prompt = f"""
        TARGET NICHE: {niche}
        STRATEGY MODE: {mode}
        CREATIVE ANGLE: {angle}
        
        TASK: Generate a high-performance social media post.
        
        RESPONSE FORMAT (JSON ONLY):
        {{
            "title": "A killer hook (max 10 words)",
            "body": "The full post content (max 150 words)",
            "framework": "The psychological framework used",
            "sentiment": "The emotional tone"
        }}
        """
        return system_instruction, user_prompt

    def generate_warhead(self, niche, mode):
        if AI_ACTIVE and client:
            try:
                logger.info(f">> [AI] Thinking about {niche}...")
                sys_inst, user_msg = self._build_expert_prompt(niche, mode)
                
                # استخدام أحدث موديل متاح
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    config=types.GenerateContentConfig(
                        system_instruction=sys_inst,
                        response_mime_type='application/json'
                    ),
                    contents=[user_msg]
                )
                
                return json.loads(response.text)
                
            except Exception as e:
                logger.error(f"!! [ERROR] Generation Failed: {e}")
                return self._generate_fallback_content(niche, mode)
        else:
            return self._generate_fallback_content(niche, mode)

sic_engine = StrategicIntelligenceCore()

# --- ROUTES ---

@app.route('/')
def system_root():
    status_color = "#0f0" if AI_ACTIVE else "#f00"
    status_text = "ONLINE (INTELLIGENT)" if AI_ACTIVE else "OFFLINE (SIMULATION - MISSING KEY)"
    
    return render_template_string(f"""
    <!DOCTYPE html>
    <body style="background:#000;color:{status_color};font-family:monospace;display:flex;justify-content:center;align-items:center;height:100vh;">
        <div style="border:1px solid #333;padding:40px;text-align:center;">
            <h1>AI DOMINATOR v13.3</h1>
            <p>STATUS: {status_text}</p>
            <p>ENGINE: GEMINI 2.0 FLASH</p>
        </div>
    </body>
    """)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ONLINE", "ai_active": AI_ACTIVE})

@app.route('/api/tactical/execute', methods=['POST'])
def execute_order():
    data = request.json or {}
    niche = data.get('niche', 'General')
    mode = data.get('mode', 'VIRAL')
    
    content = sic_engine.generate_warhead(niche, mode)
    
    return jsonify({
        "status": "SUCCESS",
        "title": content.get('title'),
        "body": content.get('body'),
        "framework": content.get('framework'),
        "metrics": {
            "viralityScore": random.randint(88, 99),
            "predictedReach": random.randint(10000, 500000),
            "sentiment": content.get('sentiment')
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
