import torch
from diffusers import StableDiffusionPipeline
import time

model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"


pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

print("model loaded, timeing starting")
start_time = time.time()

prompt = "game of mario on the Nintendo DSi, jumping on an enemy goomba"
image = pipe(prompt).images[0]  
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
    
image.save("mario_dsi.png")