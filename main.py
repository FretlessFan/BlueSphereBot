import gymnasium as gym
import gym_examples  # Mandatory: This registers the environment!

# Create the environment using your custom ID
env = gym.make("gym_examples/BlueSphere-v0")

# Test a reset
observation, info = env.reset()
print("Print Intiial info",info)
print("Initial observation:", observation)

# Test a step
obs, reward, terminated, truncated, info = env.step(3)
print("Step reward:", reward)

print("Final_Obs:",obs)
print("Final_reward:", reward)
print("Terminated:", terminated)
