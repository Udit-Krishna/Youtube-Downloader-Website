from flask import Flask
from flask import request 
from flask import render_template
from pytube import YouTube

app = Flask(__name__,static_url_path='/static')

vid = None

@app.route('/final')
def winners(): 
    return render_template('final.html')

@app.route('/',methods=['POST','GET'])
def send():
    if request.method== 'POST':
        link=request.form['link']
        print(link)
        global vid
        try:
            video = YouTube(link)
            print(video.streams)
            video.streams.get_highest_resolution().download(output_path="static", filename="download")
            return render_template('final.html')
        except:
            return render_template('errorpage.html')
    return render_template("main.html")

if __name__=="__main__":
    app.run()


    