import csv

# this assumes that you beat everyone who was beaten by someone you directly beat in the race

def eventparse(filename, tournamentName): 
    
    event = open(filename, "r", encoding='utf-8')
    
    eventList = list(csv.reader(event))
    
    pairwise = list()
    profiles = dict()
    trailing= list()

    x = 0
    for n in eventList:
        pilot = list(eventList[x])
        names = pilot[1].replace("“", "\"").replace("”", "\"").split("\"")
        fullName = names[0].strip() + " " + names[-1].strip()
        fullName = fullName.lower()
        placePair = {}
        placePair[tournamentName] = {"placement": int(pilot[0]), "total": len(eventList), "prize": pilot[2]}
        profiles[fullName] = {"tournaments": placePair}
        for otherPilot in trailing:
            pairwise.append({"winner":otherPilot, "loser":fullName})
        trailing.append(fullName)

        x += 1 

    event.close()

    return profiles, pairwise

def eventmerge():
    events = list()
    # this has to be updated for every csv 
    events.append({"file": "2018multigp.csv", "humanname": "2018 MultiGP Championship"})
    events.append({"file": "2019idrlc.csv", "humanname": "2019 IDRLC"})
    events.append({"file": "2019multigp.csv", "humanname": "2019 MultiGP Championship"})
    events.append({"file": "2020multigp.csv", "humanname": "2020 MultiGP Championship"})
    pairwise = list()
    profiles = {}
    
    for event in events:
        eventprofiles, eventpaires = eventparse(event["file"], event["humanname"])
        pairwise.extend(eventpaires)
        for name, eventprofile in eventprofiles.items():
            if name in profiles:
                profiles[name]["tournaments"].update(eventprofile["tournaments"])
            else:
                profiles[name] = eventprofile
    pairwise.reverse()
    print(pairwise)
    return profiles, pairwise

eventmerge()