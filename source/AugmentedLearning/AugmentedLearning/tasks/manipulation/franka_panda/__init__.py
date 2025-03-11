import gymnasium as gym

# Import submodules

# Register environments
# ONLY needed when using RL Environements and Mimic Environments
gym.register(
    id="Isaac-Franka-Panda-Direct-v0",
    entry_point=f"{__name__}.franka_panda_env:FrankaPandaEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.franka_panda_env:FrankaPandaEnvCfg",
        # "rl_games_cfg_entry_point": f"{agents.__name__}:rl_games_ppo_cfg.yaml",
        # "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:FrankaPandaPPORunnerCfg",
        # "skrl_cfg_entry_point": f"{agents.__name__}:skrl_ppo_cfg.yaml",
    },
)

