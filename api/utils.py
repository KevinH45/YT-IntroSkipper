
def validateVideo(vid):
    # We'll probably use the YT api to make sure this is an actual video
    return type(vid) == str

def validateIntro(intro):
    # We'll probably use the YT api to make sure that the video time exists
    return type(intro) == int and intro >= 0
