"""
مكتبة عموري - Amoory Library Store Bot
Database Module
"""

import sqlite3
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    """إدارة قاعدة البيانات SQLite"""
    
    def __init__(self, db_path="amoory_store.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
            raise
    
    def init_db(self):
        """إنشاء الجداول إذا لم تكن موجودة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # جدول المستخدمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول الأقسام
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    icon TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول المنتجات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    offer_price REAL,
                    category_id INTEGER,
                    stage TEXT,
                    stock INTEGER DEFAULT 0,
                    is_available INTEGER DEFAULT 1,
                    is_new INTEGER DEFAULT 0,
                    image_url TEXT,
                    file_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id)
                )
            ''')
            
            # جدول السلة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cart (
                    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    UNIQUE(user_id, product_id)
                )
            ''')
            
            # جدول المفضلة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS favorites (
                    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    UNIQUE(user_id, product_id)
                )
            ''')
            
            # جدول الطلبات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    order_number TEXT UNIQUE NOT NULL,
                    total_amount REAL NOT NULL,
                    discount REAL DEFAULT 0,
                    final_amount REAL NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            # جدول عناصر الطلبات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_items (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            ''')
            
            # جدول الكوبونات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS coupons (
                    coupon_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    discount_percent REAL NOT NULL,
                    discount_amount REAL,
                    min_order_amount REAL DEFAULT 0,
                    max_uses INTEGER,
                    current_uses INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1,
                    expires_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول العروض
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS offers (
                    offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    offer_price REAL NOT NULL,
                    min_quantity INTEGER DEFAULT 1,
                    max_quantity INTEGER,
                    is_active INTEGER DEFAULT 1,
                    starts_at TIMESTAMP,
                    expires_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            ''')
            
            # جدول عروض الكميات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quantity_offers (
                    qty_offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    min_quantity INTEGER NOT NULL,
                    discount_percent REAL NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            ''')
            
            # جدول الباقات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bundles (
                    bundle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    stage TEXT,
                    price REAL NOT NULL,
                    image_url TEXT,
                    file_id TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول عناصر الباقات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bundle_items (
                    bundle_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bundle_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    FOREIGN KEY (bundle_id) REFERENCES bundles(bundle_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    UNIQUE(bundle_id, product_id)
                )
            ''')
            
            # جدول الإشعارات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    type TEXT DEFAULT 'availability',
                    is_sent INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sent_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    UNIQUE(user_id, product_id, type)
                )
            ''')
            
            # جدول سجل العمليات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول الإعدادات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("✅ تم إنشاء قاعدة البيا��ات بنجاح")
        except sqlite3.Error as e:
            logger.error(f"❌ خطأ في إنشاء الجداول: {e}")
            raise
        finally:
            conn.close()
    
    # ==================== Users ====================
    
    def add_user(self, user_id, username=None, first_name=None, last_name=None):
        """إضافة مستخدم جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة المستخدم: {e}")
        finally:
            conn.close()
    
    def get_user(self, user_id):
        """الحصول على بيانات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب بيانات المستخدم: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_users(self):
        """الحصول على جميع المستخدمين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب المستخدمين: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Categories ====================
    
    def add_category(self, name, description=None, icon=None):
        """إضافة قسم جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO categories (name, description, icon)
                VALUES (?, ?, ?)
            ''', (name, description, icon))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة القسم: {e}")
            return None
        finally:
            conn.close()
    
    def get_category(self, category_id):
        """الحصول على قسم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM categories WHERE category_id = ?', (category_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب القسم: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_categories(self):
        """الحصول على جميع الأقسام"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM categories ORDER BY name')
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الأقسام: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Products ====================
    
    def add_product(self, name, price, category_id=None, description=None, 
                    offer_price=None, stage=None, stock=0, image_url=None, file_id=None):
        """إضافة منتج جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO products (name, price, category_id, description, 
                                     offer_price, stage, stock, image_url, file_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, price, category_id, description, offer_price, stage, stock, image_url, file_id))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة المنتج: {e}")
            return None
        finally:
            conn.close()
    
    def get_product(self, product_id):
        """الحصول على منتج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب المنتج: {e}")
            return None
        finally:
            conn.close()
    
    def get_products_by_category(self, category_id, page=1, per_page=10):
        """الحصول على المنتجات حسب القسم مع pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT * FROM products 
                WHERE category_id = ? AND is_available = 1
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (category_id, per_page, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب المنتجات: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_products(self, page=1, per_page=10):
        """الحصول على جميع المنتجات مع pagination"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT * FROM products 
                WHERE is_available = 1
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب المنتجات: {e}")
            return []
        finally:
            conn.close()
    
    def get_new_products(self, limit=10):
        """الحصول على المنتجات الجديدة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM products 
                WHERE is_new = 1 AND is_available = 1
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب المنتجات الجديدة: {e}")
            return []
        finally:
            conn.close()
    
    def get_trending_products(self, limit=10):
        """الحصول على المنتجات الأكثر طلباً"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT p.*, SUM(oi.quantity) as total_sold
                FROM products p
                LEFT JOIN order_items oi ON p.product_id = oi.product_id
                LEFT JOIN orders o ON oi.order_id = o.order_id
                WHERE p.is_available = 1 AND (o.status != 'cancelled' OR o.status IS NULL)
                GROUP BY p.product_id
                ORDER BY total_sold DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب المنتجات الأكثر طلباً: {e}")
            return []
        finally:
            conn.close()
    
    def search_products(self, keyword, page=1, per_page=10):
        """البحث عن المنتجات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            offset = (page - 1) * per_page
            search_term = f"%{keyword}%"
            cursor.execute('''
                SELECT * FROM products 
                WHERE is_available = 1 AND (
                    name LIKE ? OR 
                    description LIKE ? OR 
                    stage LIKE ?
                )
                ORDER BY name
                LIMIT ? OFFSET ?
            ''', (search_term, search_term, search_term, per_page, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في البحث عن المنتجات: {e}")
            return []
        finally:
            conn.close()
    
    def update_product(self, product_id, **kwargs):
        """تحديث بيانات المنتج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            allowed_fields = ['name', 'description', 'price', 'offer_price', 
                            'category_id', 'stage', 'stock', 'is_available', 
                            'is_new', 'image_url', 'file_id']
            
            updates = []
            values = []
            for key, value in kwargs.items():
                if key in allowed_fields:
                    updates.append(f"{key} = ?")
                    values.append(value)
            
            if updates:
                updates.append("updated_at = CURRENT_TIMESTAMP")
                values.append(product_id)
                query = f"UPDATE products SET {', '.join(updates)} WHERE product_id = ?"
                cursor.execute(query, values)
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في تحديث المنتج: {e}")
        finally:
            conn.close()
    
    def update_stock(self, product_id, quantity):
        """تحديث المخزون"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE products 
                SET stock = stock + ?, updated_at = CURRENT_TIMESTAMP
                WHERE product_id = ?
            ''', (quantity, product_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في تحديث المخزون: {e}")
        finally:
            conn.close()
    
    def get_unavailable_products(self, page=1, per_page=10):
        """الحصول على المنتجات غير المتوفرة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT * FROM products 
                WHERE is_available = 0 OR stock <= 0
                ORDER BY updated_at DESC
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب المنتجات غير المتوفرة: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Cart ====================
    
    def add_to_cart(self, user_id, product_id, quantity=1):
        """إضافة منتج للسلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO cart (user_id, product_id, quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + ?
            ''', (user_id, product_id, quantity, quantity))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة المنتج للسلة: {e}")
        finally:
            conn.close()
    
    def get_cart(self, user_id):
        """الحصول على سلة المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT c.*, p.name, p.price, p.offer_price, p.stock, p.is_available
                FROM cart c
                JOIN products p ON c.product_id = p.product_id
                WHERE c.user_id = ?
                ORDER BY c.added_at DESC
            ''', (user_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب السلة: {e}")
            return []
        finally:
            conn.close()
    
    def update_cart_quantity(self, user_id, product_id, quantity):
        """تحديث كمية المنتج في السلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if quantity <= 0:
                cursor.execute('''
                    DELETE FROM cart WHERE user_id = ? AND product_id = ?
                ''', (user_id, product_id))
            else:
                cursor.execute('''
                    UPDATE cart SET quantity = ? 
                    WHERE user_id = ? AND product_id = ?
                ''', (quantity, user_id, product_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في تحديث كمية السلة: {e}")
        finally:
            conn.close()
    
    def remove_from_cart(self, user_id, product_id):
        """حذف منتج من السلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                DELETE FROM cart WHERE user_id = ? AND product_id = ?
            ''', (user_id, product_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في حذف المنتج من السلة: {e}")
        finally:
            conn.close()
    
    def clear_cart(self, user_id):
        """تفريغ السلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في تفريغ السلة: {e}")
        finally:
            conn.close()
    
    # ==================== Favorites ====================
    
    def add_to_favorites(self, user_id, product_id):
        """إضافة منتج للمفضلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO favorites (user_id, product_id)
                VALUES (?, ?)
            ''', (user_id, product_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة المنتج للمفضلة: {e}")
        finally:
            conn.close()
    
    def get_favorites(self, user_id):
        """الحصول على المفضلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT p.*
                FROM favorites f
                JOIN products p ON f.product_id = p.product_id
                WHERE f.user_id = ? AND p.is_available = 1
                ORDER BY f.added_at DESC
            ''', (user_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب المفضلة: {e}")
            return []
        finally:
            conn.close()
    
    def is_favorite(self, user_id, product_id):
        """التحقق من وجود المنتج في المفضلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT 1 FROM favorites WHERE user_id = ? AND product_id = ?
            ''', (user_id, product_id))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"خطأ في التحقق من المفضلة: {e}")
            return False
        finally:
            conn.close()
    
    def remove_from_favorites(self, user_id, product_id):
        """حذف منتج من المفضلة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                DELETE FROM favorites WHERE user_id = ? AND product_id = ?
            ''', (user_id, product_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في حذف المنتج من المفضلة: {e}")
        finally:
            conn.close()
    
    # ==================== Orders ====================
    
    def create_order(self, user_id, total_amount, discount=0, final_amount=None):
        """إنشاء طلب جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if final_amount is None:
                final_amount = total_amount - discount
            
            order_number = f"ORD-{int(datetime.now().timestamp())}"
            
            cursor.execute('''
                INSERT INTO orders (user_id, order_number, total_amount, discount, final_amount)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, order_number, total_amount, discount, final_amount))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"خطأ في إنشاء الطلب: {e}")
            return None
        finally:
            conn.close()
    
    def add_order_item(self, order_id, product_id, quantity, price):
        """إضافة عنصر للطلب"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            subtotal = quantity * price
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price, subtotal)
                VALUES (?, ?, ?, ?, ?)
            ''', (order_id, product_id, quantity, price, subtotal))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة عنصر الطلب: {e}")
        finally:
            conn.close()
    
    def get_order(self, order_id):
        """الحصول على بيانات الطلب"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الطلب: {e}")
            return None
        finally:
            conn.close()
    
    def get_user_orders(self, user_id, page=1, per_page=10):
        """الحصول على طلبات المستخدم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT * FROM orders 
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (user_id, per_page, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الطلبات: {e}")
            return []
        finally:
            conn.close()
    
    def get_order_items(self, order_id):
        """الحصول على عناصر الطلب"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT oi.*, p.name, p.image_url, p.file_id
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.order_id = ?
            ''', (order_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب عناصر الطلب: {e}")
            return []
        finally:
            conn.close()
    
    def update_order_status(self, order_id, status):
        """تحديث حالة الطلب"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE orders 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE order_id = ?
            ''', (status, order_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في تحديث حالة الطلب: {e}")
        finally:
            conn.close()
    
    def get_all_orders(self, page=1, per_page=20):
        """الحصول على جميع الطلبات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            offset = (page - 1) * per_page
            cursor.execute('''
                SELECT o.*, u.username, u.first_name
                FROM orders o
                JOIN users u ON o.user_id = u.user_id
                ORDER BY o.created_at DESC
                LIMIT ? OFFSET ?
            ''', (per_page, offset))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الطلبات: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Coupons ====================
    
    def add_coupon(self, code, discount_percent=None, discount_amount=None, 
                   min_order_amount=0, max_uses=None, expires_at=None):
        """إضافة كوبون جديد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO coupons (code, discount_percent, discount_amount, 
                                    min_order_amount, max_uses, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (code, discount_percent, discount_amount, min_order_amount, max_uses, expires_at))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة الكوبون: {e}")
            return None
        finally:
            conn.close()
    
    def get_coupon(self, code):
        """الحصول على الكوبون"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM coupons WHERE code = ? AND is_active = 1', (code,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الكوبون: {e}")
            return None
        finally:
            conn.close()
    
    def use_coupon(self, coupon_id):
        """تسجيل استخدام الكوبون"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE coupons 
                SET current_uses = current_uses + 1
                WHERE coupon_id = ?
            ''', (coupon_id,))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في تسجيل استخدام الكوبون: {e}")
        finally:
            conn.close()
    
    def get_all_coupons(self):
        """الحصول على جميع الكوبونات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM coupons ORDER BY created_at DESC')
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الكوبونات: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Offers ====================
    
    def add_offer(self, product_id, offer_price, min_quantity=1, max_quantity=None, 
                  starts_at=None, expires_at=None):
        """إضافة عرض"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO offers (product_id, offer_price, min_quantity, max_quantity, 
                                   starts_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (product_id, offer_price, min_quantity, max_quantity, starts_at, expires_at))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة العرض: {e}")
            return None
        finally:
            conn.close()
    
    def get_active_offers(self):
        """الحصول على العروض النشطة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM offers 
                WHERE is_active = 1 AND 
                (expires_at IS NULL OR expires_at > datetime('now'))
                ORDER BY created_at DESC
            ''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب العروض: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Quantity Offers ====================
    
    def add_quantity_offer(self, product_id, min_quantity, discount_percent):
        """إضافة عرض كمية"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO quantity_offers (product_id, min_quantity, discount_percent)
                VALUES (?, ?, ?)
            ''', (product_id, min_quantity, discount_percent))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة عرض الكمية: {e}")
            return None
        finally:
            conn.close()
    
    def get_quantity_offers(self, product_id):
        """الحصول على عروض الكمية للمنتج"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM quantity_offers 
                WHERE product_id = ? AND is_active = 1
                ORDER BY min_quantity ASC
            ''', (product_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب عروض الكمية: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Bundles ====================
    
    def add_bundle(self, name, price, description=None, stage=None, image_url=None, file_id=None):
        """إضافة باقة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO bundles (name, price, description, stage, image_url, file_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, price, description, stage, image_url, file_id))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة الباقة: {e}")
            return None
        finally:
            conn.close()
    
    def add_bundle_item(self, bundle_id, product_id, quantity=1):
        """إضافة منتج للباقة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO bundle_items (bundle_id, product_id, quantity)
                VALUES (?, ?, ?)
            ''', (bundle_id, product_id, quantity))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة عنصر الباقة: {e}")
        finally:
            conn.close()
    
    def get_bundle(self, bundle_id):
        """الحصول على بيانات الباقة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM bundles WHERE bundle_id = ? AND is_active = 1', (bundle_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الباقة: {e}")
            return None
        finally:
            conn.close()
    
    def get_bundle_items(self, bundle_id):
        """الحصول على عناصر الباقة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT p.*, bi.quantity
                FROM bundle_items bi
                JOIN products p ON bi.product_id = p.product_id
                WHERE bi.bundle_id = ?
            ''', (bundle_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب عناصر الباقة: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_bundles(self):
        """الحصول على جميع الباقات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM bundles WHERE is_active = 1 ORDER BY name')
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الباقات: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Notifications ====================
    
    def add_notification(self, user_id, product_id, notification_type='availability'):
        """إضافة إشعار"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO notifications (user_id, product_id, type)
                VALUES (?, ?, ?)
            ''', (user_id, product_id, notification_type))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة الإشعار: {e}")
        finally:
            conn.close()
    
    def get_pending_notifications(self, product_id):
        """الحصول على الإشعارات المعلقة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM notifications 
                WHERE product_id = ? AND is_sent = 0
            ''', (product_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الإشعارات: {e}")
            return []
        finally:
            conn.close()
    
    def mark_notification_sent(self, notification_id):
        """تعليم الإشعار كمرسل"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE notifications 
                SET is_sent = 1, sent_at = CURRENT_TIMESTAMP
                WHERE notification_id = ?
            ''', (notification_id,))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في تعليم الإشعار: {e}")
        finally:
            conn.close()
    
    def delete_notification(self, notification_id):
        """حذف الإشعار"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM notifications WHERE notification_id = ?', (notification_id,))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في حذف الإشعار: {e}")
        finally:
            conn.close()
    
    # ==================== Logs ====================
    
    def add_log(self, user_id, action, details=None):
        """إضافة سجل عملية"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO logs (user_id, action, details)
                VALUES (?, ?, ?)
            ''', (user_id, action, details))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في إضافة السجل: {e}")
        finally:
            conn.close()
    
    def get_logs(self, limit=100):
        """الحصول على السجلات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM logs 
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب السجلات: {e}")
            return []
        finally:
            conn.close()
    
    # ==================== Settings ====================
    
    def set_setting(self, key, value):
        """حفظ إعداد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = CURRENT_TIMESTAMP
            ''', (key, value, value))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"خطأ في حفظ الإعداد: {e}")
        finally:
            conn.close()
    
    def get_setting(self, key):
        """الحصول على إعداد"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result['value'] if result else None
        except sqlite3.Error as e:
            logger.error(f"خطأ في جلب الإعداد: {e}")
            return None
        finally:
            conn.close()
    
    # ==================== Statistics ====================
    
    def get_total_users(self):
        """عدد المستخدمين"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) as count FROM users')
            result = cursor.fetchone()
            return result['count'] if result else 0
        except sqlite3.Error as e:
            logger.error(f"خطأ في حساب المستخدمين: {e}")
            return 0
        finally:
            conn.close()
    
    def get_total_products(self):
        """عدد المنتجات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) as count FROM products WHERE is_available = 1')
            result = cursor.fetchone()
            return result['count'] if result else 0
        except sqlite3.Error as e:
            logger.error(f"خطأ في حساب المنتجات: {e}")
            return 0
        finally:
            conn.close()
    
    def get_total_orders(self):
        """إجمالي الطلبات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) as count FROM orders')
            result = cursor.fetchone()
            return result['count'] if result else 0
        except sqlite3.Error as e:
            logger.error(f"خطأ في حساب الطلبات: {e}")
            return 0
        finally:
            conn.close()
    
    def get_completed_orders(self):
        """الطلبات المكتملة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'completed'")
            result = cursor.fetchone()
            return result['count'] if result else 0
        except sqlite3.Error as e:
            logger.error(f"خطأ في حساب الطلبات المكتملة: {e}")
            return 0
        finally:
            conn.close()
    
    def get_cancelled_orders(self):
        """الطلبات الملغاة"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'cancelled'")
            result = cursor.fetchone()
            return result['count'] if result else 0
        except sqlite3.Error as e:
            logger.error(f"خطأ في حساب الطلبات الملغاة: {e}")
            return 0
        finally:
            conn.close()
    
    def get_total_sales(self):
        """إجمالي المبيعات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT SUM(final_amount) as total 
                FROM orders 
                WHERE status != 'cancelled'
            ''')
            result = cursor.fetchone()
            return result['total'] if result and result['total'] else 0
        except sqlite3.Error as e:
            logger.error(f"خطأ في حساب المبيعات: {e}")
            return 0
        finally:
            conn.close()
    
    def get_today_sales(self):
        """مبيعات اليوم"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT SUM(final_amount) as total 
                FROM orders 
                WHERE status != 'cancelled' AND 
                DATE(created_at) = DATE('now')
            ''')
            result = cursor.fetchone()
            return result['total'] if result and result['total'] else 0
        except sqlite3.Error as e:
            logger.error(f"خطأ في حساب مبيعات اليوم: {e}")
            return 0
        finally:
            conn.close()
    
    def get_month_sales(self):
        """مبيعات هذا الشهر"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT SUM(final_amount) as total 
                FROM orders 
                WHERE status != 'cancelled' AND 
                strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
            ''')
            result = cursor.fetchone()
            return result['total'] if result and result['total'] else 0
        except sqlite3.Error as e:
            logger.error(f"خطأ في حساب مبيعات الشهر: {e}")
            return 0
        finally:
            conn.close()
