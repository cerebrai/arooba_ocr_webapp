# OCR Grammar Checker

A Flask web application that extracts text from images using OCR and performs grammar and spelling corrections using Google's Gemini AI.

## Features

- 📸 **Image Upload**: Drag & drop or browse to upload images
- 🔍 **Text Extraction**: Extracts text from images using Gemini Vision
- ✅ **Grammar Check**: Corrects grammar and spelling errors
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Clean, intuitive interface with animations

## Supported Image Formats

- PNG, JPG, JPEG, GIF, BMP, WebP
- Maximum file size: 16MB

## Setup Instructions

### 1. Clone or Download the Code

Create the following project structure:

```
ocr-grammar-checker/
├── app.py
├── requirements.txt
├── README.md
└── templates/
    └── index.html
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 4. Set Environment Variable

**On Windows:**

```bash
set GEMINI_API_KEY=your_api_key_here
```

**On macOS/Linux:**

```bash
export GEMINI_API_KEY=your_api_key_here
```

**Or create a `.env` file:**

```
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Upload an image containing text by:
   - Dragging and dropping the image onto the upload area
   - Clicking "Choose File" to browse and select an image
3. Wait for the processing to complete
4. View the results:
   - **Extracted Text**: The raw text found in the image
   - **Corrected Text**: The grammar and spelling corrected version
   - **Corrections Made**: List of specific corrections applied

## API Endpoints

- `GET /` - Main page with upload interface
- `POST /upload` - Upload and process image file

## Error Handling

The application handles various error scenarios:

- Invalid file types
- Files too large (>16MB)
- Network errors
- API key not configured
- Images with no detectable text

## Security Considerations

- File size limits prevent memory exhaustion
- Only image files are accepted
- Secure filename handling
- API key stored in environment variables

## Customization

### Modify Text Processing

Edit the prompts in `app.py` to change how text extraction and correction work:

```python
extraction_prompt = "Your custom extraction prompt..."
correction_prompt = "Your custom correction prompt..."
```

### Update UI

Modify `templates/index.html` to customize the appearance and behavior.

### Add Features

- Save results to database
- User authentication
- Batch processing
- Different AI models

## Troubleshooting

**"GEMINI_API_KEY environment variable not set"**

- Make sure you've set the environment variable correctly
- Restart your terminal/command prompt after setting it

**"Invalid file type"**

- Ensure you're uploading a supported image format
- Check the file isn't corrupted

**"File too large"**

- Reduce image size or compress the image
- Maximum supported size is 16MB

**"No text detected"**

- Ensure the image has clear, readable text
- Try improving image quality or contrast

## License

This project is open source and available under the MIT License.
