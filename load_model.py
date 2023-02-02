import torch

device = "cuda:2"
weights_yolov5 = "model/yolov5/best_old.pt"
imgsz = 640
img_size = 640

class load_model():
    #yolov5
    yolov5 = torch.hub.load('module/yolov5', 'custom', path=weights_yolov5, source='local', device=device)  # local repo