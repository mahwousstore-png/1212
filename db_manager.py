"""
إدارة قاعدة البيانات المحلية
حفظ دائم - لا فقدان للبيانات
"""
import sqlite3
import pandas as pd
from datetime import datetime
import json

class DatabaseManager:
    """مدير قاعدة البيانات"""
    
    def __init__(self, db_path='perfume_pricing.db'):
        """تهيئة قاعدة البيانات"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """إنشاء الجداول الأساسية"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول النتائج
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                our_product TEXT NOT NULL,
                our_price REAL,
                competitor_product TEXT,
                competitor_price REAL,
                competitor_name TEXT,
                match_score REAL,
                price_diff REAL,
                price_diff_percent REAL,
                decision TEXT,
                our_brand TEXT,
                our_size INTEGER,
                our_type TEXT,
                our_gender TEXT,
                comp_brand TEXT,
                comp_size INTEGER,
                comp_type TEXT,
                comp_gender TEXT,
                ai_verified BOOLEAN,
                ai_confidence REAL,
                ai_explanation TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول السجلات (Audit Log)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                details TEXT,
                user TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الإعدادات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_results(self, results_df, competitor_name=''):
        """حفظ النتائج في قاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        
        for _, row in results_df.iterrows():
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO results (
                    our_product, our_price, competitor_product, competitor_price,
                    competitor_name, match_score, price_diff, price_diff_percent,
                    decision, our_brand, our_size, our_type, our_gender,
                    comp_brand, comp_size, comp_type, comp_gender
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row.get('our_product', ''),
                row.get('our_price', 0),
                row.get('competitor_product', ''),
                row.get('competitor_price', 0),
                competitor_name,
                row.get('match_score', 0),
                row.get('price_diff', 0),
                row.get('price_diff_percent', 0),
                row.get('decision', ''),
                row.get('our_details', {}).get('brand', '') if isinstance(row.get('our_details'), dict) else '',
                row.get('our_details', {}).get('size', 0) if isinstance(row.get('our_details'), dict) else 0,
                row.get('our_details', {}).get('type', '') if isinstance(row.get('our_details'), dict) else '',
                row.get('our_details', {}).get('gender', '') if isinstance(row.get('our_details'), dict) else '',
                row.get('competitor_details', {}).get('brand', '') if isinstance(row.get('competitor_details'), dict) else '',
                row.get('competitor_details', {}).get('size', 0) if isinstance(row.get('competitor_details'), dict) else 0,
                row.get('competitor_details', {}).get('type', '') if isinstance(row.get('competitor_details'), dict) else '',
                row.get('competitor_details', {}).get('gender', '') if isinstance(row.get('competitor_details'), dict) else ''
            ))
        
        conn.commit()
        conn.close()
        
        self.log_action('save_results', f'تم حفظ {len(results_df)} منتج')
    
    def get_all_results(self, limit=None):
        """استرجاع جميع النتائج"""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM results ORDER BY created_at DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_results_by_decision(self, decision):
        """استرجاع النتائج حسب القرار"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT * FROM results WHERE decision = ? ORDER BY created_at DESC",
            conn,
            params=(decision,)
        )
        conn.close()
        return df
    
    def get_statistics(self):
        """الحصول على إحصائيات عامة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # إجمالي المنتجات
        cursor.execute("SELECT COUNT(*) FROM results")
        stats['total'] = cursor.fetchone()[0]
        
        # عدد كل قرار
        cursor.execute("""
            SELECT decision, COUNT(*) 
            FROM results 
            GROUP BY decision
        """)
        stats['decisions'] = dict(cursor.fetchall())
        
        # متوسط فرق السعر
        cursor.execute("SELECT AVG(price_diff) FROM results WHERE price_diff IS NOT NULL")
        stats['avg_price_diff'] = cursor.fetchone()[0] or 0
        
        # متوسط نسبة المطابقة
        cursor.execute("SELECT AVG(match_score) FROM results WHERE match_score > 0")
        stats['avg_match_score'] = cursor.fetchone()[0] or 0
        
        conn.close()
        return stats
    
    def log_action(self, action, details='', user='system'):
        """تسجيل إجراء في السجل"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO audit_log (action, details, user) VALUES (?, ?, ?)",
            (action, details, user)
        )
        conn.commit()
        conn.close()
    
    def get_audit_log(self, limit=100):
        """استرجاع سجل الإجراءات"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            f"SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT {limit}",
            conn
        )
        conn.close()
        return df
    
    def save_setting(self, key, value):
        """حفظ إعداد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        """استرجاع إعداد"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else default
    
    def clear_results(self):
        """مسح جميع النتائج"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM results")
        conn.commit()
        conn.close()
        self.log_action('clear_results', 'تم مسح جميع النتائج')
