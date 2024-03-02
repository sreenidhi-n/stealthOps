import PIL.Image
from PIL import ExifTags 

image = PIL.Image.open("picture_with_EXIF.jpg")
img_exif = image.getexif()
print(type(img_exif))

if img_exif is None:
    print('Sorry, image has no exif data.')
else:
    for key, val in img_exif.items():
        if key in ExifTags.TAGS:
            print(f'{ExifTags.TAGS[key]}:{val}')
        else:
            print(f'{key}:{val}')