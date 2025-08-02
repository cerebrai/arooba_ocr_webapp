import io
import logging
import os

import google.generativeai as genai
from flask import Flask, jsonify, render_template, request
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "your-secret-key-change-this"  # Change this in production
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def configure_gemini():
    """Configure Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def extract_and_correct_text(image_data):
    """Extract text from image and perform grammar/spelling correction"""
    try:
        model = configure_gemini()

        # Convert image data to PIL Image
        image = Image.open(io.BytesIO(image_data))

        # First, extract text from the image
        extraction_prompt = """
        Please extract all the text you can see in this image. 
        Return only the extracted text without any additional commentary or formatting.
        If no text is found, return "No text detected in the image."
        """

        response = model.generate_content([extraction_prompt, image])
        extracted_text = response.text.strip()

        if extracted_text == "No text detected in the image." or not extracted_text:
            return {
                "extracted_text": extracted_text,
                "corrected_text": "",
                "corrections": [],
            }

        # Now perform grammar and spelling correction
        correction_prompt = f"""
        Please analyze the following text for grammar and spelling errors, then provide corrections:

        Text to analyze: "{extracted_text}"

        Please provide your response in the following format:
        CORRECTED TEXT: [The corrected version of the text]
        CORRECTIONS MADE:
        - [List each correction made, if any]
        - [Format: "Original word/phrase" → "Corrected word/phrase" (Reason)]

        If no corrections are needed, state "No corrections needed."
        """

        correction_response = model.generate_content(correction_prompt)
        correction_result = correction_response.text.strip()

        # Parse the correction response
        lines = correction_result.split("\n")
        corrected_text = ""
        corrections = []

        parsing_corrections = False
        for line in lines:
            line = line.strip()
            if line.startswith("CORRECTED TEXT:"):
                corrected_text = line.replace("CORRECTED TEXT:", "").strip()
            elif line.startswith("CORRECTIONS MADE:"):
                parsing_corrections = True
            elif parsing_corrections and line.startswith("- "):
                corrections.append(line[2:])  # Remove "- " prefix
            elif parsing_corrections and line and not line.startswith("-"):
                # If we encounter non-correction text, stop parsing corrections
                break

        # If no corrected text was found, use the original
        if not corrected_text:
            corrected_text = extracted_text

        return {
            "extracted_text": extracted_text,
            "corrected_text": corrected_text,
            "corrections": corrections,
        }

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise e


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if file and allowed_file(file.filename):
            # Read file data
            file_data = file.read()

            # Process the image
            result = extract_and_correct_text(file_data)

            return jsonify(
                {
                    "success": True,
                    "extracted_text": result["extracted_text"],
                    "corrected_text": result["corrected_text"],
                    "corrections": result["corrections"],
                }
            )
        else:
            return jsonify(
                {"error": "Invalid file type. Please upload an image file."}
            ), 400

    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            return jsonify(
                {
                    "error": "Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
                }
            ), 500
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify(
            {
                "error": "An error occurred while processing your image. Please try again."
            }
        ), 500


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Maximum size is 16MB."}), 413


if __name__ == "__main__":
    app.run(debug=True)
