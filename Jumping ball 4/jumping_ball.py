import pygame
import pygame.gfxdraw  # For anti-aliased rendering
import math
import random
import os
import subprocess
import shutil

pygame.init()

# Screen settings
WIDTH, HEIGHT = 540, 960  # Base resolution
HIGH_RES = (WIDTH * 2, HEIGHT * 2)  # Higher resolution for better rendering
LOW_RES = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(LOW_RES)
pygame.display.set_caption("Bouncing Ball Inside a Circle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Circle properties
circle_center = (HIGH_RES[0] // 2, HIGH_RES[1] // 2)
circle_radius = 500  # Increased for high-res rendering
circle_width = 20  # Thicker for visibility

# Ball properties
ball_radius = 50  # Increased for high-res rendering

# Generate a random position in the upper half of the circle
angle = random.uniform(math.pi, 2 * math.pi)  # Restrict to upper semicircle
radius_offset = random.uniform(0, circle_radius - ball_radius - circle_width)
ball_pos = pygame.Vector2(
    circle_center[0] + radius_offset * math.cos(angle),
    circle_center[1] + radius_offset * math.sin(angle)
)

# Generate a random initial direction
angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
speed = 8  # Higher initial speed for visibility
ball_vel = pygame.Vector2(speed * math.cos(angle), speed * math.sin(angle))

gravity = 0.15  # Acceleration due to gravity
damping = 0.98  # Energy loss on bounce

running = True
clock = pygame.time.Clock()

# Create a high-resolution surface
high_res_surface = pygame.Surface(HIGH_RES)

# Generate background with 0s and 1s
font = pygame.font.SysFont("Courier", 30, bold=True)  # Adjusted for better fit
background_matrix = []

for y in range(0, HIGH_RES[1], 35):  # Adjust spacing for full coverage
    row = []
    for x in range(0, HIGH_RES[0], 25):  # Adjust spacing for full coverage
        row.append(random.choice(["0", "1"]))
    background_matrix.append(row)

def draw_background(surface):
    for i, row in enumerate(background_matrix):
        for j, text in enumerate(row):
            x_pos, y_pos = j * 25, i * 35
            rendered_text = font.render(text, True, GREEN)
            surface.blit(rendered_text, (x_pos, y_pos))

# Create frames directory if it doesn't exist
if not os.path.exists("Jumping ball 4/frames"):
    os.makedirs("Jumping ball 4/frames")

frame_count = 0
frame_delay = 10  # Faster change rate for 0s and 1s
saved_frame_count = 0  # Track actual saved frames

# Add this before the game loop
last_collision_time = 0  # Track last collision frame
collision_cooldown = 10  # Frames to wait before shrinking again

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Apply gravity
    ball_vel.y += gravity

    # Update ball position
    ball_pos += ball_vel

    # Calculate distance from the center
    dx = ball_pos.x - circle_center[0]
    dy = ball_pos.y - circle_center[1]
    dist_to_center = math.sqrt(dx**2 + dy**2)

    inner_radius = circle_radius - circle_width  # Adjusted inner boundary

    if dist_to_center + ball_radius >= inner_radius:
        # Increase ball size
        ball_radius += 5  # Adjust growth rate

        # Prevent the ball from getting too large
        if ball_radius > circle_radius - circle_width:
            ball_radius = circle_radius - circle_width
                    
        # **Fix: Ensure the circle shrinks only once per collision event**
        if frame_count - last_collision_time > collision_cooldown:
            circle_radius -= 5 # Adjust shrink rate
            last_collision_time = frame_count  # Update collision time

        # Prevent the circle from getting too small
        if circle_radius < ball_radius + circle_width:
            circle_radius = ball_radius + circle_width
            
        # Compute normal vector at the point of collision
        normal_x = dx / dist_to_center
        normal_y = dy / dist_to_center

        # Reflect velocity vector
        dot_product = ball_vel.x * normal_x + ball_vel.y * normal_y
        ball_vel.x -= 2 * dot_product * normal_x
        ball_vel.y -= 2 * dot_product * normal_y

        # Apply damping to simulate energy loss
        ball_vel *= damping

        # Reposition ball **inside** the inner boundary
        overlap = (dist_to_center + ball_radius) - inner_radius
        ball_pos.x -= overlap * normal_x
        ball_pos.y -= overlap * normal_y

    # Drawing
    high_res_surface.fill(BLACK)
    draw_background(high_res_surface)  # Background covers everything
    
    # Draw the circle on top of the background
    pygame.draw.circle(high_res_surface, BLACK, circle_center, circle_radius)  # Solid black circle to mask background
    pygame.draw.circle(high_res_surface, BLUE, circle_center, circle_radius, circle_width)
    pygame.gfxdraw.aacircle(high_res_surface, int(ball_pos.x), int(ball_pos.y), ball_radius, WHITE)
    pygame.gfxdraw.filled_circle(high_res_surface, int(ball_pos.x), int(ball_pos.y), ball_radius, WHITE)

    # Scale down for smoother rendering
    scaled_surface = pygame.transform.smoothscale(high_res_surface, LOW_RES)
    screen.blit(scaled_surface, (0, 0))

    pygame.display.flip()
    clock.tick(120)  # Higher FPS for smoother motion


    frame_count += 1  # Increase frame count each loop
    
    # Save every 2nd frame, but ensure filenames are sequential
    if frame_count % 2 == 0:
        pygame.image.save(screen, f"Jumping ball 4/frames/frame_{saved_frame_count:04d}.png")
        saved_frame_count += 1  # Only increment after saving

    if frame_count % frame_delay == 0:
        for i in range(len(background_matrix)):
            for j in range(len(background_matrix[i])):
                if random.random() < 0.3:  # Randomized toggling
                    background_matrix[i][j] = "0" if background_matrix[i][j] == "1" else "1"

pygame.quit()

if os.path.exists("Jumping ball 4/output.mp4"):
    os.remove("Jumping ball 4/output.mp4")
subprocess.run([
    "ffmpeg", "-framerate", "60", "-i", "Jumping ball 4/frames/frame_%04d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "Jumping ball 4/output.mp4"
])

# Delete all frames in the "frames" folder
if os.path.exists("Jumping ball 4/frames"):
    shutil.rmtree("Jumping ball 4/frames")  # Delete entire folder

