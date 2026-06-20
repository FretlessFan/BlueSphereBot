import os
from pathlib import Path

import cv2
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks

from gym_examples.envs import bluesphere_visualizer
import gymnasium as gym
from stable_baselines3 import DQN  # Replace with your algorithm
from gym_examples.envs import BlueSphereEnv
import glob
# 1. Load the environment
env = gym.make('gym_examples/BlueSphere-v0')


def make_training_video(location="."):
    # 3. Test the model
    obs, info = env.reset(options=None)
    destin_location = Path(location)
    print("making training video")
    photo_folder = "photo_folder"
    folder_path = Path("photo_folder")
    os.makedirs(folder_path, exist_ok=True)
    original_files = os.listdir(folder_path)

    for elem in original_files:
        os.remove(folder_path / elem)

    done = False

    state_list = []
    while not done:
        current_masks = get_action_masks(env)
        action, _states = model.predict(obs, action_masks=current_masks, deterministic=True)

        print(action)
        obs, reward, terminated, truncated, info = env.step(action)
        current_page = bluesphere_visualizer.draw_current_stage_return(obs["grid"])
        state_list.append(current_page)
        print(obs)
        print(reward)
        #    list(obs["grid"].tolist())
        done = terminated or truncated

    env.close()

    current_page = bluesphere_visualizer.draw_current_stage_return(obs["grid"])
    state_list.append(current_page)

    video = cv2.VideoWriter(destin_location/'video.avi',  cv2.VideoWriter_fourcc(*'DIVX'), 10, (state_list[0].shape[0], state_list[0].shape[0]))

    for i in range(len(state_list)):
        cv2.imwrite(folder_path/f'output_image_{i}.png', state_list[i])


    sorted_files = sorted(
        os.listdir(folder_path),
        key=lambda x: os.path.getmtime(os.path.join(folder_path, x))
    )

    for image in sorted_files:
        video.write(cv2.imread(folder_path/image))

    # Release the video file
    video.release()

    os.startfile(destin_location/'video.avi')
    print(len(state_list))
    #
    # for elem in state_list:
    #     video.write(elem)
    #
    # video.release()
    #


def diagnose_best_model():
    # 3. Test the model
    obs, info = env.reset(options=None)
    done = False

    while not done:
        current_masks = get_action_masks(env)
        action, _states = model.predict(obs, action_masks=current_masks, deterministic=True)

        print(action)
        obs, reward, terminated, truncated, info = env.step(action)
        bluesphere_visualizer.draw_current_stage(obs["grid"])

        print(obs)
        print(reward)
        #    list(obs["grid"].tolist())
        done = terminated or truncated

    env.close()


# 2. Load the trained model
# Replace with the algorithm you trained (PPO, A2C, DQN, etc.)
zip_files = glob.glob(os.path.join("models", "*.zip"))
bizness = max(zip_files, key=os.path.getmtime)
model = MaskablePPO.load(".//models//"+bizness.split("""\\""")[1], env=env)
#model = MaskablePPO.load(".//models//ppo_bluesphere_final")
done = False
print(f"Loading existing model from: {bizness}")



#obs, info = env.reset(options=None)

#diagnose_best_model()
make_training_video()