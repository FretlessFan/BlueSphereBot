import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import random
import pickle
from stable_baselines3.common.monitor import Monitor
from sb3_contrib.common.wrappers import ActionMasker
from stable_baselines3 import DQN,PPO
import os

from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.evaluation import evaluate_policy
from sb3_contrib.common.maskable.utils import get_action_masks


from stable_baselines3.common.vec_env import VecNormalize, DummyVecEnv

from gym_examples.envs import BlueSphereEnv # Even though we don't use this class here, we should include it here so that it registers the WarehouseRobot environment.

import os
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback
import glob



# 2. Build a localized environment factory
def make_env():
    # Instantiate your custom environment
    env = BlueSphereEnv()

    env = Monitor(env, filename=os.path.join("logs", "monitor.csv"))

    # Wrap it so MaskablePPO knows where to harvest the valid move data
    #env = ActionMasker(env, mask_fn)
    return env



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

def train_sb3_ppo():
    model_dir = "models"
    log_dir = "logs"
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    env = DummyVecEnv([make_env])

    #env = gym.make('gym_examples/BlueSphere-v0')
    env = VecNormalize(env, norm_obs=False, norm_reward=True, clip_reward=10.0)
    env.set_options(options="random")
    TOTAL_TIMESTEPS = 2_000_000
    SAVE_FREQ = 50_000



    # 2. Setup the automatic saving callback
    checkpoint_callback = CheckpointCallback(
        save_freq=SAVE_FREQ,
        save_path=model_dir,
        name_prefix="ppo_bluesphere"
    )

    if len(os.listdir(model_dir)) != 0:
        zip_files = glob.glob(os.path.join("models", "*.zip"))
        bizness = max(zip_files, key=os.path.getmtime)

        # Use MaskablePPO instead of DQN to load
        model = MaskablePPO.load(bizness, env=env)
        print(f"Loading existing model from: {bizness}")

        # Set PPO-compatible hyperparameters for continuing
        model.learning_rate = 1e-5

    else:
        print("Creating brand new MaskablePPO model...")
        # MaskablePPO replaces DQN entirely
        model = MaskablePPO(
            policy="MultiInputPolicy",  # Keeps MultiInputPolicy for dictionaries
            env=env,
            verbose=1,
            device="cuda",
            tensorboard_log=log_dir,
            # --- PPO HYPERPARAMETERS (Optimized for Stability) ---
            learning_rate=linear_schedule(1e-4),
            n_steps=2048,  # Batch collection size per roll-out
            batch_size=64,  # Minibatch size for gradient updates
            n_epochs=10,  # Number of optimization epochs per roll-out
            gamma=0.9975,  # Matches your original long-horizon preference
            gae_lambda=0.95,  # Generalized Advantage Estimation smoothing
            clip_range=0.2,  # PPO policy clipping threshold
            ent_coef=0.01,  # Entropy coefficient replaces epsilon-greedy for exploration
            policy_kwargs={"net_arch": dict(pi=[256, 256], vf=[256, 256])},
        )

    # 5. Train the model
    try:
        model.learn(
            total_timesteps=TOTAL_TIMESTEPS,
            callback=checkpoint_callback,
            reset_num_timesteps=False,  # Retains global steps when resuming
        )
        # Save the final version at the end of training
        model.save(os.path.join(model_dir, "ppo_bluesphere_final"))
    except KeyboardInterrupt:
        print("Training interrupted. Saving current state...")
        model.save(os.path.join(model_dir, "ppo_bluesphere_interrupted"))





