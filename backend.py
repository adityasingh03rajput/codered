import torch
import torchvision.transforms as transforms
from PIL import Image
import timm
import io

# Load the pre-trained model
model_name = "timm/seresnext50_32x4d"
model = timm.create_model(model_name, pretrained=True, num_classes=7)  # 7 skin disease types
model.eval()  # Set to evaluation mode

# Define image transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

# List of skin diseases
disease_classes = [
    "Melanoma", "Melanocytic nevus", "Basal cell carcinoma", 
    "Actinic keratosis", "Benign keratosis", "Dermatofibroma", "Vascular lesion"
]

def classify_skin_image(image_path):
    """Processes the image and predicts the skin disease."""
    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0)  # Add batch dimension

        # Make prediction
        with torch.no_grad():
            outputs = model(image)
            _, predicted_class = torch.max(outputs, 1)  # Get highest probability class

        predicted_disease = disease_classes[predicted_class.item()]
        return f"Predicted Skin Condition: {predicted_disease}"

    except Exception as e:
        return f"Error processing image: {e}"
