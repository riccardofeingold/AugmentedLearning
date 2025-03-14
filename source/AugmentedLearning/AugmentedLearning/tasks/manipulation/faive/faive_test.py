import argparse
from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Run a task.")
parser.add_argument("--num_envs", type=int, help="Number of environments to run.", default=1)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import torch
import math
import isaaclab.sim as sim_utils
from AugmentedLearning.tasks.manipulation.faive.faive_env import FaiveEnvCfg
from isaaclab.sim import SimulationContext
from isaaclab.scene import InteractiveScene

actuated_joints = [
    "root2thumb_base", "thumb_base2pp", "thumb_pp2mp",
    "root2index_pp", "index_pp2mp",
    "root2middle_pp", "middle_pp2mp",
    "root2ring_pp", "ring_pp2mp",
    "root2pinky_pp", "pinky_pp2mp"
]


def run_simulator(sim: SimulationContext, scene: InteractiveScene):
    robot = scene["faive"]
    # robot1 = scene["faive1"]
    sim_dt = sim.get_physics_dt()
    count = 0
    amplitude = 0.03
    frequency = 1
    joint_indices = torch.tensor([index for index, joint in enumerate(robot.data.joint_names) if joint in actuated_joints]).to(device=args_cli.device)
    target_pos = robot.data.default_joint_pos.clone()
    # target_pos1 = robot1.data.default_joint_pos.clone()
    while simulation_app.is_running():
        # if count % 500 == 0:
        #     count = 0

        #     joint_pos, joint_vel = robot.data.default_joint_pos.clone(), robot.data.default_joint_vel.clone()
        #     joint_pos += torch.randn_like(joint_pos) * 0.1
        #     robot.write_joint_state_to_sim(joint_pos, joint_vel)
        #     scene.reset()
        #     print("Resetting robot state!")

        time = count * sim_dt
        input = torch.tensor([2 * math.pi * frequency * time], device=args_cli.device)
        sinusoidal_position = amplitude * torch.sin(input)

        target_pos[2, joint_indices] += sinusoidal_position
        # target_pos1[:, joint_indices] += sinusoidal_position
        # target_pos += sinusoidal_position

        # robot.set_joint_position_target(target=target_pos[:, joint_indices], joint_ids=joint_indices)
        robot.write_joint_state_to_sim(target_pos, robot.data.default_joint_vel.clone())
        # robot1.write_joint_state_to_sim(target_pos1, robot1.data.default_joint_vel.clone())
        # efforts = torch.randn((joint_pos.shape[0], len(joint_indices))) * 2.0
        # efforts = efforts.to(device=args_cli.device)
        # robot.set_joint_effort_target(target=efforts, joint_ids=joint_indices)
        scene.write_data_to_sim()
        sim.step()
        count += 1
        scene.update(sim_dt)


def main():
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = SimulationContext(sim_cfg)

    sim.set_camera_view((2.5, 0.0, 4.0), (0.0, 0.0, 2.0))
    scene_cfg = FaiveEnvCfg(
        num_envs=args_cli.num_envs,
        env_spacing=2.0
    )
    scene = InteractiveScene(scene_cfg)
    sim.reset()

    run_simulator(sim, scene)


if __name__ == "__main__":
    main()
    simulation_app.close()