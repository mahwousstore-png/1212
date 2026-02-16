"""
config.py — إعدادات النظام المحدثة (V16 - Hybrid AI)
يدعم: Gemini + OpenRouter + Make.com
"""
import streamlit as st
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env إذا وجد
load_dotenv()

class Config:
    """إدارة الإعدادات المركزية"""
    
    # ── ثوابت النظام ──────────────────────────────────────────
    APP_NAME = "نظام التسعير الذكي Pro"
    VERSION = "16.0"
    
    # روابط Make.com (القيم الافتراضية التي استخرجناها سابقاً)
    DEFAULT_HOOK_PRICES = "https://hook.eu2.make.com/99oljy0d6r3chwg6bdfsptcf6bk8htsd"
    DEFAULT_HOOK_PRODUCTS = "https://hook.eu2.make.com/xvubj23dmpxu8qzilstd25cnumrwtdxm"
    
    @staticmethod
    def init_session_state():
        """تهيئة متغيرات الجلسة (Session State)"""
        defaults = {
            'gemini_api_key': '',
            'openrouter_api_key': '',  # مفتاح جديد للذكاء الهجين
            'results_df': None,
            'our_products_df': None,
            'competitor_products_df': None,
            'processing_started': False,
            'ai_connected': False,
            'current_section': 'لوحة القيادة',
            'match_threshold': 80,     # رفعنا النسبة لزيادة الدقة (كانت 75)
            'verify_threshold': 90,    # نسبة التأكيد التلقائي الجديدة
            'competitor_name': 'منافس عام'
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    # ── إدارة مفاتيح الذكاء الاصطناعي ────────────────────────
    @staticmethod
    def get_api_key():
        """Get Gemini Key (للاستخدام العام)"""
        # الأولوية: المتغيرات البيئية -> أسرار Streamlit -> حالة الجلسة
        return (os.getenv('GEMINI_API_KEY') or 
                st.secrets.get('GEMINI_API_KEY') or 
                st.session_state.get('gemini_api_key', ''))

    @staticmethod
    def get_openrouter_key():
        """Get OpenRouter Key (للمطابقة الدقيقة)"""
        return (os.getenv('OPENROUTER_API_KEY') or 
                st.secrets.get('OPENROUTER_API_KEY') or 
                st.session_state.get('openrouter_api_key', ''))

    @staticmethod
    def set_api_keys(gemini_key, openrouter_key=None):
        """حفظ المفاتيح في الجلسة"""
        st.session_state['gemini_api_key'] = gemini_key
        if openrouter_key:
            st.session_state['openrouter_api_key'] = openrouter_key
        return True
    
    @staticmethod
    def is_ai_connected():
        """هل المفاتيح موجودة؟"""
        return bool(Config.get_api_key())

    # ── إدارة روابط Make.com ─────────────────────────────────
    @staticmethod
    def get_make_webhooks():
        """استرجاع روابط الأتمتة"""
        try:
            # محاولة القراءة من Secrets أولاً
            prices = st.secrets.get("HOOK_PRICES", Config.DEFAULT_HOOK_PRICES)
            products = st.secrets.get("HOOK_PRODUCTS", Config.DEFAULT_HOOK_PRODUCTS)
        except:
            # العودة للقيم الافتراضية
            prices = Config.DEFAULT_HOOK_PRICES
            products = Config.DEFAULT_HOOK_PRODUCTS
            
        return prices, products

    # ── إعدادات النماذج ──────────────────────────────────────
    @staticmethod
    def get_models():
        return {
            "fast": "google/gemini-2.0-flash-exp:free",  # للسرعة
            "smart": "openai/gpt-4o-mini"                # للدقة (عبر OpenRouter)
        }
