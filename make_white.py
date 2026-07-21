from PIL import Image

# Open the image (which has a black icon on a transparent background)
img = Image.open('seed.png').convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    # item is (R, G, B, A)
    # If the pixel is not completely transparent, change its color to white
    if item[3] > 0:
        # keep the alpha, but make RGB white
        newData.append((255, 255, 255, item[3]))
    else:
        newData.append(item)

img.putdata(newData)
img.save('seed_white.png', "PNG")
print("Successfully created white seed icon.")
