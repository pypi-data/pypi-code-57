
import atexit
import os
import shutil
import subprocess
import tempfile

def csv_of_minibn(bn):
    def str_of_lit(l):
        return "{}{}".format("!" if not l[1] else "", l[0])
    def str_of_clause(c):
        return "+".join(map(str_of_lit, c))
    rules = []
    for i, clauses in sorted(bn.as_dnf().items()):
        if isinstance(clauses, bool):
            raise TypeError("Boolean networks with constant nodes are not supported")
        for clause in clauses:
            rules.append("{}<-{}".format(i, str_of_clause(clause)))
    return "%s\n%s\n" % (",".join(rules), ",".join(["1"]*len(rules)))

def csv_of_scenario(fixed, goal):
    head = []
    line = []
    for prefix, d in [("SC:", fixed), ("SG:", goal)]:
        items = list(d.items())
        head += ["{}{}".format(prefix, n) for n,_ in items]
        line += ["1" if v else "-1" for _,v in items]
    return "%s\n%s\n" % (",".join(head), ",".join(line))

def caspo_control(bn, goal, fixed,
        allow_goal_intervention=False, maxsize=0):

    constants = bn.constants()
    if constants:
        # make constants input nodes and move their value into fixed
        bn = bn.copy()
        for n, v in constants.items():
            bn[n] = n
            if n not in fixed:
                fixed[n] = v

    # prepare temporary working space
    wd = tempfile.mkdtemp(prefix="caspo-")
    # cleanup working directory at exit
    def cleanup():
        shutil.rmtree(wd)
    atexit.register(cleanup)

    outdir = os.path.join(wd, "out")

    inp_network = os.path.join(wd, "network.csv")
    inp_scenario = os.path.join(wd, "scenarios.csv")
    with open(inp_network, "w") as fp:
        fp.write(csv_of_minibn(bn))
    with open(inp_scenario, "w") as fp:
        fp.write(csv_of_scenario(fixed, goal))
    cmdline = ["caspo", "--out", outdir,
            "control", inp_network, inp_scenario,
            "--size", str(maxsize)]
    if allow_goal_intervention:
        cmdline.append("--allow-goal")
    subprocess.check_call(cmdline)

    controls = []
    with open(os.path.join(outdir, "strategies.csv")) as fp:
        head = [h[3:] for h in fp.readline().strip().split(",")]
        if not head:
            return controls
        for line in fp:
            line = line.strip()
            if not line:
                break
            c = zip(head, map(int,line.split(",")))
            c = dict([(n,max(0,v)) for n,v in c if v != 0])
            controls.append(c)
    return controls

