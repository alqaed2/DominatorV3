import os
import random
import time
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# --- INITIALIZATION PROTOCOLS ---
app = Flask(__name__)

# تفعيل CORS الشامل: يسمح لوحدة الاختبار المحلية بالاتصال بالخادم البعيد
CORS(app, resources={r"/*": {"origins": "*"}})

# تكوين النظام
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'DOMINATOR_SUPREME_KEY_v13')
app.config['ENV'] = 'production'

# --- THE STRATEGIC INTELLIGENCE CORE (SIC) CLASS ---
class StrategicIntelligenceCore:
    """
    SIC v13.1: العقل المدبر للنظام.
    """
    
    def __init__(self):
        self.version = "13.1 (Neuro-Link)"
        self.status = "OPERATIONAL"
        print(f">> [SYSTEM] SIC {self.version} Initialized. Ready for War.")

    def calculate_dominance_score(self, niche, mode):
        # خوارزمية محاكاة الذكاء التنبئي
        base_score = 85
        volatility = random.randint(-5, 14)
        if mode == 'VIRAL_ATTACK':
            return min(99, base_score + volatility + 2)
        return min(99, base_score + volatility)

    def generate_warhead(self, niche, mode):
        """
        توليد الرأس الحربي (المحتوى).
        """
        # قوالب الهيمنة (DNA)
        viral_hooks = [
            f"توقف فوراً عن إضاعة وقتك في {niche} بالطريقة القديمة.",
            f"الرقم السري الذي يخفيه عنك أباطرة {niche}...",
            f"كيف تحول {niche} إلى آلة طباعة أموال في 3 خطوات...",
            f"الحقيقة القاسية: 99% من العاملين في {niche} سيفلسون قريباً...",
            f"لقد راقبت أفضل 10 حسابات في {niche}، وهذا ما وجدته..."
        ]

        authority_hooks = [
            f"الدليل الشامل: هندسة {niche} للمحترفين فقط.",
            f"لماذا تفشل استراتيجيات {niche} التقليدية في 2025؟",
            f"دراسة حالة: كيف ضاعفنا نتائج {niche} عشرة أضعاف.",
            f"الخارطة الذهنية الكاملة لاحتراف {niche}.",
            f"ما لا يخبرك به الكورسات المدفوعة عن واقع {niche}..."
        ]

        hooks = viral_hooks if mode == 'VIRAL_ATTACK' else authority_hooks
        selected_hook = random.choice(hooks)
        
        if mode == 'VIRAL_ATTACK':
            framework = "Shock & Awe (الصدمة والرهبة)"
            sentiment = "Aggressive / Controversial"
            body = (
                f"معظم الناس يتعاملون مع {niche} بسذاجة.\n\n"
                f"يعتقدون أن الأمر مجرد حظ. خطأ.\n\n"
                f"لقد قمت بتفكيك استراتيجيات الـ 1% في {niche}، والنمط مرعب.\n\n"
                f"إليك المعادلة التي يرفضون مشاركتها:\n"
                f"1. السرعة قبل الجودة.\n"
                f"2. العاطفة قبل المنطق.\n"
                f"3. الهجوم قبل الدفاع.\n\n"
                f"هل أنت مستعد لتغيير اللعبة؟\n\n"
                f"#{niche.replace(' ', '')} #Dominance #Growth"
            )
        else:
            framework = "The Inverted Pyramid (الهرم المقلوب)"
            sentiment = "Authoritative / Educational"
            body = (
                f"لقد حللت بيانات الـ 48 ساعة الماضية في سوق {niche}.\n\n"
                f"النتائج تعيد تعريف كل ما نعرفه.\n\n"
                f"بينما يركز الهواة على الأدوات، يركز المحترفون على الأنظمة.\n\n"
                f"إليك المخطط الذي نستخدمه للهيمنة:\n"
                f"- المرحلة 1: الاستحواذ.\n"
                f"- المرحلة 2: التحويل.\n"
                f"- المرحلة 3: الاحتفاظ.\n\n"
                f"التفاصيل الكاملة في التعليق الأول 👇\n\n"
                f"#{niche.replace(' ', '')} #Strategy #Business"
            )

        return {
            "title": selected_hook,
            "body": body,
            "framework": framework,
            "sentiment": sentiment
        }

sic_engine = StrategicIntelligenceCore()

# --- ROUTES ---

@app.route('/')
def system_root():
    """
    صفحة الترحيب السيادية (Terminal UI)
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI DOMINATOR | SYSTEM STATUS</title>
        <style>
            body { background-color: #000; color: #0f0; font-family: 'Courier New', monospace; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .terminal { border: 1px solid #333; padding: 2rem; max-width: 700px; width: 90%; background: #050505; box-shadow: 0 0 20px rgba(0, 255, 0, 0.1); }
            h1 { border-bottom: 1px dashed #333; padding-bottom: 1rem; margin-bottom: 1rem; font-size: 1.5rem; }
            .status { color: #0f0; font-weight: bold; text-shadow: 0 0 5px #0f0; }
            .blink { animation: blink 1s infinite; }
            @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
            .info { color: #888; font-size: 0.9rem; margin-top: 2rem; border-top: 1px solid #222; padding-top: 1rem; }
        </style>
    </head>
    <body>
        <div class="terminal">
            <h1>AI DOMINATOR v13.1 <span style="font-size:0.8rem; color:#444;">[CLASSIFIED]</span></h1>
            <p>> SYSTEM STATUS: <span class="status">OPERATIONAL</span></p>
            <p>> NEURAL ENGINE: <span class="status">CONNECTED</span></p>
            <p>> SECURITY: <span class="status">MAXIMUM</span></p>
            <br>
            <p>> Awaiting tactical command...</p>
            <p>> _<span class="blink">█</span></p>
            
            <div class="info">
                [NOTICE] This is a backend node. Use the "Tactical Console" (test_console.html) to interact with this system via API endpoints.
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/health', methods=['GET'])
def system_check():
    return jsonify({"status": "ONLINE", "system": "AI DOMINATOR v13.1"})

@app.route('/api/tactical/execute', methods=['POST'])
def execute_order():
    """
    نقطة النهاية الرئيسية لتوليد المحتوى
    """
    try:
        # التعامل الآمن مع البيانات الفارغة
        data = request.json if request.is_json else {}
        niche = data.get('niche', 'General Growth')
        mode = data.get('mode', 'VIRAL_ATTACK')
        
        print(f">> [EXECUTE] Generating for: {niche} | Mode: {mode}")

        content_data = sic_engine.generate_warhead(niche, mode)
        dominance_score = sic_engine.calculate_dominance_score(niche, mode)
        
        # محاكاة التفكير
        time.sleep(1.5)
        
        return jsonify({
            "status": "MISSION_COMPLETE",
            "title": content_data['title'],
            "body": content_data['body'],
            "framework": content_data['framework'],
            "platform": random.choice(["LinkedIn", "X (Twitter)"]),
            "metrics": {
                "viralityScore": dominance_score,
                "predictedReach": random.randint(15000, 900000),
                "sentiment": content_data['sentiment']
            }
        })

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "EXECUTION_FAILURE", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
