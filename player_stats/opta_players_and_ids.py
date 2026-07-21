import json
import time
from playwright.sync_api import sync_playwright
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

url_page = 'https://theanalyst.com/competition/premier-league/stats'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    data_captured = False

    # دالة التصنت النظيفة والمصححة
    def handle_response(response):
        global data_captured
        try:
            # التأكد من الرابط وحالة الطلب بالطريقة الصح للـ Playwright (.status)
            if "tournamentstats" in response.url and response.status == 200:
                raw_text = response.text()

                if raw_text and (raw_text.strip().startswith('{') or raw_text.strip().startswith('[')):
                    json_data = json.loads(raw_text)

                    # لو طلعت رسالة طلب الجلسة القديمة، فكك منها واستنى الـ Request اللي بعده
                    if "code" in json_data and json_data["code"] == "rest_session_required":
                        return

                    # هنا الكنز الحقيقي!
                    with open(r"D:/Next Academy/My Own Project/football/player_stats/opta_clean_data.json", "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=4, ensure_ascii=False)
                    print("🎉 قفشنا الداتا وهي ماشية في السلك!")
                    print("💾 تم حفظ الكنز بنجاح في ملف: opta_clean_data.json")
                    data_captured = True
        except Exception as e:
            pass

    # تفعيل جهاز التصنت
    page.on("response", handle_response)

    print("جاري فتح الموقع...")
    page.goto(url=url_page, wait_until='domcontentloaded')

    # بنستنى 6 ثواني الصفحة تفتح براحتها
    page.wait_for_timeout(6000)

    print("جاري عمل سكرول في الصفحة لإجبار الموقع على طلب الداتا...")
    for i in range(5):
        page.evaluate("window.scrollBy(0, 600);")
        page.wait_for_timeout(2000)

        if data_captured:
            break

    time.sleep(2)
    if data_captured:
        print("Done! الملف جاهز عندك في الفولدر ونوم العوافي يا بطل.")
    else:
        print("❌ لم يتم قفش الداتا بعد، جرب تشغل الكود مرة أخرى لضمان تحميل السيرفر.")

    browser.close()
