#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import UInt16

def talker():
    k = 1 # set of integers k > 0
    n = 4 
    pub = rospy.Publisher('Ahrendt', UInt16, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(20) # 20hz
    while not rospy.is_shutdown():
        hello_int = k
        rospy.loginfo(hello_int)
        pub.publish(hello_int)
        rate.sleep()
        k += n

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass