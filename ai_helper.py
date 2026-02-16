"""
ai_helper.py — محرك الذكاء الاصطناعي الهجين (Gemini + OpenRouter)
V16: دقة قصوى في المطابقة + سرعة في التحليل
"""
import google.generativeai as genai
import requests
import json
import logging
from config import Config

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PerfumeAI")

class PerfumeAI:
    def __init__(self):
        """تهيئة المحركات الذكية"""
        self.gemini_ready = False
        self.openrouter_ready = False
        
        # 1. إعداد Gemini (للسرعة والمحادثة)
        self.gemini_key = Config.get_api_key()
        if self.gemini_key:
            try:
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")
                self.gemini_ready = True
            except Exception as e:
                logger.error(f"فشل تشغيل Gemini: {e}")

        # 2. إعداد OpenRouter (للدقة العالية والمطابقة العميقة)
        self.openrouter_key = Config.get_openrouter_key()
        if self.openrouter_key:
            self.openrouter_ready = True
            self.or_headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://mahwous-store.local", 
                "X-Title": "Mahwous Pricing System"
            }
            # نستخدم نموذج ذكي جداً للمطابقة
            self.smart_model = "openai/gpt-4o-mini" 

    def get_system_prompt(self):
        """تعليمات الخبير"""
        return """
        أنت خبير تسعير عطور في السوق السعودي (خبرة 15 سنة).
        قواعدك:
        1. الدقة في تمييز التركيز (EDP vs EDT) أمر حاسم.
        2. تحليل المنافسين يعتمد على السعر والحجم.
        3. كن مختصراً ومباشراً.
        """

    def chat(self, prompt: str) -> str:
        """محادثة عامة (تستخدم Gemini للسرعة)"""
        if not self.gemini_ready:
            return "⚠️ الذكاء الاصطناعي غير متصل (تحقق من المفاتيح في config.py)"
        try:
            full_prompt = f"{self.get_system_prompt()}\n\nالسؤال: {prompt}"
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"خطأ في Gemini: {str(e)}"

    def verify_match_deep(self, prod1: str, price1: float, prod2: str, price2: float) -> dict:
        """
        فحص التطابق العميق (Deep Match Verification)
        يستخدم OpenRouter (GPT-4o) للحسم في الحالات المشكوك فيها.
        """
        # إذا لم يتوفر OpenRouter، نستخدم Gemini كبديل
        if not self.openrouter_ready:
            return self.verify_match_fast(prod1, prod2)

        system_prompt = """
        أنت مدقق بيانات عطور صارم. مهمتك مقارنة منتجين وتحديد هل هما متطابقان تماماً (Identical).
        
        قواعد صارمة جداً للمطابقة (True):
        1. تطابق البراند (Brand) إلزامي.
        2. تطابق اسم العطر (Line) إلزامي.
        3. تطابق التركيز (Concentration) إلزامي (Parfum != EDP != EDT).
        4. تطابق الحجم (Size) إلزامي (100ml != 50ml).
        5. تجاهل اختلاف التغليف (Tester vs Box) إلا إذا طلب منك غير ذلك.
        
        المخرجات JSON فقط:
        {
            "match": boolean, 
            "confidence": number (0-100),
            "reason": "سبب واضح وقصير"
        }
        """
        
        user_prompt = f"""
        المنتج الأول (لدينا): {prod1} | السعر: {price1}
        المنتج الثاني (المنافس): {prod2} | السعر: {price2}
        """

        try:
            payload = {
                "model": self.smart_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.0, # صفر للإجابات الحتمية
                "response_format": { "type": "json_object" } 
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=self.or_headers,
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                return json.loads(result)
            else:
                logger.error(f"OpenRouter Error: {response.text}")
                # العودة للبديل في حال الفشل
                return self.verify_match_fast(prod1, prod2)
                
        except Exception as e:
            logger.error(f"Deep Verify Error: {e}")
            return {"match": False, "confidence": 0, "reason": f"خطأ اتصال: {str(e)}"}

    def verify_match_fast(self, prod1: str, prod2: str) -> dict:
        """فحص سريع باستخدام Gemini (للحالات الواضحة)"""
        if not self.gemini_ready:
            return {"match": False, "confidence": 0, "reason": "AI غير متصل"}
            
        prompt = f"""
        قارن بين المنتجين بصيغة JSON (match: bool, reason: str, confidence: int):
        1: {prod1}
        2: {prod2}
        هل هما نفس المنتج تماماً (نفس الحجم والتركيز)؟
        """
        try:
            resp = self.gemini_model.generate_content(prompt)
            text = resp.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except:
            return {"match": False, "confidence": 0, "reason": "فشل التحليل السريع"}

    def suggest_pricing(self, product: str, my_price: float, comp_price: float) -> dict:
        """تحليل استراتيجية التسعير"""
        if not self.gemini_ready:
            return {"decision": "مراجعة", "reason": "AI مفصول"}

        diff_perc = ((comp_price - my_price) / my_price) * 100
        
        prompt = f"""
        أنت مستشار تسعير.
        المنتج: {product}
        سعري: {my_price}
        المنافس: {comp_price}
        الفرق: {diff_perc:.1f}%
        
        أعطني قرار (رفع سعر / خفض سعر / موافق) مع سبب وجيه وسعر مقترح.
        JSON: {{ "decision": str, "suggested_price": float, "reason": str }}
        """
        try:
            resp = self.gemini_model.generate_content(prompt)
            text = resp.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except:
            return {"decision": "خطأ", "suggested_price": my_price, "reason": "فشل التحليل"}
