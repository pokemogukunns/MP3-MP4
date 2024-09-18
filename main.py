 from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_video():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # YouTubeの動画をダウンロード
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        output_path = stream.download()

        # 出力するMP4ファイル名
        output_video_path = "converted_video.mp4"

        # MP4形式で動画を変換
        clip = VideoFileClip(output_path)
        clip.write_videofile(output_video_path, codec="libx264")

        # ダウンロードした元のファイルを削除
        os.remove(output_path)

        return jsonify({'message': '動画の変換が完了しました！', 'file': output_video_path}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
