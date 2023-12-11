
import os

solvers = ["or-tools", "chuffed", "kissat"]

orders = range(3, 8+1)
shifts = range(-100, 100+1)

# orders = [3]
# shifts = range(0, 4)

# orders = range(3, 5+1)
# shifts = range(-10, 10+1)

with open("commands.txt", "w") as commandsfile:
    for solver in solvers:
        for order in orders:
            for shift in shifts:
                parambasename = f"order{str(order).zfill(3)}--shift{str(shift).zfill(4)}--{solver}"
                paramfilename = f"{parambasename}.param"
                infofilename = f"conjure-output/model000001-{parambasename}.eprime-info"
                if os.path.isfile(infofilename):
                    print(f"Skipping {paramfilename}")
                else:
                    print(f"Generating {paramfilename} -- missing {infofilename}")
                    with open(paramfilename, "w") as f:
                        print(f"""
                            letting order be {order}
                            letting shift be {shift}""", file=f)
                    print(f"conjure solve abnormal.essence {paramfilename} --solver={solver} --output-format=json", file=commandsfile)
