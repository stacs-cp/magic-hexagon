
import os
import json
import sys
import pprint

for model in ["abnormal", "abnormal-implied"]:
    for timelimit in [10, 60, 5*60, 10*60, None]:

        countBySolver = {}
        satisfiableBySolver = {}

        allInfo = []

        for dirpath, dirnames, filenames in os.walk(f"conjure-output-{model}"):
            for infofile in sorted(filenames):
                if infofile.endswith(".eprime-info"):
                    tmp = infofile.split(".")[0]
                    order = tmp[17:20]
                    shift = tmp[27:31]
                    solver = tmp[33:]
                    # print(tmp, order, shift, solver)
                    info = {}
                    try:
                        with open(f'{dirpath}/{infofile}', "r") as f:
                            for l in f:
                                [k, v] = l.split(":")
                                info[k.strip()] = v.strip()

                        try:
                            info["TotalTime"] = str(
                                float(info["SolverTotalTime"]) + float(info["SavileRowTotalTime"]))
                        except:
                            info["TotalTime"] = "NA"
                    except FileNotFoundError:
                        pass
                    if info["TotalTime"] != "NA":
                    # if "SolverTotalTime" in info.keys():
                        allInfo.append(([solver, order, shift], info))
                        # print(infofile)
                        if timelimit == None or float(info["TotalTime"]) <= timelimit:
                            try:
                                countBySolver[order][solver] += 1
                            except:
                                try:
                                    countBySolver[order][solver] = 1
                                except:
                                    countBySolver[order] = {}
                                    countBySolver[order][solver] = 1

                            if info["SolverSatisfiable"] == "1":
                                try:
                                    satisfiableBySolver[order][solver] += 1
                                except:
                                    try:
                                        satisfiableBySolver[order][solver] = 1
                                    except:
                                        satisfiableBySolver[order] = {}
                                        satisfiableBySolver[order][solver] = 1

        print(model, timelimit)
        print("countBySolver")
        pprint.pprint(countBySolver)
        for order in ["003", "004", "005", "006", "007", "008"]:
                print(" ".join([str(countBySolver[order][solver]) for solver in ["chuffed", "kissat", "or-tools"]]))
        print("satisfiableBySolver")
        pprint.pprint(satisfiableBySolver)
        print("\n\n")

        maxLength = 0
        maxNbInv = 0
        justTheCounts = {}

    headers = set()
    for _, info in allInfo:
        headers = headers.union(info.keys())
    headers = sorted(list(headers))

    with open(f"results/info-{model}.csv", "w") as out:
        heading = ", ".join(["solver", "length", "nbInv"] + headers)
        print(heading, file=out)
        for [solver, length, nbInv], info in allInfo:
            maxLength = max(maxLength, int(length))
            maxNbInv = max(maxNbInv, int(nbInv))
            if solver == "minionpar":
                justTheCounts[int(length), int(nbInv)] = info["SolverSolutionsFound"]
            print(", ".join([solver, length, nbInv] + [info[k] if k in info.keys() else "NA"
                for k in headers]), file=out)
