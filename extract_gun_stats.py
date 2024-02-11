import cv2
import easyocr

def load_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Perform text detection and recognition
    result = reader.readtext(image)
    return image, reader, result

def extract_text(image, reader, result, regions):
    extracted_text = {}

    # Iterate through the specified regions
    image_with_boxes = image.copy()  # Create a copy of the original image to draw boxes on
    for region_name, region_coords in regions.items():
        text_in_region = ""
        for detection in result:
            # Get bounding box coordinates
            box = detection[0]
            x1_tl, y1_tl = int(box[0][0]), int(box[0][1])
            x2_br, y2_br = int(box[2][0]), int(box[2][1])

            # Check if the bounding box intersects with the specified region
            if all(coord[0] >= region_coords[0] and coord[1] >= region_coords[1] and
                   coord[0] <= region_coords[2] and coord[1] <= region_coords[3] for coord in [(x1_tl, y1_tl), (x2_br, y2_br)]):
                text_in_region += detection[1] + " "
                # Draw a blue box around the region
                cv2.rectangle(image_with_boxes, (region_coords[0], region_coords[1]), (region_coords[2], region_coords[3]), (255, 0, 0), 2)

        extracted_text[region_name] = text_in_region.strip()

    return extracted_text, image_with_boxes

if __name__ == "__main__":
    image_path = 'image.jpeg'  # Replace with the path to your image
    image, reader, result = load_image(image_path)  # Load image and get EasyOCR result
    # Define the regions with their coordinates
    regions = {
        'Weapon Type': (75, 70, 400, 100),
        'Weapon Name': (75, 108, 562, 156),  # Example: top-left (100, 100) and bottom-right (300, 200)
        'Damage': (95, 241, 395, 403),
        'Range':(530,238,830,332),
        'Fire Rate':(530,501,839,521),
        'Recoil Control':(965,225,1291,329),
        'Accuracy':(965,501,1352,628),
        'Mobility':(1395,235,1765,401),
        'Handling':(1400,501, 1711,661)

    }
    extracted_text, image_with_boxes = extract_text(image, reader, result, regions)  # Extract text from regions and draw boxes
    print("Extracted Text:")
    for region_name, text in extracted_text.items():
        print(f"{region_name}: {text}")
    # Display the image with boxes
    cv2.imshow('Detected Text', image_with_boxes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()