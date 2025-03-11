import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg
from isaaclab.utils.assets import ISAACLAB_NUCLEUS_DIR

FAIVE_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path="/home/riccardo/CodingProjects/IsaacLabProjects/AugmentedLearning/source/AugmentedLearning/AugmentedLearning/descriptions/faive_hand_p0/faive_hand.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            # max penetration velocity permitted to be introduced by the solver
            max_depenetration_velocity=5.0
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True, solver_position_iteration_count=8, solver_velocity_iteration_count=0
        )
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "root2thumb_base": 0.0,
            "thumb_base2pp": 0.0,
            "thumb_pp2mp": 0.0,
            "root2index_pp": 0.0,
            "index_pp2mp": 0.0,
            "root2middle_pp": 0.0,
            "middle_pp2mp": 0.0,
            "root2ring_pp": 0.0,
            "ring_pp2mp": 0.0,
            "root2pinky_pp": 0.0,
            "pinky_pp2mp": 0.0,
        },
    ),

    actuators={
        "thumb": ImplicitActuatorCfg(
            joint_names_expr=["thumb_base2pp", "thumb_pp2mp"],
            effort_limit=87.0,
            velocity_limit=2.175,
            stiffness=80.0,
            damping=4.0,
        ),
        "index": ImplicitActuatorCfg(
            joint_names_expr=["root2index_pp", "index_pp2mp"],
            effort_limit=87.0,
            velocity_limit=2.175,
            stiffness=80.0,
            damping=4.0,
        ),
        "middle": ImplicitActuatorCfg(
            joint_names_expr=["root2middle_pp", "middle_pp2mp"],
            effort_limit=87.0,
            velocity_limit=2.175,
            stiffness=80.0,
            damping=4.0,
        ),
        "ring": ImplicitActuatorCfg(
            joint_names_expr=["root2ring_pp", "ring_pp2mp"],
            effort_limit=87.0,
            velocity_limit=2.175,
            stiffness=80.0,
            damping=4.0,
        ),
        "pinky": ImplicitActuatorCfg(
            joint_names_expr=["root2pinky_pp", "pinky_pp2mp"],
            effort_limit=87.0,
            velocity_limit=2.175,
            stiffness=80.0,
            damping=4.0,
        ),
    }
)