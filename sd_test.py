from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")

pipe.to("cuda")

prompt = "a very muscular minion"

image = pipe(prompt).images[0]
image.save("minion.png")
