from flask import Flask, request, jsonify, send_file, make_response, render_template
from werkzeug.utils import secure_filename
import os
from Main import speech_to_speech_streaming
import tempfile

app = Flask(__name__, static_folder='static', template_folder='templates')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}
FFMPEG_PATH = r"C:\Users\JMD\Downloads\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create templates and static directories if they don't exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Language code mapping
LANGUAGE_CODES = {
    'Hindi': 'hi',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Russian': 'ru',
    'Arabic': 'ar',
    'Portuguese': 'pt',
    'Bengali': 'bn'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept'
    return response

# Root route to serve the HTML file
@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/api/process-video', methods=['POST', 'OPTIONS'])
def process_video():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())
        
    try:
        if 'video' not in request.files:
            response = make_response(jsonify({'error': 'No video file provided'}), 400)
            return add_cors_headers(response)
        
        video_file = request.files['video']
        language = request.form.get('language')
        
        if video_file.filename == '':
            response = make_response(jsonify({'error': 'No selected file'}), 400)
            return add_cors_headers(response)
            
        if not allowed_file(video_file.filename):
            response = make_response(jsonify({'error': 'Invalid file type'}), 400)
            return add_cors_headers(response)
            
        if language not in LANGUAGE_CODES:
            response = make_response(jsonify({'error': 'Invalid language selection'}), 400)
            return add_cors_headers(response)

        # Create temporary files for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as input_video:
            video_file.save(input_video.name)
            
            # Create temporary files for output
            temp_audio = tempfile.mktemp(suffix='.mp3')
            temp_output = tempfile.mktemp(suffix='.mp4')
            
            try:
                # Process the video
                speech_to_speech_streaming(
                    FFMPEG_PATH,
                    input_video.name,
                    LANGUAGE_CODES[language],
                    temp_audio,
                    temp_output
                )
                
                # Return the processed video
                response = make_response(send_file(
                    temp_output,
                    mimetype='video/mp4',
                    as_attachment=True,
                    download_name=f'translated_{secure_filename(video_file.filename)}'
                ))
                return add_cors_headers(response)
                
            except Exception as e:
                response = make_response(jsonify({'error': str(e)}), 500)
                return add_cors_headers(response)
                
            finally:
                # Clean up temporary files
                for temp_file in [input_video.name, temp_audio, temp_output]:
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
                
    except Exception as e:
        response = make_response(jsonify({'error': str(e)}), 500)
        return add_cors_headers(response)

@app.route('/api/languages', methods=['GET', 'OPTIONS'])
def get_languages():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())
        
    response = make_response(jsonify(list(LANGUAGE_CODES.keys())))
    return add_cors_headers(response)

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    if request.method == 'OPTIONS':
        return add_cors_headers(make_response())
        
    response = make_response(jsonify({'status': 'healthy'}))
    return add_cors_headers(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)