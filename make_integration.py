# ══════════════════════════════════════════════════════════════
# make_integration.py - ربط Make.com (Webhooks) بدون تغيير
# ══════════════════════════════════════════════════════════════

import requests
import json
import logging
from datetime import datetime
from config import (
    WEBHOOK_UPDATE_PRICES, WEBHOOK_NEW_PRODUCTS, REQUEST_TIMEOUT
)

logger = logging.getLogger(__name__)


class MakeIntegration:
    """ربط مباشر مع سيناريوهات Make.com عبر Webhooks."""

    def __init__(self):
        self.webhook_prices = WEBHOOK_UPDATE_PRICES
        self.webhook_products = WEBHOOK_NEW_PRODUCTS

    # ── إرسال تحديثات الأسعار ────────────────────────────────
    def send_price_updates(self, updates: list[dict]) -> dict:
        """
        إرسال تحديثات الأسعار إلى Make.com.
        كل عنصر: {"product_name", "old_price", "new_price", "source"}
        """
        payload = {
            "action": "update_prices",
            "timestamp": datetime.utcnow().isoformat(),
            "count": len(updates),
            "data": updates
        }
        return self._send(self.webhook_prices, payload)

    # ── إرسال منتجات جديدة ───────────────────────────────────
    def send_new_products(self, products: list[dict]) -> dict:
        """
        إرسال منتجات جديدة إلى Make.com.
        كل عنصر: {"product_name", "price", "category", "brand"}
        """
        payload = {
            "action": "new_products",
            "timestamp": datetime.utcnow().isoformat(),
            "count": len(products),
            "data": products
        }
        return self._send(self.webhook_products, payload)

    # ── إرسال نتائج المقارنة ─────────────────────────────────
    def send_comparison_results(self, results: list[dict]) -> dict:
        """إرسال نتائج مقارنة الأسعار مع المنافسين إلى Make.com."""
        payload = {
            "action": "comparison_report",
            "timestamp": datetime.utcnow().isoformat(),
            "total_products": len(results),
            "data": results
        }
        return self._send(self.webhook_prices, payload)

    # ── إرسال تنبيه سعري ─────────────────────────────────────
    def send_price_alert(self, product_name: str,
                         my_price: float,
                         competitor_price: float,
                         diff_pct: float) -> dict:
        """إرسال تنبيه فوري عند اكتشاف فرق سعري كبير."""
        payload = {
            "action": "price_alert",
            "timestamp": datetime.utcnow().isoformat(),
            "product": product_name,
            "my_price": my_price,
            "competitor_price": competitor_price,
            "difference_percent": diff_pct,
            "severity": "high" if abs(diff_pct) > 20 else "medium"
        }
        return self._send(self.webhook_prices, payload)

    # ── فحص اتصال Webhook ────────────────────────────────────
    def test_connection(self) -> dict:
        """فحص اتصال جميع Webhooks."""
        results = {}
        for name, url in [
            ("تحديث_الأسعار", self.webhook_prices),
            ("منتجات_جديدة", self.webhook_products),
        ]:
            try:
                resp = requests.post(
                    url,
                    json={"action": "ping", "test": True},
                    timeout=10
                )
                results[name] = {
                    "status": "متصل" if resp.status_code == 200 else "خطأ",
                    "code": resp.status_code
                }
            except Exception as exc:
                results[name] = {"status": "غير متصل", "error": str(exc)}
        return results

    # ── إرسال عام ────────────────────────────────────────────
    def _send(self, webhook_url: str, payload: dict) -> dict:
        """إرسال بيانات إلى Webhook مع معالجة الأخطاء."""
        try:
            resp = requests.post(
                webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=REQUEST_TIMEOUT
            )
            if resp.status_code == 200:
                logger.info("Make.com: تم الإرسال بنجاح")
                return {"success": True, "status": resp.status_code}
            logger.warning("Make.com: كود %s", resp.status_code)
            return {"success": False, "status": resp.status_code,
                    "error": resp.text}
        except requests.RequestException as exc:
            logger.error("Make.com: فشل الاتصال - %s", exc)
            return {"success": False, "error": str(exc)}
