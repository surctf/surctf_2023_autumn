# yt_disk

Смотрим интересное видео, гуглим в интернете как на ютубе можно хранить файлы и находим [репозиторий](https://github.com/DvorakDwarf/Infinite-Storage-Glitch)

Скачиваем файл с помощью этого репозитория:
```bash
$ docker run -it --rm -v ${PWD}:/home/Infinite-Storage-Glitch isg ./target/release/isg_4real download                                       

> What is the url to the video ? https://youtu.be/93Kz5qJEhOg
Starting the download, there is no progress bar
Video downloaded successfully
Output path: /home/Infinite-Storage-Glitch/downloaded_2023-11-03_09-25-13.mp4
```

Вытаскиваем архив из скачаного видео:
```bash
$ docker run -it --rm -v ${PWD}:/home/Infinite-Storage-Glitch isg ./target/release/isg_4real dislodge

> What is the path to your video ? downloaded_2023-11-03_09-25-13.mp4
> Where should the output go ? memes.zip
On frame: 20
On frame: 40
On frame: 60
On frame: 80
Video read successfully
Dislodging frame ended in 6629ms
File written successfully
```

В архиве находится папка [`memes`](./memes), смотрим картинки, кекаем, находим флаг

`flag: surctf_l0v3_d3ath_4nd_c4ts`
