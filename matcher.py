# ══════════════════════════════════════════════════════════════
# matcher.py — المحرك المطور (V16) مع إصلاح الاستيرادات
# ══════════════════════════════════════════════════════════════
import re
import pandas as pd
import streamlit as st  # تم إضافة هذا السطر لإصلاح خطأ NameError
from rapidfuzz import fuzz
from concurrent.futures import ThreadPoolExecutor
from config import Config

# --- دوال المساعدة ---
def clean_text(text):
    if not isinstance(text, str): return ""
    return re.sub(r'[^\w\s]', ' ', text.lower()).strip()

def extract_size(text):
    match = re.search(r'(\d+)\s*(ml|مل)', text.lower())
    return int(match.group(1)) if match else 0

def calculate_fuzzy_score(name1, name2):
    n1, n2 = clean_text(name1), clean_text(name2)
    return (fuzz.ratio(n1, n2) * 0.2) + (fuzz.partial_ratio(n1, n2) * 0.3) + (fuzz.token_sort_ratio(n1, n2) * 0.5)

# --- المعالج الفردي (هنا يحدث ربط الذكاء 🤖) ---
def process_single_product(row, competitor_list, threshold, ai_engine):
    our_name = row.get('name', '')
    our_price = row.get('price', 0)
    
    if not our_name: return None

    best_match = None
    best_score = 0
    
    # 1. البحث السريع (Fuzzy Matching)
    for comp in competitor_list:
        score = calculate_fuzzy_score(our_name, comp['name'])
        s1, s2 = extract_size(our_name), extract_size(comp['name'])
        if s1 and s2 and s1 == s2: score += 5
        elif s1 and s2 and s1 != s2: score -= 15
            
        if score > best_score:
            best_score = score
            best_match = comp

    # إعدادات افتراضية للنتائج
    final_score = best_score
    ai_reason = "تطابق نصي مباشر"

    # 🟢 هنا "ربط الذكاء": إذا كانت النتيجة غير مؤكدة (أقل من 95%)، نستخدم OpenRouter
    if best_match and best_score >= threshold:
        if ai_engine and best_score < 95: 
            # استدعاء التحقق العميق من ai_helper.py
            ai_check = ai_engine.verify_match_deep(
                our_name, our_price, best_match['name'], best_match['price']
            )
            if ai_check.get('match'):
                final_score = 99 
                ai_reason = f"تأكيد AI: {ai_check.get('reason')}"
            else:
                final_score = 40 
                ai_reason = f"رفض AI: {ai_check.get('reason')}"

    # تحديد القرار النهائي
    decision = "مفقود"
    matched_product = best_match['name'] if best_match else "غير موجود"
    matched_price = best_match['price'] if best_match else 0
    
    if final_score >= threshold:
        diff_perc = ((matched_price - our_price) / our_price) * 100 if our_price else 0
        if diff_perc > 10: decision = "رفع سعر"
        elif diff_perc < -5: decision = "خفض سعر"
        else: decision = "موافق"
    elif best_match:
        decision = "يحتاج مراجعة"

    return {
        'our_product': our_name,
        'our_price': our_price,
        'competitor_product': matched_product,
        'competitor_price': matched_price,
        'match_score': round(final_score, 1),
        'decision': decision,
        'ai_reason': ai_reason
    }

# --- دالة الدفعة الرئيسية ---
def batch_match_products(df_our, df_comp, our_col='name', our_price_col='price',
                         comp_col='name', comp_price_col='price',
                         threshold=None, ai_engine=None, progress_callback=None):
    
    # استخدام st.session_state بشكل صحيح بعد الاستيراد
    if threshold is None:
        threshold = st.session_state.get('match_threshold', 80)

    our_data = df_our.rename(columns={our_col: 'name', our_price_col: 'price'}).to_dict('records')
    comp_list = df_comp.rename(columns={comp_col: 'name', comp_price_col: 'price'}).to_dict('records')
    
    results = []
    total = len(our_data)
    
    # المعالجة المتوازية (الخلفية)
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_single_product, row, comp_list, threshold, ai_engine) for row in our_data]
        for i, future in enumerate(futures):
            res = future.result()
            if res: results.append(res)
            if progress_callback: progress_callback(i + 1, total)

    return pd.DataFrame(results)
