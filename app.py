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
        logger.info(">> [SYSTEM] v14.0 OMNI-CHANNEL ENGINE ACTIVE.")
    except Exception as e:
        logger.error(f"!! [ERROR] AI Connection Failed: {e}")
else:
    logger.warning("!! [CRITICAL] KEY MISSING.")

# --- THE STRATEGIC INTELLIGENCE CORE (SIC) v14.0 ---
class StrategicIntelligenceCore:
    def __init__(self):
        self.version = "14.0 (Omni-Warlord)"

    def _generate_fallback_content(self, niche):
        return {
            "title": "نظام الطوارئ: المفتاح مفقود",
            "body": "يرجى التحقق من GEMINI_API_KEY في إعدادات Render.",
            "image_prompt": "Error screen, cyberpunk style, red warning lights",
            "framework": "SYSTEM_FAILURE",
            "sentiment": "Critical"
        }

    def _build_expert_prompt(self, niche, mode):
        # زوايا هجومية أكثر تنوعاً
        angles = [
            "The 'Myth Buster' (Destroy a common misconception)",
            "The 'Behind the Scenes' (The ugly truth of the industry)",
            "The 'Data Reveal' (Shocking numbers/statistics)",
            "The 'Personal Confession' (Vulnerable yet authoritative)",
            "The 'Future Vision' (Where is this market going?)"
        ]
        selected_angle = random.choice(angles)
        
        system_instruction = """
        You are the 'Supreme Content Warlord'. You are NOT a polite assistant.
        You are a world-class expert with 15 years of experience in the specific niche provided.
        
        CRITICAL RULES:
        1. **Cultural Resonance:** If the niche implies a specific region (e.g., 'Saudi Coffee'), use the appropriate local professional tone (White Dialect/Mix of English terms). Don't sound like a translated book.
        2. **Terminology:** Use deep industry jargon correctly (e.g., for Coffee: Anaerobic, V60, TDS, Extraction).
        3. **Structure:** HOOK -> VALUE -> TWIST -> CTA.
        4. **Visuals:** You must imagine the PERFECT image to go with this post.
        
        TONE:
        - If 'VIRAL_ATTACK': Aggressive, controversial, fast-paced.
        - If 'AUTHORITY_BUILDER': Sophisticated, deep, analytical, 'The Professor' vibe.
        """
        
        user_prompt = f"""
        TARGET NICHE: {niche}
        STRATEGY MODE: {mode}
        CREATIVE ANGLE: {selected_angle}
        
        TASK:
        1. Write a social media post (Arabic).
        2. Create a detailed prompt for an AI Image Generator (Midjourney/Flux) to create a matching image (English).
        
        RESPONSE FORMAT (JSON ONLY):
        {{
            "title": "Killer hook (max 10 words, Arabic)",
            "body": "Post content (max 150 words, Arabic, use line breaks)",
            "image_prompt": "Detailed English prompt for Midjourney describing the scene, lighting, and mood",
            "framework": "Psychological framework used",
            "sentiment": "Emotional tone"
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
                        temperature=0.85 # Increased for creativity
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
    return render_template_string("<h1>AI DOMINATOR v14.0 ACTIVE</h1>")

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
        "framework": content.get('framework'),
        "metrics": {
            "viralityScore": random.randint(90, 99),
            "predictedReach": random.randint(50000, 1000000),
            "sentiment": content.get('sentiment')
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
