from random import choice
import os
import sys
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
    sessions = glob.glob('*.json')
    print("Present Sessions:")
    print("[0] New Session")
    for i, path in enumerate(sessions):
        print("[{}] {}".format(i+1, path))

    inp = input("Load Session: ")
    if (inp == "" or inp == "0"):
        return None
    return sessions[int(inp)-1]


def clear(text=""):
    # for linux and mac
    if os.name == "posix":
        _ = os.system("clear")

    # for windows (here, os.name is 'nt')
    else:
        _ = os.system("cls")

    if text:
        print(text)



def get_input() -> int:
    """ Returns a number, if one got 'inputted'.
    Might throw a KeyboardInterrupt.

    Args:
        None

    Returns:
        int: number between 0 and 3

    Throws:
        KeyboardInterrupt, if the user intends to end inputting values
    """
    try:
        inp = input()
    except EOFError:
        raise KeyboardInterrupt("exiting")

    lower = inp.lower()
    if lower == "exit" or lower == "end" or not lower:
        raise KeyboardInterrupt("exiting")

    try:
        index = int(inp)
        assert index > -1
        assert index < 4
    except (ValueError, AssertionError):
        print(
            "Please enter '1', '2' or '3' to select one of the presented values, or '0' if they are of equal value to you."
        )
        return get_input()  # this might lead to a very unlikely
        # 'recursion limit error' when repeated more than 5k times.
        # (or whatever is the limit in your current python runtime)
    return index



def main(showDescr = True):
    print("welcome to the core value finder")
    values = {}
    valueset = loadValues()

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
        print("New Session")
        for v in valueset.keys():
            values[v] = 0

    # 2^len(values) comparisons are a good estimate to get solid value differences.
    # can be aborted prior to that, and repeated.
    for _ in range(2 ** len(values)):
        selection = [choice([*values]), choice([*values]), choice([*values])]
        clear()
        if showDescr:
            for i in range(0, len(selection)):
                valueName = selection[i]
                print("[{}] {} -- {}".format(i+1, valueName, valueset.get(valueName,{}).get('descr',"")))
        else:
            print("[1] {0} [2] {1} [3] {2}".format(selection[0], selection[1], selection[2]))

        try:
            index = get_input()
            if index:  # if index == 0: don't evaluate
                values[selection[index - 1]] += 1
        except KeyboardInterrupt:

            print("Saving Session: {}".format(sessionPath))
            dump = {
                "values": values,
                "timestamp": time.strftime("%Y%m%d-%H%M%S")
            }
            json_data = json.dumps(dump, indent=2)
            with open(sessionPath,'w') as file:
                file.write(json_data)
            break

    sorted_x = sorted(values.items(), key=operator.itemgetter(1), reverse=True)
    clear("Values sorted by number of times they 'outcompeted' others.")
    print("A total of {0} comparisons has been done.\n".format(sum(values.values())))
    print("----- ---------------")
    for k, v in sorted_x:
        print("{1:>4}: {0}".format(k, v))


if __name__ == "__main__":
    main(not (len(sys.argv) > 1 and sys.argv[1] == "--no-descr"))

