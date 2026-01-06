import time
from datetime import datetime

class SmartScheduler:
    """زمان‌بند هوشمند"""
    
    def __init__(self, config):
        self.config = config
        self.best_times = []
    
    def calculate_best_time(self):
        """محاسبه بهترین زمان ارسال"""
        now = datetime.now()
        
        # اگر داده‌ای از رقبا داریم
        if self.best_times:
            return random.choice(self.best_times)
        
        # ساعت‌های طلایی پیش‌فرض
        golden_hours = self.config["POST_SCHEDULE"]["hours"]
        current_hour = now.hour
        
        # اگر الان در ساعت طلایی نیست، نزدیک‌ترین رو پیدا کن
        if current_hour not in golden_hours:
            # پیدا کردن نزدیک‌ترین ساعت طلایی
            future_hours = [h for h in golden_hours if h > current_hour]
            if future_hours:
                return future_hours[0]
            else:
                return golden_hours[0]  # فردا صبح اول وقت
        
        return current_hour  # الان زمان خوبیه
    
    def should_post_now(self):
        """آیا الان باید پست گذاشت؟"""
        now = datetime.now()
        best_hour = self.calculate_best_time()
        
        return now.hour == best_hour and now.minute < 30
    
    def wait_until_next(self):
        """صبر کن تا زمان بعدی"""
        now = datetime.now()
        best_hour = self.calculate_best_time()
        
        if now.hour < best_hour:
            hours_to_wait = best_hour - now.hour
        else:
            hours_to_wait = (24 - now.hour) + best_hour
        
        # به دقیقه تبدیل کن
        minutes_to_wait = hours_to_wait * 60
        print(f"⏳ {minutes_to_wait} دقیقه تا پست بعدی...")
        
        return minutes_to_wait
