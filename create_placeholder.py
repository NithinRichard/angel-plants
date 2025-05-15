from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(text, width=300, height=300, bg_color=(240, 240, 240), text_color=(150, 150, 150)):
    """Create a placeholder image with the given text."""
    # Create a new image with the specified background color
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a nice font if available, otherwise use default
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw the text
    draw.text((x, y), text, font=font, fill=text_color)
    
    # Draw a border
    border = 2
    draw.rectangle([(border, border), (width - border, height - border)], outline=text_color, width=1)
    
    return image

if __name__ == "__main__":
    # Create the media directory if it doesn't exist
    media_dir = os.path.join('media', 'products')
    os.makedirs(media_dir, exist_ok=True)
    
    # Create and save the placeholder image
    placeholder_path = os.path.join(media_dir, 'placeholder.jpg')
    placeholder = create_placeholder_image("No Image Available")
    placeholder.save(placeholder_path, 'JPEG')
    
    print(f"Created placeholder image at: {placeholder_path}")
