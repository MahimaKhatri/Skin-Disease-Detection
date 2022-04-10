import torch
from PIL import Image
import torchvision.transforms as T
import os
import argparse

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


if __name__ == "__main__":
    classes = ['acanthosis-nigricans',
                'acne',
                'acne-scars',
                'alopecia-areata',
                'dry',
                'melasma',
                'oily',
                'vitiligo',
                'warts']

    tr = get_transforms()
    # Parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--model', required=True, help="Faster RCNN Model Path")
    ap.add_argument('-i', '--image', required=True, help='Image Path')
    args = vars(ap.parse_args())

    model = torch.load(args['model'], map_location=torch.device('cpu'))

    # device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    device = torch.device('cpu')
    model.to(device);

    img = Image.open(args['image']).convert("RGB")

    res = predict(model, img, tr, classes)

    print("The model has predicted the class: "+str(res))
