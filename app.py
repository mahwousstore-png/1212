"""
🎯 نظام التسعير الذكي للعطور - Pro
نظام احترافي متكامل مع ذكاء اصطناعي مدمج
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

# إعداد الصفحة
st.set_page_config(
    page_title="نظام التسعير الذكي - مهووس",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق التصميم
st.markdown(apply_custom_styles(), unsafe_allow_html=True)

# تهيئة
Config.init_session_state()
db = DatabaseManager()

# تهيئة الذكاء الاصطناعي
api_key = Config.get_api_key()
ai = PerfumeAI(api_key)

# =======================
# الشريط الجانبي - القائمة
# =======================

with st.sidebar:
    st.markdown(f"<h1 style='text-align: center; color: #fbbf24;'>{ICONS['gem']} مهووس للعطور</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # حالة الاتصال بالذكاء الاصطناعي
    if ai.is_connected:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: #10b981; border-radius: 8px; color: white;'>
            {ICONS['check']} الذكاء الاصطناعي متصل
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: #ef4444; border-radius: 8px; color: white;'>
            {ICONS['warning']} الذكاء الاصطناعي غير متصل
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # القائمة الرئيسية
    st.markdown("### 📂 الأقسام")
    
    sections = {
        f"{ICONS['dashboard']} لوحة القيادة": "dashboard",
        f"{ICONS['upload']} رفع الملفات": "upload",
        f"{ICONS['increase']} رفع سعر": "increase",
        f"{ICONS['decrease']} خفض سعر": "decrease",
        f"{ICONS['ok']} موافق عليها": "ok",
        f"{ICONS['missing']} منتجات مفقودة": "missing",
        f"{ICONS['review']} يحتاج مراجعة": "review",
        f"{ICONS['ai']} AI محلل ذكي": "ai_analyzer",
        f"{ICONS['settings']} الإعدادات": "settings"
    }
    
    current_section = st.radio(
        "اختر القسم",
        list(sections.keys()),
        label_visibility="collapsed"
    )
    
    st.session_state['current_section'] = sections[current_section]
    
    st.markdown("---")
    
    # إحصائيات سريعة
    if st.session_state.get('results_df') is not None and len(st.session_state['results_df']) > 0:
        st.markdown("### 📊 إحصائيات سريعة")
        results = st.session_state['results_df']
        
        total = len(results)
        st.metric("إجمالي المنتجات", total)
        
        decisions = results['decision'].value_counts()
        if 'رفع سعر' in decisions:
            st.metric("رفع سعر", decisions['رفع سعر'], delta=f"{decisions['رفع سعر']/total*100:.1f}%")
        if 'خفض سعر' in decisions:
            st.metric("خفض سعر", decisions['خفض سعر'], delta=f"{decisions['خفض سعر']/total*100:.1f}%")
    
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: white; font-size: 0.9rem;'>
        {ICONS['crown']} نظام التسعير الذكي v2.0<br>
        {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </div>
    """, unsafe_allow_html=True)


# =======================
# المحتوى الرئيسي
# =======================

