"""vision_agent.py
FastAPI Vision Agent: accepts image upload, returns MCP-style JSON with OCR and scene classification.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from PIL import Image, ImageEnhance
import pytesseract
import io
import numpy as np
import random
import time

app = FastAPI(title='ExpoEye Vision Agent')

def enhance_image_for_ocr(img: Image.Image) -> Image.Image:
    if img.mode != 'L':
        img = img.convert('L')
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    img.thumbnail((1200, 1200))
    return img

def simple_scene_classify(img: Image.Image) -> Dict[str, Any]:
    arr = np.array(img.convert('L'))
    mean = arr.mean()
    if mean < 80:
        return {'scene': 'screen', 'confidence': 0.9}
    if img.size[0] > img.size[1] * 1.5:
        return {'scene': 'map', 'confidence': 0.85}
    return {'scene': random.choice(['person','crowd','booth','signage']), 'confidence': 0.65}

@app.post('/analyze')
async def analyze_image(file: UploadFile = File(...)):
    try:
        content = await file.read()
        img = Image.open(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid image')

    enhanced = enhance_image_for_ocr(img)
    try:
        ocr_text = pytesseract.image_to_string(enhanced, lang='eng')
    except Exception as e:
        ocr_text = f'[OCR ERROR] {e}'

    scene = simple_scene_classify(img)
    payload = {
        'mcp_version': '0.1',
        'agent': 'vision_agent',
        'timestamp': time.time(),
        'payload': {
            'ocr_text': ocr_text,
            'scene': scene['scene'],
            'scene_confidence': scene['confidence'],
            'image_size': img.size,
            'file_name': getattr(file, 'filename', 'upload.jpg')
        }
    }
    return JSONResponse(content=payload)

if __name__ == '__main__':
    import uvicorn, os
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('VISION_AGENT_PORT', 8101)))
