import os
import time
from datetime import datetime

# ایمپورت ماژول‌های خودمان
from config import CONFIG
from analyzer import CompetitorAnalyzer
from content_generator import AIContentGenerator
from scheduler import SmartScheduler
from database import Database

class UltimateAIBot:
    """ربات نهایی هوش مصنوعی"""
    
    def __init__(self):
        self.config = CONFIG
        self.analyzer = CompetitorAnalyzer()
        self.content_gen = AIContentGenerator(self.analyzer)
        self.scheduler = SmartScheduler(self.config)
        self.db = Database()
        
        print("""
╔══════════════════════════════════════════╗
║     🤖 ULTIMATE AI BOT v3.0             ║
║     🎯 کانال: @hoshmasnoye             ║
║     🧠 سیستم هوش مصنوعی کامل          ║
╚══════════════════════════════════════════╝
        """)
    
    def run_analysis_phase(self):
        """فاز تحلیل و یادگیری"""
        print("🔍 شروع تحلیل رقبا...")
        
        # تحلیل رقبا (در نسخه واقعی از API دریافت می‌شود)
        competitor_posts = self.simulate_competitor_data()
        analysis = self.analyzer.analyze_competitor_posts(competitor_posts)
        
        print("✅ تحلیل کامل شد!")
        print(f"   📊 کلمات کلیدی برتر: {[kw[0] for kw in analysis['top_keywords'][:3]]}")
        print(f"   🏷️ هشتگ‌های پرکاربرد: {[h[0] for h in analysis['hashtags'][:3]]}")
        
        return analysis
    
    def simulate_competitor_data(self):
        """شبیه‌سازی داده‌های رقیب"""
        # در نسخه واقعی از API دریافت می‌شود
        return [
            "آموزش رایگان پایتون برای مبتدیان #پایتون #آموزش",
            "چطور با ChatGPT پول دربیاریم؟ #ChatGPT #کسب_درآمد",
            "پروژه عملی: ساخت ربات تلگرام #پروژه #ربات"
        ]
    
    def send_post(self, content):
        """ارسال پست به کانال"""
        try:
            url = f"https://tapi.bale.ai/bot{self.config['BOT_TOKEN']}/sendMessage"
            
            response = requests.post(url, json={
                "chat_id": self.config["CHANNEL"],
                "text": content,
                "parse_mode": "HTML"
            }, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ پست ارسال شد!")
                return True
            else:
                print(f"❌ خطا در ارسال: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ خطا: {e}")
            return False
    
    def run(self):
        """اجرای اصلی"""
        # فاز ۱: تحلیل
        context = self.run_analysis_phase()
        
        # فاز ۲: تولید و ارسال
        post_count = 0
        
        print("\n🚀 شروع تولید و ارسال محتوا...")
        
        try:
            while True:
                # بررسی زمان
                if self.scheduler.should_post_now():
                    # تولید محتوای هوشمند
                    content = self.content_gen.generate_content(context)
                    
                    # ارسال پست
                    success = self.send_post(content)
                    
                    if success:
                        post_count += 1
                        print(f"\n📊 پست #{post_count}")
                        print(f"   🕐 {datetime.now().strftime('%H:%M')}")
                        print(f"   📝 {content[:50]}...")
                        
                        # ذخیره در دیتابیس
                        self.db.save_post(content, datetime.now())
                    
                    # انتظار برای پست بعدی
                    wait_time = self.scheduler.wait_until_next()
                    time.sleep(wait_time * 60)  # به دقیقه
                
                else:
                    # چک وضعیت هر دقیقه
                    time.sleep(60)
                    
        except KeyboardInterrupt:
            print(f"\n\n🎯 ربات متوقف شد!")
            print(f"📈 {post_count} پست ارسال کرد")
            print("💾 داده‌ها ذخیره شدند")

# اجرای ربات
if __name__ == "__main__":
    bot = UltimateAIBot()
    bot.run()
