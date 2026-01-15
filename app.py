import os
import random
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- INITIALIZATION PROTOCOLS ---
app = Flask(__name__)

# تفعيل CORS للسماح للواجهة (Frontend) بالاتصال بالمحرك
CORS(app, resources={r"/api/*": {"origins": "*"}})

# تكوين النظام
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'DOMINATOR_SUPREME_KEY_v13')
app.config['ENV'] = 'production'

# --- THE STRATEGIC INTELLIGENCE CORE (SIC) CLASS ---
class StrategicIntelligenceCore:
    """
    SIC v13.0: العقل المدبر للنظام.
    المسؤولية: تحليل النيش، استخراج الحمض النووي الفيروسي، وتوليد محتوى الهيمنة.
    """
    
    def __init__(self):
        self.version = "13.1 (Neuro-Link)"
        self.status = "OPERATIONAL"
        print(f">> [SYSTEM] SIC {self.version} Initialized. Waiting for targets...")

    def calculate_dominance_score(self, niche, mode):
        """حساب احتمالية الهيمنة بناءً على خوارزمية معقدة محاكية"""
        base_score = 85
        volatility = random.randint(-5, 14)
        if mode == 'VIRAL_ATTACK':
            return min(99, base_score + volatility + 2)
        return min(99, base_score + volatility)

    def generate_warhead(self, niche, mode):
        """
        توليد الرأس الحربي (المحتوى) بناءً على الوضع المختار.
        ملاحظة: في النسخة الكاملة، يتم استبدال هذا المنطق باستدعاء Gemini Pro API.
        """
        
        # --- قاعدة بيانات القوالب الفيروسية (Internal DNA Database) ---
        viral_hooks = [
            f"توقف فوراً عن إضاعة وقتك في {niche} بالطريقة القديمة.",
            f"الرقم الذي يخفيه عنك أباطرة {niche}...",
            f"كيف تحول {niche} إلى آلة طباعة أموال في 3 خطوات (بدون خبرة)...",
            f"الحقيقة القاسية: 99% من العاملين في {niche} سيفلسون قريباً...",
            f"لقد راقبت أفضل 10 حسابات في {niche}، وهذا ما وجدته..."
        ]

        authority_hooks = [
            f"الدليل الشامل: هندسة {niche} للمحترفين فقط.",
            f"لماذا تفشل استراتيجيات {niche} التقليدية في 2025؟ (تحليل بيانات).",
            f"دراسة حالة: كيف ضاعفنا نتائج {niche} عشرة أضعاف باستخدام 'قانون الرافعة'.",
            f"الخارطة الذهنية الكاملة لاحتراف {niche} (احفظ هذا المنشور).",
            f"ما لا يخبرك به الكورسات المدفوعة عن واقع {niche}..."
        ]

        # اختيار القالب بناءً على الوضع
        hooks = viral_hooks if mode == 'VIRAL_ATTACK' else authority_hooks
        selected_hook = random.choice(hooks)
        
        # بناء الجسم (Body) باستخدام "هندسة الإقناع"
        if mode == 'VIRAL_ATTACK':
            framework = "Shock & Awe (الصدمة والرهبة)"
            sentiment = "Aggressive / Controversial"
            body = (
                f"معظم الناس يتعاملون مع {niche} بسذاجة.\n\n"
                "يظنون أن الأمر يتعلق بـ 'العمل الجاد'. خطأ.\n"
                "الأمر يتعلق بـ 'النفوذ'.\n\n"
                "إليك المعادلة التي استخدمتها لكسر الكود:\n\n"
                "1️⃣ الخطوة الأولى: تجاهل المنافسين (هم مخطئون).\n"
                "2️⃣ الخطوة الثانية: استخدم الرافعة التقنية.\n"
                "3️⃣ الخطوة الثالثة: هاجم نقاط الألم.\n\n"
                "إذا لم تبدأ اليوم، ستندم بعد 6 أشهر.\n\n"
                f"#{niche.replace(' ', '')} #Growth #Dominance"
            )
        else:
            framework = "The Inverted Pyramid (الهرم المقلوب)"
            sentiment = "Authoritative / Educational"
            body = (
                f"لقد قضيت الـ 48 ساعة الماضية في تحليل بيانات {niche}.\n\n"
                "النتائج كانت صادمة.\n\n"
                "بينما يركز الجميع على التكتيكات السطحية، يركز الـ 1% الناجحون على شيء واحد فقط:\n"
                "--> الأنظمة (Systems).\n\n"
                "إليك النظام المكون من 4 خطوات للهيمنة على السوق:\n\n"
                "1. التمركز الاستراتيجي.\n"
                "2. المحتوى عالي القيمة.\n"
                "3. التوزيع الآلي.\n"
                "4. التحليل والتحسين.\n\n"
                "هل تطبق هذا النظام؟ أخبرني في التعليقات.\n\n"
                f"#{niche.replace(' ', '')} #Strategy #Business"
            )

        return {
            "title": selected_hook,
            "body": body,
            "framework": framework,
            "sentiment": sentiment
        }

