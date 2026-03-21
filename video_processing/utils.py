from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

# Load model once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def frames_to_text(folder_path="outputs/frames"):
    descriptions = []

    frame_files = sorted(os.listdir(folder_path))[:5]

    for file in frame_files:
        if file.endswith(".jpg"):
            path = os.path.join(folder_path, file)
            image = Image.open(path).convert("RGB")

            inputs = processor(image, return_tensors="pt")
            out = model.generate(**inputs)

            caption = processor.decode(out[0], skip_special_tokens=True)
            descriptions.append(caption)

    return " ".join(descriptions)