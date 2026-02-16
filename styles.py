"""
تصميم احترافي لنظام التسعير الذكي
أيقونات كبيرة - ألوان واضحة - تجربة مستخدم ممتازة
"""

def apply_custom_styles():
    """تطبيق التصميم المخصص"""
    return """
    <style>
    /* === الخطوط العربية === */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif !important;
    }
    
    /* === تحسين العناوين === */
    h1, h2, h3 {
        color: #1e3a8a !important;
        font-weight: 700 !important;
        text-align: right !important;
    }
    
    h1 {
        font-size: 3rem !important;
        margin-bottom: 2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        font-size: 2.2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    h3 {
        font-size: 1.8rem !important;
        margin-top: 1.5rem !important;
    }
    
    /* === القائمة الجانبية === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #fbbf24 !important;
        font-size: 2rem !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
    }
    
    /* === الأزرار === */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 0.8rem 2rem !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2) !important;
        background: linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%);
    }
    
    /* === أزرار AI الذكية === */
    .ai-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        font-size: 1.5rem !important;
    }
    
    .ai-button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    }
    
    /* === البطاقات (Cards) === */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
    }
    
    /* === الجداول === */
    .dataframe {
        font-size: 1.1rem !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .dataframe thead tr th {
        background: #1e3a8a !important;
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        padding: 1.2rem !important;
        text-align: center !important;
    }
    
    .dataframe tbody tr td {
        padding: 1rem !important;
        text-align: center !important;
        font-size: 1.1rem !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #f1f5f9 !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #e0e7ff !important;
        transition: all 0.2s ease;
    }
    
    /* === ألوان القرارات === */
    .decision-increase {
        background-color: #fee2e2 !important;
        color: #dc2626 !important;
        font-weight: 600 !important;
    }
    
    .decision-decrease {
        background-color: #fef3c7 !important;
        color: #d97706 !important;
        font-weight: 600 !important;
    }
    
    .decision-ok {
        background-color: #d1fae5 !important;
        color: #059669 !important;
        font-weight: 600 !important;
    }
    
    .decision-missing {
        background-color: #dbeafe !important;
        color: #2563eb !important;
        font-weight: 600 !important;
    }
    
    .decision-review {
        background-color: #fed7aa !important;
        color: #ea580c !important;
        font-weight: 600 !important;
    }
    
    /* === مؤشرات الحالة === */
    .status-connected {
        color: #10b981 !important;
        font-size: 1.5rem !important;
    }
    
    .status-disconnected {
        color: #ef4444 !important;
        font-size: 1.5rem !important;
    }
    
    /* === شريط التقدم === */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6, #10b981) !important;
        height: 1.5rem !important;
        border-radius: 8px !important;
    }
    
    /* === الأيقونات الكبيرة === */
    .big-icon {
        font-size: 3rem !important;
        margin: 1rem 0 !important;
        display: block;
        text-align: center;
    }
    
    /* === التنبيهات === */
    .stAlert {
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        padding: 1.5rem !important;
    }
    
    /* === Expander === */
    .streamlit-expanderHeader {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        background: #f1f5f9 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* === عداد الوقت === */
    .time-counter {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* === مقارنة بصرية === */
    .product-comparison {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .product-our {
        background: #dbeafe;
        padding: 1rem;
        border-radius: 8px;
        flex: 1;
        margin: 0 0.5rem;
    }
    
    .product-competitor {
        background: #fee2e2;
        padding: 1rem;
        border-radius: 8px;
        flex: 1;
        margin: 0 0.5rem;
    }
    
    .vs-badge {
        background: #fbbf24;
        color: #78350f;
        padding: 0.5rem 1rem;
        border-radius: 50%;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* === تحسين الإدخالات === */
    .stTextInput input, .stNumberInput input {
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
        border-radius: 8px !important;
        border: 2px solid #cbd5e1 !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* === ملف الرفع === */
    [data-testid="stFileUploader"] {
        border: 3px dashed #3b82f6 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        background: #f8fafc !important;
    }
    
    /* === تحسين التخطيط === */
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }
    
    /* === Tabs === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        border-radius: 8px 8px 0 0 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3b82f6 !important;
        color: white !important;
    }
    </style>
    """

# الأيقونات الكبيرة
ICONS = {
    "dashboard": "🏠",
    "upload": "📤",
    "increase": "🔴",
    "decrease": "🟡",
    "ok": "🟢",
    "missing": "🔵",
    "review": "⚠️",
    "ai": "🤖",
    "settings": "⚙️",
    "chart": "📊",
    "time": "⏱️",
    "check": "✅",
    "warning": "⚠️",
    "star": "⭐",
    "fire": "🔥",
    "rocket": "🚀",
    "gem": "💎",
    "crown": "👑",
    "sparkles": "✨"
}

# ألوان القرارات
COLORS = {
    "increase": "#dc2626",
    "decrease": "#d97706",
    "ok": "#059669",
    "missing": "#2563eb",
    "review": "#ea580c",
    "primary": "#1e3a8a",
    "secondary": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#06b6d4"
}
