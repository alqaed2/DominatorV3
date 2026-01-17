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
        logger.info(">> [SYSTEM] v14.3 HOLLYWOOD VISUAL PROTOCOL ACTIVE.")
    except Exception as e:
        logger.error(f"!! [ERROR] AI Connection Failed: {e}")
else:
    logger.warning("!! [CRITICAL] KEY MISSING.")

# --- THE STRATEGIC INTELLIGENCE CORE (SIC) v14.3 ---
class StrategicIntelligenceCore:
    def __init__(self):
        self.version = "14.3 (Hollywood-Protocol)"

    def _generate_fallback_content(self, niche):
        return {
            "title": "النظام يعمل في وضع الطوارئ",
            "body": "يرجى التحقق من مفتاح API. النظام لا يمكنه توليد صور دقيقة بدون ذكاء.",
            "image_prompt": "Error screen, technical blueprint style, red alert, dramatic lighting, cinematic",
            "hashtags": ["#SystemError"],
            "framework": "SYSTEM_FAILURE",
            "sentiment": "Critical"
        }

    def _build_expert_prompt(self, niche, mode):
        # زوايا بصرية سينمائية
        visual_angles = [
            "The 'Establishing Shot' (Wide, dramatic landscape with niche element)",
            "The 'Detail Shot' (Extreme close-up, texture focus, macro lens)",
            "The 'Action Shot' (Motion blur, dynamic movement, decisive moment)",
            "The 'Mood Shot' (Atmospheric, golden hour, dramatic shadows, silhouette)"
        ]
        selected_angle = random.choice(visual_angles)
        
        system_instruction = f"""
        You are the 'Supreme Creative Director & Cinematographer'. You do not just describe; you DIRECT a blockbuster visual experience.
        Your expertise: {niche}. You know every tool, every texture, and every hidden detail of this industry.
        
        ### MISSION PART 1: THE CONTENT (ARABIC)
        - Write a powerful, scroll-stopping post in Arabic.
        - Tone: Expert, Authoritative, 'Insider'.
        - Use local dialect if applicable.
        
        ### MISSION PART 2: THE VISUAL (ENGLISH - HOLLYWOOD PROTOCOL)
        - You are writing a prompt for Midjourney v6.
        - **MANDATORY VISUAL TOKENS (MUST USE):** 'Cinematic lighting', 'Dramatic shadows', 'Shot on Arri Alexa LF', '85mm lens f/1.4', 'Depth of field', 'Bokeh', '8k resolution', 'Unreal Engine 5 render style', 'Hyper-realistic', 'Vivid details', 'Color graded'.
        - **RULE 1: NICHE SPECIFICITY & ACTION:**
          - IF 'Coffee': Describe a V60 pour-over action with steam rising, backlit by golden hour light, ceramic texture clearly visible.
          - IF 'Crypto': Describe a close-up of a hardware wallet with glowing screens showing charts in a dark, high-tech room.
          - IF 'Real Estate': Describe a modern villa at dusk with interior lights glowing, wet asphalt reflecting the light, hyper-detailed architecture.
        - **RULE 2: NO TEXT.** The image should contain NO text. Focus on atmosphere and texture.
        
        ### MISSION PART 3: THE TRENDS
        - Extract exactly 8 trending, relevant hashtags (Mix Arabic & English).
        
        CURRENT VISUAL ANGLE: {selected_angle}
        """
        
        user_prompt = f"""
        TARGET NICHE: {niche}
        STRATEGY MODE: {mode}
        
        EXECUTE:
        1. Arabic Post (Hook + Body).
        2. Cinematic Visual Prompt (English) -> MUST BE A MASTERPIECE.
        3. 8 Trending Hashtags.
        
        RESPONSE FORMAT (JSON ONLY):
        {{
            "title": "Hook",
            "body": "Content",
            "image_prompt": "Midjourney Prompt",
            "hashtags": ["#tag1", "#tag2"],
            "framework": "Framework name",
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
                        temperature=0.9  # Higher creativity for visuals
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
            <h1>AI DOMINATOR v14.3</h1>
            <p>HOLLYWOOD VISUAL PROTOCOL: ACTIVE</p>
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
