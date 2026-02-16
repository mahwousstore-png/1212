"""
مساعد الذكاء الاصطناعي - Gemini Pro
متصل دائماً - ذكي في كل قسم - تدريب متقدم
"""
import google.generativeai as genai
import json
from typing import Dict, List, Optional

class PerfumeAI:
    """مساعد الذكاء الاصطناعي للعطور"""
    
    def __init__(self, api_key: str):
        """تهيئة الذكاء الاصطناعي"""
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.is_connected = True
        else:
            self.model = None
            self.is_connected = False
        
        # قاعدة المعرفة - تدريب مسبق
        self.knowledge_base = {
            "pricing_rules": {
                "increase": "رفع السعر إذا كان سعرنا أقل بأكثر من 10%",
                "decrease": "خفض السعر إذا كان سعرنا أعلى بأكثر من 5%",
                "ok": "الموافقة إذا كان الفرق ضمن ±5%",
                "review": "المراجعة إذا كانت المطابقة أقل من 85%"
            },
            "brands": [
                "Dior", "Chanel", "Gucci", "Tom Ford", "Creed",
                "Armani", "Versace", "Givenchy", "YSL", "Prada"
            ],
            "perfume_types": {
                "EDP": "Eau de Parfum - الأقوى (15-20% تركيز)",
                "EDT": "Eau de Toilette - متوسط (5-15% تركيز)",
                "EDC": "Eau de Cologne - خفيف (2-5% تركيز)"
            }
        }
    
    def get_system_prompt(self):
        """البرومبت الأساسي المدرب"""
        return """
أنت خبير تسعير عطور فاخرة في السوق السعودي. لديك خبرة 15+ سنة.

## قواعد التسعير:
1. رفع السعر: إذا كان سعرنا أقل من المنافس بأكثر من 10%
2. خفض السعر: إذا كان سعرنا أعلى من المنافس بأكثر من 5%
3. موافق: إذا كان الفرق ضمن النطاق (±5%)
4. يحتاج مراجعة: إذا كانت المطابقة غير مؤكدة (< 85%)

## العلامات التجارية المعروفة:
Dior, Chanel, Gucci, Tom Ford, Creed, Armani, Versace, Givenchy, YSL, Prada, 
Burberry, Carolina Herrera, Dolce & Gabbana, Bvlgari, Montblanc, Hugo Boss,
Calvin Klein, Davidoff, Lancôme, Narciso Rodriguez, Valentino, Hermès

## أنواع العطور:
- Eau de Parfum (EDP): الأقوى (15-20% تركيز)
- Eau de Toilette (EDT): متوسط (5-15% تركيز)
- Eau de Cologne (EDC): خفيف (2-5% تركيز)

## الأحجام الشائعة:
30ml, 50ml, 75ml, 100ml, 125ml, 150ml, 200ml

## مهمتك:
- تحليل المنتجات بدقة عالية
- اقتراح أسعار تنافسية
- تقديم نصائح استراتيجية
- شرح القرارات بوضوح

كن دقيقاً، محترفاً، وموجزاً.
"""
    
    def verify_product_match(self, our_product: str, competitor_product: str, 
                            our_price: float, competitor_price: float,
                            match_score: float) -> Dict:
        """
        التحقق من صحة المطابقة باستخدام AI
        """
        if not self.is_connected:
            return {
                "verified": False,
                "confidence": 0,
                "explanation": "الذكاء الاصطناعي غير متصل",
                "suggestion": "قم بإدخال Gemini API Key في الإعدادات"
            }
        
        prompt = f"""
{self.get_system_prompt()}

## تحقق من المطابقة:

منتجنا: {our_product}
سعرنا: {our_price} ريال

منتج المنافس: {competitor_product}
سعر المنافس: {competitor_price} ريال

نسبة المطابقة (الخوارزمية): {match_score}%

### المطلوب:
1. هل المنتجان متطابقان فعلاً؟
2. ما مدى ثقتك بالمطابقة؟ (0-100%)
3. لماذا؟ (شرح مختصر)
4. ما القرار الموصى به؟

أجب بصيغة JSON فقط:
{{
  "verified": true/false,
  "confidence": 85,
  "explanation": "شرح مختصر",
  "decision": "رفع سعر / خفض سعر / موافق / يحتاج مراجعة",
  "suggested_price": 450.00
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            # محاولة تحليل JSON
            text = response.text.strip()
            # إزالة markdown code blocks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(text)
            return result
        except Exception as e:
            return {
                "verified": None,
                "confidence": 0,
                "explanation": f"خطأ في التحليل: {str(e)}",
                "decision": "يحتاج مراجعة"
            }
    
    def analyze_pricing_decision(self, our_product: str, our_price: float,
                                 competitor_product: str, competitor_price: float) -> Dict:
        """
        تحليل قرار التسعير
        """
        if not self.is_connected:
            return {
                "decision": "غير متاح",
                "reason": "الذكاء الاصطناعي غير متصل",
                "suggested_price": our_price
            }
        
        prompt = f"""
{self.get_system_prompt()}

