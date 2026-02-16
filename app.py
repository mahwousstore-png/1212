"""
🎯 نظام التسعير الذكي للعطور - V16 Pro
نظام احترافي متكامل: Hybrid AI (Gemini + OpenRouter) + Parallel Processing + Make.com
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# الاستيراد من الوحدات المحدثة
from styles import apply_custom_styles, ICONS, COLORS
from config import Config
from matcher import batch_match_products
from ai_helper import PerfumeAI
from db_manager import DatabaseManager

# ── إعداد الصفحة ────────────────────────────────────────────
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التصميم الاحترافي
st.markdown(apply_custom_styles(), unsafe_allow_html=True)

# ── تهيئة الخدمات ──────────────────────────────────────────
Config.init_session_state()
db = DatabaseManager()

# تهيئة المحرك الهجين (يقرأ المفاتيح تلقائياً من config)
ai = PerfumeAI()

# ══════════════════════════════════════════════════════════════
#  الشريط الجانبي - القائمة المتطورة
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(f"<h1 style='text-align: center; color: #fbbf24;'>{ICONS['gem']} مهووس Pro</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: white;'>الإصدار {Config.VERSION}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # مراقب حالة الذكاء الاصطناعي (Hybrid Status)
    status_color = "#10b981" if ai.gemini_ready and ai.openrouter_ready else "#f59e0b"
    if not ai.gemini_ready and not ai.openrouter_ready: status_color = "#ef4444"
    
    st.markdown(f"""
    <div style='padding: 0.8rem; background: {status_color}; border-radius: 10px; color: white; text-align: center;'>
        {ICONS['ai']} <b>حالة المحرك الهجين</b><br>
        <small>Gemini: {"✅" if ai.gemini_ready else "❌"} | OpenRouter: {"✅" if ai.openrouter_ready else "❌"}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # القائمة الرئيسية
    st.markdown("### 📂 الأقسام الرئيسية")
    sections = {
        f"{ICONS['dashboard']} لوحة القيادة": "dashboard",
        f"{ICONS['upload']} رفع ومعالجة": "upload",
        f"{ICONS['chart']} تحليل الأسعار": "analysis",
        f"{ICONS['ai']} مستشار AI": "ai_analyzer",
        f"{ICONS['settings']} الإعدادات والربط": "settings"
    }
    
    current_label = st.radio("القائمة", list(sections.keys()), label_visibility="collapsed")
    st.session_state['current_section'] = sections[current_label]

    # إحصائيات سريعة حية
    if st.session_state.get('results_df') is not None:
        st.markdown("---")
        st.markdown("### 📊 حالة السوق")
        res = st.session_state['results_df']
        st.metric("إجمالي المنتجات", len(res))
        dec = res['decision'].value_counts()
        st.metric("توصيات بالرفع", dec.get('رفع سعر', 0), delta_color="normal")

# ══════════════════════════════════════════════════════════════
#  المحتوى الرئيسي - لوحة القيادة
# ══════════════════════════════════════════════════════════════

if st.session_state['current_section'] == 'dashboard':
    st.markdown(f"# {ICONS['dashboard']} لوحة القيادة الذكية")
    
    if st.session_state.get('results_df') is None:
        st.info("👋 مرحباً بك! ابدأ برفع ملفات المنتجات من قسم 'رفع ومعالجة' لتشغيل التحليل.")
    else:
        results = st.session_state['results_df']
        
        # كروت الإحصائيات (KPIs)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("المنتجات", len(results), help="إجمالي المنتجات التي تمت معالجتها")
        with c2: st.metric("سعرك أعلى", len(results[results['decision']=='خفض سعر']), delta_color="inverse")
        with c3: st.metric("سعرك أقل", len(results[results['decision']=='رفع سعر']), delta_color="normal")
        with c4: st.metric("تطابق دقيق", f"{results['match_score'].mean():.1f}%", help="متوسط دقة المطابقة")

        st.markdown("---")
        
        # الرسوم البيانية
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("### 📈 توزيع القرارات")
            fig = px.pie(results, names='decision', color='decision',
                         color_discrete_map={'رفع سعر':'#dc2626', 'خفض سعر':'#d97706', 'موافق':'#059669', 'مفقود':'#2563eb', 'يحتاج مراجعة':'#ea580c'})
            st.plotly_chart(fig, use_container_width=True)
            
        with col_right:
            st.markdown("### 🤖 رؤى الذكاء الاصطناعي (Quick Scan)")
            if ai.gemini_ready:
                if st.button("توليد تقرير سريع 📄"):
                    with st.spinner("جاري قراءة بيانات السوق..."):
                        summary = ai.chat(f"حلل هذه النتائج لمتجر عطور: {results['decision'].value_counts().to_dict()}")
                        st.success(summary)
            else: st.warning("قم بإضافة مفتاح Gemini لتفعيل التقارير.")

# ══════════════════════════════════════════════════════════════
#  قسم المعالجة المتوازية (Parallel processing)
# ══════════════════════════════════════════════════════════════

