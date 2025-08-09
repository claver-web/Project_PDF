from PIL import Image
import os

def image_resize(pic_path, height, width):
    img = Image.open(pic_path)
    resized = img.resize((width, height), Image.LANCZOS)

    save_path = os.path.splitext(pic_path)[0] + "_resized.jpg"
    resized.save(save_path, format="JPEG")
    return save_path  # Return the path, not the Image object