## تحليل التسعير:

منتجنا: {our_product}
سعرنا الحالي: {our_price} ريال

منتج المنافس: {competitor_product}
سعر المنافس: {competitor_price} ريال

الفرق: {competitor_price - our_price} ريال ({((competitor_price - our_price) / our_price * 100):.1f}%)

### المطلوب:
1. ما القرار الأفضل؟
2. لماذا؟
3. ما السعر المقترح؟
4. ما المخاطر؟

أجب بصيغة JSON:
{{
  "decision": "رفع سعر / خفض سعر / موافق",
  "reason": "شرح مفصل",
  "suggested_price": 450.00,
  "risks": "المخاطر المحتملة",
  "confidence": 90
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            return json.loads(text)
        except Exception as e:
            return {
                "decision": "خطأ",
                "reason": str(e),
                "suggested_price": our_price
            }
    
    def chat(self, message: str, context: Optional[Dict] = None) -> str:
        """
        محادثة حرة مع الذكاء الاصطناعي
        """
        if not self.is_connected:
            return "⚠️ الذكاء الاصطناعي غير متصل. قم بإدخال Gemini API Key في الإعدادات."
        
        full_prompt = f"{self.get_system_prompt()}\n\n"
        
        if context:
            full_prompt += f"السياق:\n{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
        
        full_prompt += f"السؤال: {message}\n\nأجب بشكل مختصر ومفيد:"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"❌ خطأ: {str(e)}"
    
    def batch_analyze(self, products: List[Dict]) -> List[Dict]:
        """
        تحليل مجموعة من المنتجات دفعة واحدة
        """
        if not self.is_connected:
            return [{"error": "الذكاء الاصطناعي غير متصل"}] * len(products)
        
        results = []
        for product in products:
            analysis = self.analyze_pricing_decision(
                product.get('our_product', ''),
                product.get('our_price', 0),
                product.get('competitor_product', ''),
                product.get('competitor_price', 0)
            )
            results.append(analysis)
        
        return results
    
    def suggest_new_product_price(self, product_name: str, 
                                  similar_products: List[Dict]) -> Dict:
        """
        اقتراح سعر لمنتج جديد بناءً على منتجات مشابهة
        """
        if not self.is_connected:
            return {"suggested_price": 0, "reason": "الذكاء الاصطناعي غير متصل"}
        
        similar_info = "\n".join([
            f"- {p['name']}: {p['price']} ريال"
            for p in similar_products[:5]
        ])
        
        prompt = f"""
{self.get_system_prompt()}

## اقتراح سعر لمنتج جديد:

المنتج الجديد: {product_name}

منتجات مشابهة في السوق:
{similar_info}

### المطلوب:
اقترح سعر مناسب وتنافسي لهذا المنتج.

أجب بصيغة JSON:
{{
  "suggested_price": 450.00,
  "reason": "شرح السبب",
  "price_range": {{"min": 400, "max": 500}},
  "confidence": 85
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            
            return json.loads(text)
        except Exception as e:
            return {
                "suggested_price": 0,
                "reason": f"خطأ: {str(e)}"
            }
    
    def get_market_insights(self, products_df) -> str:
        """
        تحليل السوق والحصول على رؤى استراتيجية
        """
        if not self.is_connected:
            return "⚠️ الذكاء الاصطناعي غير متصل"
        
        # إحصائيات أساسية
        total = len(products_df)
        decisions = products_df['decision'].value_counts().to_dict()
        avg_diff = products_df['price_diff'].mean() if 'price_diff' in products_df else 0
        
        prompt = f"""
{self.get_system_prompt()}

## تحليل السوق:

إجمالي المنتجات: {total}
القرارات:
{json.dumps(decisions, ensure_ascii=False, indent=2)}

متوسط فرق السعر: {avg_diff:.2f} ريال

### المطلوب:
قدم تحليل استراتيجي للسوق:
1. ما الوضع العام؟
2. ما التوصيات الرئيسية؟
3. ما الفرص؟
4. ما المخاطر؟

أجب بشكل منظم ومختصر (5-7 نقاط).
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ خطأ: {str(e)}"
