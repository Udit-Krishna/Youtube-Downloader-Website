from flask import Flask
from flask import request
from flask import render_template, send_from_directory
import youtube_dl
import os
from time import sleep

app = Flask(__name__, static_url_path='/static')


@app.route('/',methods=['POST','GET'])
def send():
    if request.method== 'POST':
        link=request.form['link']
        fmt=request.form['options']
        try:
            aydl_opts = {'format': 'bestaudio/best',
                            'outtmpl': 'downloads/download.mp3',
                        'extractaudio': True,
                        'audioformat': "mp3",}
            vydl_opts = {'format': 'bestvideo[filesize<50M][height<=?1080]+bestaudio/best',
                        'outtmpl': 'downloads/download',}
            if fmt == 'audio':
                with youtube_dl.YoutubeDL(aydl_opts) as ydl:
                    ydl.download([f'{link}'])
                    return send_from_directory('downloads', 'download.mp3', as_attachment=True)
            if fmt == 'video':
                if link.find('twitter') != -1:
                    vydl_opts = {'format': 'bestvideo[filesize<10M][height<=?720]+bestaudio/best',
                        'outtmpl': 'downloads/download.mp4',}
                with youtube_dl.YoutubeDL(vydl_opts) as ydl:
                    ydl.download([f'{link}'])
                l = os.listdir('downloads')
                vid_name = []
                for a in l:
                    if a.split('.')[0]=='download':
                        vid_name.append(a)
                filename = vid_name[0]
                return send_from_directory('downloads', filename, as_attachment = True)
        except:
            return render_template('errorpage.html')
    return render_template("main.html")

@app.before_request
def remove_file1():
    if request.path == '/' and request.path.find('/downloads/download') == -1:
        try:
            l = os.listdir('downloads')
            for a in l:
                if a.find('download') != -1:
                    os.remove(f'downloads/{a}')     
        except:
            pass

@app.after_request
def remove_file2(response):
    sleep(1)
    if request.path.find('/download') != -1:
        try:
            l = os.listdir('downloads')
            for a in l:
                if a.find('download') != -1:
                    print(a)
                    os.remove(f'downloads/{a}')     
        except:
            pass
    return response
       
if __name__=="__main__":
    app.run()


    
