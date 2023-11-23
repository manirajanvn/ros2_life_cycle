import rclpy
from rclpy.lifecycle import State, TransitionCallbackReturn, Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self, node_name,**kwargs) -> None:
        super().__init__(node_name,**kwargs)
        self.i = 0
        self.timer_period = 0.5  # seconds

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{state.label}'. Transitioning to 'configure'")
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{state.label}'. Transitioning to 'activate'")
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.subscription = self.create_subscription(String, 'topic', self.listener_callback, 10)
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{state.label}'. Transitioning to 'deactivate'")
        self.timer.destroy()
        self.destroy_publisher(self.publisher_)
        self.destroy_subscription(self.subscription)
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{state.label}'. Transitioning to 'shutdown'")
        return TransitionCallbackReturn.SUCCESS

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

    
def main(args=None) -> None:
    rclpy.init(args=args)
    lifecycle_node = MinimalPublisher("lifecycle_node")
    rclpy.spin(lifecycle_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
