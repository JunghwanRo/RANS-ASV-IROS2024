from omniisaacgymenvs.tasks.virtual_floating_platform.MFP2D_core import Core, parse_data_dict
from omniisaacgymenvs.tasks.virtual_floating_platform.MFP2D_task_rewards import TrackXYOVelocityReward
from omniisaacgymenvs.tasks.virtual_floating_platform.MFP2D_task_parameters import TrackXYOVelocityParameters

import math
import torch

EPS = 1e-6   # small constant to avoid divisions by 0 and log(0)

class TrackXYOVelocityTask(Core):
    """
    Implements the GoToPose task. The robot has to reach a target position and heading."""

    def __init__(self, task_param, reward_param, num_envs, device):
        super(TrackXYOVelocityTask, self).__init__(num_envs, device)
        # Task and reward parameters
        self._task_parameters = parse_data_dict(TrackXYOVelocityParameters(), task_param)
        self._reward_parameters = parse_data_dict(TrackXYOVelocityReward(), reward_param)

        # Buffers
        self._goal_reached = torch.zeros((self._num_envs), device=self._device, dtype=torch.int32)
        self._target_linear_velocities = torch.zeros((self._num_envs, 2), device=self._device, dtype=torch.float32)
        self._target_angular_velocities = torch.zeros((self._num_envs), device=self._device, dtype=torch.float32)
        self._task_label = self._task_label * 0 

    def create_stats(self, stats:dict) -> dict:
        """
        Creates a dictionary to store the training statistics for the task."""

        torch_zeros = lambda: torch.zeros(self._num_envs, dtype=torch.float, device=self._device, requires_grad=False)

        if not "linear_velocity_reward" in stats.keys():
            stats["linear_velocity_reward"] = torch_zeros()
        if not "linear_velocity_error" in stats.keys():
            stats["linear_velocity_error"] = torch_zeros()
        if not "angular_velocity_reward" in stats.keys():
            stats["angular_velocity_reward"] = torch_zeros()
        if not "angular_velocity_error" in stats.keys():
            stats["angular_velocity_error"] = torch_zeros()
        return stats

    def get_state_observations(self, current_state: dict) -> torch.Tensor:
        """
        Computes the observation tensor from the current state of the robot."""""

        self._linear_velocity_error = self._target_linear_velocities - current_state["linear_velocity"]
        self._angular_velocity_error = self._target_angular_velocities - current_state["angular_velocity"]
        self._position_error = current_state["position"]
        self._task_data[:,:2] = self._linear_velocity_error
        self._task_data[:,2] = self._angular_velocity_error
        return self.update_observation_tensor(current_state)

    def compute_reward(self, current_state: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        """
        Computes the reward for the current state of the robot."""

        # position error
        self.position_dist = torch.sqrt(torch.square(self._position_error).sum(-1))
        self.linear_velocity_dist = torch.sqrt(torch.square(self._linear_velocity_error).sum(-1))
        self.angular_velocity_dist = torch.sqrt(torch.square(self._angular_velocity_error).sum(-1))

        # Checks if the goal is reached
        lin_goal_is_reached = (self.linear_velocity_dist < self._task_parameters.lin_vel_tolerance).int()
        ang_goal_is_reached = (self.angular_velocity_dist < self._task_parameters.ang_vel_tolerance).int()
        goal_is_reached = lin_goal_is_reached * ang_goal_is_reached
        self._goal_reached *= goal_is_reached # if not set the value to 0
        self._goal_reached += goal_is_reached # if it is add 1

        # Rewards
        self.linear_velocity_reward, self.angular_velocity_reward = self._reward_parameters.compute_reward(current_state, actions, self.linear_velocity_dist, self.angular_velocity_dist)
    
        return self.linear_velocity_reward + self.angular_velocity_reward
    
    def update_kills(self) -> torch.Tensor:
        """
        Updates if the platforms should be killed or not."""

        die = torch.zeros_like(self._goal_reached, dtype=torch.long)
        ones = torch.ones_like(self._goal_reached, dtype=torch.long)
        die = torch.where(self.position_dist > self._task_parameters.kill_dist, ones, die)
        die = torch.where(self._goal_reached > self._task_parameters.kill_after_n_steps_in_tolerance, ones, die)
        return die
    
    def update_statistics(self, stats: dict) -> dict:
        """
        Updates the training statistics."""

        stats["linear_velocity_reward"] += self.linear_velocity_reward
        stats["linear_velocity_error"] += self.linear_velocity_dist
        stats["angular_velocity_reward"] += self.angular_velocity_reward
        stats["angular_velocity_error"] += self.angular_velocity_dist
        return stats

    def reset(self, env_ids: torch.Tensor) -> None:
        """
        Resets the goal_reached_flag when an agent manages to solve its task."""

        self._goal_reached[env_ids] = 0

    def get_goals(self, env_ids: torch.Tensor, target_positions: torch.Tensor, target_orientations: torch.Tensor) -> list:
        """
        Generates a random goal for the task."""

        num_goals = len(env_ids)
        self._target_linear_velocities[env_ids] = torch.rand((num_goals, 2), device=self._device)*self._task_parameters.goal_random_linear_velocity*2 - self._task_parameters.goal_random_linear_velocity
        self._target_angular_velocities[env_ids] = torch.rand((num_goals), device=self._device)*self._task_parameters.goal_random_angular_velocity*2 - self._task_parameters.goal_random_angular_velocity
        # This does not matter
        return target_positions, target_orientations
    
    def get_spawns(self, env_ids: torch.Tensor, initial_position: torch.Tensor, initial_orientation: torch.Tensor, step: int=0) -> list:
        """
        Generates spawning positions for the robots following a curriculum."""

        num_resets = len(env_ids)
        # Resets the counter of steps for which the goal was reached
        self._goal_reached[env_ids] = 0

        # Randomizes the heading of the platform
        random_orient = torch.rand(num_resets, device=self._device) * math.pi
        initial_orientation[env_ids, 0] = torch.cos(random_orient*0.5)
        initial_orientation[env_ids, 3] = torch.sin(random_orient*0.5)
        return initial_position, initial_orientation