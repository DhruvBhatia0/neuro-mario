import pygame
import sys
import os
import time  # Import time for timestamps

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1000, 500  
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('White Screen')

# Load and resize sprite images
sprite_images = [
    pygame.transform.scale(
        pygame.image.load(os.path.join('./nm_sprite', f'neuro_mario_{i}.png')), 
        (100, 100)
    ) for i in range(3)
]

# Character settings
character_x, character_y = screen_width // 2, screen_height - 100
character_speed = 10
jump_height = 20  # Increased jump height
gravity = 1
is_jumping = False
jump_velocity = jump_height
current_sprite = 0
facing_right = True

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Create directory for frames if it doesn't exist
os.makedirs('collected_training_data/frames', exist_ok=True)

# Open log file
log_file = open('collected_training_data/log.txt', 'w')

# Frame counter
frame_count = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    current_time = time.time()  # Get current timestamp

    if keys[pygame.K_RIGHT]:
        character_x += character_speed
        if (character_x + 100) > screen_width:
            character_x = screen_width - 100
        facing_right = True
        current_sprite = (current_sprite + 1) % len(sprite_images)  # Faster animation
        log_file.write(f"{current_time}, {frame_count}, RIGHT\n")  # Log RIGHT input
    elif keys[pygame.K_LEFT]:
        character_x -= character_speed
        if (character_x) < 0:
            character_x = 0
        facing_right = False
        current_sprite = (current_sprite + 1) % len(sprite_images)  # Faster animation
        log_file.write(f"{current_time}, {frame_count}, LEFT\n")  # Log LEFT input
    else:
        current_sprite = 0  # Reset to frame zero when not moving

    if keys[pygame.K_UP] and not is_jumping:
        is_jumping = True
        jump_velocity = jump_height
        log_file.write(f"{current_time}, {frame_count}, JUMP\n")  # Log JUMP input

    if is_jumping:
        character_y -= jump_velocity
        jump_velocity -= gravity
        if character_y >= screen_height - 100:
            character_y = screen_height - 100
            is_jumping = False

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the character
    sprite = sprite_images[current_sprite]
    if not facing_right:
        sprite = pygame.transform.flip(sprite, True, False)
    screen.blit(sprite, (character_x, character_y))

    # Save the current frame
    frame_filename = f'collected_training_data/frames/frame_{frame_count}.png'
    pygame.image.save(screen, frame_filename)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 30 FPS for smoother animation
    clock.tick(30)

    # Increment frame count
    frame_count += 1

# Close log file
log_file.close()

# Quit Pygame
pygame.quit()
sys.exit()
