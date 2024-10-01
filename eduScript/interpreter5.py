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

# InterpreterWithSimulator Class to Handle Command Queue
class InterpreterWithSimulator(Interpreter):
    def __init__(self, ast, simulator):
        super().__init__(ast, simulator)
        self.command_queue = []
        self.populate_command_queue(ast)
        self.last_command_time = time.time()
        self.command_interval = 0.1  # Execute one command every 0.1 seconds for smoother simulation

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

# Simulator Class
class Simulator:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1200, 800  # Increased window size for a bigger route
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("EduScript Robot Simulation")
        self.clock = pygame.time.Clock()
        self.robot_pos = [100.0, 100.0]  # Starting at top-left corner
        self.robot_angle = 0  # Degrees, 0 pointing to the right
        self.robot_size = 20
        self.font = pygame.font.SysFont(None, 24)
        self.carried_objects = []  # List to store carried objects
        self.objects = [
            {'pos': [250.0, 300.0], 'picked': False},  # First object
            {'pos': [500.0, 300.0], 'picked': False},  # Second object
            {'pos': [750.0, 300.0], 'picked': False}   # Third object
        ]
        self.obstacles = [
            {'pos': [400.0, 300.0], 'radius': 50},
            {'pos': [700.0, 500.0], 'radius': 30}
        ]

    def move_forward(self, distance):
        target_x = self.robot_pos[0] + distance * math.cos(math.radians(self.robot_angle))
        target_y = self.robot_pos[1] + distance * math.sin(math.radians(self.robot_angle))

        # Boundary check
        if not (0 + self.robot_size <= target_x <= self.width - self.robot_size and
                0 + self.robot_size <= target_y <= self.height - self.robot_size):
            print("Robot cannot move outside the window boundaries.")
            return

        # Obstacle check
        if self.is_path_clear(self.robot_pos, [target_x, target_y]):
            self.robot_pos = [target_x, target_y]
            print(f"Robot moves forward {distance} units to {self.robot_pos}")
        else:
            print("Robot detected an obstacle! Movement halted.")

    def move_backward(self, distance):
        self.move_forward(-distance)

    def turn_right(self, angle):
        self.robot_angle += angle
        self.robot_angle %= 360  # Ensure angle stays within 0-359
        print(f"Robot turns right {angle} degrees to {self.robot_angle}°")

    def turn_left(self, angle):
        self.robot_angle -= angle
        self.robot_angle %= 360  # Ensure angle stays within 0-359
        print(f"Robot turns left {angle} degrees to {self.robot_angle}°")

    def pick_up_object(self):
        for obj in self.objects:
            if not obj['picked']:
                distance = self.calculate_distance(self.robot_pos, obj['pos'])
                print(f"Attempting to pick up object at {obj['pos']} (Distance: {distance:.2f})")
                if distance <= self.robot_size + 10:  # robot_size + object_radius
                    obj['picked'] = True
                    self.carried_objects.append(obj)
                    print(f"Robot picks up the object at {obj['pos']}. Total objects carried: {len(self.carried_objects)}")
                    return
        print("No objects within pickup range.")

    def drop_object(self):
        if self.carried_objects:
            obj = self.carried_objects.pop(0)
            obj['pos'] = list(self.robot_pos)  # Drop at current position
            print(f"Robot drops the object at {obj['pos']}. Objects left to carry: {len(self.carried_objects)}")
        else:
            print("Robot has no object to drop.")

    def detect_obstacle(self):
        # Check if any obstacle is within collision range ahead
        look_ahead_distance = 50  # Look ahead 50 units
        look_x = self.robot_pos[0] + math.cos(math.radians(self.robot_angle)) * look_ahead_distance
        look_y = self.robot_pos[1] + math.sin(math.radians(self.robot_angle)) * look_ahead_distance

        for obstacle in self.obstacles:
            distance = self.calculate_distance([look_x, look_y], obstacle['pos'])
            if distance <= obstacle['radius'] + self.robot_size:
                return True
        return False

    def measure_distance(self):
        # Measure distance to the nearest object
        min_distance = float('inf')
        for obj in self.objects:
            if not obj['picked']:
                distance = self.calculate_distance(self.robot_pos, obj['pos'])
                if distance < min_distance:
                    min_distance = distance
        return min_distance if min_distance != float('inf') else 0

    def calculate_distance(self, pos1, pos2):
        return math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])

    def is_path_clear(self, start, end):
        """
        Check if the path from start to end intersects any obstacle.
        """
        for obstacle in self.obstacles:
            if self.line_circle_intersection(start, end, obstacle['pos'], obstacle['radius'] + self.robot_size):
                return False
        return True

    def line_circle_intersection(self, p1, p2, center, radius):
        """
        Determine if the line segment from p1 to p2 intersects the circle centered at 'center' with 'radius'.
        """
        # Vector from p1 to p2
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        # Vector from p1 to center
        fx = p1[0] - center[0]
        fy = p1[1] - center[1]

        a = dx**2 + dy**2
        b = 2 * (fx * dx + fy * dy)
        c = fx**2 + fy**2 - radius**2

        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            # No intersection
            return False
        else:
            discriminant = math.sqrt(discriminant)
            t1 = (-b - discriminant) / (2 * a)
            t2 = (-b + discriminant) / (2 * a)

            if (0 <= t1 <= 1) or (0 <= t2 <= 1):
                # Intersection occurs within the segment
                return True

        return False

    def draw_robot(self):
        self.screen.fill((255, 255, 255))  # White background

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(obstacle['pos'][0]), int(obstacle['pos'][1])), obstacle['radius'])

        # Draw objects
        for obj in self.objects:
            if not obj['picked']:
                pygame.draw.circle(self.screen, (0, 255, 0), (int(obj['pos'][0]), int(obj['pos'][1])), 10)  # Green object

        # Draw robot as a circle
        pygame.draw.circle(self.screen, (0, 0, 255), (int(self.robot_pos[0]), int(self.robot_pos[1])), self.robot_size)

        # Draw direction indicator
        end_x = self.robot_pos[0] + self.robot_size * math.cos(math.radians(self.robot_angle))
        end_y = self.robot_pos[1] + self.robot_size * math.sin(math.radians(self.robot_angle))
        pygame.draw.line(self.screen, (255, 255, 0), self.robot_pos, (end_x, end_y), 2)  # Yellow line for direction

        # Display robot position
        position_text = f"Position: ({self.robot_pos[0]:.1f}, {self.robot_pos[1]:.1f})"
        text_surface = self.font.render(position_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 60))

        # Display number of carried objects
        carried_text = f"Objects Carried: {len(self.carried_objects)}"
        text_surface = self.font.render(carried_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 30))

        # Display number of remaining commands
        remaining_commands = len(interpreter.command_queue)
        commands_text = f"Remaining Commands: {remaining_commands}"
        text_surface = self.font.render(commands_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))

        pygame.display.flip()
       # print(f"Drawing robot at position {self.robot_pos}, carrying {len(self.carried_objects)} object(s)")

    def update_display(self):
        self.draw_robot()
        self.clock.tick(60)

# InterpreterWithSimulator Class to Handle Command Queue
class InterpreterWithSimulator(Interpreter):
    def __init__(self, ast, simulator):
        super().__init__(ast, simulator)
        self.command_queue = []
        self.populate_command_queue(ast)
        self.last_command_time = time.time()
        self.command_interval = 0.5  # Execute one command every 0.5 seconds for balanced speed

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
          
            moveForward(150);        
            turnRight(90);              
            if (detectObstacle()) {     
                turnLeft(45);           
                moveForward(50);        
            }
            moveForward(200);          
            pickUpObject();             
            
           
                   
            if (detectObstacle()) {     
                turnRight(45);         
                moveForward(50);        
            }
            moveForward(250);          
            pickUpObject();            
            
           
            turnRight(90);             
            if (detectObstacle()) {    
                turnLeft(45);          
                moveForward(50);        
            }
            moveForward(250);         
            pickUpObject();           
            
         
            turnLeft(90);              
            moveBackward(750);          
            
            dropObject();              
            dropObject();              
            dropObject();           
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
