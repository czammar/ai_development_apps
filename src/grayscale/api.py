from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
import io


app = FastAPI()

@app.post("/grayscale")
async def to_grayscale(file: UploadFile = File(...)):
    """
    Receives an image file, converts it to grayscale, and returns the result.
    """
    try:
        # Read the image content from the uploaded file
        image_data = await file.read()
        image_stream = io.BytesIO(image_data)

        # Open image using Pillow
        img = Image.open(image_stream)

        # **Transform to Grayscale** (Pillow's 'L' mode)
        grayscale_img = img.convert('L') # 'L' is the standard grayscale mode

        # Save the grayscale image back to a BytesIO object
        output_stream = io.BytesIO()
        # Save as PNG to avoid potential quality loss (JPEG is lossy)
        grayscale_img.save(output_stream, format="PNG")
        output_stream.seek(0)

        # Return the processed image bytes as a file response
        return Response(content=output_stream.read(), media_type="image/png")

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # The API will run on http://127.0.0.1:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
