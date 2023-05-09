# Copyright (c) 2018-2022, NVIDIA Corporation
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


def initialize_task(config, env, init_sim=True):
    from .config_utils.sim_config import SimConfig
    sim_config = SimConfig(config)

    from omniisaacgymenvs.tasks.allegro_hand import AllegroHandTask
    from omniisaacgymenvs.tasks.ant import AntLocomotionTask
    from omniisaacgymenvs.tasks.anymal import AnymalTask
    from omniisaacgymenvs.tasks.anymal_terrain import AnymalTerrainTask
    from omniisaacgymenvs.tasks.ball_balance import BallBalanceTask
    from omniisaacgymenvs.tasks.cartpole import CartpoleTask
    from omniisaacgymenvs.tasks.factory.factory_task_nut_bolt_pick import FactoryTaskNutBoltPick
    from omniisaacgymenvs.tasks.franka_cabinet import FrankaCabinetTask
    from omniisaacgymenvs.tasks.humanoid import HumanoidLocomotionTask
    from omniisaacgymenvs.tasks.ingenuity import IngenuityTask
    from omniisaacgymenvs.tasks.quadcopter import QuadcopterTask
    from omniisaacgymenvs.tasks.shadow_hand import ShadowHandTask
    from omniisaacgymenvs.tasks.crazyflie import CrazyflieTask
    from omniisaacgymenvs.tasks.floating_platform import FloatingPlatformTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy import MFP2DGoToXYTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy_v2 import MFP2DGoToXYVirtualTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy_dict_obs import MFP2DGoToXYDictTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy_dict_RP import MFP2DGoToXYDictRPTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy_dict_SR import MFP2DGoToXYDictSRTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy_dict_SR_v2 import MFP2DGoToXYVirtualDictSRTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy_dict_SR_plus_v2 import MFP2DGoToXYVirtualDictSRPlusTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy_dict_SR_plus_plus_v2 import MFP2DGoToXYVirtualDictSRPlusPlusTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_xy_crippled import MFP2DGoToXYCrippledTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_pose import MFP2DGoToPoseTask
    from omniisaacgymenvs.tasks.MFP2D_go_to_pose_crippled import MFP2DGoToPoseCrippledTask
    from omniisaacgymenvs.tasks.MFP2D_track_xy_vel import MFP2DTrackXYVelocityTask
    from omniisaacgymenvs.tasks.MFP2D_track_xyo_vel import MFP2DTrackXYOVelocityTask
    from omniisaacgymenvs.tasks.MFP2D_track_xy_vel_match_heading import MFP2DTrackXYVelocityMatchHeadingTask

    # Mappings from strings to environments
    task_map = {
        "AllegroHand": AllegroHandTask,
        "Ant": AntLocomotionTask,
        "Anymal": AnymalTask,
        "AnymalTerrain": AnymalTerrainTask,
        "BallBalance": BallBalanceTask,
        "Cartpole": CartpoleTask,
        "FactoryTaskNutBoltPick": FactoryTaskNutBoltPick,
        "FrankaCabinet": FrankaCabinetTask,
        "Humanoid": HumanoidLocomotionTask,
        "Ingenuity": IngenuityTask,
        "Quadcopter": QuadcopterTask,
        "Crazyflie": CrazyflieTask,
        "ShadowHand": ShadowHandTask,
        "ShadowHandOpenAI_FF": ShadowHandTask,
        "ShadowHandOpenAI_LSTM": ShadowHandTask,
        "FloatingPlatform": FloatingPlatformTask,
        "MFP2DGoToXY": MFP2DGoToXYTask,
        "MFP2DGoToXYVirtual": MFP2DGoToXYVirtualTask,
        "MFP2DGoToXYDict": MFP2DGoToXYDictTask,
        "MFP2DGoToXYDictRT": MFP2DGoToXYDictRPTask,
        "MFP2DGoToXYDictSR": MFP2DGoToXYDictSRTask,
        "MFP2DGoToXYVirtualDictSR": MFP2DGoToXYVirtualDictSRTask,
        "MFP2DGoToXYVirtualDictSRPlus": MFP2DGoToXYVirtualDictSRPlusTask,
        "MFP2DGoToXYVirtualDictSRPlusPlus": MFP2DGoToXYVirtualDictSRPlusPlusTask,
        "MFP2DGoToXYCrippled": MFP2DGoToXYCrippledTask,
        "MFP2DGoToPose": MFP2DGoToPoseTask,
        "MFP2DGoToPoseCrippled": MFP2DGoToPoseCrippledTask,
        "MFP2DTrackXYVelocity": MFP2DTrackXYVelocityTask,
        "MFP2DTrackXYOVelocity": MFP2DTrackXYOVelocityTask,
        "MFP2DTrackXYVelocityMatchHeading": MFP2DTrackXYVelocityMatchHeadingTask,
    }

    cfg = sim_config.config
    task = task_map[cfg["task_name"]](
        name=cfg["task_name"], sim_config=sim_config, env=env
    )

    env.set_task(task=task, sim_params=sim_config.get_physics_params(), backend="torch", init_sim=init_sim)
    return task