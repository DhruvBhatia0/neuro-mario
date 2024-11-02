import torch
from diffusers import StableDiffusionPipeline
import numpy as np
import cv2
from moviepy.editor import ImageSequenceClip

# Load Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

def generate_frame(prompt, seed=None):
    # Ensure seed is an integer
    if seed is not None:
        seed = int(seed)
    generator = torch.Generator(device=device).manual_seed(seed) if seed is not None else None
    image = pipe(prompt, generator=generator).images[0]
    return image

# Settings
prompt = "A beautiful landscape with the sun rising, frame number :"
num_frames = 60  # Number of frames in the video
fps = 12  # Frames per second
seeds = np.linspace(0, 1000, num_frames, dtype=int)  # Different seeds for each frame
frames = []

# Generate each frame
for i, seed in enumerate(seeds):
    print(f"Generating frame {i+1}/{num_frames} with seed {seed}")
    frame = generate_frame(prompt + str(i), seeds[0])
    frames.append(np.array(frame))

# Save frames as video
video_clip = ImageSequenceClip([cv2.cvtColor(f, cv2.COLOR_RGB2BGR) for f in frames], fps=fps)
video_clip.write_videofile("stable_diffusion_video.mp4", codec="libx264")
