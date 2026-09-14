"""
مكتبة عموري - Amoory Library Store Bot
Configuration Module
"""

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من .env
load_dotenv()

# ==================== Bot Configuration ====================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
LOW_STOCK_THRESHOLD = int(os.getenv("LOW_STOCK_THRESHOLD", "5"))

# ==================== Database Configuration ====================
DATABASE_PATH = "amoory_store.db"
BACKUP_DIR = "backups"

# ==================== Store Information ====================
STORE_NAME = "🛍️ متجر مكتبة عموري"
STORE_DESCRIPTION = "Amoory Library Store Bot"
CURRENCY = "د.ع"  # Iraqi Dinar

# ==================== User States ====================
class UserStates:
    """حالات المستخدم في المحادثة"""
    MAIN_MENU = "main_menu"
    BROWSING_PRODUCTS = "browsing_products"
    VIEWING_PRODUCT = "viewing_product"
    SEARCHING = "searching"
    CART = "cart"
    CHECKOUT = "checkout"
    FAVORITES = "favorites"
    ORDERS = "orders"
    ADMIN_PANEL = "admin_panel"
    ADDING_PRODUCT = "adding_product"
    EDITING_PRODUCT = "editing_product"
    MANAGING_STOCK = "managing_stock"
    MANAGING_OFFERS = "managing_offers"
    MANAGING_COUPONS = "managing_coupons"
    MANAGING_BUNDLES = "managing_bundles"
    MAINTENANCE_MODE = "maintenance_mode"
    SEARCH_ORDERS = "search_orders"
    SEARCH_USERS = "search_users"

# ==================== Order Status ====================
class OrderStatus:
    """حالات الطلبات"""
    PENDING = "pending"  # تم الحجز
    RECEIVED = "received"  # تم الاستلام
    COMPLETED = "completed"  # مكتمل
    CANCELLED = "cancelled"  # ملغي

ORDER_STATUS_EMOJI = {
    OrderStatus.PENDING: "🕐",
    OrderStatus.RECEIVED: "📦",
    OrderStatus.COMPLETED: "✅",
    OrderStatus.CANCELLED: "❌",
}

ORDER_STATUS_TEXT = {
    OrderStatus.PENDING: "تم الحجز",
    OrderStatus.RECEIVED: "تم الاستلام",
    OrderStatus.COMPLETED: "مكتمل",
    OrderStatus.CANCELLED: "ملغي",
}

# ==================== Emoji & Icons ====================
EMOJI = {
    "home": "🏠",
    "back": "↩️",
    "categories": "📚",
    "products": "📁",
    "new": "🆕",
    "trending": "🔥",
    "search": "🔍",
    "favorites": "❤️",
    "cart": "🛒",
    "orders": "📋",
    "reorder": "🔄",
    "track": "📦",
    "offers": "🎁",
    "bundles": "🎒",
    "unavailable": "🔔",
    "info": "ℹ️",
    "add": "➕",
    "remove": "➖",
    "delete": "🗑️",
    "clear": "🧹",
    "checkout": "💳",
    "admin": "👑",
    "stats": "📊",
    "orders_admin": "📦",
    "users": "👥",
    "inventory": "📦",
    "offers_admin": "🏷️",
    "coupons": "🎟️",
    "reports": "📈",
    "export": "📤",
    "backup": "💾",
    "logs": "📝",
    "maintenance": "🛠️",
    "warning": "⚠️",
    "price": "💰",
    "discount": "🏷️",
    "rating": "⭐",
    "quantity": "📊",
    "available": "✅",
    "unavailable_item": "❌",
    "notify": "🔔",
    "previous": "⬅️",
    "next": "➡️",
    "page": "📄",
    "description": "📝",
    "image": "🖼️",
    "related": "🧩",
}

