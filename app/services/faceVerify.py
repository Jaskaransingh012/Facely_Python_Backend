from deepface import DeepFace
import tempfile
import cv2
import os
import gc

def resize_image(image_path, target_size=(300, 300)):
    img = cv2.imread(image_path)
    resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(image_path, resized)

def compare_faces(img1_file, img2_file):
    try:
        # 1. Use lighter model
        model_name = "Facenet"  # 90MB vs VGG-Face's 500MB
        
        # 2. Reduce image size before processing
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp1, \
             tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp2:

            # Save original files
            img1_file.save(temp1.name)
            img2_file.save(temp2.name)

            # Resize images to reduce memory footprint
            resize_image(temp1.name)
            resize_image(temp2.name)

        # 3. Force garbage collection
        gc.collect()

        # 4. Process with memory optimizations
        result = DeepFace.verify(
            img1_path=temp1.name,
            img2_path=temp2.name,
            model_name=model_name,
            enforce_detection=False,  # Skip if no face found
            detector_backend="retinaface"  # More memory-efficient
        )

        # 5. Cleanup
        os.unlink(temp1.name)
        os.unlink(temp2.name)
        gc.collect()

        return result

    except Exception as e:
        print(f"🔥 Error: {str(e)}")
        return {"error": str(e)}