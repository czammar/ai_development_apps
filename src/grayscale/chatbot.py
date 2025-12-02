import streamlit as st
import requests

# Define the FastAPI endpoint URL
FASTAPI_URL = "http://127.0.0.1:8000/grayscale"

st.title("Grayscale Image Converter Chatbot")
st.write("""
    Upload an image below, and I'll use a FastAPI backend to instantly
    convert it to grayscale!
    """)

uploaded_file = st.file_uploader(
    "Choose an image (JPEG or PNG)...",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Display the original image
    st.subheader("Original Image")
    st.image(uploaded_file, caption=uploaded_file.name)

    # Checkbox to trigger the conversion
    if st.button("Convert to Grayscale via FastAPI"):
        st.subheader("Grayscale Image (from API)")

        # Prepare the file for the POST request
        # The requests library requires a dictionary format for multipart/form-data
        files = {
            "file": (
                uploaded_file.name, uploaded_file.getvalue(),
                uploaded_file.type
                )
            }

        # Call the FastAPI endpoint
        with st.spinner('Contacting FastAPI backend and transforming image...'):
            try:
                response = requests.post(
                    FASTAPI_URL,
                    files=files
                    )

                # Check for a successful response (status code 200)
                if response.status_code == 200 and 'image/png' in response.headers.get('Content-Type', ''):
                    # The response content is the grayscale image data
                    st.image(response.content, caption="Grayscale Image")

                    # Optional: Add a download button
                    st.download_button(
                        label="Download Grayscale Image",
                        data=response.content,
                        file_name=f"grayscale_{uploaded_file.name.replace('.', '_')}.png",
                        mime="image/png"
                    )
                else:
                    st.error(f"Error from API (Status: {response.status_code}): {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("""
                Could not connect to the FastAPI server.
                Please ensure the backend is running at http://127.0.0.1:8000.
                """)
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
