import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import google.generativeai as genai
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Gemini Configuration
# Ensure GEMINI_API_KEY is set in environment variables or .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def adapt_cv_with_gemini(tex_content, job_description):
    """
    Uses Gemini to adapt the LaTeX CV content based on the job description.
    """
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API Key is missing.")

    model = genai.GenerativeModel('models/gemini-3-pro-image-preview')
    prompt = f"""
    You are an expert CV tailor.
    I have a LaTeX CV and a Job Description.
    Your task is to modify the 'Profile' or 'Summary' section and the 'Title' of the CV to better match the Job Description.
    Do NOT invent false information. Only highlight relevant skills and experiences already present or implied.
    Keep the LaTeX structure valid. Return ONLY the full valid LaTeX code.

    Job Description:
    {job_description}

    LaTeX CV:
    {tex_content}
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

def compile_latex(tex_path, output_dir):
    """
    Compiles the LaTeX file to PDF using pdflatex.
    """
    # Run pdflatex twice to ensure references are correct (though usually once is enough for simple CVs)
    # We use -interaction=nonstopmode to prevent hanging on errors
    pdflatex_path = r'C:\Users\ayman\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe'
    pdf_filename = os.path.splitext(os.path.basename(tex_path))[0] + ".pdf"
    expected_pdf_path = os.path.join(output_dir, pdf_filename)

    try:
        # check=False allows us to handle non-zero exit codes manually
        result = subprocess.run([pdflatex_path, '-interaction=nonstopmode', '-output-directory', output_dir, tex_path], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if PDF was created despite potential errors/warnings
        if os.path.exists(expected_pdf_path):
            return expected_pdf_path
        else:
            # If no PDF, then it was a fatal error
            raise RuntimeError(f"LaTeX compilation failed. Return code: {result.returncode}. Stderr: {result.stderr.decode('latin1')}")

    except FileNotFoundError:
        raise RuntimeError(f"pdflatex not found at {pdflatex_path}. Please ensure MiKTeX is installed correctly.")
    except Exception as e:
        raise RuntimeError(f"LaTeX compilation error: {str(e)}")

def send_email(pdf_path, recipient_email):
    """
    Sends the generated PDF to the user via email.
    Note: This requires a valid Gmail account and App Password or Service Account setup.
    For simplicity in this demo, we'll assume standard SMTP with App Password if provided,
    or just log it if not fully configured.
    """
    sender_email = os.getenv('GMAIL_USER')
    sender_password = os.getenv('GMAIL_PASSWORD').replace(" ", "")

    if not sender_email or not sender_password:
        print("Gmail credentials not found in .env. Skipping email.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Your Adapted CV"

    body = "Please find attached your adapted CV based on the provided job description."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(pdf_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(pdf_path)}",
        )
        msg.attach(part)

        # Use SMTP_SSL for port 465
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.starttls() # Not needed for SSL
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

        # Don't raise, just log, so the user still gets the download


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'job_description' not in request.form:
            flash('No job description provided')
            return redirect(request.url)
        
        job_description = request.form['job_description']
        recipient_email = request.form.get('email')
        
        # Hardcoded CV path
        cv_filename = 'CV.tex'
        file_path = os.path.abspath(cv_filename)
        
        if not os.path.exists(file_path):
            flash(f'Error: {cv_filename} not found in the project directory.')
            return redirect(request.url)
            
        try:
            # 1. Read LaTeX
            with open(file_path, 'r', encoding='utf-8') as f:
                tex_content = f.read()
            
            # 2. Adapt with Gemini
            adapted_tex_content = adapt_cv_with_gemini(tex_content, job_description)
            
            # Clean up markdown code blocks if Gemini adds them
            if adapted_tex_content.startswith("```latex"):
                adapted_tex_content = adapted_tex_content[8:]
            if adapted_tex_content.startswith("```"):
                adapted_tex_content = adapted_tex_content[3:]
            if adapted_tex_content.endswith("```"):
                adapted_tex_content = adapted_tex_content[:-3]
            
            # Save adapted version
            adapted_filename = f"adapted_{cv_filename}"
            adapted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], adapted_filename)
            
            with open(adapted_file_path, 'w', encoding='utf-8') as f:
                f.write(adapted_tex_content)
            
            # 3. Compile to PDF
            pdf_path = compile_latex(adapted_file_path, app.config['OUTPUT_FOLDER'])
            
            # 4. Send Email (Optional)
            if recipient_email:
                send_email(pdf_path, recipient_email)
                flash(f'CV Adapted! Email sent to {recipient_email}. Downloading now...')
            else:
                flash('CV Adapted! Downloading now...')
            
            return send_file(pdf_path, as_attachment=True)

        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
