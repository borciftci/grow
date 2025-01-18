import math
import random


class Tree:
    def __init__(self, canvas):
        self.canvas = canvas
        self.iterations = 0  # Number of recursive steps
        self.angle = 30  # Default angle for branches
        self.length = 100  # Base length of the main branch
        self.branch_data = {}  # Store randomness for each branch

    def set_iterations(self, iterations):
        """Set the number of iterations for the tree."""
        self.iterations = iterations

    def draw_tree(self, x, y, angle, length, depth, branch_id="0"):
        """
        Recursively draw the tree.

        :param branch_id: Unique ID for the branch in the tree structure.
        :param x: Starting x-coordinate.
        :param y: Starting y-coordinate.
        :param angle: Current angle of the branch.
        :param length: Current length of the branch.
        :param depth: Remaining depth of recursion.
        :return:
        """
        if depth <= 0 or length <= 0:
            return

        # Create a unique ID for this branch
        current_branch_id = f"{branch_id}-{depth}"

        # Retrieve or initialize randomness for this branch
        if current_branch_id not in self.branch_data:
            self.branch_data[current_branch_id] = {
                "angle_variation": random.uniform(-10, 10),  # Random angle variation
                "length_multiplier": random.uniform(0.8, 1.2)  # Random length multiplier
            }

        random_angle_variation = self.branch_data[current_branch_id]["angle_variation"]
        random_length_variation = self.branch_data[current_branch_id]["length_multiplier"]

        # Adjust angle and length with randomness
        angle += random_angle_variation
        length *= random_length_variation

        # Calculate end point of the branch
        x_end = x + length * math.cos(math.radians(angle))
        y_end = y - length * math.sin(math.radians(angle))  # Subtract for upward growth

        # Ensure branches stay within canvas bounds
        if y_end > int(self.canvas.cget("height")):
            return

        # Draw the branch on the canvas
        self.canvas.create_line(x, y, x_end, y_end, fill="green", width=4)

        length_shortener_multiplier = 0.7

        # Recursively draw the left and right branches
        self.draw_tree(
            x_end,
            y_end,
            angle - self.angle,
            length * length_shortener_multiplier,
            depth - 1
        )
        self.draw_tree(
            x_end,
            y_end,
            angle + self.angle,
            length * length_shortener_multiplier,
            depth - 1
        )

    def generate_and_draw(self):
        """Generate and draw the tree based on the current iterations."""
        self.canvas.delete("all")  # Clear the canvas
        # Draw the tree starting from the base center of the canvas
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))
        self.draw_tree(
            x=canvas_width // 2,
            y=canvas_height,  # Start at the bottom of the canvas
            angle=90,  # Upward direction
            length=self.length,
            depth=self.iterations,
        )
