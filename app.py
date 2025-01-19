from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure downloads folder exists
if not os.path.exists(os.path.join(os.path.expanduser('~'), 'Downloads')):
    os.makedirs(os.path.join(os.path.expanduser('~'), 'Downloads'))

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('videoUrl')  
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400

    try:
        # Define options for yt-dlp (best combined format)
        ydl_opts = {
            'outtmpl': os.path.join(os.path.expanduser('~'), 'Downloads', '%(title)s.%(ext)s'),  # Save in user's Downloads folder
            'format': 'best',      # Download best combined format
            'noplaylist': True,    # Don't download entire playlist
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)  # Download video
            file_path = ydl.prepare_filename(info)            # Get downloaded file path
            if not os.path.isfile(file_path):
                return jsonify({"error": "File not found after download"}), 500

            # Send the file to the user
            return send_file(file_path, as_attachment=True)

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"Failed to download video: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)