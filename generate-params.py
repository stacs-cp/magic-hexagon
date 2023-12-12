
import os

solvers = ["or-tools", "chuffed", "kissat"]

orders = range(3, 8+1)
shifts = range(-100, 100+1)

with open("commands.txt", "w") as commandsfile:
    for model in ["abnormal", "abnormal-implied"]:
        for solver in solvers:
            for order in orders:
                for shift in shifts:
                    parambasename = f"order{str(order).zfill(3)}--shift{str(shift).zfill(4)}--{solver}"
                    paramfilename = f"{parambasename}.param"
                    infofilename = f"conjure-output-{model}/model000001-{parambasename}.eprime-info"
                    if os.path.isfile(infofilename):
                        print(f"Skipping {paramfilename}")
                        pass
                    else:
                        print(f"Generating {paramfilename} -- missing {infofilename}")
                        with open(paramfilename, "w") as f:
                            print(f"""
                                letting order be {order}
                                letting shift be {shift}""", file=f)
                        if solver == "or-tools":
                            print(f"conjure solve {model}.essence {paramfilename} --output-directory=conjure-output-{model} --solver={solver} --output-format=json --copy-solutions=no --solver-options='--threads 8'", file=commandsfile)
                        else:
                            print(f"conjure solve {model}.essence {paramfilename} --output-directory=conjure-output-{model} --solver={solver} --output-format=json --copy-solutions=no", file=commandsfile)
