from deepface import DeepFace
import tempfile
import os

def compare_faces(img1_file, img2_file):
    try:
        # Create temporary files with delete=False
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp1, \
             tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp2:

            # Save file paths before closing
            temp1_path = temp1.name
            temp2_path = temp2.name

            # Write file content
            img1_file.seek(0)  # Ensure reading from start
            temp1.write(img1_file.read())
            img2_file.seek(0)
            temp2.write(img2_file.read())

        # Verify faces using the saved paths
        result = DeepFace.verify(img1_path=temp1_path, img2_path=temp2_path)
        
        # Cleanup temporary files
        os.unlink(temp1_path)
        os.unlink(temp2_path)
        
        return result

    except Exception as e:
        print("🔥 DeepFace error:", str(e))
        return {"error": f"Exception while processing: {str(e)}"}