import eventparse
import elo
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

profiles, pairwise = eventparse.eventmerge()
for name, profile in profiles.items():
    profile["elo"] = 1500
for match in pairwise:
    winner = match["winner"]
    loser = match["loser"]
    winnerscore, loserscore = elo.EloRating(profiles[winner]["elo"], profiles[loser]["elo"], 40, 1)
    profiles[winner]["elo"] = winnerscore
    profiles[loser]["elo"] = loserscore

def elofunction(profile):
    return profile[1]["elo"]

eloranked = sorted(profiles.items(), reverse = True, key = elofunction)
print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in eloranked) + "}")


env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(os.path.abspath(__file__))),
    autoescape=select_autoescape()
)
pilottemplate = env.get_template("pilot.html")
for name, profile in profiles.items():
    out = pilottemplate.render(name = name, profile = profile)
    outfile = open("output/{}.html".format(name.replace(" ", "_")), "w")
    outfile.write(out)
    outfile.close()
indextemplate = env.get_template("index.html")
out = indextemplate.render(profiles = profiles)
outfile = open("output/index.html", "w")
outfile.write(out)
outfile.close()
