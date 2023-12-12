
import datetime
import time
import socket
import resource
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# given order : int
order = 4

# letting ix be order - 1
ix = order - 1

# letting diameter be order * 2 - 1
diameter = order * 2 - 1

# letting max_val be 3 * order**2 - 3 * order + 1
max_val = 3 * order**2 - 3 * order + 1

# letting total_sum be max_val * (max_val+1) / 2 $ or: sum i : int(1 .. max_val) . i
total_sum = int(max_val * (max_val+1) / 2)

# $ See the "Cube coordinates" variant explained here: https://math.stackexchange.com/questions/2254655/hexagon-grid-coordinate-system
# $ Even better: https://www.redblobgames.com/grids/hexagons/#coordinates

# find hexagon : matrix indexed by [int(-ix..ix), int(-ix..ix), int(-ix..ix)] of int(0..max_val)
# $ used cells
# such that
# [ hexagon[i, j, k] != 0
# | i, j, k : int(-ix..ix)
# , i + j + k = 0
# ]


# $ unused cells
# such that
# [ hexagon[i, j, k] = 0
# | i, j, k : int(-ix..ix)
# , i + j + k != 0
# ]

hexagon = {}
for i in range(-ix, ix+1):
    for j in range(-ix, ix+1):
        for k in range(-ix, ix+1):
            if i + j + k == 0:
                hexagon[i, j, k] = model.NewIntVar(1, max_val, "")
            else:
                hexagon[i, j, k] = 0

# such that allDiff([ hexagon[i, j, k]
#                   | i, j, k : int(-ix..ix)
#                   , i + j + k = 0
#                   ])

model.AddAllDifferent([hexagon[i, j, k] for i in range(-ix, ix+1)
                       for j in range(-ix, ix+1)
                       for k in range(-ix, ix+1)
                       if i + j + k == 0
                       ])


# find sumsto : int(0..total_sum)

sumsto = model.NewIntVar(0, total_sum, "")

# $ such that diameter * sumsto = total_sum


# such that
# [ sumsto = sum([hexagon[i, j, k] | j, k : int(-ix..ix)])
# | i : int(-ix..ix)
# ]
for i in range(-ix, ix+1):
    model.Add(sum([hexagon[i, j, k]
                   for j in range(-ix, ix+1)
                   for k in range(-ix, ix+1)]) == sumsto)

# such that
# [ sumsto = sum([hexagon[i, j, k] | i, k : int(-ix..ix)])
# | j : int(-ix..ix)
# ]
for j in range(-ix, ix+1):
    model.Add(sum([hexagon[i, j, k]
                   for i in range(-ix, ix+1)
                   for k in range(-ix, ix+1)]) == sumsto)

# such that
# [ sumsto = sum([hexagon[i, j, k] | i, j : int(-ix..ix)])
# | k : int(-ix..ix)
# ]
for k in range(-ix, ix+1):
    model.Add(sum([hexagon[i, j, k]
                   for i in range(-ix, ix+1)
                   for j in range(-ix, ix+1)]) == sumsto)


# $ symmetry breaking
# $ see: https://proofwiki.org/wiki/Definition:Symmetry_Group_of_Regular_Hexagon#Group_Action_on_Vertices

# find A : int(0..max_val) such that A = hexagon[0,ix,-ix]
# find B : int(0..max_val) such that B = hexagon[ix,0,-ix]
# find C : int(0..max_val) such that C = hexagon[ix,-ix,0]
# find D : int(0..max_val) such that D = hexagon[-ix,0,ix]
# find E : int(0..max_val) such that E = hexagon[0,-ix,ix]
# find F : int(0..max_val) such that F = hexagon[-ix,ix,0]

# such that [A,B,C,D,E,F] <=lex [B,C,D,E,F,A]
# such that [A,B,C,D,E,F] <=lex [C,D,E,F,A,B]
# such that [A,B,C,D,E,F] <=lex [D,E,F,A,B,C]
# such that [A,B,C,D,E,F] <=lex [E,F,A,B,C,D]
# such that [A,B,C,D,E,F] <=lex [F,A,B,C,D,E]

# such that [A,B,C,D,E,F] <=lex [A,F,E,D,C,B]
# such that [A,B,C,D,E,F] <=lex [B,A,F,E,D,C]
# such that [A,B,C,D,E,F] <=lex [C,B,A,F,E,D]
# such that [A,B,C,D,E,F] <=lex [D,C,B,A,F,E]
# such that [A,B,C,D,E,F] <=lex [E,D,C,B,A,F]
# such that [A,B,C,D,E,F] <=lex [F,E,D,C,B,A]


################################################################################
# tick
################################################################################


hostname = socket.gethostname()


def getMemory():
    if hostname.startswith("manifesto"):
        # manifesto gives us kilobytes
        divisor = 1000
    else:
        # whereas my laptop gives bytes...
        divisor = 1000000
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / divisor


startTime = time.time()


def tick(message):
    diffTime = time.time() - startTime
    print("%-100s %10.2fMB %10.2fsecs %10.2fsecs" %
          (message, getMemory(), time.process_time(), diffTime))


def log(message):
    print(message)


solver = cp_model.CpSolver()
# solver.parameters.subsolvers = ["default_lp", "fixed", "less_encoding", "no_lp", "max_lp", "pseudo_costs", "reduced_costs", "quick_restart", "quick_restart_no_lp", "lb_tree_search", "probing"]
# solver.parameters.subsolvers = ["quick_restart"]
solutionPrinter = cp_model.ObjectiveSolutionPrinter()
solver.cp_trace_propagation = True
solver.cp_trace_search = True
solver.parameters.max_time_in_seconds = 10
solver.parameters.num_search_workers = 4
solver.parameters.log_search_progress = True
solverStartTime = datetime.datetime.now()
status = solver.SolveWithSolutionCallback(model, solutionPrinter)
solutionTime = (datetime.datetime.now() - solverStartTime).total_seconds()
log("")
log("Total Solution Time: " + str(round(solutionTime, 2)) + " s")

log("status: %d" % status)
if status == cp_model.OPTIMAL:
    log("status: OPTIMAL")
elif status == cp_model.FEASIBLE:
    log("status: FEASIBLE")
elif status == cp_model.INFEASIBLE:
    log("status: INFEASIBLE")
elif status == cp_model.MODEL_INVALID:
    log("status: MODEL_INVALID")
elif status == cp_model.UNKNOWN:
    log("status: UNKNOWN")

if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    for i in range(-ix, ix+1):
        for j in range(-ix, ix+1):
            for k in range(-ix, ix+1):
                if i + j + k == 0:
                    print(solver.Value(hexagon[i, j, k]), end='')
            print('\t', end='')
        print()
