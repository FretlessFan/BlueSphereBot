from gymnasium.envs.registration import register

register(
    id="gym_examples/BlueSphere-v0",
    entry_point="gym_examples.envs:BlueSphereEnv",
    max_episode_steps=200,  # Matches your turn_count truncated condition
)