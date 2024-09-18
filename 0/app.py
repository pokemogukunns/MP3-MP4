
from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_youtube_as_mp4(url):
    # 一時ファイルの保存先として /tmp を使用
    temp_dir = "/tmp"
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title', None)
        return os.path.join(temp_dir, f"{title}.mp4")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        mp4_file = download_youtube_as_mp4(url)
        return send_file(mp4_file, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
