from PIL import Image, ExifTags
import os
import traceback
from flask import current_app

def mean(numbers):
    return round(float(sum(numbers)) / max(len(numbers), 1),1)

def rotateImage(path,fileName):
    try :
        current_app.logger.error('Rotation -open image')
        image=Image.open(os.path.join(path, fileName))
        for orientation in ExifTags.TAGS.keys() :
            if ExifTags.TAGS[orientation]=='Orientation' : break
        exif=dict(image._getexif().items())

        current_app.logger.info('Rotation ' + str(exif[orientation]))
        if   exif[orientation] == 3 :
            image=image.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6 :
            image=image.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8 :
            image=image.transpose(Image.ROTATE_90)

        #image.thumbnail((250 , 250), Image.ANTIALIAS)
        image.save(os.path.join(path,fileName))

    except:
        traceback.print_exc()
