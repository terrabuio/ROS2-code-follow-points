#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class Meu1No(Node):

    #instancia o objeto
    def __init__(self):
        super().__init__("py_1")
        self.counter=0
        self.get_logger().info("Operando")
        self.create_timer(0.5, self.timer_callback)

    
    def timer_callback(self):
        self.counter += 1
        self.get_logger().info("eu amo a giovanna à "+str(self.counter)+" dias")

def main (args=None):
    rclpy.init(args=args)
    node=Meu1No()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()