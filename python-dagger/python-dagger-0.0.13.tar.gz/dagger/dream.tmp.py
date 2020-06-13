# Dagger on Lambda
from dagger import initDagger
initDagger('asdf')

# Dagger in Python CLI Runtime
from dagger import initDagger
dagger_api = initDagger('asdf')

def main(input):
    return 1

if __name__ == "__main__":
    main = dagger_api.wrapTaskFunction(main)
    main()

# Dagger manually
from dagger import initDagger
dagger_api = initDagger('asdf')

def main(some_input):
    dagger_task = dagger_api.createTask('my task name', 'my unique run id')
    dagger_task.update(
        status='running',
        input=some_input
    )

    # do some things

    dagger_task.update(
        status='succeeded',
        output=some_output_value
    )
