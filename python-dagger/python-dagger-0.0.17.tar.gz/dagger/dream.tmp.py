# Dagger on Lambda
from dagger import initDagger
initDagger('asdf')

import dagger

dagger.init('asdf')

# Dagger in Python CLI Runtime
from dagger import initDagger
dagger_api = initDagger('asdf')

def main(input):
    return 1

if __name__ == "__main__":
    main = dagger_api.wrapTaskFunction(main)
    main()


import dagger
dagger.init('apikey')
dagger.wrap(main)


import dagger
dagger.init('apikey')
dagger.wrap(main, task_name='', task_run_id='')

import dagger
dagger.init('apikey')
dagger.wrap(
    main, 
    task_name=lambda: some_variable, 
    task_run_id=lambda: os.getenv('something')
)

import dagger
dagger.init('apikey')
dagger.wrap(
    main, 
    task_name=lambda: some_variable, 
    task_run_id=lambda: os.getenv('something'),
    integration='aws_ecs'
)

import dagger
dagger.init('apikey')
dagger.wrap(
    main, 
    task_name=lambda: some_variable, 
    task_run_id=lambda: os.getenv('something'),
    integration=dagger.integrations.aws_ecs.AWSECSIntegration
)

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

