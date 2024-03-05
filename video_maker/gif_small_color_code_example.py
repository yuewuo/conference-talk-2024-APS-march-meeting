import imageio

NAME = "small_color_code_example"
FRAME_RATE = 60
FRAME_PER_SEC = 6
DURATION = 30
SLOWER = 3.0

FOLDER = f"screenshots_{NAME}"
INTERVAL = FRAME_RATE // FRAME_PER_SEC

images = []
for index in range(DURATION * FRAME_PER_SEC):
    images.append(imageio.v2.imread(f"{FOLDER}/{index * INTERVAL}.png"))
imageio.mimsave(f'{NAME}.gif', images, duration=DURATION * SLOWER, loop=65535)
