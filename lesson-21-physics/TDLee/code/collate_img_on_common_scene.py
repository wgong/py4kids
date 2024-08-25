"""
pip install opencv-python

"""

import cv2
import numpy as np

def collate_images(background_path, image_paths, output_dir, scale_factor=0.9):
  """
  Collates images with a background, preserving aspect ratio and using a fixed scale factor.

  Args:
    background_path: Path to the background image.
    image_paths: List of paths to images to be collated.
    output_dir: Output directory for the collated images.
    scale_factor: The scaling factor for the images (0.0 - 1.0).
  """

  background = cv2.imread(background_path)
  bg_height, bg_width, _ = background.shape

  for image_path in image_paths:
    image = cv2.imread(image_path)
    img_height, img_width, _ = image.shape

    # Determine the larger dimension and calculate new size based on scale factor
    if img_width > img_height:
      new_width = int(bg_width * scale_factor)
      new_height = int(img_height * (new_width / img_width))
    else:
      new_height = int(bg_height * scale_factor)
      new_width = int(img_width * (new_height / img_height))

    # Resize image
    resized_image = cv2.resize(image, (new_width, new_height))

    # Create a mask for the image
    mask = np.zeros_like(resized_image)
    mask[0:new_height, 0:new_width] = 255

    # Calculate position for placing the image on the background
    x = (bg_width - new_width) // 2
    y = (bg_height - new_height) // 2

    # Create a copy of the background image
    result = background.copy()

    # Put the resized image on the background
    result[y:y+new_height, x:x+new_width] = resized_image

    # Save the resulting image
    output_path = f"{output_dir}/{image_path.split('/')[-1]}"
    cv2.imwrite(output_path, result)

# Example usage
background_path = "background.jpg"
image_paths = ["image1.jpg", "image2.png", "image3.bmp"]
output_dir = "output"
scale_factor = 0.9

collate_images(background_path, image_paths, output_dir, scale_factor)
