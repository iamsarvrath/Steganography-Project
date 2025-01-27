from PIL import Image

def encode_message(image_path: str, message: str, output_path: str):
    """Encodes a secret message into an image."""
    try:
        
        image = Image.open(image_path)
        image = image.convert('RGB')

       
        pixels = list(image.getdata())

        
        message += 'END'  
        binary_message = ''.join(format(ord(char), '08b') for char in message)

        if len(binary_message) > len(pixels) * 3:
            raise ValueError("Message is too long to encode in the given image.")

        
        new_pixels = []
        binary_index = 0

        for pixel in pixels:
            r, g, b = pixel
            if binary_index < len(binary_message):
                r = (r & ~1) | int(binary_message[binary_index])  
                binary_index += 1
            if binary_index < len(binary_message):
                g = (g & ~1) | int(binary_message[binary_index])  
                binary_index += 1
            if binary_index < len(binary_message):
                b = (b & ~1) | int(binary_message[binary_index])  
                binary_index += 1
            new_pixels.append((r, g, b))

        
        new_image = Image.new(image.mode, image.size)
        new_image.putdata(new_pixels)
        new_image.save(output_path)

        print(f"Message encoded and saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

def decode_message(image_path: str) -> str:
    """Decodes a secret message from an image."""
    try:
        
        image = Image.open(image_path)
        image = image.convert('RGB')

        
        pixels = list(image.getdata())

        
        binary_message = ''
        for pixel in pixels:
            for value in pixel:
                binary_message += str(value & 1)

        
        characters = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)]
        message = ''.join(characters)

        
        end_index = message.find('END')
        if end_index != -1:
            return message[:end_index]
        else:
            return "No hidden message found."
    except Exception as e:
        print(f"Error: {e}")
        return ""


if __name__ == "__main__":
    
    encode_message(
        image_path="input_image.png", 
        message="Type The Message Here", 
        output_path="output_image.png"
    )

    decoded_message = decode_message("output_image.png")
    print(f"Decoded message: {decoded_message}")
