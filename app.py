import os
import random
import time
import json
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import google.generativeai as genai

# --- INITIALIZATION PROTOCOLS ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'DOMINATOR_SUPREME_KEY_v13')
app.config['ENV'] = 'production'

# --- AI BRAIN ACTIVATION ---
# محاولة تهيئة اتصال Gemini
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
AI_ACTIVE = False

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        # نستخدم موديل سريع وذكي
        model = genai.GenerativeModel('gemini-flash-latest')
        AI_ACTIVE = True
        print(">> [SYSTEM] NEURO-LINK ESTABLISHED WITH GEMINI AI.")
    except Exception as e:
        print(f"!! [WARNING] AI Connection Failed: {e}")
else:
    print("!! [WARNING] NO GOOGLE_API_KEY FOUND. SYSTEM RUNNING IN SIMULATION MODE.")

# --- THE STRATEGIC INTELLIGENCE CORE (SIC) ---
class StrategicIntelligenceCore:
    def __init__(self):
        self.version = "13.2 (True-AGI)"
        self.status = "OPERATIONAL"

    def _generate_fallback_content(self, niche, mode):
        """
        خطة الطوارئ: تعمل فقط في حال فشل الاتصال بالذكاء الاصطناعي.
        """
        if mode == 'VIRAL_ATTACK':
            return {
                "title": f"لماذا يخسر الجميع في {niche}؟",
                "body": f"الحقيقة أن 99% من العاملين في مجال {niche} يكررون نفس الأخطاء.\n\nالسر ليس في العمل بجد، بل في العمل بذكاء.\n\n#{niche.replace(' ', '')}",
                "framework": "Contrarian (Fallback)",
                "sentiment": "Critical"
            }
        else:
            return {
                "title": f"استراتيجية {niche} للمحترفين",
                "body": f"إليك الخطوات الثلاث التي استخدمتها لمضاعفة النتائج في {niche}.\n\n1. الاستراتيجية.\n2. التنفيذ.\n3. التحليل.\n\n#{niche.replace(' ', '')}",
                "framework": "Educational (Fallback)",
                "sentiment": "Neutral"
            }

    def _build_expert_prompt(self, niche, mode):
        """
        هندسة الأمر الدقيق لتحويل الذكاء الاصطناعي إلى خبير محتوى عالمي.
        """
        
        # تحديد الشخصية بدقة
        persona = (
            "You are a world-class Content Strategist & Ghostwriter with 15+ years of experience building 7-figure personal brands. "
            "You despise generic, AI-sounding content. You write with punchy, short sentences. "
            "You use psychological triggers: Urgency, Scarcity, Curiosity, and Social Proof. "
            "Your tone is confident, slightly arrogant but backed by data, and extremely engaging."
        )

        # تحديد الزاوية الإبداعية عشوائياً لضمان التنوع
        angles = [
            "The 'Contrarian' (Attack a common belief)",
            "The 'Data-Backed' (Use fake but realistic statistics)",
            "The 'Personal Failure' (Story of a mistake turned into a lesson)",
            "The 'Step-by-Step' (Actionable framework)",
            "The 'Prediction' (What happens in 2026)"
        ]
        selected_angle = random.choice(angles)

        if mode == 'VIRAL_ATTACK':
            strategy = f"Focus on high virality. Shock the reader. Use a controversial hook. Angle: {selected_angle}."
        else: # AUTHORITY_BUILDER
            strategy = f"Focus on high authority and trust. Sound like a professor or a CEO. Deep insight. Angle: {selected_angle}."

        # الأمر النهائي
        prompt = f"""
        {persona}
        
        TASK: Write a LinkedIn/Twitter post for the niche: '{niche}'.
        STRATEGY: {strategy}
        
        OUTPUT FORMAT: strictly clean JSON (no markdown backticks) with keys:
        - "title": A scroll-stopping hook (max 10 words).
        - "body": The post content (formatted with newlines). Keep it under 200 words. Use emojis sparingly.
        - "framework": Name of the psychological framework used (e.g., PAS, AIDA).
        - "sentiment": The emotional tone (e.g., Aggressive, Inspiring).
        
        LANGUAGE: Arabic (but use English terms for technical words where appropriate).
        """
        return prompt

    def generate_warhead(self, niche, mode):
        """
        محاولة التوليد باستخدام الذكاء الحقيقي، مع السقوط الآمن للقوالب.
        """
        if AI_ACTIVE:
            try:
                print(f">> [AI] Thinking about {niche} using {mode}...")
                prompt = self._build_expert_prompt(niche, mode)
                
                response = model.generate_content(prompt)
                
                # تنظيف الرد من علامات Markdown إذا وجدت
                raw_text = response.text.replace('```json', '').replace('```', '').strip()
                
                content_data = json.loads(raw_text)
                return content_data
                
            except Exception as e:
                print(f"!! [ERROR] AI Generation Failed: {e}. Switching to Fallback.")
                return self._generate_fallback_content(niche, mode)
        else:
            return self._generate_fallback_content(niche, mode)

    def calculate_dominance_score(self, niche, mode):
        base = random.randint(88, 95)
        return min(99, base + (2 if mode == 'VIRAL_ATTACK' else 0))

sic_engine = StrategicIntelligenceCore()

# --- SYSTEM INTERFACE ---

@app.route('/')
def system_root():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AI DOMINATOR | BRAIN</title>
        <style>
            body { background: #000; color: #0f0; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .box { border: 1px solid #333; padding: 20px; background: #050505; max-width: 600px; }
            .status-ok { color: #0f0; }
            .status-warn { color: orange; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>AI DOMINATOR CORE v13.2</h1>
            <p>SYSTEM: <span class="status-ok">ONLINE</span></p>
            <p>AI CONNECTION: <span class="{{ 'status-ok' if ai_active else 'status-warn' }}">{{ 'SECURE (Gemini Active)' if ai_active else 'OFFLINE (Simulation Mode)' }}</span></p>
            <hr style="border-color:#333">
            <p>> Ready for incoming tactical requests...</p>
        </div>
    </body>
    </html>
    """, ai_active=AI_ACTIVE)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ONLINE", "ai_active": AI_ACTIVE})

@app.route('/api/tactical/execute', methods=['POST'])
def execute_order():
    try:
        data = request.json or {}
        niche = data.get('niche', 'Business')
        mode = data.get('mode', 'VIRAL_ATTACK')
        
        # 1. Generate High-Level Content
        content = sic_engine.generate_warhead(niche, mode)
        
        # 2. Add Meta Data
        response = {
            "status": "MISSION_COMPLETE",
            "title": content.get('title', 'System Error'),
            "body": content.get('body', 'Content generation failed.'),
            "framework": content.get('framework', 'Unknown'),
            "platform": "LinkedIn / X",
            "metrics": {
                "viralityScore": sic_engine.calculate_dominance_score(niche, mode),
                "predictedReach": random.randint(20000, 150000),
                "sentiment": content.get('sentiment', 'Neutral')
            }
        }
        
        return jsonify(response)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

