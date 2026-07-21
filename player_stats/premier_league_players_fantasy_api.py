import sys
import requests

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

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
            "Nott'm Forest": "1qtaiy11gswx327s0vkibf70n",
            'Spurs': '22doj4sgsocqpxw45h607udje',
            'Sunderland': '1r3545b2dzan8yqa80gtmcjch',
            'Wolves': 'b9si1jn1lfxfund69e9ogcu2n',
            'Burnley': '64bxxwu2mv2qqlv0monbkj1om'}

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    teams_dict = {team['id']: team['name'] for team in data['teams']}
    element_dic = {element['id']: element["singular_name"]
                   for element in data['element_types']}
    counter = 0
    with open("D:/Next Academy/My Own Project/football/player_stats/premier_league_players.csv", "w+", encoding="utf-8") as f:
        f.write(
            "Club ID,Player Id,Club Name,Full Name,Web Name,Pos,Cost\n")
        for player in data['elements']:
            first_name = player['first_name']
            second_name = player['second_name']
            full_name = f"{first_name} {second_name}".strip()
            web_name = player['web_name']
            club_name = teams_dict.get(player['team'], "Unknown Club")
            club_id = club_dic.get(club_name)
            element_type = element_dic.get(
                player['element_type'], "Unknow Element")
            player_cost = player['now_cost']
            player_id = player['opta_code']
            counter += 1
            f.write(
                f"{club_id},{player_id},{club_name},{full_name},{web_name},{element_type},{player_cost/10}M\n")
except Exception as e:
    print(f"Raised an Error: {e}")
