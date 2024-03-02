from PIL import Image
from PIL.ExifTags import TAGS
import exifread

def get_exif_data(image):
    exif_data = image._getexif()
    if exif_data is not None:
        exif = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif[tag_name] = value
        return exif
    return None

def convert_to_degrees(value):
    d, m, s = value
    return d + m / 60.0 + s / 3600.0

def get_gps_coordinates(image):
    with open(image.filename, 'rb') as f:
        exif_tags = exifread.process_file(f)
        gps_latitude = exif_tags.get('GPS GPSLatitude')
        gps_longitude = exif_tags.get('GPS GPSLongitude')
        gps_latitude_ref = exif_tags.get('GPS GPSLatitudeRef')
        gps_longitude_ref = exif_tags.get('GPS GPSLongitudeRef')
        if gps_latitude and gps_longitude and gps_latitude_ref and gps_longitude_ref:
            latitude = convert_to_degrees(gps_latitude.values)
            longitude = convert_to_degrees(gps_longitude.values)
            return latitude, longitude, gps_latitude_ref.values, gps_longitude_ref.values
    return None


def get_date_taken(path):
    exif = Image.open(path)._getexif()
    if not exif:
        raise Exception('Image does not have EXIF data.')
    return exif[36867]

image_path = 'DSCN0042.jpg'
image = Image.open(image_path)
gps_data = get_gps_coordinates(image)
if gps_data:
    latitude, longitude, latitude_ref, longitude_ref = gps_data
    print("GPS Coordinates:")
    print("Latitude:", latitude, latitude_ref)
    print("Longitude:", longitude, longitude_ref)
else:
    print("No GPS data found in the image.")

