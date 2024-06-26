import torch
import pytorch3d.transforms
from omniisaacgymenvs.envs.USV.Utils import *

"""
Following Fossen's Equation, 
Fossen, T. I. (1991). Nonlinear modeling and control of Underwater Vehicles. Doctoral thesis, Department of Engineering Cybernetics, Norwegian Institute of Technology (NTH), June 1991.
"""


class HydrostaticsObject:
    def __init__(
        self,
        num_envs,
        device,
        water_density,
        gravity,
        metacentric_width,
        metacentric_length,
        average_hydrostatics_force_value,
        amplify_torque,
        offset_added_mass,
        scaling_added_mass,
        alpha,
        last_time,
    ):
        self._num_envs = num_envs
        self.device = device
        self.drag = torch.zeros(
            (self._num_envs, 6), dtype=torch.float32, device=self.device
        )

        # Buoyancy
        self.water_density = water_density
        self.gravity = gravity
        self.metacentric_width = metacentric_width
        self.metacentric_length = metacentric_length
        self.archimedes_force_global = torch.zeros(
            (self._num_envs, 3), dtype=torch.float32, device=self.device
        )
        self.archimedes_torque_global = torch.zeros(
            (self._num_envs, 3), dtype=torch.float32, device=self.device
        )
        self.archimedes_force_local = torch.zeros(
            (self._num_envs, 3), dtype=torch.float32, device=self.device
        )
        self.archimedes_torque_local = torch.zeros(
            (self._num_envs, 3), dtype=torch.float32, device=self.device
        )

        # data
        self.average_hydrostatics_force_value = average_hydrostatics_force_value
        self.amplify_torque = amplify_torque

        # acceleration
        self.alpha = alpha
        self._filtered_acc = torch.zeros([6], device=self.device)
        self._last_time = last_time
        self._last_vel_rel = torch.zeros([6], device=self.device)

        return

    def compute_archimedes_metacentric_global(self, submerged_volume, rpy):
        roll, pitch = rpy[:, 0], rpy[:, 1]  # roll and pich are given in global frame

        # compute buoyancy force
        self.archimedes_force_global[:, 2] = (
            -self.water_density * self.gravity * submerged_volume
        )

        # torques expressed in global frame, size is (num_envs,3)
        self.archimedes_torque_global[:, 0] = (
            -1
            * self.metacentric_width
            * (torch.sin(roll) * self.archimedes_force_global[:, 2])
        )
        self.archimedes_torque_global[:, 1] = (
            -1
            * self.metacentric_length
            * (torch.sin(pitch) * self.archimedes_force_global[:, 2])
        )

        self.archimedes_torque_global[:, 0] = (
            -1
            * self.metacentric_width
            * (torch.sin(roll) * self.average_hydrostatics_force_value)
        )  # cannot multiply by the hydrostatics force in isaac sim because of the simulation rate (low then high value)
        self.archimedes_torque_global[:, 1] = (
            -1
            * self.metacentric_length
            * (torch.sin(pitch) * self.average_hydrostatics_force_value)
        )

        # debugging
        # print("self.archimedes_force global: ", self.archimedes_force_global[0,:])
        # print("self.archimedes_torque global: ", self.archimedes_torque_global[0,:])

        return self.archimedes_force_global, self.archimedes_torque_global

    def compute_archimedes_metacentric_local(self, submerged_volume, rpy, quaternions):
        # get archimedes global force
        self.compute_archimedes_metacentric_global(submerged_volume, rpy)

        # get rotation matrix from quaternions in world frame, size is (3*num_envs, 3)
        R = getWorldToLocalRotationMatrix(quaternions)

        # print("R:", R[0,:,:])

        # Arobot = Rworld * Aworld. Resulting matrix should be size (3*num_envs, 3) * (num_envs,3) =(num_envs,3)
        self.archimedes_force_local = torch.bmm(
            R.mT, torch.unsqueeze(self.archimedes_force_global, 1).mT
        )  # add batch dimension to tensor and transpose it
        self.archimedes_force_local = self.archimedes_force_local.mT.squeeze(
            1
        )  # remove batch dimension to tensor

        self.archimedes_torque_local = torch.bmm(
            R.mT, torch.unsqueeze(self.archimedes_torque_global, 1).mT
        )
        self.archimedes_torque_local = self.archimedes_torque_local.mT.squeeze(1)

        # not sure if torque have to be multiply by the rotation matrix also.
        self.archimedes_torque_local = self.archimedes_torque_global

        return torch.hstack(
            [
                self.archimedes_force_local,
                self.archimedes_torque_local * self.amplify_torque,
            ]
        )
