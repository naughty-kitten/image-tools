import os
from PIL import Image
import pillow_heif  # For HEIC support
import keyboard  # For capturing arrow keys
import time  # To avoid fast scrolling

# Function to display a format selection carousel-like prompt
def carousel_selection(options, prompt_text):
    current_index = 0
    print(f"\n{prompt_text}\nUse LEFT and RIGHT arrow keys to choose, and press ENTER to select:")

    while True:
        # Display the carousel-style format list
        print("\r" + " | ".join([f"<{option}>" if i == current_index else f" {option} " for i, option in enumerate(options)]), end="")

        # Wait for key input
        if keyboard.is_pressed('right'):  # Move to next option
            current_index = (current_index + 1) % len(options)
            #time.sleep(0.025)  # Avoid fast scrolling
            while keyboard.is_pressed('right'):
                pass  # Wait for key release

        elif keyboard.is_pressed('left'):  # Move to previous option
            current_index = (current_index - 1) % len(options)
            #time.sleep(0.025)  # Avoid fast scrolling
            while keyboard.is_pressed('left'):
                pass  # Wait for key release

        elif keyboard.is_pressed('enter'):  # Select current option
            selected_option = options[current_index]
            print(f"\nSelected: {selected_option}")
            return selected_option.lower()  # Return the selected option in lowercase

        time.sleep(0.1)  # Brief delay to allow key detection

# Function to bulk convert images to the selected format with optional prefix
def bulk_convert_images(input_dir, output_format, prefix):
    # Define supported input formats
    supported_formats = ['jpg', 'jpeg', 'png', 'heic', 'webp', 'bmp', 'gif']

    # Iterate through all files in the given directory
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            # Get the file extension and make it lower case
            file_extension = file_name.split('.')[-1].lower()

            # Check if the file is an image that needs conversion
            if file_extension in supported_formats:
                file_path = os.path.join(root, file_name)
                base_name = '.'.join(file_name.split('.')[:-1])  # Filename without extension
                new_file_name = f"{prefix}{base_name}.{output_format}"
                new_file_path = os.path.join(root, new_file_name)

                # Skip conversion if the file is already in the desired format
                if file_extension == output_format:
                    print(f"{file_path} is already in {output_format.upper()} format. Skipping.")
                    continue

                try:
                    # Handle HEIC format separately
                    if file_extension == 'heic':
                        heif_image = pillow_heif.read_heif(file_path)
                        image = Image.frombytes(
                            heif_image.mode, heif_image.size, heif_image.data, "raw"
                        )
                    else:
                        # Open the image for other formats
                        image = Image.open(file_path)

                    # Convert and save the image to the specified format
                    image.save(new_file_path, output_format.upper())
                    print(f"{file_path} converted successfully to {output_format.upper()} format.")

                except Exception as e:
                    print(f"Error converting {file_path}: {e}")

            else:
                print(f"{file_name} is not an image or not in a supported format. Skipping.")

# Main program
if __name__ == "__main__":
    # Step 1: Ask the user for the input directory
    print("Bulk Image Covnerter V1.0 (bulk_image_converter.exe)\nPython 3, PyInstaller\n\n")
    input_directory = input("Please enter the directory or drag a folder containing the images: ")

    # Step 2: Ask the user to select the output format
    format_options = ['WebP', 'PNG', 'JPEG', 'BMP', 'GIF']
    output_format = carousel_selection(format_options, "Select the output format:")

    # Adding a small delay between selections to ensure no keypresses are skipped
    time.sleep(0.5)

    # Step 3: Ask the user to select the file name prefix
    prefix_options = ['no-prefix', 'converted_', 'c_']
    selected_prefix = carousel_selection(prefix_options, "Select the prefix option:")
    if selected_prefix == 'no-prefix':
        prefix = ''  # No prefix, leave the original name
    else:
        prefix = selected_prefix  # Use the selected prefix (e.g., 'convert_' or 'out_')

    # Step 4: Run the bulk conversion
    bulk_convert_images(input_directory, output_format, prefix)
