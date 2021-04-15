from flask import Flask
from flask import request 
from flask import render_template
import youtube_dl
import os

app = Flask(__name__,static_url_path='/static')

@app.route('/final_vid')
def final_vid():
    files = os.listdir('static') 
    for a in files:
        if a.split('.')[0] == 'download':
            fo = a
    return render_template('final_video.html', filename = fo)

@app.route('/final_aud')
def final_aud():
    files = os.listdir('static') 
    for a in files:
        if a.split('.')[0] == 'download':
            fo = a
    return render_template('final_video.html', filename = fo)

@app.route('/',methods=['POST','GET'])
def send():
    if request.method== 'POST':
        link=request.form['link']
        fmt=request.form['options']
        if not fmt:
            fmt = 'video'
        print(link,fmt)
        try:
            os.remove('static/download.mp3')
        except:
            pass
        try:
            os.remove('static/download.mkv')
        except:
            pass
        try:
            aydl_opts = {'format': 'bestaudio/best',
                         'outtmpl': 'static/download.mp3',
                        'extractaudio': True,
                        'audioformat': "mp3",}
            if fmt == 'audio':
                with youtube_dl.YoutubeDL(aydl_opts) as ydl:
                    ydl.download([f'{link}'])
                    return render_template('final_audio.html')
            if fmt == 'video':
                os.system(f'youtube-dl -f "bestvideo[filesize<500M][height<=?720]+bestaudio/best" -o "/static/download" --no-continue {link}')
                return render_template('final_video.html')
        except:
            return render_template('errorpage.html')
    return render_template("main.html")

if __name__=="__main__":
    app.run()


    