"""
🎯 نظام التسعير الذكي للعطور - V16 Pro (النسخة الكاملة)
إصلاح أخطاء التنقل + تفعيل كافة صفحات المنتجات + ربط Make.com
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# الاستيراد من الوحدات
from styles import apply_custom_styles, ICONS, COLORS
from config import Config
from matcher import batch_match_products
from ai_helper import PerfumeAI
from db_manager import DatabaseManager
from make_integration import MakeIntegration

# ── إعداد الصفحة ────────────────────────────────────────────
st.set_page_config(
    page_title="نظام مهووس Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التصميم
st.markdown(apply_custom_styles(), unsafe_allow_html=True)

# تهيئة الخدمات
Config.init_session_state()
db = DatabaseManager()
ai = PerfumeAI()
make = MakeIntegration()

# ══════════════════════════════════════════════════════════════
#  الشريط الجانبي
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"<h1 style='text-align: center; color: #fbbf24;'>{ICONS['gem']} مهووس Pro</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # القائمة الرئيسية
    sections = {
        f"{ICONS['dashboard']} لوحة القيادة": "dashboard",
        f"{ICONS['upload']} رفع ومعالجة": "upload",
        f"{ICONS['increase']} رفع سعر": "increase",
        f"{ICONS['decrease']} خفض سعر": "decrease",
        f"{ICONS['ok']} موافق عليها": "ok",
        f"{ICONS['missing']} مفقودة": "missing",
        f"{ICONS['review']} مراجعة يدوية": "review",
        f"{ICONS['ai']} مستشار AI": "ai_analyzer",
        f"{ICONS['settings']} الإعدادات": "settings"
    }
    
    selected_label = st.radio("القائمة", list(sections.keys()), label_visibility="collapsed")
    # تصحيح الخطأ: حفظ القسم المختار في session_state
    st.session_state['current_section'] = sections[selected_label]

    if st.session_state.get('results_df') is not None:
        st.markdown("---")
        st.metric("إجمالي المنتجات", len(st.session_state['results_df']))

# ══════════════════════════════════════════════════════════════
#  المحتوى الرئيسي
# ══════════════════════════════════════════════════════════════

curr = st.session_state['current_section']

# 1. لوحة القيادة
if curr == 'dashboard':
    st.markdown(f"# {ICONS['dashboard']} لوحة القيادة")
    if st.session_state.get('results_df') is None:
        st.info("👋 ابدأ برفع الملفات من قسم 'رفع ومعالجة'")
    else:
        res = st.session_state['results_df']
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("المنتجات", len(res))
        with c2: st.metric("رفع سعر", len(res[res['decision']=='رفع سعر']))
        with c3: st.metric("خفض سعر", len(res[res['decision']=='خفض سعر']))
        with c4: st.metric("دقة المطابقة", f"{res['match_score'].mean():.1f}%")
        
        st.markdown("---")
        fig = px.pie(res, names='decision', color='decision', 
                     color_discrete_map={'رفع سعر':'#dc2626', 'خفض سعر':'#d97706', 'موافق':'#059669'})
        st.plotly_chart(fig, use_container_width=True)

# 2. رفع ومعالجة
elif curr == 'upload':
    st.markdown(f"# {ICONS['upload']} رفع ومعالجة الملفات")
    u1, u2 = st.columns(2)
    with u1: f1 = st.file_uploader("ملف منتجاتك", type=['csv', 'xlsx'])
    with u2: f2 = st.file_uploader("ملف المنافس", type=['csv', 'xlsx'])

    if f1 and f2:
        df1 = pd.read_csv(f1) if f1.name.endswith('.csv') else pd.read_excel(f1)
        df2 = pd.read_csv(f2) if f2.name.endswith('.csv') else pd.read_excel(f2)
        
        col_n = st.selectbox("عمود الاسم (عندك)", df1.columns)
        col_p = st.selectbox("عمود السعر (عندك)", df1.columns)
        col_cn = st.selectbox("عمود الاسم (المنافس)", df2.columns)
        col_cp = st.selectbox("عمود السعر (المنافس)", df2.columns)

        if st.button("🚀 بدء المطابقة الذكية", type="primary"):
            prog = st.progress(0)
            res_df = batch_match_products(
                df1, df2, our_col=col_n, our_price_col=col_p,
                comp_col=col_cn, comp_price_col=col_cp,
                ai_engine=ai, progress_callback=lambda c, t: prog.progress(c/t)
            )
            st.session_state['results_df'] = res_df
            st.success("تمت المعالجة!")
            st.rerun()

# 3. صفحات المنتجات المفلترة (رفع / خفض / موافق / مفقود / مراجعة)
elif curr in ['increase', 'decrease', 'ok', 'missing', 'review']:
    titles = {'increase': "رفع سعر", 'decrease': "خفض سعر", 'ok': "موافق عليها", 'missing': "مفقودة", 'review': "مراجعة"}
    st.markdown(f"# {titles[curr]}")
    
    if st.session_state.get('results_df') is not None:
        res = st.session_state['results_df']
        # الفلترة بناءً على القرار المكتوب في matcher.py
        filtered = res[res['decision'] == titles[curr]]
        
        if filtered.empty:
            st.success("لا توجد منتجات في هذا القسم.")
        else:
            st.dataframe(filtered, use_container_width=True)
            
            # زر إرسال لميك (Make.com) للأقسام التي تحتاج تغيير
            if curr in ['increase', 'decrease']:
                if st.button(f"🚀 إرسال هذه القائمة ({len(filtered)}) إلى المتجر فوراً"):
                    with st.spinner("جاري التحديث..."):
                        success, msg = make.send_price_updates(filtered.to_dict('records'))
                        if success: st.success(msg)
                        else: st.error(msg)
    else:
        st.warning("يرجى معالجة الملفات أولاً.")

# 4. مستشار AI
elif curr == 'ai_analyzer':
    st.markdown(f"# {ICONS['ai']} مستشار التسعير الذكي")
    user_q = st.chat_input("اسأل عن حالة السوق أو منتج معين...")
    if user_q:
        with st.chat_message("assistant"):
            st.write(ai.chat(user_q))

# 5. الإعدادات
elif curr == 'settings':
    st.markdown(f"# {ICONS['settings']} الإعدادات والربط")
    st.subheader("🔗 روابط Make.com النشطة")
    p_h, n_h = Config.get_make_webhooks()
    st.text_input("رابط تحديث الأسعار", p_h, disabled=True)
    st.text_input("رابط المنتجات الجديدة", n_h, disabled=True)
    
    if st.button("🗑️ مسح النتائج الحالية"):
        st.session_state['results_df'] = None
        st.success("تم المسح.")
        st.rerun()
