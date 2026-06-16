import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import random
import pickle
from stable_baselines3 import DQN,PPO
import os
from gym_examples.envs import BlueSphereEnv # Even though we don't use this class here, we should include it here so that it registers the WarehouseRobot environment.

import os
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback


# 1. Define a learning rate schedule function based on 2 million total steps
def linear_schedule(initial_value: float):
    """
    Linear learning rate schedule.
    :param initial_value: Initial learning rate.
    :return: schedule that computes current learning rate depending on remaining progress
    """

    def func(progress_remaining: float) -> float:
        """
        Progress remaining decreases from 1.0 (start) to 0.0 (end)
        """
        return progress_remaining * initial_value

    return func


def train_sb3_dqn():
    model_dir = "models"
    log_dir = "logs"
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    env = gym.make('gym_examples/BlueSphere-v0')

    TOTAL_TIMESTEPS = 2_000_000
    SAVE_FREQ = 50_000

    # 2. Setup the automatic saving callback
    checkpoint_callback = CheckpointCallback(
        save_freq=SAVE_FREQ,
        save_path=model_dir,
        name_prefix="dqn_bluesphere"
    )

    # Check if we should resume training
    if len(os.listdir(model_dir)) != 0:
        bizness = sorted(os.listdir(model_dir))
        model_path = os.path.join(model_dir, bizness[-1])
        print(f"Loading existing model from: {model_path}")
        model = DQN.load(model_path, env=env)

        # Optional: Reset the total timesteps in the environment if resuming fresh
        model.num_timesteps = 0
    else:
        print("Creating brand new model...")
        model = DQN(
            policy='MultiInputPolicy',
            env=env,
            verbose=1,
            device='cuda',
            tensorboard_log=log_dir,

            # --- THE "PERFORMANCE" HYPERPARAMETERS ---
            # Pass the schedule function instead of a static float
            learning_rate=linear_schedule(1e-4),
            buffer_size=100_000,
            learning_starts=5000,
            batch_size=64,
            tau=1.0,
            target_update_interval=1000,
            train_freq=4,

            # --- THE MEMORY/STABILITY TWEAKS ---
            gamma=0.99,
            # Exploration will decay smoothly over 70% of the 2,000,000 steps
            exploration_fraction=0.7,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.06,

            policy_kwargs={"net_arch":[256,256]}
        )

    # 3. Train the model using a single call with the callback
    try:
        model.learn(
            total_timesteps=TOTAL_TIMESTEPS,
            callback=checkpoint_callback,
            reset_num_timesteps=False  # Keeps tracking total steps if resuming
        )
        # Save the final version at the end of training
        model.save(os.path.join(model_dir, "dqn_bluesphere_final"))
    except KeyboardInterrupt:
        print("Training interrupted. Saving current state...")
        model.save(os.path.join(model_dir, "dqn_bluesphere_interrupted"))

def train_sb3_dqn_basic():
    # Where to store trained model and logs_DQN
    model_dir = "models_nopa"
    log_dir = "basic"
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    env = gym.make('gym_examples/BlueSphere-v0')


    # Use MlpPolicy for observation space 1D vector.
    model = DQN('MultiInputPolicy', env, verbose=1, device='cuda', tensorboard_log=log_dir,
                exploration_fraction=0.5,  # Agent will explore for 50% of total training steps (default is 0.1)
                exploration_initial_eps=1.0,  # Starts with 100% random actions (default is 1.0)
                exploration_final_eps=0.05  # Stays at 5% random actions indefinitely after the fraction ends
                )


    # This loop will keep training until you stop it with Ctr-C.
    # Start another cmd prompt and launch Tensorboard: tensorboard --logdir logs_DQN
    # Once Tensorboard is loaded, it will print a URL. Follow the URL to see the status of the training.
    # Stop the training when you're satisfied with the status.
    TIMESTEPS = 1000
    iters = 0
    while True:
        iters += 1

        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)  # train
        model.save(f"{model_dir}/a2c_{TIMESTEPS * iters}")  # Save a trained model every TIMESTEPS


train_sb3_dqn()
