"""
matcher.py — محرك المطابقة الهجين (V16)
يجمع بين سرعة RapidFuzz ودقة AI + المعالجة المتوازية
"""
import re
import pandas as pd
from rapidfuzz import fuzz
from concurrent.futures import ThreadPoolExecutor
from config import Config

# --- الثوابت وقوائم التنظيف ---
BRANDS = [
    "Dior", "Chanel", "Gucci", "Tom Ford", "Creed", "Armani", "Versace",
    "Givenchy", "YSL", "Prada", "Burberry", "Carolina Herrera", "D&G",
    "Bvlgari", "Montblanc", "Hugo Boss", "Calvin Klein", "Lancome",
    "Hermes", "Mancera", "Montale", "Amouage", "Parfums de Marly", "Lattafa"
]

PERFUME_TYPES = {
    "EDP": ["eau de parfum", "edp", "parfum", "بارفيوم"],
    "EDT": ["eau de toilette", "edt", "تواليت"],
    "EDC": ["eau de cologne", "edc", "كولونيا"],
    "Extrait": ["extrait", "elixir", "مركز"]
}

# --- دوال المساعدة (Extraction Helpers) ---
def clean_text(text):
    if not isinstance(text, str): return ""
    return re.sub(r'[^\w\s]', ' ', text.lower()).strip()

def extract_size(text):
    match = re.search(r'(\d+)\s*(ml|مل)', text.lower())
    return int(match.group(1)) if match else 0

def extract_type(text):
    text = text.lower()
    for ptype, keywords in PERFUME_TYPES.items():
        if any(k in text for k in keywords):
            return ptype
    return "Unknown"

# --- منطق المطابقة الأساسي ---
def calculate_fuzzy_score(name1, name2):
    """حساب نسبة التطابق النصي السريع"""
    n1, n2 = clean_text(name1), clean_text(name2)
    
    # 1. مطابقة كاملة
    ratio = fuzz.ratio(n1, n2)
    
    # 2. مطابقة جزئية (مفيد للأسماء الطويلة)
    partial = fuzz.partial_ratio(n1, n2)
    
    # 3. ترتيب الكلمات (يتجاهل اختلاف الترتيب)
    token_sort = fuzz.token_sort_ratio(n1, n2)
    
    # الوزن النسبي: التركيز على token_sort لأنه الأفضل في العطور
    final_score = (ratio * 0.2) + (partial * 0.3) + (token_sort * 0.5)
    return final_score

# --- المعالج الفردي (يعمل في الخلفية) ---
def process_single_product(row, competitor_list, threshold, ai_engine):
    """معالجة منتج واحد (Fuzzy -> AI Check)"""
    our_name = row.get('name', '')
    our_price = row.get('price', 0)
    
    if not our_name: return None

    best_match = None
    best_score = 0
    
    # 1. البحث السريع (RapidFuzz)
    for comp in competitor_list:
        score = calculate_fuzzy_score(our_name, comp['name'])
        
        # تحسين النتيجة إذا تطابق الحجم
        s1 = extract_size(our_name)
        s2 = extract_size(comp['name'])
        if s1 and s2 and s1 == s2:
            score += 5  # بونص للحجم الصحيح
        elif s1 and s2 and s1 != s2:
            score -= 15 # عقوبة قوية للحجم الخطأ
            
        if score > best_score:
            best_score = score
            best_match = comp

    # 2. اتخاذ القرار المبدئي
    decision = "مفقود"
    final_score = best_score
    matched_product = "غير موجود"
    matched_price = 0
    ai_confidence = 0
    ai_reason = "لم يتم التحقق"

    if best_match and best_score >= threshold:
        matched_product = best_match['name']
        matched_price = best_match['price']
        
        # 3. التحقق الذكي (Hybrid AI Check)
        # نستخدم AI فقط للحالات التي تحتاج تأكيد (لتقليل التكلفة وتسريع العمل)
        # أو إذا طلب المستخدم "دقة قصوى" (يمكن تفعيلها دائماً)
        if ai_engine and best_score < 95: # إذا لم تكن المطابقة 100% واضحة
            ai_check = ai_engine.verify_match_deep(
                our_name, our_price, matched_product, matched_price
            )
            if ai_check.get('match'):
                final_score = 99 # رفعنا الثقة لأن AI أكدها
                ai_confidence = ai_check.get('confidence', 90)
                ai_reason = ai_check.get('reason', 'AI Confirm')
            else:
                final_score = 40 # خفضنا الثقة لأن AI رفضها
                ai_reason = ai_check.get('reason', 'AI Reject')

        # تحديد القرار السعري
        if final_score >= threshold:
            diff_perc = ((matched_price - our_price) / our_price) * 100 if our_price else 0
            if diff_perc > 10: decision = "رفع سعر"
            elif diff_perc < -5: decision = "خفض سعر"
            else: decision = "موافق"
        else:
            decision = "يحتاج مراجعة" # وجدنا شبيه لكن لسنا متأكدين

    return {
        'our_product': our_name,
        'our_price': our_price,
        'competitor_product': matched_product,
        'competitor_price': matched_price,
        'match_score': round(final_score, 1),
        'price_diff': matched_price - our_price if matched_price else 0,
        'decision': decision,
        'ai_reason': ai_reason
    }

# --- دالة الدفعة الرئيسية (Parallel Batch) ---
def batch_match_products(df_our, df_comp, 
                         our_col='name', our_price_col='price',
                         comp_col='name', comp_price_col='price',
                         threshold=None, ai_engine=None, progress_callback=None):
    
    # قراءة الإعدادات
    if threshold is None:
        threshold = st.session_state.get('match_threshold', 80)

    # تجهيز البيانات
    our_data = df_our.rename(columns={our_col: 'name', our_price_col: 'price'}).to_dict('records')
    comp_list = df_comp.rename(columns={comp_col: 'name', comp_price_col: 'price'}).to_dict('records')
    
    results = []
    total = len(our_data)
    
    # المعالجة المتوازية (Magic happens here 🚀)
    # نستخدم 10 عمال (Workers) لتسريع العملية 10 أضعاف
    with ThreadPoolExecutor(max_workers=10) as executor:
        # إرسال المهام
        futures = []
        for row in our_data:
            futures.append(
                executor.submit(process_single_product, row, comp_list, threshold, ai_engine)
            )
        
        # تجميع النتائج وتحديث شريط التقدم
        for i, future in enumerate(futures):
            res = future.result()
            if res:
                results.append(res)
            if progress_callback:
                progress_callback(i + 1, total)

    return pd.DataFrame(results)
