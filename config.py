"""
ملف التكوين - إدارة الإعدادات
"""
import streamlit as st
import os

class Config:
    """إدارة الإعدادات"""
    
    @staticmethod
    def init_session_state():
        """تهيئة session state"""
        defaults = {
            'gemini_api_key': '',
            'results_df': None,
            'our_products_df': None,
            'competitor_products_df': None,
            'processing_started': False,
            'ai_connected': False,
            'current_section': 'لوحة القيادة',
            'match_threshold': 75,
            'competitor_name': 'منافس عام'
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    @staticmethod
    def get_api_key():
        """الحصول على API Key"""
        # محاولة الحصول من المتغيرات البيئية أولاً
        key = os.getenv('GEMINI_API_KEY', '')
        if key:
            return key
        
        # أو من session state
        return st.session_state.get('gemini_api_key', '')
    
    @staticmethod
    def set_api_key(key):
        """تعيين API Key"""
        st.session_state['gemini_api_key'] = key
        return True
    
    @staticmethod
    def is_ai_connected():
        """التحقق من اتصال الذكاء الاصطناعي"""
        return bool(Config.get_api_key())
