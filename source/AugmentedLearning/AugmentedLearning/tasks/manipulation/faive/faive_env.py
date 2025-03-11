from __future__ import annotations

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg, AssetBaseCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.utils import configclass
from AugmentedLearning.assets.robots.faive import FAIVE_CFG

@configclass
class FaiveEnvCfg(InteractiveSceneCfg):
    # adding grround plane
    ground = AssetBaseCfg(
        prim_path="/World/groundPlane",
        spawn=sim_utils.GroundPlaneCfg()
    )

    # lights
    dome_light = AssetBaseCfg(
        prim_path="/World/Light",
        spawn=sim_utils.DomeLightCfg(intensity=3000.0, color=(0.75, 0.75, 0.75))
    )

    faive: ArticulationCfg = FAIVE_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
