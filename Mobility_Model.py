import math
import random

class MobilityModel:
    def __init__(self, topology, mobile_node, env, speed_range, boundary, type ,pause_time_range =(1,2), time_step=0.1):
        self.topology = topology
        self.mobile_node = mobile_node
        self.env = env
        self.speed_range = speed_range
        self.boundary = boundary
        self.pause_time_range = pause_time_range
        self.time_step = time_step  # Time step for continuous movement
        self.type = type

        # Start the mobility process
        if type ==1 :
            self.action = env.process(self.random_walk())
        if type == 2:
            self.action = env.process(self.random_waypoint())
        if type == 3:
            self.action = env.process(self.random_direction())

    def get_random_speed(self):
        return random.uniform(*self.speed_range)

    def get_random_pause_time(self):
        return random.uniform(*self.pause_time_range)

    def random_waypoint(self):
        direction = 0  # Initial direction, move in the x-axis direction (horizontal)
        while True:
            # Get a random speed
            speed = self.get_random_speed()

            # Calculate the new position based on the direction
            new_x = self.mobile_node.x + speed * self.time_step * math.cos(direction)
            new_y = self.mobile_node.y + speed * self.time_step * math.sin(direction)

            # Ensure the node stays within the boundary
            new_x = max(min(new_x, self.boundary), 0)
            new_y = max(min(new_y, self.boundary), 0)

            # Move the mobile node to the new position
            self.topology.move_mobile_node(self.mobile_node, new_x, new_y)
            yield self.env.timeout(self.time_step)

            # Check if the mobile node reaches the boundaries in the x or y directions
            if new_x >= self.boundary or new_x <= 0 or new_y >= self.boundary or new_y <= 0:
                direction = random.uniform(0, 2 * math.pi)  # Random angle in radians
                pause_time = self.get_random_pause_time()
                yield self.env.timeout(pause_time)

    def  random_walk(self):
        while True:
            # Get a random speed
            speed = self.get_random_speed()

            # Get a random direction
            direction = random.uniform(0, 2 * math.pi)

            # Calculate the new position based on the direction
            new_x = self.mobile_node.x + speed * self.time_step * math.cos(direction)
            new_y = self.mobile_node.y + speed * self.time_step * math.sin(direction)

            # Ensure the node stays within the boundary
            new_x = max(min(new_x, self.boundary), 0)
            new_y = max(min(new_y, self.boundary), 0)

            # Move the mobile node to the new position
            self.topology.move_mobile_node(self.mobile_node, new_x, new_y)
            yield self.env.timeout(self.time_step)

            # Check if the mobile node reaches the boundaries in the x or y directions
            if new_x >= self.boundary or new_x <= 0 or new_y >= self.boundary or new_y <= 0:
                pause_time = self.get_random_pause_time()
                yield self.env.timeout(pause_time)
    def random_direction(self):
        while True:
            # Get a random speed
            speed = self.get_random_speed()

            # Randomly choose a new direction
            direction = random.uniform(0, 2 * math.pi)

            # Calculate the new position based on the direction
            new_x = self.mobile_node.x + speed * self.time_step * math.cos(direction)
            new_y = self.mobile_node.y + speed * self.time_step * math.sin(direction)

            # Ensure the node stays within the boundary
            new_x = max(min(new_x, self.boundary), 0)
            new_y = max(min(new_y, self.boundary), 0)

            # Move the mobile node to the new position
            self.topology.move_mobile_node(self.mobile_node, new_x, new_y)
            yield self.env.timeout(self.time_step)

            # Check if the mobile node reaches the boundaries in the x or y directions
            if new_x >= self.boundary or new_x <= 0 or new_y >= self.boundary or new_y <= 0:
                direction = random.uniform(0, 2 * math.pi)  # Random angle in radians
                pause_time = self.get_random_pause_time()
                yield self.env.timeout(pause_time)