from playwright.sync_api import sync_playwright
import sys
import csv

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
url = "https://theanalyst.com/competition/premier-league/stats"

club_dic = {'a3nyxabgsqlnqfkeg41m6tnpp': 'Man City',
            '9q0arba2kbnywth8bkxlhgmdr': "Chelsea",
            '4dsgumo7d4zupm2ugsvm4zm4d': 'Arsenal',
            '6eqit8ye8aomdsrrq0hk3v7gh': 'Man Utd',
            '1pse9ta7a45pi2w2grjim70ge': 'Bournemouth',
            'c8h9bw1l82s06h77xxrelzhur': 'Liverpool',
            '7yx5dqhhphyvfisohikodajhv': 'Brentford',
            '1c8m2ko0wxq1asfkuykurdr0y': 'Crystal Palace',
            'e5p0ehyguld7egzhiedpdnc3w': 'Brighton',
            '7vn2i2kd35zuetw6b38gw9jsz': 'Newcastle',
            '48gk2hpqtsl6p9sx9kjhaydq4': 'Leeds',
            'hzqh7z0mdl3v7gwete66syxp': 'Fulham',
            'b496gs285it6bheuikox6z9mj': 'Aston Villa',
            'ehd2iemqmschhj2ec0vayztzz': 'Everton',
            '4txjdaqveermfryvbfrr4taf7': 'West Ham',
            "1qtaiy11gswx327s0vkibf70n": "Nott'm Forest",
            '22doj4sgsocqpxw45h607udje': 'Spurs',
            '1r3545b2dzan8yqa80gtmcjch': 'Sunderland',
            'b9si1jn1lfxfund69e9ogcu2n': 'Wolves',
            '64bxxwu2mv2qqlv0monbkj1om': 'Burnley'}
player_dic = dict({})
with open(r"D:/Next Academy/My Own Project/football/player_stats/opta_clean_data.csv", "r", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for players in reader:
        player_dic[players['Player Name']] = players['Player Id']

with sync_playwright() as p:
    counter = 1
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url=url, wait_until="commit")
    page.locator("text=filter players").click()
    min_slider = page.get_by_role("slider").first
    min_slider.focus()
    page.keyboard.press("Home")
    page.wait_for_timeout(300)
    max_slider = page.get_by_role("slider").last
    max_slider.focus()
    page.keyboard.press("End")
    page.wait_for_timeout(500)
    last_page_number = 13
    page.wait_for_selector("table")
    headers = page.locator("table th").all_inner_texts()
    headers[0] = 'player_name'
    headers[1] = 'matches_played'
    last_index = headers[-1]
    with open(r"D:/Next Academy/My Own Project/football/player_stats/players_attacking_25-26.csv", "w+", encoding='utf-8') as f:
        for header in headers:
            if header != last_index:
                f.write(
                    f"{header.lower().replace(' ','_').replace('%','percentage')},")
            else:
                f.write(f"{header},player_id,club_name\n")
        while counter <= last_page_number:
            rows = page.locator("table tbody tr").all()
            for row in rows:
                row_data = row.locator("td").all_inner_texts()
                player_name = row_data[0]
                c = 1
                club_img = row.locator("td img").first
                img_src = club_img.get_attribute("src")
                if img_src and "id=" in img_src:
                    opta_team_id = img_src.split("id=")[-1]
                else:
                    opta_team_id = "unknown"
                for data in row_data:
                    if c == len(row_data):
                        f.write(
                            f"{data},{player_dic.get(player_name)},{club_dic.get(opta_team_id)}\n")
                    else:
                        f.write(f"{data},")
                        c += 1
            page.get_by_role("button", name=">").click()
            page.wait_for_timeout(1000)
            counter += 1
