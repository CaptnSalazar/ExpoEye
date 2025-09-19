from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image, ImageEnhance
import pytesseract, io, numpy as np, random, time
app = FastAPI(title='ExpoEye Vision Agent')

def enhance_image(img: Image.Image):
    if img.mode!='L': img=img.convert('L')
    img=ImageEnhance.Contrast(img).enhance(2.0)
    img.thumbnail((1200,1200))
    return img

def simple_scene(img: Image.Image):
    arr = np.array(img.convert('L'))
    mean = arr.mean()
    if mean<85: return ('screen',0.9)
    if img.size[0] > img.size[1]*1.5: return ('map',0.88)
    return (random.choice(['person','crowd','booth','signage']),0.65)

@app.post('/analyze')
async def analyze(file: UploadFile = File(...)):
    try:
        content = await file.read()
        img = Image.open(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400,detail='Invalid image')
    enhanced = enhance_image(img)
    try:
        ocr = pytesseract.image_to_string(enhanced, lang='eng')
    except Exception as e:
        ocr = f'[OCR-ERR] {e}'
    scene, conf = simple_scene(img)
    payload = {'mcp_version':'0.1','agent':'vision_agent','timestamp':time.time(),'payload':{'ocr_text':ocr,'scene':scene,'scene_confidence':conf,'image_size':img.size}}
    return JSONResponse(payload)
