import databoost
from databoost.envs.metaworld.utils import load_env_state
from databoost.utils.data import find_h5, read_h5
import cv2
import pickle
import numpy as np

lens = []
total_len = 0
min_len = 999
max_len = 0
min_file = ""
max_file = ""
file_paths = find_h5("/data/jullian-yapeter/DataBoostBenchmark/metaworld/data/prior")
for file_path in file_paths:
    curr_len = len(read_h5(file_path).observations)
    if curr_len > max_len:
        max_len = curr_len
        max_file = file_path
    if curr_len < min_len:
        min_len = curr_len
        min_file = file_path
    total_len += curr_len
    lens.append(curr_len)
print(f"avg_len: {total_len//len(file_paths)}")
print(f"max_len: {max_len}, {max_file}")
print(f"min_len: {min_len}, {min_file}")
print(f"std: {np.std(lens)}")
# max file = /data/jullian-yapeter/DataBoostBenchmark/metaworld/data/prior/plate-slide-side/plate-slide-side_2.h5
# benchmark = databoost.get_benchmark("metaworld")
# env = benchmark.get_env("pick-place-wall")
# ob = env.reset()
# with open("/data/jullian-yapeter/DataBoostBenchmark/metaworld/data/seed/plate-slide-back-side/plate-slide-back-side_5.pkl", "rb") as f:
#     env = pickle.load(f)
#     print(env.random_init)
# env.env = env_copy
# env = load_env_state(env, state)
# cv2.imwrite("plate-slide-back-side_5_test.jpg", env.default_render())
'''
dataset = env.get_prior_dataloader(seq_len=1, goal_condition=True)
i = 0
for traj in dataset:
    # print(traj["imgs"][0][0].shape)
    # print(goal["imgs"][0][0].shape)
    cv2.imwrite(f"traj_{i}.jpg", traj["imgs"][0][0].numpy())
    # cv2.imwrite(f"goal_{i}.jpg", goal["imgs"][0][0].numpy())
    if i > 10: break
    i += 1
'''