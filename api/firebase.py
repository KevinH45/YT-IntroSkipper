from firebase_admin import db

def getVideoIntroTime(vid):
    '''
    Gets the video intro time from the DB
    :param vid: Video id from YouTube
    :return: An integer of the seconds
    '''
    ref = db.reference("videos")
    snapshot = ref.order_by_child("vid").equal_to(vid)

    video = snapshot.get()
    try:
        refId = str(list(video.keys())[0])
    except IndexError:
        return None

    beforeIntro = None
    afterIntro = None

    if video[refId]["beforeIntro"]["pre"] != "null":
        # Get pre value
        beforeIntro = video[refId]["beforeIntro"]["pre"]
    else:
        # Get mean
        try: beforeIntro = video[refId]["beforeIntro"]["sum"]/video[refId]["beforeIntro"]["len"]
        except ZeroDivisionError: beforeIntro = 0

    if video[refId]["afterIntro"]["pre"] != "null":
        # Get pre value
        afterIntro = video[refId]["afterIntro"]["pre"]
    else:
        # Get mean
        try: afterIntro = video[refId]["afterIntro"]["sum"]/video[refId]["afterIntro"]["len"]
        except ZeroDivisionError: afterIntro = 0

    return beforeIntro, afterIntro

def createNewIntro(vid, beforeIntro, afterIntro):

    ref = db.reference("videos")
    vidRef = ref.push()

    # You can't save a null value in firebase
    vidRef.set({
        "vid": vid,
        "beforeIntro": {"sum": beforeIntro, "len": 1, "pre": "null"},
        "afterIntro": {"sum": afterIntro, "len": 1, "pre": "null"},
    })
    return True

def updateBeforeDict(snapshot, beforeIntro):
    video = snapshot.get()
    refId = str(list(video.keys())[0])
    beforeSum, beforeLen, beforePre = video[refId]["beforeIntro"]["sum"],video[refId]["beforeIntro"]["len"],video[refId]["beforeIntro"]["pre"]

    if beforeLen >= 200:
        if beforePre == "null":
            beforePre = beforeSum / beforeLen
            beforeSum = beforePre
            beforeLen = 1
        else:
            tmp = beforeSum / beforeLen

            if abs(beforePre - tmp) > 1:
                beforePre = tmp
                beforeSum = tmp
                beforeLen = 1
        return {"sum": beforeSum, "len": beforeLen, "pre": beforePre}

    return {"sum": beforeSum+beforeIntro, "len": beforeLen+1, "pre": beforePre}

def updateAfterDict(snapshot, afterIntro):
    video = snapshot.get()
    refId = str(list(video.keys())[0])
    afterSum, afterLen, afterPre = video[refId]["afterIntro"]["sum"], video[refId]["afterIntro"]["len"], video[refId]["beforeIntro"]["pre"]

    if afterLen >= 200:
        if afterPre == "null":
            afterPre = afterSum / afterLen
            afterSum = afterPre
            afterLen = 1
        else:
            tmp = afterSum / afterLen

            if abs(afterPre - tmp) > 1:
                afterPre = tmp
                afterSum = tmp
                afterLen = 1
        return {"sum": afterSum, "len": afterLen, "pre": afterPre}

    return {"sum": afterSum+afterIntro, "len": afterLen+1, "pre": afterPre}

def updateIntro(vid, beforeIntro, afterIntro):
    ref = db.reference("/videos")
    snapshot = ref.order_by_child("vid").equal_to(vid)

    video = snapshot.get()
    refId = str(list(video.keys())[0])

    ref.child(refId).update({"afterIntro": updateAfterDict(snapshot, afterIntro),
                             "beforeIntro": updateBeforeDict(snapshot, beforeIntro)})

    return True

def setVideoIntro(vid, beforeIntro, afterIntro):
    '''
    Sets the video's intro time in the DB
    :param vid: Video id from YouTube
    :return: True if succces, False if failure.
    '''

    # If video already exists in DB
    if getVideoIntroTime(vid) is not None:
        status = updateIntro(vid, beforeIntro, afterIntro)
    else:
        status = createNewIntro(vid, beforeIntro, afterIntro)

    return status


