import copy
from typing import Dict

import gym
import numpy as np

from databoost.base import DataBoostEnvWrapper, DataBoostBenchmarkBase
from databoost.envs.metaworld.utils import initialize_env, render
import databoost.envs.metaworld.config as cfg


class DataBoostBenchmarkMetaworld(DataBoostBenchmarkBase):

    def __init__(self, mask_goal_pos=True):
        '''Meta-World DataBoost benchmark.

        Attributes:
            tasks_list [List]: the list of tasks compatible with this benchmark
        '''
        self.tasks_list = list(cfg.tasks.keys())
        if mask_goal_pos:
            def mask_goal_func(obs, reward, done, info):
                if len(obs.shape) == 1:
                    obs[-3:] = 0.0
                elif len(obs.shape) == 2:
                    obs[:, -3:] = 0.0
                elif len(obs.shape) == 3:
                    obs[:, :, -3:] = 0.0
                else:
                    raise ValueError
                return obs, reward, done, info
            self.postproc_func = mask_goal_func
        else:
            self.postproc_func = None

    def get_env(self, task_name: str) -> DataBoostEnvWrapper:
        '''get the wrapped gym environment corresponding to the specified task.

        Args:
            task_name [str]: the name of the task; must be from the list of
                             tasks compatible with this benchmark (self.tasks_list)
        Returns:
            env [DataBoostEnvWrapper]: wrapped env that implements getters for
                                       the corresponding seed and prior offline
                                       datasets
        '''
        task_cfg = cfg.tasks.get(task_name)
        assert task_cfg is not None, f"{task_name} is not a valid task name."
        task_cfg = copy.deepcopy(task_cfg)
        env = DataBoostEnvWrapper(
                initialize_env(task_cfg.env()),
                seed_dataset_url=task_cfg.seed_dataset,
                prior_dataset_url=cfg.prior_dataset_dir,
                test_dataset_url=task_cfg.test_dataset if "test_dataset" in task_cfg else None,
                render_func=render,
                postproc_func=self.postproc_func
            )
        return env

    def evaluate_success(self,
                         env: gym.Env,
                         ob: np.ndarray,
                         rew: float,
                         done: bool,
                         info: Dict) -> bool:
        '''evaluates whether the given environment step constitutes a success
        in terms of the task at hand. This is used in the benchmark's policy
        evaluator.

        Args:
            env [gym.Env]: gym environment
            ob [np.ndarray]: an observation of the environment this step
            rew [float]: reward received for this env step
            done [bool]: whether the trajectory has reached an end
            info [Dict]: metadata of the environment step
        Returns:
            success [bool]: success flag
        '''
        return info["success"]


__all__ = [DataBoostBenchmarkMetaworld]
