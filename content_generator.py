import random
import re
from datetime import datetime

class AIContentGenerator:
    """تولیدکننده محتوای هوشمند"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.templates = self.load_templates()
    
    def load_templates(self):
        """بارگذاری قالب‌های محتوا"""
        return {
            "educational": [
                "🎓 آموزش {موضوع}\n\n{نکات}\n\n#آموزش #{موضوع}",
                "📚 راهنمای کامل {موضوع}\n\n✅ {قدم1}\n✅ {قدم2}\n✅ {قدم3}",
                "🎯 {موضوع} در {زمان} روز\n\nنکات طلایی👇"
            ],
            "project": [
                "🚀 پروژه عملی: {پروژه}\n\n🔧 ابزارها: {ابزارها}\n\n#پروژه #عملی",
                "💼 ساخت {پروژه} از صفر\n\nزمان: {زمان}\nسطح: {سطح}",
                "🔨 پروژه این هفته: {پروژه}\n\nآماده‌ای شروع کنیم؟"
            ],
            "question": [
                "❓ سوال: {سوال}\n\nنظر شما چیه؟ 👇",
                "🤔 {سوال}\n\n۱. گزینه اول\n۲. گزینه دوم\n۳. گزینه سوم",
                "💭 بحث آزاد: {موضوع}\n\nنظراتتون رو بنویسید"
            ]
        }
    
    def generate_content(self, context=None):
        """تولید محتوای هوشمند"""
        # اگر تحلیل رقبا داریم، ازش استفاده می‌کنیم
        if context and "top_keywords" in context:
            # استفاده از کلمات کلیدی رقبا
            keywords = [kw[0] for kw in context["top_keywords"][:5]]
            topic = random.choice(keywords)
        else:
            # موضوعات پیش‌فرض
            topics = ["پایتون", "هوش مصنوعی", "ChatGPT", "برنامه‌نویسی", "کسب درآمد"]
            topic = random.choice(topics)
        
        # انتخاب نوع محتوا
        if context and "content_patterns" in context:
            # استفاده از الگوهای موفق رقبا
            pattern_types = [p["type"] for p in context["content_patterns"]]
            if pattern_types:
                content_type = max(set(pattern_types), key=pattern_types.count)
            else:
                content_type = random.choice(["educational", "project", "question"])
        else:
            content_type = random.choice(["educational", "project", "question"])
        
        # انتخاب قالب
        template = random.choice(self.templates[content_type])
        
        # جایگزینی متغیرها
        replacements = {
            "موضوع": topic,
            "پروژه": random.choice(["ربات تلگرام", "وبسایت", "اپ موبایل", "سیستم هوشمند"]),
            "سوال": f"بهترین راه برای یادگیری {topic} چیست؟",
            "نکات": self.generate_tips(topic),
            "قدم1": "مبانی را یاد بگیر",
            "قدم2": "تمرین عملی داشته باش",
            "قدم3": "پروژه واقعی بساز",
            "ابزارها": "پایتون، کتابخانه‌های رایگان",
            "زمان": random.choice(["۱ ساعت", "۳ ساعت", "یک روز"]),
            "سطح": random.choice(["مبتدی", "متوسط", "پیشرفته"])
        }
        
        # جایگزینی
        for key, value in replacements.items():
            template = template.replace("{" + key + "}", value)
        
        # اضافه کردن هشتگ‌های هوشمند
        template += self.generate_smart_hashtags(topic, content_type)
        
        # اضافه کردن زمان
        template += f"\n\n⏰ {datetime.now().strftime('%H:%M')}"
        
        return template
    
    def generate_tips(self, topic):
        """تولید نکات آموزشی"""
        tips = [
            "روزانه ۳۰ دقیقه وقت بذار",
            "پروژه‌های کوچک شروع کن",
            "از منابع رایگان استفاده کن",
            "با جامعه برنامه‌نویسان در ارتباط باش"
        ]
        return "\n".join([f"• {tip}" for tip in random.sample(tips, 3)])
    
    def generate_smart_hashtags(self, topic, content_type):
        """تولید هشتگ‌های هوشمند"""
        base_tags = ["#هوش_مصنوعی", "#AI"]
        
        # هشتگ‌های موضوعی
        topic_tags = {
            "پایتون": ["#پایتون", "#برنامه_نویسی"],
            "هوش مصنوعی": ["#یادگیری_ماشین", "#ChatGPT"],
            "کسب درآمد": ["#کسب_درآمد_آنلاین", "#فریلنسینگ"]
        }
        
        # هشتگ‌های نوع محتوا
        type_tags = {
            "educational": ["#آموزش_رایگان", "#یادگیری"],
            "project": ["#پروژه_عملی", "#پورتفولیو"],
            "question": ["#نظرسنجی", "#بحث"]
        }
        
        # ترکیب هشتگ‌ها
        all_tags = base_tags
        all_tags.extend(topic_tags.get(topic, []))
        all_tags.extend(type_tags.get(content_type, []))
        
        # حداکثر ۸ هشتگ
        selected_tags = all_tags[:6]
        random.shuffle(selected_tags)
        
        return "\n" + " ".join(selected_tags)
