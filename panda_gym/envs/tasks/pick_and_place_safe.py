from typing import Any, Dict, Union

import numpy as np

from panda_gym.envs.core_safe import Task
from panda_gym.pybullet import PyBullet
from panda_gym.utils import distance


class PickAndPlaceSafe(Task):
    def __init__(
        self,
        sim: PyBullet,
        get_ee_position,
        reward_type: str = "dense",
        distance_threshold: float = 0.05,
        goal_xy_range: float = 0.3,
        goal_z_range: float = 0.2,
        obj_xy_range: float = 0.3,
    ) -> None:
        super().__init__(sim)
        self.reward_type = reward_type
        self.distance_threshold = distance_threshold
        self.object_size = 0.04
        self.get_ee_position = get_ee_position
        # unsafe parameters
        self.unsafe_region_radius = 0.1
        self.max_x_base_unsafe = 0.25 # max x pos to put unsafe space
        self.min_x_base_unsafe = -0.25
        self.max_y_base_unsafe_boundary = 0.25
        # unsafe parameters
        self.goal_range_low = np.array([-goal_xy_range / 2, -goal_xy_range / 2, 0])
        self.goal_range_high = np.array([goal_xy_range / 2, goal_xy_range / 2, goal_z_range])
        self.obj_range_low = np.array([-obj_xy_range / 2, -obj_xy_range / 2, 0])
        self.obj_range_high = np.array([obj_xy_range / 2, obj_xy_range / 2, 0])
        with self.sim.no_rendering():
            self._create_scene()
            self.sim.place_visualizer(target_position=np.zeros(3), distance=0.9, yaw=45, pitch=-30)

    def _create_scene(self) -> None:
        """Create the scene."""
        self.sim.create_plane(z_offset=-0.4)
        self.sim.create_table(length=1.1, width=0.7, height=0.4, x_offset=-0.3)
        self.sim.create_box(
            body_name="object",
            half_extents=np.ones(3) * self.object_size / 2,
            mass=1.0,
            position=np.array([0.0, 0.0, self.object_size / 2]),
            rgba_color=np.array([0.1, 0.9, 0.1, 1.0]),
        )
        self.sim.create_box(
            body_name="target",
            half_extents=np.ones(3) * self.object_size / 2,
            mass=0.0,
            ghost=True,
            position=np.array([0.0, 0.0, 0.05]),
            rgba_color=np.array([0.1, 0.9, 0.1, 0.3]),
        )


        self.sim.create_sphere(
            body_name = "unsafe_region",
            radius = self.unsafe_region_radius,
            mass = 0.0,
            ghost = True,
            position = np.array([0.0, 0.0, -self.object_size / 2]),
            rgba_color = np.array([0.9, 0.1, 0.1, 0.3]),
        )

    def get_obs(self) -> np.ndarray:
        # position, rotation of the object
        target_position = np.array(self.sim.get_base_position("target"))
        object_position = self.sim.get_base_position("object")
        object_rotation = self.sim.get_base_rotation("object")
        object_velocity = self.sim.get_base_velocity("object")
        object_angular_velocity = self.sim.get_base_angular_velocity("object")
        unsafe_space = self.sim.get_base_position("unsafe_region")
        end_effector_pos = self.get_end_effector_position().copy()
        observation = np.concatenate(
        [
            object_position, 
            object_rotation,
            object_velocity,
            object_angular_velocity,
            unsafe_space,
            np.array([self.unsafe_region_radius]), # unsafe region radius or size
                # add target position and possibly orientation
            target_position,
            end_effector_pos
        ])
        return observation

    def get_end_effector_position(self) -> np.ndarray:
        ee_position = np.array(self.get_ee_position())
        return ee_position

    def get_achieved_goal(self) -> np.ndarray:
        object_position = np.array(self.sim.get_base_position("object"))
        return object_position

    def _sample_unsafe_state_z_boundary(self):
        # height boundary constraint
        return np.random.uniform(0.28, - self.object_size / 2 )

    def _sample_unsafe_state_x_boundary(self):
        # x boundary constraint
        return np.random.uniform(self.max_x_base_unsafe,  self.min_x_base_unsafe )

    def _sample_unsafe_state_y_boundary(self):
        return np.random.uniform(self.max_y_base_unsafe_boundary, -self.max_y_base_unsafe_boundary )

    def _sample_unsafe_state(self):
        # sample boundary to right after base of robot    
        random_x_base = self._sample_unsafe_state_x_boundary()
        random_z_base = self._sample_unsafe_state_z_boundary()
        randome_y_base = self._sample_unsafe_state_y_boundary()
        return np.array([random_x_base, randome_y_base ,random_z_base ])

    def _target_in_unsafe_region(self):
        target_pos = self.goal
        # distance between object anf unsafe space
        distance_target_unsafe = distance(target_pos , self.unsafe_state_pos )
       
        # lowest distance possible is sphere radius plus max posssible value using size 
        # this is a mathematical apporximation
        min_distance_treshhold = self.unsafe_region_radius + (self.object_size / 2)
        return distance_target_unsafe < min_distance_treshhold

    def _object_in_unsafe_region(self):
        object_pos = self.get_achieved_goal()
        # distance between object anf unsafe space
        distance_obj_unsafe = distance(object_pos , self.unsafe_state_pos )
        
        # lowest distance possible is sphere radius plus max posssible value using size 
        # this is a mathematical apporximation
        min_distance_treshhold = self.unsafe_region_radius + (self.object_size / 2)
        return (distance_obj_unsafe < min_distance_treshhold)

    def _end_effector_in_unsafe_region(self):
        end_effector_pos = self.get_end_effector_position()
        # distacne between end effector and unsafe space center
        distance_end_effector_unsafe = distance(end_effector_pos , self.unsafe_state_pos )
       
        min_distance_treshhold = self.unsafe_region_radius
        return (distance_end_effector_unsafe < min_distance_treshhold)

    def reset(self) -> None:
        self.unsafe_state_pos = self._sample_unsafe_state()
        self.sim.set_base_pose("unsafe_region",
                            self.unsafe_state_pos,
                            np.array([0.0, 0.0, 0.0, 1.0]))

        self.goal = self._sample_goal()
        object_position = self._sample_object()
        self.sim.set_base_pose("object", object_position, np.array([0.0, 0.0, 0.0, 1.0]))
        
        while  self._target_in_unsafe_region():
            self.goal = self._sample_goal()
            self.sim.set_base_pose("target", self.goal, np.array([0.0, 0.0, 0.0, 1.0]))

        while self._object_in_unsafe_region():
            object_position = self._sample_object()
            self.sim.set_base_pose("object", object_position, np.array([0.0, 0.0, 0.0, 1.0]))

    def _sample_goal(self) -> np.ndarray:
        """Sample a goal."""
        goal = np.array([0.0, 0.0, self.object_size / 2])  # z offset for the cube center
        noise = self.np_random.uniform(self.goal_range_low, self.goal_range_high)
        if self.np_random.random() < 0.3:
            noise[2] = 0.0
        goal += noise
        return goal

    def _sample_object(self) -> np.ndarray:
        """Randomize start position of object."""
        object_position = np.array([0.0, 0.0, self.object_size / 2])
        noise = self.np_random.uniform(self.obj_range_low, self.obj_range_high)
        object_position += noise
        return object_position

    def _object_not_on_table(self):
        object_pos = self.get_achieved_goal()
        # distance between object anf unsafe space
        z_pos = object_pos[2]
        return z_pos < 0.0
    def _compute_cost_function(self):
        '''
        two possible contontitions to get a non 0 cost
        1 Object enters unsafe space 1  or 2
        2 end effector enters unsafe space 1 or 2
        '''
        if self._object_in_unsafe_region():
            return 1.0
        elif self._end_effector_in_unsafe_region():
            return 1.0
        elif self._object_not_on_table():
            return 2.0
        else:
            return 0.0

    def compute_cost(self) -> Union[np.ndarray, float]:
        
        unsafe_cost = self._compute_cost_function()
        
        return unsafe_cost
        
    def is_success(self, achieved_goal: np.ndarray, desired_goal: np.ndarray) -> Union[np.ndarray, float]:
        d = distance(achieved_goal, desired_goal)
        return np.array(d < self.distance_threshold, dtype=np.float64)
        
    def compute_reward(self, achieved_goal, desired_goal, info: Dict[str, Any]) -> Union[np.ndarray, float]:
        d = distance(achieved_goal, desired_goal)
        if self.reward_type == "sparse":
            return -np.array(d > self.distance_threshold, dtype=np.float64)
        else:
            if d <= self.distance_threshold:
                return 5.0  # Additional positive reward for success
            else:
                return -d

            # return -d
