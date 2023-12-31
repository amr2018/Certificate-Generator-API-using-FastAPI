
import cv2
from fastapi import FastAPI
from fastapi.responses import FileResponse
from uuid import uuid4

# create funtion to write user name on the certificate template
text_pos = (170, 290)

def write_text_on_image(text : str):
    # read the image
    img = cv2.imread('template.png')
    # write text on the image
    img = cv2.putText(
        img, text, text_pos, 
        fontFace=cv2.FONT_HERSHEY_COMPLEX,
        thickness = 2,
        fontScale=1,
        color = (0, 0, 0)
    )

    # save the image
    image_id = str(uuid4())
    cv2.imwrite(f'out/{image_id}.png', img)

    return image_id


# create the api
app = FastAPI()

# now we need a url for this certificate
@app.get('/certificate/{_id}')
def show_certificate(_id):
    return FileResponse(f'out/{_id}.png')

# we need to get the name from user to generate the certificate
@app.get('/user-name/{name}')
def get_name(name : str):
    c_id = write_text_on_image(f'This certificate is awarded to {name}')
    return {'c_id': f'http://127.0.0.1:8000/certificate/{c_id}'}
