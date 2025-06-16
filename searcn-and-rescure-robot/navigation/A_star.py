import cozmo
from cozmo.util import degrees, Pose
import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0

def heuristic(node, goal):
    return abs(node.position[0] - goal[0]) + abs(node.position[1] - goal[1]) + abs(node.position[2] - goal[2])

def get_neighbors(current_node):
    # For simplicity, consider neighboring positions within a certain range
    x, y, z = current_node.position
    neighbors = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]
    return neighbors

def a_star(robot, start, goal):
    start_node = Node(start)
    goal_node = Node(goal)

    open_set = []
    closed_set = set()

    heapq.heappush(open_set, (0, start_node))

    while open_set:
        current_node = heapq.heappop(open_set)[1]

        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node.position)

        for neighbor_pos in get_neighbors(current_node):
            if neighbor_pos in closed_set:
                continue

            neighbor_node = Node(neighbor_pos, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor_node, goal_node.position)

            if (neighbor_node.g, neighbor_node.position) not in [(node.g, node.position) for _, node in open_set]:
                heapq.heappush(open_set, (neighbor_node.g + neighbor_node.h, neighbor_node))

    return None  # No path found


def main(robot: cozmo.robot.Robot):
    start_position = robot.pose.position
    goal_position = (0, 0, 0)

    path = a_star(robot, start_position, goal_position)

    if path:
        print("Path found:", path)

        # Instruct Cozmo to follow the path
        for position in path:
            destination_pose = Pose(position[0], position[1], position[2], angle_z=degrees(0))
            robot.go_to_pose(destination_pose).wait_for_completed()
            print("Moved to:", position)

        print("Reached the goal!")

    else:
        print("No path found.")


cozmo.run_program(main)








