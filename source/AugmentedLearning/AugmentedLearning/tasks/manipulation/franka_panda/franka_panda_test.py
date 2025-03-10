import argparse
from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Run a task.")
parser.add_argument("--num_envs", type=int, help="Number of environments to run.", default=1)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import torch
import isaaclab.sim as sim_utils
from AugmentedLearning.tasks.manipulation.franka_panda.franka_panda_env import FrankaPandaEnvCfg
from isaaclab.sim import SimulationContext
from isaaclab.scene import InteractiveScene


def run_simulator(sim: SimulationContext, scene: InteractiveScene):
    robot = scene["franka_panda"]
    sim_dt = sim.get_physics_dt()
    count = 0

    while simulation_app.is_running():
        if count % 500 == 0:
            count = 0

            joint_pos, joint_vel = robot.data.default_joint_pos.clone(), robot.data.default_joint_vel.clone()
            joint_pos += torch.randn_like(joint_pos) * 0.1
            robot.write_joint_state_to_sim(joint_pos, joint_vel)
            scene.reset()
            print("Resetting robot state!")
        
        efforts = torch.randn_like(robot.data.joint_pos) * 2.0
        robot.set_joint_effort_target(efforts)
        scene.write_data_to_sim()
        sim.step()
        count += 1
        scene.update(sim_dt)


def main():
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = SimulationContext(sim_cfg)

    sim.set_camera_view((2.5, 0.0, 4.0), (0.0, 0.0, 2.0))
    scene_cfg = FrankaPandaEnvCfg(num_envs=args_cli.num_envs, env_spacing=2.0)
    scene = InteractiveScene(scene_cfg)
    sim.reset()

    run_simulator(sim, scene)


if __name__ == "__main__":
    main()
    simulation_app.close()