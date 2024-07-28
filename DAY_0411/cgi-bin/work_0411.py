import cgi, cgitb, sys, codecs, datetime
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights

cgitb.enable()

# WEB 인코딩 설정
sys.stdout = codecs. getwriter(encoding = 'utf-8')(sys.stdout.detach())

# 사전학습된 모델 인스턴스 생성
res_model = resnet18(weights = ResNet18_Weights.DEFAULT)

# 전결합층 변경
# in feature : FeatureMap에서 받은 피처 수, out_featrues : 출력/분류 클래스 수
res_model.fc = nn.Sequential(nn.Linear(512, 256),
              nn.BatchNorm1d(num_features = 256),
              nn.ReLU(),
              nn.Dropout(),
              nn.Linear(256, 128),
              nn.BatchNorm1d(num_features = 128),
              nn.ReLU(),
              nn.Dropout(),
              nn.Linear(128, 64),
              nn.BatchNorm1d(num_features = 64),
              nn.ReLU(),
              nn.Dropout(),
              nn.Linear(64, 32),
              nn.BatchNorm1d(num_features = 32),
              nn.Linear(32, 23))

# 모델 불러오기
res_model = torch.load('./Models/My_ResNet18.pt')

# 예측 함수
def predict(data):
    
    with torch.no_grad():
        output = res_model(data)
    prediction = output.max(1, keepdim = True)[1]
        
    return prediction

# client 요청 데이터 즉, form 데이터 저장 인스턴스
form = cgi.FieldStorage()

preprocessing = transforms.Compose([transforms.Resize(size = (64, 64)),
                                     transforms.ToTensor(),
                                     transforms.Normalize(mean = (0.485, 0.456, 0.406), std = (0.229, 0.224, 0.225))])

# 클라이언트의 요청 데이터 추출
if 'img_file' in form and 'message' in form:
    
    fileitem = form['img_file']  # form.getvalue(key = 'img_file')
    if fileitem is not None:
    # 서버에 이미지 파일 저장
    # ext = '.' + fileitem.filename.rsplit('.')[-1]
        img_file = fileitem.filename
    
        suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S')

        save_path = f'./image/{suffix}_{img_file}'
        with open(save_path, mode = 'wb') as f:
            f.write(fileitem.file.read())

        img_path = f'./image/{suffix}_{img_file}'
        #msg = form.getvalue('message')
    else:
        img_path = None
        msg = None
else:
    img_path = None
    msg = None

if img_path is not None:
    data = Image.open(img_path)
    data = preprocessing(data)
    data = data.unsqueeze(0)
    prediction = predict(data)
    tdata_path = './DATA/artist_train.csv'
    train_infoDF = pd.read_csv(tdata_path, header = None)
    train_infoDF = pd.concat([train_infoDF[0].str.split('/', expand = True), train_infoDF[1]], axis = 1)
    train_infoDF.columns = ['style', 'file name', 'class']
    df = train_infoDF[train_infoDF['class'] == prediction.item()]
    result = f"모델이 예측한 화가는 {df['file name'].str.split('_').iloc[0][0]}입니다.\n"
else:
    result = '결과 없음'

# Web 브라우저 화면 출력 코드
file_path = 'my_img_input.html'

def print_browser(file_path, pred = ''):
    # HTML 파일 읽기 => body 문자열
    with open(file_path, 'r', encoding = 'utf-8') as f:
        web_string = f.read()
        # HTML Header
        print('Content-Type : text/html; charset = utf-8')
        print()  # 무조건 한줄 띄어야 함
        
        # HTML Body
        print(web_string.format(pred))

# def print_browser(img_path):
#     # HTML 파일 읽기 => body 문자열
#     # HTML Header
#     print('Content-Type : text/html; charset = utf-8')
#     print()  # 무조건 한줄 띄어야 함
#     print('<TITLE>CGI script output</TITLE>')
#     print('<h1>This is my fisrt CGI script</h1>')
#     print(f'Hello, world!')
#     print(f'<img src={img_path}>')
#     print(f'<h3>{img_path}</h3>')
#     print(f'<h3>{msg}</h3>')

# 브라우징 : 함수 실행
print_browser(file_path, pred = result)