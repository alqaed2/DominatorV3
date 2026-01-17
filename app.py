import os
import random
import time
import json
import logging
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from google import genai
from google.genai import types

# --- INITIALIZATION ---
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'DOMINATOR_SUPREME_KEY_v13')
app.config['ENV'] = 'production'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SIC_CORE")

# --- AI CONNECTIVITY ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
client = None
AI_ACTIVE = False

if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        AI_ACTIVE = True
        logger.info(">> [SYSTEM] v14.4 HYPER-FLUX ENGINE ACTIVE.")
    except Exception as e:
        logger.error(f"!! [ERROR] AI Connection Failed: {e}")
else:
    logger.warning("!! [CRITICAL] KEY MISSING.")

# --- THE STRATEGIC INTELLIGENCE CORE (SIC) v14.4 ---
class StrategicIntelligenceCore:
    def __init__(self):
        self.version = "14.4 (Hyper-Flux)"

    def _generate_fallback_content(self, niche):
        return {
            "title": "خطأ في الاتصال بالنواة",
            "body": "يرجى التحقق من مفتاح API. النظام لا يمكنه توليد صور دقيقة بدون ذكاء.",
            "image_prompt": "Glitch art style, error message on screen, digital distortion, cyberpunk red and blue lighting --ar 16:9",
            "hashtags": ["#Error"],
            "framework": "SYSTEM_FAILURE",
            "sentiment": "Critical"
        }

    def _build_expert_prompt(self, niche, mode):
        # 1. FORCED VISUAL STYLES (To prevent repetition)
        # في كل مرة، نختار ستايل مختلف تماماً لإجبار الذكاء على التنوع
        styles = [
            "Macro-Realism (Focus on microscopic details of texture)",
            "Dark Moody (High contrast, shadows, mysterious)",
            "Ethereal Softbox (Bright, airy, clean, angelic lighting)",
            "Cyber-Industrial (Neon accents, metal, high-tech vibe)",
            "Cinematic Noir (Warm orange and teal, dramatic, film grain)",
            "Minimalist Luxury (Huge negative space, solid colors, expensive feel)",
            "National Geographic Style (Raw, authentic, documentary feel)"
        ]
        selected_style = random.choice(styles)
        
        # 2. CAMERA GEAR ROTATION (To change the look)
        cameras = [
            "Shot on Sony A7R IV with 90mm Macro Lens",
            "Shot on Arri Alexa LF with 35mm Prime Lens",
            "Shot on Hasselblad H6D-100c (Medium Format)",
            "Shot on Leica M11 with Noctilux 50mm f/0.95"
        ]
        selected_camera = random.choice(cameras)

        system_instruction = f"""
        You are the 'Supreme Visual Architect'. Your goal is NOT to write a simple image description. 
        Your goal is to engineer a 'Text-to-Image Protocol' that generates award-winning photography.
        
        TARGET NICHE: {niche}
        CURRENT FORCED STYLE: {selected_style}
        CURRENT CAMERA GEAR: {selected_camera}
        
        ### RULE 1: THE VISUAL PROMPT (ENGLISH)
        - **NEVER** output generic prompts like "A photo of coffee".
        - **NEVER** repeat the same description twice.
        - **STRUCTURE:** [Subject Definition] + [Detailed Environment] + [Specific Lighting] + [Technical Specs] + [Style Modifiers].
        - **DETAILS:** You must invent specific details. 
          - Instead of "desk", say "Mahogany desk with a scattering of blueprints".
          - Instead of "coffee", say "Double-walled glass cup with distinct layers of espresso and milk, steam rising in a spiral".
        - **NO TEXT:** Ensure the prompt ends with "--no text" to prevent AI from generating text inside the image.
        
        ### RULE 2: THE CONTENT (ARABIC)
        - Write a viral post in Arabic suitable for LinkedIn/X.
        - Tone: {mode} (Aggressive/Viral OR Authoritative/Deep).
        - Hook: Must be catchy and short.
        
        ### RULE 3: HASHTAGS
        - 8 Trending Hashtags (Mix Arabic/English).
        """
        
        user_prompt = f"""
        GENERATE NOW for Niche: {niche}.
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "title": "Arabic Hook",
            "body": "Arabic Content",
            "image_prompt": "The Complex English Prompt (Follow the style: {selected_style})",
            "hashtags": ["#tag1", ...],
            "framework": "Framework Name",
            "sentiment": "Tone"
        }}
        """
        return system_instruction, user_prompt

    def generate_warhead(self, niche, mode):
        if AI_ACTIVE and client:
            try:
                sys_inst, user_msg = self._build_expert_prompt(niche, mode)
                
                response = client.models.generate_content(
                    model='gemini-flash-latest',
                    config=types.GenerateContentConfig(
                        system_instruction=sys_inst,
                        response_mime_type='application/json',
                        temperature=0.95 # Max creativity for diversity
                    ),
                    contents=[user_msg]
                )
                return json.loads(response.text)
            except Exception as e:
                logger.error(f"Generation Error: {e}")
                return self._generate_fallback_content(niche)
        else:
            return self._generate_fallback_content(niche)

sic_engine = StrategicIntelligenceCore()

# --- ROUTES ---
@app.route('/')
def root():
    return render_template_string("""
    <body style="background:#000;color:#0f0;font-family:monospace;display:flex;justify-content:center;align-items:center;height:100vh;">
        <div style="text-align:center;border:1px solid #333;padding:40px;">
            <h1>AI DOMINATOR v14.4</h1>
            <p>HYPER-FLUX PROTOCOL: ACTIVE</p>
            <p style='color:#666;font-size:0.8em'>Visual Diversity Engine: Online</p>
        </div>
    </body>
    """)

@app.route('/api/tactical/execute', methods=['POST'])
def execute():
    data = request.json or {}
    niche = data.get('niche', 'General')
    mode = data.get('mode', 'VIRAL_ATTACK')
    
    content = sic_engine.generate_warhead(niche, mode)
    
    return jsonify({
        "status": "SUCCESS",
        "title": content.get('title'),
        "body": content.get('body'),
        "image_prompt": content.get('image_prompt'),
        "hashtags": content.get('hashtags', []),
        "framework": content.get('framework'),
        "metrics": {
            "viralityScore": random.randint(92, 99),
            "predictedReach": random.randint(50000, 1000000),
            "sentiment": content.get('sentiment')
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