# تهيئة المحرك
sic_engine = StrategicIntelligenceCore()

# --- API ROUTES (NEURO-LINKS) ---

@app.route('/health', methods=['GET'])
def system_check():
    """فحص سلامة النظام"""
    return jsonify({
        "status": "ONLINE",
        "system": "AI DOMINATOR v13.0",
        "latency": f"{random.randint(10, 40)}ms"
    })

@app.route('/api/tactical/scan', methods=['POST'])
def tactical_scan():
    """
    المرحلة الأولى: مسح النيش واستخراج الأنماط.
    يتم استدعاؤها عندما يبدأ النظام في وضع 'Scanning'.
    """
    data = request.json
    niche = data.get('niche', 'General')
    
    # محاكاة زمن المعالجة (لإعطاء شعور بالعمليات الثقيلة)
    time.sleep(1.5) 
    
    return jsonify({
        "status": "TARGET_ACQUIRED",
        "logs": [
            f">> Connecting to Neural Network for '{niche}'...",
            ">> Analyzing top 50 performing assets...",
            ">> 3 Viral Patterns detected [High Probability].",
            ">> Extracting DNA Sequence..."
        ]
    })

@app.route('/api/tactical/execute', methods=['POST'])
def execute_order():
    """
    المرحلة الثانية: تنفيذ أمر الهيمنة وتوليد المحتوى.
    """
    try:
        data = request.json
        niche = data.get('niche', 'Growth')
        mode = data.get('mode', 'VIRAL_ATTACK')
        
        print(f">> [EXECUTION] Generaring content for {niche} in {mode} mode.")
        
        # 1. استدعاء المحرك لتوليد المحتوى
        content_data = sic_engine.generate_warhead(niche, mode)
        
        # 2. حساب المقاييس التنبؤية
        dominance_score = sic_engine.calculate_dominance_score(niche, mode)
        predicted_reach = random.randint(15000, 850000)
        
        # 3. بناء هيكل الاستجابة النهائي (متوافق مع الواجهة)
        response_payload = {
            "status": "MISSION_COMPLETE",
            "title": content_data['title'],
            "body": content_data['body'],
            "framework": content_data['framework'],
            "platform": random.choice(["LinkedIn", "X (Twitter)"]),
            "metrics": {
                "viralityScore": dominance_score,
                "predictedReach": predicted_reach,
                "sentiment": content_data['sentiment']
            }
        }
        
        # محاكاة زمن التفكير العميق
        time.sleep(2)
        
        return jsonify(response_payload)

    except Exception as e:
        print(f"!! [CRITICAL ERROR] {str(e)}")
        return jsonify({"error": "SYSTEM FAILURE", "details": str(e)}), 500

# --- MAIN ENTRY POINT ---
if __name__ == '__main__':
    # تشغيل الخادم على المنفذ القياسي
    port = int(os.environ.get('PORT', 5000))
    print(f">> [BOOT] AI DOMINATOR System Online on Port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
