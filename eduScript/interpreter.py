# interpreter.py

import pygame
import sys
import time
from parser import build_parser, Program, FunctionDef, Command, IfStatement, RepeatLoop, FunctionCall, ReturnStatement, BinaryOp, UnaryOp, Number, Identifier
import textwrap
import math

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Undefined variable '{name}'")

    def set(self, name, value):
        self.vars[name] = value

class Interpreter:
    def __init__(self, ast, simulator):
        self.ast = ast
        self.functions = {}
        self.global_env = Environment()
        self.current_env = self.global_env
        self.simulator = simulator  # Reference to the Simulator
        self.built_in_functions = {
            'detectObstacle': self.built_in_detect_obstacle,
            'measureDistance': self.built_in_measure_distance
            # Add more built-in functions here if needed
        }

    def interpret(self):
        # Register all user-defined functions
        for func in self.ast.functions:
            self.functions[func.name] = func

        # Look for 'main' function
        if 'main' not in self.functions:
            raise Exception("No 'main' function defined.")

        # Execute 'main'
        self.execute_function('main', [])

    def execute_function(self, name, args):
        if name in self.built_in_functions:
            return self.built_in_functions[name](args)
        elif name in self.functions:
            func = self.functions[name]
            env = Environment(parent=self.global_env)
            # Currently, EduScript functions have no parameters
            # Push new environment
            previous_env = self.current_env
            self.current_env = env
            try:
                self.execute_statements(func.body)
            except ReturnException as ret:
                self.current_env = previous_env
                return ret.value
            self.current_env = previous_env
        else:
            raise Exception(f"Undefined function '{name}'")

    def execute_statements(self, statements):
        for stmt in statements:
            self.execute_statement(stmt)

    def execute_statement(self, stmt):
        if isinstance(stmt, Command):
            self.execute_command(stmt)
        elif isinstance(stmt, IfStatement):
            condition = self.evaluate_expression(stmt.condition)
            if condition:
                self.execute_statements(stmt.if_body)
            elif stmt.else_body is not None:
                self.execute_statements(stmt.else_body)
        elif isinstance(stmt, RepeatLoop):
            times = self.evaluate_expression(stmt.times)
            for _ in range(int(times)):
                self.execute_statements(stmt.body)
        elif isinstance(stmt, FunctionCall):
            self.execute_function(stmt.name, stmt.args)
        elif isinstance(stmt, ReturnStatement):
            value = self.evaluate_expression(stmt.expression)
            raise ReturnException(value)
        else:
            raise Exception(f"Unknown statement type: {type(stmt)}")

    def execute_command(self, cmd):
        command = cmd.command
        args = [self.evaluate_expression(arg) for arg in cmd.args]
        # Implement the robotic commands
        if command == 'moveForward':
            distance = args[0]
            self.simulator.move_forward(distance)
        elif command == 'moveBackward':
            distance = args[0]
            self.simulator.move_backward(distance)
        elif command == 'turnRight':
            angle = args[0]
            self.simulator.turn_right(angle)
        elif command == 'turnLeft':
            angle = args[0]
            self.simulator.turn_left(angle)
        elif command == 'pickUpObject':
            self.simulator.pick_up_object()
        elif command == 'dropObject':
            self.simulator.drop_object()
        else:
            raise Exception(f"Unknown command '{command}'")

    def evaluate_expression(self, expr):
        if isinstance(expr, Number):
            return expr.value
        elif isinstance(expr, Identifier):
            return self.current_env.get(expr.name)
        elif isinstance(expr, BinaryOp):
            left = self.evaluate_expression(expr.left)
            right = self.evaluate_expression(expr.right)
            return self.apply_binary_op(expr.op, left, right)
        elif isinstance(expr, UnaryOp):
            operand = self.evaluate_expression(expr.operand)
            return self.apply_unary_op(expr.op, operand)
        elif isinstance(expr, FunctionCall):
            return self.execute_function(expr.name, expr.args)
        else:
            raise Exception(f"Unknown expression type: {type(expr)}")

    def apply_binary_op(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        elif op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        elif op == '&&':
            return left and right
        elif op == '||':
            return left or right
        else:
            raise Exception(f"Unknown binary operator '{op}'")

    def apply_unary_op(self, op, operand):
        if op == '!':
            return not operand
        else:
            raise Exception(f"Unknown unary operator '{op}'")

    # Built-in function implementations
    def built_in_detect_obstacle(self, args):
        if len(args) != 0:
            raise Exception("detectObstacle() takes no arguments.")
        # Simulate obstacle detection
        obstacle_detected = self.simulator.detect_obstacle()
        print(f"detectObstacle() called, returning {obstacle_detected}")
        return obstacle_detected

    def built_in_measure_distance(self, args):
        if len(args) != 0:
            raise Exception("measureDistance() takes no arguments.")
        # Simulate distance measurement
        distance = self.simulator.measure_distance()
        print(f"measureDistance() called, returning {distance}")
        return distance

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# Simulator Class
class Simulator:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("EduScript Robot Simulation")
        self.clock = pygame.time.Clock()
        self.robot_pos = [400.0, 300.0]  # Starting at center
        self.robot_angle = 0  # Degrees, 0 pointing to the right
        self.robot_size = 20
        self.font = pygame.font.SysFont(None, 24)
        self.object_picked = False  # Example state
        self.object_pos = [505.0, 300.0]  # Position of the object within pickup range

    def move_forward(self, distance):
        rad = math.radians(self.robot_angle)
        delta_x = distance * math.cos(rad)
        delta_y = distance * math.sin(rad)
        self.robot_pos[0] += delta_x
        self.robot_pos[1] += delta_y
        print(f"Robot moves forward {distance} units to {self.robot_pos}")

    def move_backward(self, distance):
        self.move_forward(-distance)

    def turn_right(self, angle):
        self.robot_angle -= angle
        self.robot_angle %= 360  # Ensure angle stays within 0-359
        print(f"Robot turns right {angle} degrees to {self.robot_angle}")

    def turn_left(self, angle):
        self.robot_angle += angle
        self.robot_angle %= 360  # Ensure angle stays within 0-359
        print(f"Robot turns left {angle} degrees to {self.robot_angle}")

    def pick_up_object(self):
        if self.object_picked:
            print("Robot already has the object.")
            return
        distance = self.calculate_distance(self.robot_pos, self.object_pos)
        print(f"Distance to object: {distance:.2f} units.")
        if distance <= self.robot_size + 10:  # robot_size + object_radius
            self.object_picked = True
            print("Robot picks up the object.")
        else:
            print("Object is too far to pick up.")

    def drop_object(self):
        if self.object_picked:
            self.object_picked = False
            # Drop the object at the robot's current position
            self.object_pos = list(self.robot_pos)
            print("Robot drops the object.")
        else:
            print("Robot has no object to drop.")

    def detect_obstacle(self):
        # Simulate obstacle detection
        # For demonstration, we'll always return False
        obstacle_detected = False
        return obstacle_detected

    def measure_distance(self):
        # Simulate a distance measurement
        distance = self.calculate_distance(self.robot_pos, self.object_pos)
        return distance

    def calculate_distance(self, pos1, pos2):
        return math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])

    def draw_robot(self):
        self.screen.fill((255, 255, 255))  # White background

        # Draw object if not picked up
        if not self.object_picked:
            pygame.draw.circle(
                self.screen,
                (0, 255, 0),  # Green color
                (int(self.object_pos[0]), int(self.object_pos[1])),
                10  # Object radius
            )

        # Draw robot as a circle
        pygame.draw.circle(
            self.screen,
            (0, 0, 255),  # Blue color
            (int(self.robot_pos[0]), int(self.robot_pos[1])),
            self.robot_size
        )

        # Draw direction indicator
        end_x = self.robot_pos[0] + self.robot_size * math.cos(math.radians(self.robot_angle))
        end_y = self.robot_pos[1] + self.robot_size * math.sin(math.radians(self.robot_angle))
        pygame.draw.line(
            self.screen,
            (255, 0, 0),  # Red color
            self.robot_pos,
            (end_x, end_y),
            2  # Line thickness
        )

        # Display robot position
        position_text = f"Position: ({self.robot_pos[0]:.1f}, {self.robot_pos[1]:.1f})"
        text_surface = self.font.render(position_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 30))

        # Display object status
        status_text = f"Object Picked: {self.object_picked}"
        text_surface = self.font.render(status_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        #print(f"Drawing robot at position {self.robot_pos}")

    def update_display(self):
        self.draw_robot()
        self.clock.tick(60)

class InterpreterWithSimulator(Interpreter):
    def __init__(self, ast, simulator):
        super().__init__(ast, simulator)
        self.command_queue = []
        self.populate_command_queue(ast)
        self.last_command_time = time.time()
        self.command_interval = 1  # Execute one command every second

    def populate_command_queue(self, ast):
        # Flatten all commands into a queue for sequential execution
        for func in ast.functions:
            if func.name == 'main':
                self.command_queue.extend(func.body)

    def execute_next_command(self):
        if self.command_queue:
            stmt = self.command_queue.pop(0)
            self.execute_statement(stmt)

    def update(self):
        current_time = time.time()
        if self.command_queue and (current_time - self.last_command_time) >= self.command_interval:
            try:
                self.execute_next_command()
                self.last_command_time = current_time
            except Exception as e:
                print(f"Error during interpretation: {e}")

# Main Execution
if __name__ == "__main__":
    parser = build_parser()
    data = textwrap.dedent('''\
        function main() {
            moveForward(100);
            if (detectObstacle()) {
                turnRight(90);
            } else {
                moveForward(5);
            }
            repeat(3) {
                pickUpObject();
                moveBackward(5);
            }
        }


        ''')
    ast = parser.parse(data)
    if ast:
        simulator = Simulator()
        interpreter = InterpreterWithSimulator(ast, simulator)
        # Start interpreting commands with delay
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Execute commands at controlled intervals
            interpreter.update()

            # Update and draw the robot
            simulator.update_display()

            # Control the loop speed
            # Already handled by simulator.clock.tick(60)
    else:
        print("Parsing failed.")
