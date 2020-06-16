import suanpan
from suanpan.app import app
from suanpan.app.arguments import String

app.sio.disable()

@app.trigger.interval(5)
@app.trigger.output(String(key="outputData1"))
def test2(_):
    return "test"


if __name__ == "__main__":
    suanpan.run(app)
