from gym.envs.registration import register

register(
    id='foo-v0',
    entry_point='luwi_gym_foo.envs:FooEnv',
)

