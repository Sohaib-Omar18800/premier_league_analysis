from playwright.sync_api import sync_playwright
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
url = "https://theanalyst.com/competition/premier-league/stats"
club_dic = {'Man City': 'a3nyxabgsqlnqfkeg41m6tnpp',
            "Chelsea": '9q0arba2kbnywth8bkxlhgmdr',
            'Arsenal': '4dsgumo7d4zupm2ugsvm4zm4d',
            'Man Utd': '6eqit8ye8aomdsrrq0hk3v7gh',
            'Bournemouth': '1pse9ta7a45pi2w2grjim70ge',
            'Liverpool': 'c8h9bw1l82s06h77xxrelzhur',
            'Brentford': '7yx5dqhhphyvfisohikodajhv',
            'Crystal Palace': '1c8m2ko0wxq1asfkuykurdr0y',
            'Brighton': 'e5p0ehyguld7egzhiedpdnc3w',
            'Newcastle': '7vn2i2kd35zuetw6b38gw9jsz',
            'Leeds': '48gk2hpqtsl6p9sx9kjhaydq4',
            'Fulham': 'hzqh7z0mdl3v7gwete66syxp',
            'Aston Villa': 'b496gs285it6bheuikox6z9mj',
            'Everton': 'ehd2iemqmschhj2ec0vayztzz',
            'West Ham': '4txjdaqveermfryvbfrr4taf7',
            "Nottm Forest": "1qtaiy11gswx327s0vkibf70n",
            'Spurs': '22doj4sgsocqpxw45h607udje',
            'Sunderland': '1r3545b2dzan8yqa80gtmcjch',
            'Wolves': 'b9si1jn1lfxfund69e9ogcu2n',
            'Burnley': '64bxxwu2mv2qqlv0monbkj1om'}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url=url, wait_until="commit")
    page.locator("text=teams").click()
    page.wait_for_selector("table")
    rows = page.locator("table tbody tr").all()
    with open(r"D:/Next Academy/My Own Project/football/attacking/clubs_attacking_overall_25-26.csv", "+w", newline='\n') as f:
        f.write(
            "club_name,matches_played,goal,xg,goals_vs_xg,shots,sot,conv_percentage,xg_per_shot,club_id\n")
        for row in rows:
            counter = 1
            row_data = row.locator("td").all_inner_texts()
            club_id = club_dic.get(row_data[0])
            for data in row_data:
                if counter == len(row_data):
                    f.write(f"{data},{club_id}\n")

                else:
                    f.write(f"{data},")
                    counter += 1
    browser.close()
