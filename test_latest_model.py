import os
from gym_examples.envs import bluesphere_visualizer
import gymnasium as gym
from stable_baselines3 import DQN  # Replace with your algorithm
from gym_examples.envs import BlueSphereEnv
# 1. Load the environment
env = gym.make('gym_examples/BlueSphere-v0')

# 2. Load the trained model
# Replace with the algorithm you trained (PPO, A2C, DQN, etc.)
bizness = os.listdir("models")
model = DQN.load(".//models//"+bizness[-1], env=env)

# 3. Test the model
obs, info = env.reset()

done = False


while not done:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    bluesphere_visualizer.draw_current_stage(obs["grid"])
    print(obs)
#    list(obs["grid"].tolist())
    done = terminated or truncated

env.close()

