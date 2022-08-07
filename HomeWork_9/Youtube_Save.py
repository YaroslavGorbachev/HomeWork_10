from pytube import YouTube

#https://www.youtube.com/watch?v=jvipPYFebWc     моё любимое видео


vid = input('Вставьте ссылку на видео, которое хотите скачать: ')
yt = YouTube(vid)

path = input('Напишите адрес папки, куда скачать файл: ')
yt.streams.filter(progressive=True, file_extension='mp4')
yt.streams.order_by('resolution')
yt.streams.desc()
yt.streams.first().download(path)