elif st.session_section == 'upload':
    st.markdown(f"# {ICONS['upload']} المعالجة الذكية فائقة السرعة")
    
    u_col1, u_col2 = st.columns(2)
    with u_col1:
        f1 = st.file_uploader("ملف منتجات متجر مهووس", type=['csv', 'xlsx'])
    with u_col2:
        f2 = st.file_uploader("ملف المنافس (خبير، نايس ون، إلخ)", type=['csv', 'xlsx'])

    if f1 and f2:
        st.markdown("---")
        st.markdown("### ⚙️ إعدادات المحرك الهجين (Parallel Engine)")
        
        # تحديد الأعمدة
        df1 = pd.read_csv(f1) if f1.name.endswith('.csv') else pd.read_excel(f1)
        df2 = pd.read_csv(f2) if f2.name.endswith('.csv') else pd.read_excel(f2)
        
        c_set1, c_set2, c_set3 = st.columns(3)
        with c_set1:
            name_col = st.selectbox("عمود الاسم (عندك)", df1.columns)
            price_col = st.selectbox("عمود السعر (عندك)", df1.columns)
        with c_set2:
            c_name_col = st.selectbox("عمود الاسم (المنافس)", df2.columns)
            c_price_col = st.selectbox("عمود السعر (المنافس)", df2.columns)
        with c_set3:
            threshold = st.slider("دقة المطابقة الدنيا %", 50, 100, 80)
            use_deep_ai = st.toggle("تفعيل الفحص العميق (OpenRouter)", value=True)

        if st.button(f"{ICONS['rocket']} ابدأ المعالجة الآن", type="primary", use_container_width=True):
            with st.status("🚀 جاري المعالجة المتوازية...", expanded=True) as status:
                st.write("1. تحليل ملفات البيانات...")
                progress_bar = st.progress(0)
                
                # استدعاء المحرك المطور (matcher.py)
                results_df = batch_match_products(
                    df1, df2, 
                    our_col=name_col, our_price_col=price_col,
                    comp_col=c_name_col, comp_price_col=c_price_col,
                    threshold=threshold,
                    ai_engine=ai if use_deep_ai else None,
                    progress_callback=lambda c, t: progress_bar.progress(c/t)
                )
                
                st.session_state['results_df'] = results_df
                db.save_results(results_df, "منافس")
                status.update(label="✅ اكتملت المعالجة بنجاح!", state="complete")
            st.balloons()
            st.rerun()

# ══════════════════════════════════════════════════════════════
#  قسم تحليل الأسعار والربط مع Make.com
# ══════════════════════════════════════════════════════════════

elif st.session_state['current_section'] == 'analysis':
    st.markdown(f"# {ICONS['chart']} تحليل وتصدير القرارات")
    
    if st.session_state.get('results_df') is not None:
        res = st.session_state['results_df']
        
        # فلترة النتائج
        filter_dec = st.multiselect("تصفية حسب القرار", res['decision'].unique(), default=res['decision'].unique())
        filtered_res = res[res['decision'].isin(filter_dec)]
        
        st.dataframe(filtered_res, use_container_width=True)

        st.markdown("---")
        st.subheader(f"{ICONS['crown']} منطقة الأتمتة (Make.com Integration)")
        
        col_make1, col_make2 = st.columns([2, 1])
        with col_make1:
            st.info("سيتم إرسال كافة المنتجات التي تحمل قرار (رفع سعر / خفض سعر) إلى متجرك لتحديثها تلقائياً.")
        with col_make2:
            if st.button("🚀 تنفيذ التحديثات في المتجر الآن", type="primary", use_container_width=True):
                # تجهيز البيانات للإرسال
                updates = filtered_res[filtered_res['decision'].isin(['رفع سعر', 'خفض سعر'])].to_dict('records')
                if updates:
                    from make_integration import MakeIntegration
                    make_client = MakeIntegration()
                    success, msg = make_client.send_price_updates(updates)
                    if success: st.success(msg)
                    else: st.error(msg)
                else: st.warning("لا توجد تحديثات سعرية لإرسالها.")

# ══════════════════════════════════════════════════════════════
#  قسم الإعدادات (حفظ المفاتيح)
# ══════════════════════════════════════════════════════════════

elif st.session_state['current_section'] == 'settings':
    st.markdown(f"# {ICONS['settings']} إعدادات النظام المتقدمة")
    
    t1, t2 = st.tabs(["مفاتيح API", "روابط الربط (Webhooks)"])
    
    with t1:
        st.markdown("### 🔑 إدارة المفاتيح الذكية")
        g_key = st.text_input("Gemini API Key", value=Config.get_api_key(), type="password")
        o_key = st.text_input("OpenRouter API Key (للدقة القصوى)", value=Config.get_openrouter_key(), type="password")
        
        if st.button("حفظ المفاتيح 💾"):
            Config.set_api_keys(g_key, o_key)
            st.success("✅ تم تحديث المفاتيح بنجاح")
            st.rerun()

    with t2:
        st.markdown("### 🔗 روابط Make.com")
        p_hook, n_hook = Config.get_make_webhooks()
        st.text_input("رابط تحديث الأسعار", value=p_hook, disabled=True)
        st.text_input("رابط المنتجات الجديدة", value=n_hook, disabled=True)
        st.caption("ملاحظة: هذه الروابط مستخرجة من ملفاتك السابقة وتعمل تلقائياً.")

# ── التذييل ────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: gray;'>{ICONS['crown']} نظام مهووس V16 - تم التطوير لدعم السوق السعودي 🇸🇦</div>", unsafe_allow_html=True)
