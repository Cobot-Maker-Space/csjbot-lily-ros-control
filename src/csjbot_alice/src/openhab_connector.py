#!/usr/bin/env python3

from xmlrpc.client import Boolean
import rospy
from std_msgs.msg import String, Bool
from openhab import openHAB

class OpenHABConnector(object):

    def __init__(self):
        rospy.init_node('openhab_connector')
        rospy.Subscriber("/alice/openhab/state/", Bool, self.switch_state)

        self.pub_speech = rospy.Publisher("/speech/", String, queue_size=10, latch=False)
        
        self.openhab_base_url = rospy.get_param("/alice/openhab/base_url", None)
        self.openhab = openHAB(self.openhab_base_url)
        self.openhab_connection_active = False

        self.sensor_list = rospy.get_param("/alice/openhab/sensors/", None)
        self.initialise_sensor_states()
    
        self.listen()

    def initialise_sensor_states(self):
        if self.openhab_connection_active:
            for sensor in self.sensor_list:
                state = self.retrieve_openhab_item_state(sensor)
                if (state != None):
                    self.update_current_sensor_state(sensor, state)
                    
    def update_current_sensor_state(self, sensor, state):
        rospy.set_param("/alice/openhab/" + sensor + "/current/", state)
    
    def fetch_current_sensor_state(self, sensor):
        state = rospy.get_param("/alice/openhab/" + sensor + "/current/", None)
        return state

    def fetch_sensor_speech_state(self, sensor, state):
        param_topic = "/alice/openhab/sensors/" + sensor + "/speech-state-" + state
        speech = rospy.get_param(param_topic, None)
        return speech

    def listen(self):
        while not rospy.is_shutdown():
            if self.openhab_connection_active:
                for sensor in self.sensor_list:
                    current_state = self.fetch_current_sensor_state(sensor)
                    new_state = self.retrieve_openhab_item_state(sensor)
                    if (current_state != new_state):
                        self.update_current_sensor_state(sensor, new_state)
                        speech = self.fetch_sensor_speech_state(sensor, new_state)
                        if speech is not None:
                            self.pub_speech.publish(speech)
                    print(f"{sensor}, {current_state}, {new_state}")
            else:
                print("not active")
            rospy.sleep(0.5)    

    def switch_state(self, msg):
        self.openhab_connection_active = msg.data

    def retrieve_openhab_item_state(self, sensor_id):
        item = self.openhab.get_item(sensor_id)
        return item.state
        
if __name__ == '__main__':
    OpenHABConnector()
