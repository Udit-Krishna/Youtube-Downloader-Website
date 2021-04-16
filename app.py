from flask import Flask
from flask import request
from flask import render_template
from flask.helpers import url_for
import youtube_dl
import os
from time import sleep

app = Flask(__name__, static_url_path='/static')

#@app.route('/final')
#def final():
#    l = os.listdir('static')
#    vid_name = []
#    for a in l:
#        if a.split('.')[0]=='download':
#            vid_name.append(a)
#    filename = vid_name[0]
#    return render_template('final_video.html', filename = filename)

#@app.route('/final')
#def final_aud():
#    files = os.listdir('static') 
#    for a in files:
#        if a.split('.')[0] == 'download':
#            fo = a
#    return render_template('final_audio.html', filename =fo)


@app.route('/',methods=['POST','GET'])
def send():
    if request.method== 'POST':
        link=request.form['link']
        fmt=request.form['options']
        if not fmt:
            fmt = 'video'
        try:
            aydl_opts = {'format': 'bestaudio/best',
                            'outtmpl': 'static/download.mp3',
                        'extractaudio': True,
                        'audioformat': "mp3",}
            vydl_opts = {'format': 'bestvideo[filesize<50M][height<=?1080]+bestaudio/best',
                        'outtmpl': 'static/download',}
            if fmt == 'audio':
                with youtube_dl.YoutubeDL(aydl_opts) as ydl:
                    ydl.download([f'{link}'])
                    return render_template('final_audio.html')
            if fmt == 'video':
                with youtube_dl.YoutubeDL(vydl_opts) as ydl:
                    ydl.download([f'{link}'])
                l = os.listdir('static')
                vid_name = []
                for a in l:
                    if a.split('.')[0]=='download':
                        vid_name.append(a)
                filename = vid_name[0]
                return render_template('final_video.html', filename = filename)
        except:
            return render_template('errorpage.html')
    return render_template("main.html")

@app.before_request
def remove_file1():
    if request.path == '/':
        try:
            l = os.listdir('static')
            for a in l:
                if a.find('download') != -1:
                    os.remove(f'static/{a}')     
        except:
            pass

@app.after_request
def remove_file2(response):
    sleep(1)
    if request.path.find('/static/download') != -1:
        try:
            l = os.listdir('static')
            for a in l:
                if a.find('download') != -1:
                    os.remove(f'static/{a}')     
        except:
            pass
    return response
        
if __name__=="__main__":
    app.run()


    