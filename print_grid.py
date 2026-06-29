from PIL import Image
import numpy as np

img = Image.open("/Users/igorcerovsky/.gemini/antigravity-ide/brain/9fd776c4-a728-4953-8802-5b9982294113/media__1782321297101.png")
print("Mode:", img.mode)
if img.mode == 'RGBA':
    # create white background
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bg.paste(img, mask=img.split()[3])
    img = bg
img = img.resize((40, 40))
img = img.convert("L")
arr = np.array(img)
print("Min:", np.min(arr), "Max:", np.max(arr))
threshold = (int(np.min(arr)) + int(np.max(arr))) // 2
for row in arr:
    print("".join(["#" if x < threshold else " " for x in row]))
