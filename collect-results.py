
import os
import json
import sys
import pprint

countBySolver = {"chuffed": 0, "kissat": 0, "or-tools": 0}

allInfo = []

for dirpath, dirnames, filenames in os.walk("conjure-output"):
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
            allInfo.append(([solver, order, shift], info))
            if float(info["SolverTotalTime"]) <= 10:
                countBySolver[solver] += 1

pprint.pprint(countBySolver)

maxLength = 0
maxNbInv = 0
justTheCounts = {}

headers = set()
for _, info in allInfo:
    headers = headers.union(info.keys())
headers = sorted(list(headers))

with open("outputs/info.csv", "w") as out:
    heading = ", ".join(["solver", "length", "nbInv"] + headers)
    print(heading, file=out)
    for [solver, length, nbInv], info in allInfo:
        maxLength = max(maxLength, int(length))
        maxNbInv = max(maxNbInv, int(nbInv))
        if solver == "minionpar":
            justTheCounts[int(length), int(nbInv)] = info["SolverSolutionsFound"]
        print(", ".join([solver, length, nbInv] + [info[k] if k in info.keys() else "NA"
              for k in headers]), file=out)
