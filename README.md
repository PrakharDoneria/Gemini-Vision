# Flask Application Documentation

This Flask application provides an endpoint for vision processing using Gemini Pro API.

## Endpoints

### Vision Endpoint

- **URL:** `/gemini/vision`
- **Method:** GET
- **Parameters:**
  - `url`: The URL of the image to process.
  - `prompt`: Prompt for the vision processing.
- **Response:** JSON object containing the processed vision data.

## Usage

To use the vision processing endpoint, make a GET request to `/gemini/vision` with the required parameters. Here's an example using cURL:

```bash
curl "https://YourSite.com/gemini/vision?url=<image_url>&prompt=<prompt>"
