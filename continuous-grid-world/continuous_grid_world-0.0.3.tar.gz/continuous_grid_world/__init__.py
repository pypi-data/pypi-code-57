from gym.envs.registration import register

register(
    id='ContinuousGridWorld-v0',
    entry_point='continuous_grid_world.envs:ContinuousGridWorldEnv',
    kwargs={
         'width': 1,
         'height': 1,
         'max_step': 0.1,
         'goal_x': 0.45,
         'goal_y': 0.45,
         'goal_side': 0.1,
         'radial_basis_fn': True,
         'x_dim': 10,
         'y_dim': 10
    }

)
