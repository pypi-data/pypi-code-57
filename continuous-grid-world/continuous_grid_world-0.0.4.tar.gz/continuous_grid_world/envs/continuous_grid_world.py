import gym
from gym import spaces
import numpy as np
from continuous_grid_world.radial_basis_function_2D import RadialBasisFunction2D

class ContinuousGridWorldEnv(gym.Env):
    def __init__(self, width, height, max_step, goal_x, goal_y, goal_side, radial_basis_fn, x_dim, y_dim):

        self.width = width
        self.height = height
        self.max_step = max_step
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_side = goal_side
        self.radial_basis_fn = radial_basis_fn

        obs_low = np.array([0., 0.], dtype=np.float32)
        obs_high = np.array([width, height], dtype=np.float32)
        act_high = np.array([max_step, max_step])
        self.action_space = spaces.Box(low=-act_high, high=act_high, dtype=np.float32)
        self.true_observation_space = spaces.Box(low=-obs_low, high=obs_high, dtype=np.float32)

        if self.radial_basis_fn:
            n_dim = x_dim * y_dim
            obs_low = np.array([0.] * n_dim, dtype=np.float32)
            obs_high = np.array([1.] * n_dim, dtype=np.float32)
            self.transformer = RadialBasisFunction2D(0.0, width, 0.0, height, x_dim, y_dim, 0.05)
            self.observation_space = spaces.Box(low=-obs_low, high=obs_high, dtype=np.float32)
        else:
            self.observation_space = self.true_observation_space

    def step(self, action):
        action = np.clip(action, -self.max_step, self.max_step).reshape(self.state.shape)
        self.state += action

        self.state = np.clip(self.state, self.true_observation_space.low, self.true_observation_space.high)
        reward = 0

        if self.in_box():
            reward = 1

        done = True if reward else False

        if self.radial_basis_fn:
            return self.radial_basis_state(), np.array([reward]), done, {}

        return self.state, np.array([reward]), done, {}

    def reset(self):
        self.state = self.true_observation_space.sample()

        if self.radial_basis_fn:
            return self.radial_basis_state()

        return self.state

    def render(self, mode='human', close=False):
        print(f'state: {self.state}')

    def in_box(self):
        x, y = self.state

        return ((x >= self.goal_x and x <= (self.goal_x + self.goal_side))
                and (y >= self.goal_y and y <= (self.goal_y + self.goal_side)))

    def radial_basis_state(self):
        return self.transformer.transform(self.state.reshape(1,-1))[0]
