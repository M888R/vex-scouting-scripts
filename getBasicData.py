import requests
import json

# can loop through some data file for which teams to search
requested_team = "2150B"

get_rankings_url = "https://api.vexdb.io/v1/get_rankings?team=" + requested_team + "&season=Turning Point"
get_matches_url = "https://api.vexdb.io/v1/get_matches?team=" + requested_team + "&season=Turning Point"

get_rankings = requests.get(get_rankings_url)
get_matches = requests.get(get_matches_url)

if get_rankings.status_code == 0 or get_matches.status_code == 0:
  print("You have likely given an invalid team.\n")

matches_data = get_matches.json()
matches_result = matches_data['result']

average_score = 0.0
num_matches = len(matches_result)

for match in matches_result:
  if match['scored'] == 0:
    num_matches -= 1
    print(num_matches)
  isBlue = False
  if match['blue1'] == requested_team or match['blue2'] == requested_team or match['blue3'] == requested_team:
    isBlue = True
  else:
    isBlue = False

  if isBlue:
    average_score += match['bluescore']
  else:
    average_score += match['redscore']

average_score /= num_matches

print("Average Score: " + str(average_score))

rankings_data = get_rankings.json()
rankings_result = rankings_data['result']

most_recent_opr = rankings_result[0]['opr']
print("Most Recent OPR: " + str(most_recent_opr))

most_recent_dpr = rankings_result[0]['dpr']
print("Most Recent DPR: " + str(most_recent_dpr))

average_ap = 0.0
num_events = 0

worlds_sku = 'RE-VRC-18-6082'

for ranking in rankings_result:
  if ranking['sku'] == worlds_sku:
    continue
  num_events += 1
  average_ap += ranking['ap']

if num_events == 0:
  print("This team has not been to any events.")
else:
  average_ap /= num_events

print("Average AP: " + str(average_ap))