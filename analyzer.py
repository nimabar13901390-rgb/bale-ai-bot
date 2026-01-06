import re
from collections import Counter

class CompetitorAnalyzer:
    """تحلیل‌گر رقبا"""
    
    def __init__(self):
        self.competitor_data = {}
        self.learned_patterns = []
    
    def analyze_competitor_posts(self, posts):
        """تحلیل پست‌های رقیب"""
        analysis = {
            "top_keywords": [],
            "best_times": [],
            "content_patterns": [],
            "hashtags": [],
            "engagement_patterns": []
        }
        
        # استخراج کلمات کلیدی
        all_text = " ".join(posts)
        words = re.findall(r'\b\w+\b', all_text.lower())
        
        # حذف کلمات عمومی
        stop_words = {'و', 'در', 'با', 'از', 'به', 'برای'}
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # پیدا کردن کلمات پرتکرار
        word_counts = Counter(filtered_words)
        analysis["top_keywords"] = word_counts.most_common(20)
        
        # استخراج هشتگ‌ها
        hashtags = re.findall(r'#(\w+)', all_text)
        analysis["hashtags"] = Counter(hashtags).most_common(10)
        
        # تشخیص الگوهای محتوا
        analysis["content_patterns"] = self.detect_content_patterns(posts)
        
        return analysis
    
    def detect_content_patterns(self, posts):
        """تشخیص الگوهای محتوای موفق"""
        patterns = []
        
        for post in posts:
            pattern = {
                "type": self.classify_post_type(post),
                "length": len(post),
                "has_question": "؟" in post or "?" in post,
                "has_emoji": bool(re.findall(r'[^\w\s#@]', post)),
                "hashtag_count": len(re.findall(r'#\w+', post))
            }
            patterns.append(pattern)
        
        return patterns
    
    def classify_post_type(self, content):
        """طبقه‌بندی نوع پست"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["آموزش", "یادگیری", "درس"]):
            return "educational"
        elif any(word in content_lower for word in ["پروژه", "ساخت", "عملی"]):
            return "project"
        elif any(word in content_lower for word in ["سوال", "چطور", "چرا"]):
            return "question"
        elif any(word in content_lower for word in ["درآمد", "کسب", "پول"]):
            return "monetization"
        else:
            return "general"
