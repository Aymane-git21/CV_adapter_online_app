# CV Adapter Online App

A powerful web application that tailors your LaTeX CV and generates professional cover letters based on specific job descriptions. This tool uses AI to analyze job requirements and adapt your experience to match, helping you stand out to recruiters and ATS (Applicant Tracking System) software.

## Features

-   **CV Tailoring**: Automatically rewrites your CV's bullet points to highlight skills and experiences relevant to the job description.
-   **Cover Letter Generation**: Creates a personalized cover letter that aligns with the company's values and job requirements.
-   **PDF Generation**: Compiles your tailored CV and cover letter into professional PDF documents using LaTeX.
-   **ATS Scoring**: Provides an estimated ATS match score and suggests missing keywords.
-   **History Tracking**: Keeps a record of all your applications for easy reference.

## Prerequisites

-   **Python 3.8+**
-   **MiKTeX** (or another LaTeX distribution) with `pdflatex` available in your system PATH.
-   **Google Gemini API Key**: You will need an API key from Google AI Studio.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/CV_adapter_online_app.git
    cd CV_adapter_online_app
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**:
    Create a `.env` file in the root directory and add your API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    flask_secret_key=your_secret_key
    ```

## Usage

1.  **Start the application**:
    ```bash
    python app.py
    ```

2.  **Open your browser**:
    Navigate to `http://127.0.0.1:5000`.

3.  **Upload & Generate**:
    -   Upload your master CV (in LaTeX format) or paste the text.
    -   Paste the Job Description.
    -   Click "Start Adaptation".

## Project Structure

-   `app.py`: Main Flask application.
-   `templates/`: HTML templates for the web interface.
-   `static/`: CSS and Client-side JavaScript.
-   `CV.tex` & `CoverLetter.tex`: LaTeX templates used for generation.
-   `uploads/` & `outputs/`: Directories for handling files.

## License

[MIT License](LICENSE)