# ==================== Buttons Text ====================
BUTTONS = {
    "categories": f"{EMOJI['categories']} الأقسام",
    "all_products": f"{EMOJI['products']} جميع المنتجات",
    "new": f"{EMOJI['new']} جديدنا",
    "trending": f"{EMOJI['trending']} الأكثر طلباً",
    "search": f"{EMOJI['search']} البحث",
    "favorites": f"{EMOJI['favorites']} المفضلة",
    "cart": f"{EMOJI['cart']} السلة",
    "orders": f"{EMOJI['orders']} طلباتي",
    "reorder": f"{EMOJI['reorder']} إعادة الطلب",
    "track": f"{EMOJI['track']} متابعة الطلب",
    "offers": f"{EMOJI['offers']} العروض",
    "bundles": f"{EMOJI['bundles']} الباقات",
    "unavailable": f"{EMOJI['unavailable']} المنتجات غير المتوفرة",
    "info": f"{EMOJI['info']} معلومات المكتبة",
    "home": f"{EMOJI['home']} الرئيسية",
    "back": f"{EMOJI['back']} رجوع",
    "add_to_cart": f"{EMOJI['add']} إضافة للسلة",
    "add_to_favorites": f"{EMOJI['favorites']} إضافة للمفضلة",
    "notify_when_available": f"{EMOJI['notify']} أبلغني عند التوفر",
    "related_products": f"{EMOJI['related']} أشياء مرتبطة",
    "similar_products": f"{EMOJI['search']} منتجات مشابهة",
    "increase": f"{EMOJI['add']}",
    "decrease": f"{EMOJI['remove']}",
    "remove": f"{EMOJI['delete']} حذف",
    "clear_cart": f"{EMOJI['clear']} تفريغ السلة",
    "checkout": f"{EMOJI['checkout']} إتمام الطلب",
    "admin": f"{EMOJI['admin']} لوحة تحكم مكتبة عموري",
    "stats": f"{EMOJI['stats']} الإحصائيات",
    "orders_admin": f"{EMOJI['orders_admin']} الطلبات",
    "users": f"{EMOJI['users']} الزبائن",
    "products": f"{EMOJI['products']} المنتجات",
    "inventory": f"{EMOJI['inventory']} المخزون",
    "offers": f"{EMOJI['offers_admin']} العروض",
    "coupons": f"{EMOJI['coupons']} الكوبونات",
    "bundles": f"{EMOJI['bundles']} الباقات",
    "reports": f"{EMOJI['reports']} التقارير",
    "excel": f"{EMOJI['export']} تصدير Excel",
    "backup": f"{EMOJI['backup']} نسخة احتياطية",
    "logs": f"{EMOJI['logs']} سجل العمليات",
    "maintenance": f"{EMOJI['maintenance']} وضع الصيانة",
    "enable_maintenance": f"{EMOJI['maintenance']} تفعيل الصيانة",
    "disable_maintenance": f"{EMOJI['maintenance']} إيقاف الصيانة",
}

# ==================== Messages ====================
MESSAGES = {
    "maintenance": f"{EMOJI['maintenance']} البوت حالياً تحت الصيانة.\n\nسنعود قريباً ❤️",
    "unauthorized": "❌ ليس لديك صلاحية للوصول إلى هذا الخيار.",
    "no_results": f"{EMOJI['search']} لم نجد منتجات مطابقة لبحثك.",
    "product_not_found": "❌ المنتج غير موجود.",
    "order_not_found": "❌ الطلب غير موجود.",
    "user_not_found": "❌ المستخدم غير موجود.",
    "out_of_stock": f"{EMOJI['unavailable_item']} المنتج غير متوفر حالياً.",
    "low_stock": f"{EMOJI['warning']} الكمية المطلوبة غير متوفرة.",
    "cart_empty": f"{EMOJI['cart']} السلة فارغة.",
    "no_favorites": f"{EMOJI['favorites']} لا توجد منتجات مفضلة.",
    "no_orders": f"{EMOJI['orders']} لا توجد طلبات.",
    "welcome": "مرحباً في متجر مكتبة عموري! 👋\n\nاختر ما تريده من القائمة أدناه:",
    "help": "قائمة الأوامر:\n\n/start - الرئيسية\n/help - المساعدة\n/search - البحث\n/admin - لوحة التحكم",
}

# ==================== Validation ====================
MIN_PRODUCT_PRICE = 100
MAX_PRODUCT_PRICE = 999999
MIN_PRODUCT_STOCK = 0
MAX_PRODUCT_STOCK = 99999
MAX_COUPON_DISCOUNT = 100
MIN_ORDER_AMOUNT = 1000
