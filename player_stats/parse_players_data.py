import ijson
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

unique_data = set({})
with open(r"D:/Next Academy/My Own Project/football/player_stats/opta_clean_data.json", mode='r', encoding='utf-8') as f:
    json_file_attackers = ijson.items(f, 'player.attack.overall.item')

    for data in json_file_attackers:
        unique_data.add(
            f"{data.get('team_uuid')},p{data.get('player_id')},{data.get('player')},{data.get('contestantShortName')},{data.get('date_of_birth')}")
    f.seek(0)
    json_file_defenders = ijson.items(f, 'player.defending.overall.item')
    for data in json_file_defenders:
        unique_data.add(
            f"{data.get('team_uuid')},p{data.get('player_id')},{data.get('player')},{data.get('contestantShortName')},{data.get('date_of_birth')}")
    f.seek(0)
    json_file_goalkeeper = ijson.items(f, 'player.goalkeeping.overall.item')
    for data in json_file_goalkeeper:
        unique_data.add(
            f"{data.get('team_uuid')},p{data.get('player_id')},{data.get('player')},{data.get('contestantShortName')},{data.get('date_of_birth')}")

with open(r"D:/Next Academy/My Own Project/football/player_stats/opta_clean_data.csv", mode='w', encoding='utf-8') as f:
    f.write('club_id,player_id,player_name,club_name,birth_date\n')
    for data in unique_data:
        f.write(f"{data}\n")
