import gymnasium as gym

import panda_gym

env = gym.make("PandaReach-v3", render_mode="human")

observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()

env.close()
