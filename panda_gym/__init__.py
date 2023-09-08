import os

from gymnasium.envs.registration import register

with open(os.path.join(os.path.dirname(__file__), "version.txt"), "r") as file_handler:
    __version__ = file_handler.read().strip()

ENV_IDS = []

for task in ["Reach", "Slide", "Push", "PickAndPlace", "Stack", "Flip",\
            "ReachSafe", "PushSafe", "SlideSafe", "PickAndPlaceSafe",  "StackSafe"\
            "Stack3", "StackPyramid", "BuildL" ]:
    for reward_type in ["sparse", "dense"]:
        for control_type in ["ee", "joints"]:
            reward_suffix = "Dense" if reward_type == "dense" else ""
            control_suffix = "Joints" if control_type == "joints" else ""
            env_id = f"Panda{task}{control_suffix}{reward_suffix}-v3"

            register(
                id=env_id,
                entry_point=f"panda_gym.envs:Panda{task}Env",
                kwargs={"reward_type": reward_type, "control_type": control_type},
                max_episode_steps=100 if task == "Stack" else 50,
            )

            ENV_IDS.append(env_id)



        # register(
        #     id="PandaReachSafe{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaReachSafeEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )
      

        # register(
        #     id="PandaPush{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaPushEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )

        # register(
        #     id="PandaPushSafe{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaPushSafeEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )

        # register(
        #     id="PandaSlide{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaSlideEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )

        # register(
        #     id="PandaSlideSafe{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaSlideSafeEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )

        # register(
        #     id="PandaPickAndPlace{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaPickAndPlaceEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )

        # register(
        #     id="PandaPickAndPlaceSafe{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaPickAndPlaceSafeEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )

        # register(
        #     id="PandaPickAndPlacePlatform{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaPickAndPlacePlatformEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )
        

        # register(
        #     id="PandaStack{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaStackEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=100,
        # )
          
        # register(
        #     id="PandaStackSafe{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaStackSafeEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=100,
        # )


        # register(
        #     id="PandaStack3{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaStack3Env",
        #     kwargs=kwargs,
        #     max_episode_steps=100,
        # )
        # register(
        #     id="PandaStackPyramid{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaStackPyramidEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=100,
        # )

        # register(
        #     id="PandaBuildL{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaBuildLEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=100,
        # )

        
        # register(
        #     id="PandaFlip{}{}-v2".format(control_suffix, reward_suffix),
        #     entry_point="panda_gym.envs:PandaFlipEnv",
        #     kwargs=kwargs,
        #     max_episode_steps=50,
        # )
