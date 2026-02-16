# ══════════════════════════════════════════════════════════════
# make_integration.py - إصلاح تعارض الاستيراد (V16 Compatible)
# ══════════════════════════════════════════════════════════════

import requests
import json
import logging
from datetime import datetime
# استيراد الكلاس Config بدلاً من المتغيرات المنفردة
from config import Config

logger = logging.getLogger(__name__)

class MakeIntegration:
    """إدارة الربط المباشر مع سيناريوهات Make.com"""

    def __init__(self):
        # استرجاع الروابط باستخدام الدالة المخصصة في Config
        self.webhook_prices, self.webhook_products = Config.get_make_webhooks()
        # ضبط مهلة الطلب (Timeout)
        self.timeout = 15

    def send_price_updates(self, updates: list[dict]) -> tuple[bool, str]:
        """إرسال تحديثات الأسعار إلى Make.com"""
        if not updates:
            return False, "لا توجد بيانات للإرسال"

        payload = {
            "action": "update_prices",
            "store": "mahwous",
            "timestamp": datetime.now().isoformat(),
            "count": len(updates),
            "products": updates
        }
        
        return self._send(self.webhook_prices, payload)

    def _send(self, url: str, payload: dict) -> tuple[bool, str]:
        """دالة الإرسال الفعلية مع معالجة الأخطاء"""
        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return True, "✅ تم الإرسال بنجاح إلى Make.com!"
            else:
                return False, f"❌ خطأ من الخادم: {response.status_code}"
                
        except Exception as e:
            logger.error(f"فشل الاتصال بـ Make: {e}")
            return False, f"❌ فشل الاتصال: {str(e)}"
