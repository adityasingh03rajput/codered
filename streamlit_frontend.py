import streamlit as st
from backend import classify_skin_image
from PIL import Image
import os

def main():
    st.set_page_config(page_title="AI Dermatologist", layout="centered")
    st.title("📸 AI Dermatologist: Skin Disease Scanner")
    st.write("Upload a skin image to analyze and get a diagnosis.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "webp"])
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Save the uploaded file temporarily
        temp_path = "temp_image" + os.path.splitext(uploaded_file.name)[-1]
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process image
        st.write("🔍 Analyzing image...")
        result = classify_skin_image(temp_path)
        
        # Display result
        st.subheader("🩺 Diagnosis:")
        st.success(result)

        # Remove temp file
        os.remove(temp_path)

if __name__ == "__main__":
    main()
