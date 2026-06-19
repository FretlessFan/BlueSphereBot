import os
from gym_examples.envs import bluesphere_visualizer
import gymnasium as gym
from stable_baselines3 import DQN  # Replace with your algorithm
from gym_examples.envs import BlueSphereEnv
import glob
# 1. Load the environment
env = gym.make('gym_examples/BlueSphere-v0')

# 2. Load the trained model
# Replace with the algorithm you trained (PPO, A2C, DQN, etc.)
zip_files = glob.glob(os.path.join("models", "*.zip"))
bizness = max(zip_files, key=os.path.getmtime)
model = DQN.load(".//models//"+bizness.split("""\\""")[1], env=env)
#model = DQN.load(".//models//dqn_bluesphere_2000000_steps")
done = False
print(f"Loading existing model from: {bizness}")


# 3. Test the model
#obs, info = env.reset(options="random")
obs, info = env.reset(options=None)

done = False


while not done:
    action, _states = model.predict(obs, deterministic=True)
    print(action)
    obs, reward, terminated, truncated, info = env.step(action)
    bluesphere_visualizer.draw_current_stage(obs["grid"])
    print(obs)
    print(reward)
#    list(obs["grid"].tolist())
    done = terminated or truncated

env.close()

