from taipy.gui import Gui, Markdown
import requests
import pandas as pd



title="Pac-Man Global Leaderboard"

response = requests.get("http://127.0.0.1:8000/users_pac/").json()['data']
response = pd.DataFrame.from_records(response)
response = response.drop(columns=["id"])

def update_leaderboard(state):
    res = requests.get("http://127.0.0.1:8000/users_pac/").json()['data']
    state.response = pd.DataFrame.from_records(res).drop(columns=["id"])
    
    

# Definition of the page
pmleaderboard_page = Markdown("""
## Pac-Man Global Leaderboard
<|{response}|table|page_size=10|filter=true|>
<|Refresh|button|on_action=update_leaderboard|>
""")


