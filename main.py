from music_bot import make_video

file = open("links.txt", "r")
text = file.read()
for link in text.split("\n"):
    if link:
        print("doing: " + link)
        make_video(link)
file.close()