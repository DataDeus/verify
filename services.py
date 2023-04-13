# Verify takes a screenshot and checks that it matches Druve's standards. Checks include:
# - is a whatsapp generated screenshot, the screenshot is unique to ad and user
# Logic - This will change
# Get image from Seyi in the format, <adID_emailAddress.png>
# finding duplicate screnshots will be via the device meta data
# find users with very low end devices and trace their screenshots if possible

# dependencies
import PIL
import numpy as np
import pytesseract as pt
from PIL import Image as img
from roboflow import Roboflow


# screenshot = 'test_image.jpg' # works
# screenshot = '5e9f02c18cbe0c3102c56473_godsenteliel@gmail.com.png' # works
# screenshot = '5e9f02c18cbe0c3102c56473_godsenteliel@gmail.com.jpg'
# screenshot = '/Users/eliel/Documents/Dev/Druve/verify/200/4a33ce6a-03be-4a02-8af2-860cebfc6957-Screenshot_2022_0620_183955_jimaoo.png' # pending
# screenshot = '/Users/eliel/Documents/Dev/Druve/verify/200/053f896d-e9a8-4cbf-afe4-641b48906b85-Screenshot_2022_0620_183848_fjt7zi.png' # pending

# screenshot = '/Users/eliel/Documents/Dev/Druve/verify/100/image 10.png'

# metaData = screenshot.split('_')
# adType = metaData[0]
# views = metaData[1]
# email = metaData[2]

def match(screenshot):
    # print(screenshot)
    # Confirm whatsapp screenshot
    rf = Roboflow(api_key="gwE918lUhcpdzpBqpNTv")
    project = rf.workspace().project("verify-pqshw")
    model = project.version(2).model
    predictions = model.predict(screenshot, confidence=40, overlap=30).json()

    predictions = predictions.get('predictions')

    if len(predictions) == 1:
        return 'undefined'
        
    elif len(predictions) == 2:
        if predictions[0].get('class') == 'pictureMatch_y' and predictions[1].get('class') == 'viewsMatch_y':
            return True
        elif predictions[0].get('class') == 'viewsMatch_y' and predictions[1].get('class') == 'pictureMatch_y':
            return True
        elif predictions[0].get('class') == 'viewsMatch_n' or predictions[1].get('class') == 'pictureMatch_n':
            return False
        else:
            return False

def detect(screenshot):

    viewsNumber = None
    # Detect views
    image = img.open(screenshot)
    pillow = image.transpose(img.FLIP_TOP_BOTTOM)
    # pillow = pillow.crop((20, 0, 600, 200)) # (left, top, right, bottom)
    pillow = pillow.crop((20, 0, 600, 150))
    pillow = pillow.transpose(img.FLIP_TOP_BOTTOM)
    croppedImage = pillow.crop((340, 40, 400, 250)) 
    # croppedImage = pillow.crop((340, 20, 400, 150)) 

    # check for views
    char = np.array(croppedImage)
    views = pt.image_to_string(char)

    if '\n' in views:
        views = views.replace('\n', '')
        views = int(views)
        #return views
        viewsNumber = views

    if viewsNumber == None:
        image = img.open(screenshot)
        pillow = image.transpose(img.FLIP_TOP_BOTTOM)
        pillow = pillow.crop((20, 0, 600, 200)) # (left, top, right, bottom)
        # pillow = pillow.crop((20, 0, 600, 150))
        pillow = pillow.transpose(img.FLIP_TOP_BOTTOM)
        # croppedImage = pillow.crop((340, 40, 400, 250)) 
        croppedImage = pillow.crop((340, 20, 400, 152)) 
        # check for views
        char = np.array(croppedImage)
        views = pt.image_to_string(char)

        if '\n' in views:
            views = views.replace('\n', '')
            views = int(views)
            #return views
            viewsNumber = views

    if viewsNumber == None:
        image = img.open(screenshot)
        pillow = image.transpose(img.FLIP_TOP_BOTTOM)
        pillow = pillow.crop((20, 0, 600, 200)) # (left, top, right, bottom)
        # pillow = pillow.crop((20, 0, 600, 150))
        pillow = pillow.transpose(img.FLIP_TOP_BOTTOM)
        # croppedImage = pillow.crop((340, 40, 400, 250)) 
        croppedImage = pillow.crop((340, 20, 400, 200)) 
        # check for views
        char = np.array(croppedImage)
        views = pt.image_to_string(char)

        if '\n' in views:
            views = views.replace('\n', '')
            views = int(views)
            #return views
            viewsNumber = views

    # check for ad if text
    if viewsNumber == None:
        ad = pt.image_to_string(image)
        views = ad[-3:]
        if '\n' in views:
            views = views.replace('\n', '')
            views = int(views)
            #return views
            viewsNumber = views

    return viewsNumber
# response = {'verified': match(screenshot),
#                 'views': detect(screenshot)}
# print(response)