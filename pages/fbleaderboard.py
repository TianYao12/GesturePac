from taipy.gui import Gui, Markdown
import requests
import pandas as pd



title="Flappy Bird Global Leaderboard"

response = requests.get("http://127.0.0.1:8000/users_flap/").json()['data']
response = pd.DataFrame.from_records(response)
response = response.drop(columns=["id"])

def update_leaderboard(state):
    res = requests.get("http://127.0.0.1:8000/users_flap/").json()['data']
    state.response = pd.DataFrame.from_records(res).drop(columns=["id"])
    
    

# Definition of the page
fbleaderboard_page = Markdown("""
## Flappy Bird Global Leaderboard
<|{response}|table|page_size=10|filter=true|>
<|Refresh|button|on_action=update_leaderboard|>
""")


