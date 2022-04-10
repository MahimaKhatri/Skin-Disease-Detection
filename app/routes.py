from flask import Flask, request, Response
from flask.templating import render_template
from flask import request
from werkzeug.utils import secure_filename
from app import app
import torch
from PIL import Image
import torchvision.transforms as T
import os

def predict(model, img, tr, classes):
    img_tensor = tr(img)
    out = model(img_tensor.unsqueeze(0))
    pred, idx = torch.max(out, 1)
    return classes[idx]

def get_transforms():
    transform = []
    transform.append(T.Resize((512, 512)))
    transform.append(T.ToTensor())
    return T.Compose(transform)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    res = None
    if request.method == 'POST':
        classes = ['acanthosis-nigricans',
                'acne',
                'acne-scars',
                'alopecia-areata',
                'dry',
                'melasma',
                'oily',
                'vitiligo',
                'warts']
        f = request.files['file']
        filename = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_PATH'], filename)
        f.save(path)
        model = torch.load('./skin-model-pokemon.pt', map_location=torch.device('cpu'))
        device = torch.device('cpu')
        model.to(device);
        img = Image.open(path).convert("RGB")
        tr = get_transforms()
        res = predict(model, img, tr, classes)

    return render_template("index.html", res=res)