# === لوحة القيادة ===
if st.session_state['current_section'] == 'dashboard':
    st.markdown(f"# {ICONS['dashboard']} لوحة القيادة")
    st.markdown("### نظرة عامة على جميع المنتجات والقرارات")
    
    if st.session_state.get('results_df') is None or len(st.session_state['results_df']) == 0:
        st.info(f"{ICONS['info']} قم برفع الملفات أولاً من قسم 'رفع الملفات' لبدء المقارنة")
    else:
        results = st.session_state['results_df']
        
        # إحصائيات رئيسية
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(results)
        decisions = results['decision'].value_counts()
        
        with col1:
            st.markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, #3b82f6, #2563eb);'>
                <div style='font-size: 3rem;'>{ICONS['chart']}</div>
                <div style='font-size: 2.5rem; font-weight: 700; color: white;'>{total}</div>
                <div style='font-size: 1.2rem; color: #dbeafe;'>إجمالي المنتجات</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            increase_count = decisions.get('رفع سعر', 0)
            st.markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, #dc2626, #b91c1c);'>
                <div style='font-size: 3rem;'>{ICONS['increase']}</div>
                <div style='font-size: 2.5rem; font-weight: 700; color: white;'>{increase_count}</div>
                <div style='font-size: 1.2rem; color: #fee2e2;'>رفع سعر ({increase_count/total*100:.1f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            decrease_count = decisions.get('خفض سعر', 0)
            st.markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, #d97706, #b45309);'>
                <div style='font-size: 3rem;'>{ICONS['decrease']}</div>
                <div style='font-size: 2.5rem; font-weight: 700; color: white;'>{decrease_count}</div>
                <div style='font-size: 1.2rem; color: #fef3c7;'>خفض سعر ({decrease_count/total*100:.1f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            ok_count = decisions.get('موافق', 0)
            st.markdown(f"""
            <div class='metric-card' style='background: linear-gradient(135deg, #059669, #047857);'>
                <div style='font-size: 3rem;'>{ICONS['ok']}</div>
                <div style='font-size: 2.5rem; font-weight: 700; color: white;'>{ok_count}</div>
                <div style='font-size: 1.2rem; color: #d1fae5;'>موافق ({ok_count/total*100:.1f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # رسم بياني للتوزيع
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 توزيع القرارات")
            fig = px.pie(
                values=decisions.values,
                names=decisions.index,
                color=decisions.index,
                color_discrete_map={
                    'رفع سعر': '#dc2626',
                    'خفض سعر': '#d97706',
                    'موافق': '#059669',
                    'مفقود': '#2563eb',
                    'يحتاج مراجعة': '#ea580c'
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400, font=dict(size=14, family='Cairo'))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 💰 توزيع فروق الأسعار")
            # فلترة البيانات (إزالة القيم المفقودة)
            price_diff_data = results[results['decision'] != 'مفقود']['price_diff'].dropna()
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=price_diff_data,
                nbinsx=30,
                marker_color='#3b82f6',
                marker_line=dict(color='white', width=1)
            ))
            fig.update_layout(
                height=400,
                xaxis_title="فرق السعر (ريال)",
                yaxis_title="عدد المنتجات",
                font=dict(size=14, family='Cairo')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # جدول عينة من النتائج
        st.markdown("### 📋 عينة من النتائج")
        sample = results.head(10).copy()
        
        # تنسيق العرض
        display_df = pd.DataFrame({
            'منتجنا': sample['our_product'],
            'سعرنا': sample['our_price'].apply(lambda x: f"{x:.2f} ريال"),
            'منتج المنافس': sample['competitor_product'],
            'سعر المنافس': sample['competitor_price'].apply(lambda x: f"{x:.2f} ريال" if x > 0 else "-"),
            'الفرق': sample['price_diff'].apply(lambda x: f"{x:+.2f} ريال" if pd.notna(x) else "-"),
            'المطابقة': sample['match_score'].apply(lambda x: f"{x:.1f}%" if x > 0 else "-"),
            'القرار': sample['decision']
        })
        
        st.dataframe(display_df, use_container_width=True, height=400)
        
        # زر AI للتحليل الشامل
        if ai.is_connected:
            st.markdown("---")
            if st.button(f"{ICONS['ai']} تحليل شامل بالذكاء الاصطناعي", key="dashboard_ai"):
                with st.spinner("🔄 جاري التحليل..."):
                    insights = ai.get_market_insights(results)
                    st.markdown("### 🤖 رؤى السوق من الذكاء الاصطناعي")
                    st.info(insights)


# === رفع الملفات ===
elif st.session_state['current_section'] == 'upload':
    st.markdown(f"# {ICONS['upload']} رفع الملفات ومعالجتها")
    st.markdown("### قم برفع ملف منتجاتك وملف المنافس للمقارنة")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {ICONS['gem']} ملف منتجاتنا")
        our_file = st.file_uploader(
            "ملف Excel أو CSV",
            type=['xlsx', 'xls', 'csv'],
            key="our_file",
            help="ملف يحتوي على منتجاتنا وأسعارنا"
        )
        
        if our_file:
            try:
                if our_file.name.endswith('.csv'):
                    df = pd.read_csv(our_file)
                else:
                    df = pd.read_excel(our_file)
                
                st.success(f"✅ تم تحميل {len(df)} منتج")
                st.session_state['our_products_df'] = df
                
                # عرض عينة
                with st.expander("عرض عينة من البيانات"):
                    st.dataframe(df.head(10), use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
    
    with col2:
        st.markdown(f"### {ICONS['fire']} ملف المنافس")
        comp_file = st.file_uploader(
            "ملف Excel أو CSV",
            type=['xlsx', 'xls', 'csv'],
            key="comp_file",
            help="ملف يحتوي على منتجات المنافس وأسعاره"
        )
        
        if comp_file:
            try:
                if comp_file.name.endswith('.csv'):
                    df = pd.read_csv(comp_file)
                else:
                    df = pd.read_excel(comp_file)
                
                st.success(f"✅ تم تحميل {len(df)} منتج")
                st.session_state['competitor_products_df'] = df
                
                # عرض عينة
                with st.expander("عرض عينة من البيانات"):
                    st.dataframe(df.head(10), use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف: {str(e)}")
    
    # إعدادات المعالجة
    if st.session_state.get('our_products_df') is not None and st.session_state.get('competitor_products_df') is not None:
        st.markdown("---")
        st.markdown("### ⚙️ إعدادات المعالجة")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # اختيار أعمدة منتجاتنا
            our_cols = list(st.session_state['our_products_df'].columns)
            our_name_col = st.selectbox("عمود اسم المنتج (منتجاتنا)", our_cols, key="our_name_col")
            our_price_col = st.selectbox("عمود السعر (منتجاتنا)", our_cols, key="our_price_col")
        
        with col2:
            # اختيار أعمدة المنافس
            comp_cols = list(st.session_state['competitor_products_df'].columns)
            comp_name_col = st.selectbox("عمود اسم المنتج (المنافس)", comp_cols, key="comp_name_col")
            comp_price_col = st.selectbox("عمود السعر (المنافس)", comp_cols, key="comp_price_col")
        
        with col3:
            threshold = st.slider(
                "نسبة المطابقة الدنيا",
                min_value=50,
                max_value=95,
                value=75,
                step=5,
                help="النسبة الدنيا لقبول المطابقة"
            )
            st.session_state['match_threshold'] = threshold
            
            competitor_name = st.text_input(
                "اسم المنافس",
                value="منافس عام",
                help="اسم المنافس للتمييز"
            )
            st.session_state['competitor_name'] = competitor_name
        
        # زر المعالجة
        st.markdown("---")
        col1, col2, col3 = st.columns([1,2,1])
        
        with col2:
            if st.button(
                f"{ICONS['rocket']} بدء المعالجة والمقارنة",
                key="start_processing",
                use_container_width=True,
                type="primary"
            ):
                st.session_state['processing_started'] = True
        
        # المعالجة
        if st.session_state.get('processing_started'):
            st.markdown("---")
            st.markdown(f"### {ICONS['time']} جاري المعالجة...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            time_text = st.empty()
            
            start_time = time.time()
            
            def update_progress(current, total):
                progress = current / total
                progress_bar.progress(progress)
                elapsed = time.time() - start_time
                status_text.markdown(f"**معالجة:** {current} / {total} منتج")
                time_text.markdown(f"**الوقت المنقضي:** {elapsed:.1f} ثانية")
            
            try:
                # المطابقة
                results_df = batch_match_products(
                    st.session_state['our_products_df'],
                    st.session_state['competitor_products_df'],
                    our_name_col=our_name_col,
                    our_price_col=our_price_col,
                    comp_name_col=comp_name_col,
                    comp_price_col=comp_price_col,
                    threshold=threshold,
                    progress_callback=update_progress
                )
                
                # حفظ النتائج
                st.session_state['results_df'] = results_df
                db.save_results(results_df, competitor_name)
                
                elapsed_time = time.time() - start_time
                
                st.success(f"✅ تمت المعالجة بنجاح! ({elapsed_time:.1f} ثانية)")
                st.success(f"📊 تم العثور على {len(results_df)} مطابقة")
                
                # إحصائيات سريعة
                decisions = results_df['decision'].value_counts()
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("رفع سعر", decisions.get('رفع سعر', 0))
                with col2:
                    st.metric("خفض سعر", decisions.get('خفض سعر', 0))
                with col3:
                    st.metric("موافق", decisions.get('موافق', 0))
                with col4:
                    st.metric("مفقود", decisions.get('مفقود', 0))
                
                st.session_state['processing_started'] = False
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ خطأ في المعالجة: {str(e)}")
                st.session_state['processing_started'] = False


# === رفع سعر ===
elif st.session_state['current_section'] == 'increase':
    st.markdown(f"# {ICONS['increase']} منتجات تحتاج رفع سعر")
    st.markdown("### المنتجات التي سعرنا أقل من المنافس بأكثر من 10%")
    
    if st.session_state.get('results_df') is None:
        st.info(f"{ICONS['info']} قم برفع الملفات أولاً")
    else:
        results = st.session_state['results_df']
        increase_df = results[results['decision'] == 'رفع سعر'].copy()
        
        if len(increase_df) == 0:
            st.success(f"{ICONS['check']} لا توجد منتجات تحتاج رفع سعر!")
        else:
            st.warning(f"⚠️ {len(increase_df)} منتج يحتاج رفع سعر")
            
            # عرض الجدول مع أزرار AI
            for idx, row in increase_df.head(20).iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**منتجنا:** {row['our_product']}")
                        st.markdown(f"**المنافس:** {row['competitor_product']}")
                    
                    with col2:
                        st.markdown(f"**سعرنا:** {row['our_price']:.2f} ريال")
                        st.markdown(f"**سعر المنافس:** {row['competitor_price']:.2f} ريال")
                    
                    with col3:
                        diff = row['price_diff']
                        diff_percent = row['price_diff_percent']
                        st.markdown(f"**الفرق:** {diff:+.2f} ريال")
                        st.markdown(f"**النسبة:** {diff_percent:+.1f}%")
                    
                    with col4:
                        if ai.is_connected:
                            if st.button(f"{ICONS['ai']}", key=f"ai_inc_{idx}"):
                                with st.spinner("تحليل..."):
                                    analysis = ai.analyze_pricing_decision(
                                        row['our_product'],
                                        row['our_price'],
                                        row['competitor_product'],
                                        row['competitor_price']
                                    )
                                    st.info(f"**القرار:** {analysis.get('decision')}\n\n**السبب:** {analysis.get('reason')}\n\n**السعر المقترح:** {analysis.get('suggested_price', 0):.2f} ريال")
                    
                    st.markdown("---")


# === خفض سعر ===
elif st.session_state['current_section'] == 'decrease':
    st.markdown(f"# {ICONS['decrease']} منتجات تحتاج خفض سعر")
    st.markdown("### المنتجات التي سعرنا أعلى من المنافس بأكثر من 5%")
    
    if st.session_state.get('results_df') is None:
        st.info(f"{ICONS['info']} قم برفع الملفات أولاً")
    else:
        results = st.session_state['results_df']
        decrease_df = results[results['decision'] == 'خفض سعر'].copy()
        
        if len(decrease_df) == 0:
            st.success(f"{ICONS['check']} لا توجد منتجات تحتاج خفض سعر!")
        else:
            st.warning(f"⚠️ {len(decrease_df)} منتج يحتاج خفض سعر")
            
            for idx, row in decrease_df.head(20).iterrows():
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**منتجنا:** {row['our_product']}")
                        st.markdown(f"**المنافس:** {row['competitor_product']}")
                    
                    with col2:
                        st.markdown(f"**سعرنا:** {row['our_price']:.2f} ريال")
                        st.markdown(f"**سعر المنافس:** {row['competitor_price']:.2f} ريال")
                    
                    with col3:
                        diff = row['price_diff']
                        diff_percent = row['price_diff_percent']
                        st.markdown(f"**الفرق:** {diff:+.2f} ريال")
                        st.markdown(f"**النسبة:** {diff_percent:+.1f}%")
                    
                    with col4:
                        if ai.is_connected:
                            if st.button(f"{ICONS['ai']}", key=f"ai_dec_{idx}"):
                                with st.spinner("تحليل..."):
                                    analysis = ai.analyze_pricing_decision(
                                        row['our_product'],
                                        row['our_price'],
                                        row['competitor_product'],
                                        row['competitor_price']
                                    )
                                    st.info(f"**القرار:** {analysis.get('decision')}\n\n**السبب:** {analysis.get('reason')}\n\n**السعر المقترح:** {analysis.get('suggested_price', 0):.2f} ريال")
                    
                    st.markdown("---")


# === موافق عليها ===
elif st.session_state['current_section'] == 'ok':
    st.markdown(f"# {ICONS['ok']} منتجات موافق عليها")
    st.markdown("### المنتجات ضمن النطاق المقبول (±5%)")
    
    if st.session_state.get('results_df') is None:
        st.info(f"{ICONS['info']} قم برفع الملفات أولاً")
    else:
        results = st.session_state['results_df']
        ok_df = results[results['decision'] == 'موافق'].copy()
        
        st.success(f"✅ {len(ok_df)} منتج بأسعار مناسبة")
        
        if len(ok_df) > 0:
            display_df = pd.DataFrame({
                'منتجنا': ok_df['our_product'],
                'سعرنا': ok_df['our_price'].apply(lambda x: f"{x:.2f} ريال"),
                'منتج المنافس': ok_df['competitor_product'],
                'سعر المنافس': ok_df['competitor_price'].apply(lambda x: f"{x:.2f} ريال"),
                'الفرق': ok_df['price_diff'].apply(lambda x: f"{x:+.2f} ريال"),
                'المطابقة': ok_df['match_score'].apply(lambda x: f"{x:.1f}%")
            })
            
            st.dataframe(display_df, use_container_width=True, height=600)


# === منتجات مفقودة ===
elif st.session_state['current_section'] == 'missing':
    st.markdown(f"# {ICONS['missing']} منتجات مفقودة")
    st.markdown("### المنتجات غير الموجودة عند المنافس")
    
    if st.session_state.get('results_df') is None:
        st.info(f"{ICONS['info']} قم برفع الملفات أولاً")
    else:
        results = st.session_state['results_df']
        missing_df = results[results['decision'] == 'مفقود'].copy()
        
        st.info(f"ℹ️ {len(missing_df)} منتج غير موجود عند المنافس")
        
        if len(missing_df) > 0:
            display_df = pd.DataFrame({
                'منتجنا': missing_df['our_product'],
                'سعرنا': missing_df['our_price'].apply(lambda x: f"{x:.2f} ريال"),
                'الحالة': ['غير موجود عند المنافس'] * len(missing_df)
            })
            
            st.dataframe(display_df, use_container_width=True, height=600)


# === يحتاج مراجعة ===
elif st.session_state['current_section'] == 'review':
    st.markdown(f"# {ICONS['review']} يحتاج مراجعة")
    st.markdown("### المنتجات بمطابقة منخفضة (< 85%)")
    
    if st.session_state.get('results_df') is None:
        st.info(f"{ICONS['info']} قم برفع الملفات أولاً")
    else:
        results = st.session_state['results_df']
        review_df = results[results['decision'] == 'يحتاج مراجعة'].copy()
        
        if len(review_df) == 0:
            st.success(f"{ICONS['check']} لا توجد منتجات تحتاج مراجعة!")
        else:
            st.warning(f"⚠️ {len(review_df)} منتج يحتاج مراجعة يدوية")
            
            for idx, row in review_df.head(20).iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.markdown(f"**منتجنا:** {row['our_product']}")
                        st.markdown(f"**المنافس:** {row['competitor_product']}")
                    
                    with col2:
                        st.markdown(f"**المطابقة:** {row['match_score']:.1f}%")
                        st.markdown(f"**الفرق:** {row['price_diff']:+.2f} ريال")
                    
                    with col3:
                        if ai.is_connected:
                            if st.button(f"{ICONS['ai']} تحقق", key=f"ai_rev_{idx}"):
                                with st.spinner("جاري التحقق..."):
                                    verification = ai.verify_product_match(
                                        row['our_product'],
                                        row['competitor_product'],
                                        row['our_price'],
                                        row['competitor_price'],
                                        row['match_score']
                                    )
                                    
                                    if verification['verified']:
                                        st.success(f"✅ متطابق ({verification['confidence']}%)\n\n{verification['explanation']}")
                                    else:
                                        st.error(f"❌ غير متطابق\n\n{verification['explanation']}")
                    
                    st.markdown("---")


# === AI محلل ذكي ===
elif st.session_state['current_section'] == 'ai_analyzer':
    st.markdown(f"# {ICONS['ai']} AI المحلل الذكي")
    st.markdown("### محادثة مع خبير التسعير الذكي")
    
    if not ai.is_connected:
        st.error("❌ الذكاء الاصطناعي غير متصل. قم بإدخال API Key في الإعدادات")
    else:
        st.success("✅ الذكاء الاصطناعي متصل وجاهز")
        
        # محادثة
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        
        # عرض المحادثات السابقة
        for msg in st.session_state['chat_history']:
            if msg['role'] == 'user':
                st.markdown(f"**أنت:** {msg['content']}")
            else:
                st.info(f"**AI:** {msg['content']}")
            st.markdown("---")
        
        # إدخال جديد
        user_input = st.text_area(
            "اسأل خبير التسعير",
            placeholder="مثال: ما رأيك في استراتيجية التسعير الحالية؟",
            height=100
        )
        
        if st.button(f"{ICONS['rocket']} إرسال", type="primary"):
            if user_input:
                # إضافة سؤال المستخدم
                st.session_state['chat_history'].append({
                    'role': 'user',
                    'content': user_input
                })
                
                # الحصول على رد AI
                with st.spinner("🤖 AI يفكر..."):
                    context = {}
                    if st.session_state.get('results_df') is not None:
                        context['total_products'] = len(st.session_state['results_df'])
                        context['decisions'] = st.session_state['results_df']['decision'].value_counts().to_dict()
                    
                    response = ai.chat(user_input, context)
                    
                    st.session_state['chat_history'].append({
                        'role': 'ai',
                        'content': response
                    })
                
                st.rerun()


# === الإعدادات ===
elif st.session_state['current_section'] == 'settings':
    st.markdown(f"# {ICONS['settings']} الإعدادات")
    st.markdown("### إعدادات النظام والذكاء الاصطناعي")
    
    tab1, tab2 = st.tabs([f"{ICONS['ai']} الذكاء الاصطناعي", f"{ICONS['chart']} النظام"])
    
    with tab1:
        st.markdown("### 🔑 Gemini API Key")
        
        current_key = Config.get_api_key()
        if current_key:
            st.success("✅ API Key محفوظ")
            masked_key = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "***"
            st.code(masked_key)
        
        new_key = st.text_input(
            "أدخل Gemini API Key الجديد",
            type="password",
            help="احصل على مفتاح مجاني من https://makersuite.google.com/app/apikey"
        )
        
        if st.button("حفظ API Key", type="primary"):
            if new_key:
                Config.set_api_key(new_key)
                db.save_setting('gemini_api_key', new_key)
                st.success("✅ تم الحفظ! أعد تشغيل التطبيق")
                st.rerun()
            else:
                st.error("❌ الرجاء إدخال المفتاح")
        
        # اختبار الاتصال
        st.markdown("---")
        if st.button("🧪 اختبار الاتصال"):
            if ai.is_connected:
                with st.spinner("جاري الاختبار..."):
                    try:
                        response = ai.chat("مرحباً")
                        st.success(f"✅ الاتصال ناجح!\n\n{response}")
                    except Exception as e:
                        st.error(f"❌ فشل الاتصال: {str(e)}")
            else:
                st.error("❌ لم يتم إدخال API Key")
    
    with tab2:
        st.markdown("### ⚙️ إعدادات عامة")
        
        # مسح البيانات
        st.markdown("#### 🗑️ إدارة البيانات")
        st.warning("⚠️ هذا سيحذف جميع النتائج المحفوظة!")
        
        if st.button("مسح جميع النتائج", type="secondary"):
            db.clear_results()
            st.session_state['results_df'] = None
            st.success("✅ تم المسح!")
            st.rerun()


# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #94a3b8; padding: 2rem;'>
    {ICONS['gem']} نظام التسعير الذكي v2.0 - مهووس للعطور<br>
    {ICONS['sparkles']} Powered by Gemini AI & RapidFuzz
</div>
""", unsafe_allow_html=True)
