import requests
import json

# can loop through some data file for which teams to search
requested_team = input("What team would you like stats for? ")  

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
  if match['scored'] == 0: # if match hasn't been scored remove it
    num_matches -= 1
    continue
  isBlue = False
  if match['blue1'] == requested_team or match['blue2'] == requested_team or match['blue3'] == requested_team:
    isBlue = True
  else:
    isBlue = False

  if isBlue:
    average_score += match['bluescore']
  else:
    average_score += match['redscore']

if num_matches == 0:
  print("This team hasn't played any matches.")
else:
  average_score /= num_matches


print(requested_team + " Statistics")
print("Average Score: " + str(average_score))

rankings_data = get_rankings.json()
rankings_result = rankings_data['result']

most_recent_opr = rankings_result[0]['opr']
print("Most Recent OPR: " + str(most_recent_opr))

most_recent_dpr = rankings_result[0]['dpr']
print("Most Recent DPR: " + str(most_recent_dpr))

average_ap = 0.0
num_events = 0
avg_percent_autons_won = 0.0

worlds_sku = 'RE-VRC-18-6082'

# get the % autos won for one tourney
# and then get the average % autos won for all tourneys
for event in rankings_result:
  if event['sku'] == worlds_sku:
    continue
  get_matches_event_url = "https://api.vexdb.io/v1/get_matches?team=" + requested_team + "&season=Turning Point" + "&sku=" + event['sku']
  get_matches_event = requests.get(get_matches_event_url)
  get_matches_event_data = get_matches_event.json()
  get_matches_event_result = get_matches_event_data['result']
  num_matches = 0
  last_match_num = 0
  for match in get_matches_event_result:
    if match['matchnum'] <= last_match_num:
      break
    last_match_num = match['matchnum']
    num_matches += 1
  num_events += 1
  current_ap = event['ap']
  percent_autons_won = current_ap / 4.0 / num_matches
  avg_percent_autons_won += percent_autons_won
  average_ap += event['ap']

if num_events == 0:
  print("This team has not been to any events.")
else:
  avg_percent_autons_won /= num_events
  average_ap /= num_events

print("Average AP: " + str(average_ap))
print("Average % Autons: " + str(avg_percent_autons_won * 100.0) + "%")