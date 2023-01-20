import rclpy
from rclpy.node import Node
import math

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import random

class TurtleControl(Node):

	def __init__(self):
		super().__init__("TurtleController")

		self.positions=[{5,8},{2,9},{4,9},{2,9},{2,3}]
		self.positionCounter=0

		self.counter=0
		self.pose=None

		self.declare_parameter("dest_x",0.0)
		self.declare_parameter("dest_y",0.0)
		
		self.destino_x=self.get_parameter("dest_x").get_parameter_value().double_value
		self.destino_y=self.get_parameter("dest_y").get_parameter_value().double_value



		self.get_logger().info("Oieee")
		self.publisher_=self.create_publisher(Twist,"turtle1/cmd_vel",1)
		self.subscriber=self.create_subscription(Pose,"turtle1/pose",self.turtlePose,1)
		self.create_timer(0.1,self.control_sign)
		self.valor=1

	def publish_news(self):
		msg=Twist()
		msg.angular.x=0.0
		msg.angular.y=0.0
		msg.angular.z=0.0
		msg.linear.x=1.5*self.valor
		msg.linear.y=0.0
		msg.linear.z=0.0
		print(self.pose)
		
		if self.pose!=None:
			if self.pose.x>8:
				self.valor=-1
			elif self.pose.x<2:
				self.valor=1
		self.publisher_.publish(msg)
    
	def control_sign(self):

		if self.pose == None:
			return
		try:
			self.destino_x,self.destino_y=self.positions[self.positionCounter]
			dist_x=self.destino_x - self.pose.x
			dist_y=self.destino_y - self.pose.y

			distance=math.sqrt(math.pow(dist_x,2) + math.pow(dist_y,2))
			angle_dist= math.atan2(dist_y,dist_x)

			orientation= angle_dist -self.pose.theta
			if orientation>math.pi:
				orientation-=2*math.pi
			
			elif orientation<-math.pi:
				orientation+=2*math.pi
			
			msg=Twist()
			
			if distance>0.5:
				#msg.linear.x=0.2*distance
				msg.linear.x=0.4
				msg.angular.z=1*orientation

			
			elif self.positionCounter!=len(self.positions)-1:
				self.positionCounter+=1
				msg.linear.x=0.4
				msg.angular.z=0
			
			else:
				msg.linear.x=0
				msg.angular.z=0
			#print(msg)
			self.publisher_.publish(msg)
		except:
			return

	def turtlePose(self,msg):
		self.pose=msg
		print(self.pose)
		#self.get_logger().info(msg).

def main(args=None):
    rclpy.init(args=args)
    node=TurtleControl()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()