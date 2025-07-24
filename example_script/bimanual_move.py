#!/usr/bin/env python3
import rospy

import actionlib
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal, JointTolerance

## from calibration pose to working pose
## joints of left arm first
walk_out_j = [[-0.0424, -2.2905, 2.3236, 0.5279, -0.0033, 0.6589, -0.0003, 0.0406, -2.2915, -2.3245, 0.5284, 0.0046, 0.6579, -0.0001],\
              [-0.1474, -2.3397, 2.2430, 0.5372, -0.0127, 0.5629, -0.0003, 0.1425, -2.3452, -2.2443, 0.5369, 0.0162, 0.5617, -0.0001],\
              [-0.2818, -2.3949, 2.1382, 0.5464, -0.0251, 0.4495, -0.0003, 0.2739, -2.4063, -2.1390, 0.5455, 0.0308, 0.4479, -0.0001],\
              [-0.4125, -2.4340, 2.0333, 0.5506, -0.0380, 0.3568, -0.0003, 0.4034, -2.4514, -2.0320, 0.5493, 0.0443, 0.3544, -0.0001],\
              [-0.5613, -2.4511, 1.9079, 0.5346, -0.0542, 0.2842, -0.0003, 0.5543, -2.4761, -1.9010, 0.5340, 0.0586, 0.2803, -0.0001],\
              [-0.7358, -2.4581, 1.7582, 0.4994, -0.0739, 0.2148, -0.0003, 0.7328, -2.4922, -1.7432, 0.5001, 0.0748, 0.2089, -0.0001],\
              [-0.8809, -2.4591, 1.6327, 0.4642, -0.0906, 0.1628, -0.0003, 0.8818, -2.5009, -1.6104, 0.4663, 0.0881, 0.1551, -0.0001],\
              [-0.9414, -2.4585, 1.5801, 0.4482, -0.0976, 0.1424, -0.0003, 0.9442, -2.5035, -1.5546, 0.4510, 0.0936, 0.1339, -0.0001],\
              [-1.5778, -2.4226, 0.6920, 0.4850, -0.0026, 0.2117, -0.0007, 1.5778, -2.4226, -0.6920, 0.4850, 0.0026, 0.2117, -0.0007]]

### Move the robot joints to the values given in terminal if run as a script

if __name__ == '__main__':
    rospy.init_node('joint_ctrl_test', anonymous=True)
    rospy.loginfo("Node initialized, waiting for action server...")

    client = actionlib.SimpleActionClient('/yumi/joint_traj_pos_controller_both/follow_joint_trajectory', FollowJointTrajectoryAction)

    joints_list = ['yumi_joint_1_l', 'yumi_joint_2_l', 'yumi_joint_7_l', 'yumi_joint_3_l', 'yumi_joint_4_l', 'yumi_joint_5_l', 'yumi_joint_6_l',
                    'yumi_joint_1_r', 'yumi_joint_2_r', 'yumi_joint_7_r', 'yumi_joint_3_r', 'yumi_joint_4_r', 'yumi_joint_5_r', 'yumi_joint_6_r']

    # Wait for the action servers to be available
    if not client.wait_for_server(rospy.Duration(5)):
        rospy.logerr("Action server not available!")
        exit(1)

    # go through set of goals
    for jointPos in walk_out_j:

        # set goal for joints
        goal =  FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = joints_list
        
        # Create a trajectory point with the desired joint values
        point = JointTrajectoryPoint()
        point.positions = jointPos
        point.time_from_start = rospy.Duration(1)
        
        # Add the point to the trajectory
        goal.trajectory.points.append(point)
        client.send_goal(goal)

        # Wait for the arms to finish movement
        client.wait_for_result()
        print("Result:", client.get_result())
            

        

