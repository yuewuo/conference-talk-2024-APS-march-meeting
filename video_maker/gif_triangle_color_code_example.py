import imageio

NAME = "triangle_color_code_example"
FRAME_RATE = 60
FRAME_PER_SEC = 1 / 0.15
DURATION = 2
SLOWER = 100.0

FOLDER = f"screenshots_{NAME}"
INTERVAL = int(FRAME_RATE / FRAME_PER_SEC)

images = []
for index in range(int(DURATION * FRAME_PER_SEC)):
    images.append(imageio.v2.imread(f"{FOLDER}/{index * INTERVAL}.png"))
imageio.mimsave(f'{NAME}.gif', images, duration=DURATION * SLOWER, loop=65535)
