import json
def load(file_name):
    bl = []
    with open(file_name, "r") as rl:
        bl_j = json.loads(rl.read())
    for i in bl_j.keys():
        exec(f"{i}=Dingrobot.robot.robot('{bl_j[i]['token']}','{bl_j[i]['key']}')")
    return bl