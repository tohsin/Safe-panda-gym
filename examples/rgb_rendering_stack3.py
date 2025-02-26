import gym
import panda_gym
from numpngw import write_apng  # pip install numpngw or pip install panda-gym[extra]

env = gym.make("PandaStack3-v2", render=True)
images = []


obs = env.reset()
done = False
v = env.render(mode = "rgb_array")
# images.append(env.render("rgb_array"))
images.append(v)

while not done:
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    v = env.render(mode = "rgb_array")
    images.append(v)

env.close()

write_apng("push-safe.png", images, delay=40)
