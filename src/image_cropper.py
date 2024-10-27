from PIL import Image
import os

def crop_image_to_aspect(image_path, target_aspect_width=3000, target_aspect_height=4000):
    # Open the image
    img = Image.open(image_path)
    original_width, original_height = img.size

    # Calculate aspect ratios
    target_aspect_ratio = target_aspect_width / target_aspect_height  # 3:4 aspect ratio (width / height)
    original_aspect_ratio = original_width / original_height  # Original aspect ratio (e.g., 4:3 for 2048x1536)

    print(f"\nOriginal image size: {original_width}x{original_height}")
    print(f"Target aspect ratio: {target_aspect_width}:{target_aspect_height} ({target_aspect_ratio:.2f})")

    # Crop horizontally or vertically to match the aspect ratio
    if original_aspect_ratio > target_aspect_ratio:
        # Original is wider (needs to crop width)
        new_width = int(original_height * target_aspect_ratio)
        new_height = original_height
        print(f"\nCropping horizontally: new dimensions: {new_width}x{new_height}")

        # Default cropping direction to center
        direction = input("\nChoose cropping side ( center | left | right ): ").strip().lower() or 'center'

        if direction == 'left':
            left = 0
            right = new_width
        elif direction == 'right':
            left = original_width - new_width
            right = original_width
        elif direction == 'center':
            left = (original_width - new_width) // 2
            right = left + new_width
        else:
            print("Invalid option!")

        # Perform the crop
        img_cropped = img.crop((left, 0, right, new_height))

    elif original_aspect_ratio < target_aspect_ratio:
        # Original is taller (needs to crop height)
        new_width = original_width
        new_height = int(original_width / target_aspect_ratio)
        print(f"\nCropping vertically: new dimensions: {new_width}x{new_height}")

        # Default cropping direction to center
        direction = input("\nChoose cropping side ( center | top | bottom ): ").strip().lower() or 'center'

        if direction == 'top':
            top = 0
            bottom = new_height
        elif direction == 'bottom':
            top = original_height - new_height
            bottom = original_height
        elif direction == 'center':
            top = (original_height - new_height) // 2
            bottom = top + new_height
        else:
            print("Invalid option!")

        # Perform the crop
        img_cropped = img.crop((0, top, new_width, bottom))

    else:
        # Aspect ratio already matches
        print("No cropping needed, aspect ratio already matches.\nConvertion will still work.")
        return img

    # Return cropped image without resizing to preserve resolution
    return img_cropped

def save_image_with_suffix(image, image_path, suffix="_cropped", output_format='webp'):
    # Extract the filename and extension
    directory, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)

    # Create a new filename with the suffix and change extension if saving as WebP
    if output_format.lower() == 'webp':
        new_filename = f"{name}{suffix}.webp"
    elif output_format.lower() == 'png':
        new_filename = f"{name}{suffix}.png"
    elif output_format.lower() == 'jpg' or 'jpeg': # Check for both JPG and JPEG because they are both standardized
        new_filename = f"{name}{suffix}.jpg"
    else:
        new_filename = f"{name}{suffix}{ext}" # Fallback just in case

    # Join the directory and the new filename
    save_path = os.path.join(directory, new_filename)

    # Save the image in WebP format unless specified otherwise
    image.save(save_path, format=output_format.upper())
    print(f"\nImage saved successfully at {save_path} in {output_format.upper()} format.\n\n")

if __name__ == "__main__":
    print("Image Cropper V1.0 (image_cropper.exe)\nPython 3, PyInstaller\n\n")

    # Ask for image path
    image_path = input("Enter the path of the image or drag a file: ").strip()

    # Ask for target aspect ratio, default to 3:4
    aspect_ratio_input = input("Enter target aspect ratio in 'width:height' format (default is 3000:4000): ").strip()

    # Parse aspect ratio input
    if aspect_ratio_input:
        try:
            target_width, target_height = map(int, aspect_ratio_input.split(':'))
        except ValueError:
            print("Invalid format. Using default aspect ratio of 3:4.")
            target_width, target_height = 3000, 4000
    else:
        target_width, target_height = 3000, 4000

    # Crop the image to match the target aspect ratio
    cropped_img = crop_image_to_aspect(image_path, target_width, target_height)

    # Ask for output format (default to WebP)
    output_format = input("Enter output format ( WebP | PNG | JPEG ): ").strip().lower() or 'webp'

    # Automatically save with a _cropped suffix in the same directory and specified format
    if cropped_img:
        save_image_with_suffix(cropped_img, image_path, output_format=output_format)
