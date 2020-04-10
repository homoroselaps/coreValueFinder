from random import choice
import operator
import json
import time
import glob

def loadValues():
    valuesFiles = glob.glob('*.values')
    selection = 0
    if (len(valuesFiles) > 1):
        print("Present value sets:")
        for i, path in enumerate(valuesFiles):
            print("[{}] {}".format(i+1, path))
        selection = int(input("Load value set: "))
    try:
        with open(valuesFiles[selection-1]) as json_file:
            return json.load(json_file)
    except Exception as e:
        print("Failed loading value set: {}".format(str(e)))
        return {}

def getSessionFilePath():
    sessions = glob.glob('.*.session')
    print("Present Sessions:")
    print("[0] New Session")
    for i, path in enumerate(sessions):
        print("[{}] {}".format(i+1, path))
        
    inp = input("Load Session: ")
    if (inp == "" or inp == "0"):
        return None
    return sessions[int(inp)-1]

def main():
    print("welcome to the core value finder")
    values = {}
    valueset = loadValues()
    showDescr = True

    sessionPath = getSessionFilePath()
    try:
        with open(sessionPath) as json_file:
            data = json.load(json_file)
            values = data['values']
    except Exception as e:
        print("Failed loading Session: {}".format(str(e)))
        print("Fallback to new Session")
        sessionPath = None

    if not sessionPath:
        sessionPath = ".{}.session".format(time.strftime("%Y-%m-%d-%H:%M"))
        print("New Session: {}".format(sessionPath))
        for v in valueset.keys():
            values[v] = 0
    
    while True:
        selection = [choice([*values]), choice([*values]), choice([*values])]
        if showDescr:
            for i in range(0, len(selection)):
                valueName = selection[i]
                print("[{}] {} -- {}".format(i+1, valueName, valueset.get(valueName,{}).get('descr',"")))
        else:
            print("[1] {0} [2] {1} [3] {2}".format(selection[0], selection[1], selection[2]))

        inp = input()
        if (inp.lower() == "descr"):
            showDescr = not showDescr
            continue
        if (inp.lower() == "exit" or inp.lower() == "quit"):
            sessionPath = sessionPath if sessionPath else "Session{}.json".format(time.strftime("%Y%m%d-%H%M%S"))
            print("Saving Session: {}".format(sessionPath))
            dump = {
                "values": values,
                "timestamp": time.strftime("%Y%m%d-%H%M%S")
            }
            json_data = json.dumps(dump, indent=2)
            with open(sessionPath,'w') as file:
                file.write(json_data)
            break
        try:
            index = int(inp)
            values[selection[index-1]] += 1
        except:
            print("Invalid Selection or command.")
            print("[1-3] : Select the value")
            print("exit/quit : Exit with saving the Session")
            print("descr : toggle description")

    sorted_x = sorted(values.items(), key=operator.itemgetter(1), reverse=True)
    for k,v in sorted_x:
        print("{0}:{1}".format(k,v))

main()