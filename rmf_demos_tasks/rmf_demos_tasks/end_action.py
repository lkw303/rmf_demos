#!/usr/bin/env python3

# Copyright 2022 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import uuid
import argparse
import json

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rclpy.qos import qos_profile_system_default
from rclpy.qos import QoSProfile
from rclpy.qos import QoSHistoryPolicy as History
from rclpy.qos import QoSDurabilityPolicy as Durability
from rclpy.qos import QoSReliabilityPolicy as Reliability

from rmf_fleet_msgs.msg import ModeRequest, RobotMode


###############################################################################

class EndAction(Node):

    def __init__(self, argv=sys.argv):
        super().__init__('task_requester')
        parser = argparse.ArgumentParser()
        parser.add_argument('-F', '--fleet', required=True, default='',
                            type=str, help='Fleet name')
        parser.add_argument('-R', '--robot', required=True, default='',
                            type=str, help='Robot name')

        self.args = parser.parse_args(argv[1:])

        transient_qos = QoSProfile(
            history=History.KEEP_LAST,
            depth=1,
            reliability=Reliability.RELIABLE,
            durability=Durability.TRANSIENT_LOCAL)

        self.pub = self.create_publisher(
          ModeRequest, "/action_execution_notice", transient_qos)


        # Construct task
        mode_request = ModeRequest()
        mode_request.fleet_name = self.args.fleet
        mode_request.robot_name = self.args.robot
        mode_request.task_id =  "end_action"
        mode_request.mode.mode = RobotMode.MODE_IDLE
        self.pub.publish(mode_request)


###############################################################################


def main(argv=sys.argv):
    rclpy.init(args=sys.argv)
    args_without_ros = rclpy.utilities.remove_ros_args(sys.argv)

    end_action = EndAction(args_without_ros)
    rclpy.shutdown()


if __name__ == '__main__':
    main(sys.argv)
