import config, subprocess
from functions import *

subprocess.run(["python3", "agent_1.py"], check=True)
subprocess.run(["python3", "agent_2.py"], check=True)
subprocess.run(["python3", "agent_3.py"], check=True)

repair_recommendations_json("data/recommendations.json", "data/recommendations.json")
recommendations_json_to_md("data/recommendations.json", "data/recommendations.md")
md_to_pdf("data/recommendations.md", "data/recommendations.pdf")
