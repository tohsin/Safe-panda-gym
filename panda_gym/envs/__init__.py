from panda_gym.envs.panda_tasks import (
    PandaFlipEnv,
    PandaPickAndPlaceEnv,
    PandaPushEnv,
    PandaReachEnv,
    PandaSlideEnv,
    PandaStackEnv,

    #new environments
    PandaStack3Env,
    PandaStackPyramidEnv,
    PandaPickAndPlacePlatformEnv,

    #safe environments
    PandaPushSafeEnv,
    PandaReachSafeEnv,
    PandaSlideSafeEnv,
    PandaPickAndPlaceSafeEnv,
    PandaStackSafeEnv
)

# from panda_gym.envs.panda_tasks.panda_pick_and_place_platform import PandaPickAndPlacePlatformEnv
# from panda_gym.envs.panda_tasks.panda_stack_pyramid import PandaStackPyramidEnv
#from panda_gym.envs.panda_tasks.panda_stack_3 import PandaStack3Env
#from panda_gym.envs.panda_tasks.panda_stack_pyramid import PandaStackPyramidEnv
#from panda_gym.envs.panda_tasks.panda_build_L import  PandaBuildLEnv
from panda_gym.envs.panda_tasks.panda_push_safe import PandaPushSafeEnv
from panda_gym.envs.panda_tasks.panda_reach_safe import PandaReachSafeEnv
from panda_gym.envs.panda_tasks.panda_slide_safe import PandaSlideSafeEnv
from panda_gym.envs.panda_tasks.panda_pick_and_place_safe import PandaPickAndPlaceSafeEnv
from panda_gym.envs.panda_tasks.panda_stack_safe import PandaStackSafeEnv