def train_sb3_ppo_multi_agents(num_cores=16):
    model_dir = "models"
    log_dir = "logs"
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    env = SubprocVecEnv([make_env for _ in range(num_cores)])

    #env = DummyVecEnv([make_env])

    #env = gym.make('gym_examples/BlueSphere-v0')
    env = VecNormalize(env, norm_obs=False, norm_reward=True, clip_reward=10.0)
    env.set_options(options="random")
    TOTAL_TIMESTEPS = 3_000_000
    SAVE_FREQ = 50_000



    # 2. Setup the automatic saving callback
    checkpoint_callback = CheckpointCallback(
        save_freq=SAVE_FREQ,
        save_path=model_dir,
        name_prefix="ppo_bluesphere"
    )

    if len(os.listdir(model_dir)) != 0:
        zip_files = glob.glob(os.path.join("models", "*.zip"))
        bizness = max(zip_files, key=os.path.getmtime)

        # Use MaskablePPO instead of DQN to load
        model = MaskablePPO.load(bizness, env=env)
        print(f"Loading existing model from: {bizness}")

        # Set PPO-compatible hyperparameters for continuing
        model.learning_rate = 1e-5

    else:
        print("Creating brand new MaskablePPO model...")
        # MaskablePPO replaces DQN entirely
        model = MaskablePPO(
            policy="MultiInputPolicy",  # Keeps MultiInputPolicy for dictionaries
            env=env,
            verbose=1,
            device="cuda",
            tensorboard_log=log_dir,
            # --- PPO HYPERPARAMETERS (Optimized for Stability) ---
            learning_rate=linear_schedule(1e-4),
            n_steps=2048,  # Batch collection size per roll-out
            batch_size=64,  # Minibatch size for gradient updates
            n_epochs=10,  # Number of optimization epochs per roll-out
            gamma=0.9975,  # Matches your original long-horizon preference
            gae_lambda=0.95,  # Generalized Advantage Estimation smoothing
            clip_range=0.2,  # PPO policy clipping threshold
            ent_coef=0.01,  # Entropy coefficient replaces epsilon-greedy for exploration
            policy_kwargs={"net_arch": dict(pi=[256, 256], vf=[256, 256])},
        )

    # 5. Train the model
    try:
        model.learn(
            total_timesteps=TOTAL_TIMESTEPS,
            callback=checkpoint_callback,
            reset_num_timesteps=False,  # Retains global steps when resuming
        )
        # Save the final version at the end of training
        model.save(os.path.join(model_dir, "ppo_bluesphere_final"))
    except KeyboardInterrupt:
        print("Training interrupted. Saving current state...")
        model.save(os.path.join(model_dir, "ppo_bluesphere_interrupted"))




def train_sb3_dqn():
    model_dir = "models"
    log_dir = "logs"
    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    env = DummyVecEnv([lambda: BlueSphereEnv()])
    #env = gym.make('gym_examples/BlueSphere-v0')
    env = VecNormalize(env, norm_obs=False, norm_reward=True, clip_reward=10.0)
    env.set_options(options="random")
    TOTAL_TIMESTEPS = 3_000_000
    SAVE_FREQ = 50_000



    # 2. Setup the automatic saving callback
    checkpoint_callback = CheckpointCallback(
        save_freq=SAVE_FREQ,
        save_path=model_dir,
        name_prefix="dqn_bluesphere"
    )

    # Check if we should resume training
    if len(os.listdir(model_dir)) != 0:
        zip_files = glob.glob(os.path.join("models", "*.zip"))
        bizness = max(zip_files, key=os.path.getmtime)
        model = DQN.load(".//models//" + bizness.split("""\\""")[1], env=env)
        print(f"Loading existing model from: {bizness}")


        # Optional: Reset the total timesteps in the environment if resuming fresh
        #model.num_timesteps = 0
        model.learning_rate = 1e-5

        # 2. Lock exploration to a low constant rate (prevents it from decaying to 0)
        model.exploration_initial_eps = 0.20
        model.exploration_final_eps = 0.07

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
            gamma=0.9975,
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
            reset_num_timesteps=False,  # Keeps tracking total steps if resuming,

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


if __name__ == '__main__':
    train_sb3_ppo_multi_agents(4)
