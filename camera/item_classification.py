import pygame
import subprocess
import os
from pygame.locals import *
from gpiozero import Button
from time import sleep
from encryption_utils import *
from client_endpoint_test import *
import time
import board
import adafruit_dht
import cv2
# import a utility function for loading Roboflow models
from inference import get_roboflow_model
# import supervision to visualize our results
import supervision as sv
# import cv2 to helo load our image
import cv2

import os

# Set an environment variable
os.environ['ROBOFLOW_API_KEY'] = 'rc3jBJ1qI0zzIcVU57Nx'

# Initialize Pygame
pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption("Camera Preview - Press Button to capture, Q to quit")




jacks_device = "http://52.52.9.39:5000"
prod_server_url = "http://52.8.39.250:5000"

# Set up font
font = pygame.font.Font(None, 36)

# Initialize Button
button = Button(23)

def display_message(message, position, color=(255, 255, 255), duration=0):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)
    pygame.display.update(text_rect)
    if duration > 0:
        pygame.time.wait(duration)

preview_command = ['libcamera-still', '--nopreview', '--timeout', '1', '--width', '800', '--height', '480', '-o']
capture_command = ['libcamera-still', '--nopreview', '--timeout', '1', '--width', '1920', '--height', '1080', '-o']

def update_frame(show_capture_message=False):
    image_path = '/tmp/preview.jpg'
    subprocess.run(preview_command + [image_path])
    if os.path.exists(image_path):
        frame = pygame.image.load(image_path).convert()
        frame = pygame.transform.rotate(frame, 90)  # Rotate the frame to be vertical

        # Calculate the scale factor to fill the screen height
        scale_factor = infoObject.current_h / frame.get_height()
        new_width = int(frame.get_width() * scale_factor)
        new_height = infoObject.current_h  # Fill the screen height

        frame = pygame.transform.scale(frame, (new_width, new_height))  # Scale the frame

        # Center the frame horizontally
        x_offset = (infoObject.current_w - new_width) // 2

        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(frame, (x_offset, 0))  # Blit the frame centered horizontally
        display_message("Press Button to capture, Q to quit", (infoObject.current_w // 2, infoObject.current_h - 50))

        if show_capture_message:
            display_message("IMAGE CAPTURED", (infoObject.current_w // 2, 50), (255, 20, 0), 1000)

        pygame.display.flip()  # Update the entire screen
        os.remove(image_path)

def capture_high_res_image(image_path):
    subprocess.run(capture_command + [image_path])
    if os.path.exists(image_path):
        high_res_frame = pygame.image.load(image_path).convert()
        high_res_frame = pygame.transform.rotate(high_res_frame, 90)  # Ensure vertical orientation
        pygame.image.save(high_res_frame, image_path)  # Save the rotated image
        print(f"Captured and rotated image saved as {image_path}")

running = True
image_counter = 1
try:
    while running:
        update_frame()  # Regular frame update
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    running = False

        if button.is_pressed:
            image_file = f'Image{image_counter}.jpg'
            capture_high_res_image(image_file)  # Capture image when button is pressed
            image_counter += 1
            update_frame(True)  # Show capture message
       
            #IMAGE CLASSIFICATION SECTION
            # define the image url to use for inference
            image = cv2.imread(image_file)

            # load a pre-trained yolov8n model
            model = get_roboflow_model(model_id="group_work/2")

            # run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
            results = model.infer(image)
            print(results)

            # load the results into the supervision Detections api
            detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
            best_guess="Unknown Item"
            if results[0].predictions:
                 print("PREDICTION MADE!!!")
                 best_guess = results[0].predictions[0].class_name
                 print(best_guess) 

            # Upload the newly captured image
            response = item_image_upload(jacks_device, str(XXXXXX), best_guess, image_file)
            print("Image uploaded successfully.")
            sleep(0.5)  # Debounce delay
finally:
    pygame.quit()
