# 모듈 로딩
import cgi, cgitb
import torch
import pickle
import torch.nn as nn
from konlpy.tag import Mecab

# web 인코딩 설정
import sys, codecs
sys.stdout = codecs.getwriter(encoding = 'utf-8')(sys.stdout.detach())

# Error 확인
cgitb.enable()  

# Web 브라우저 화면 출력 코드
file_path = './html/test2.html'

def print_browser(file_path, pred = ''):
    # HTML 파일 읽기 => body 문자열
    with open(file_path, 'r', encoding = 'utf-8') as f:
        web_string = f.read()
        # HTML Header
        print('Content-Type : text/html; charset = utf-8')
        print()  # 무조건 한줄 띄어야 함
        
        # HTML Body
        print(web_string.format(pred))

# 모델 클래스 정의
class TextModel(nn.Module):
    
    def __init__(self, VOCAB_SIZE, EMBEDD_DIM, HIDDEN_SIZE, NUM_CLASS):
        super().__init__()
        # 모델 구성 층 정의
        self.embedding = nn.EmbeddingBag(VOCAB_SIZE, EMBEDD_DIM, sparse = False)
        self.rnn = nn.GRU(EMBEDD_DIM, HIDDEN_SIZE, batch_first = True, bidirectional = True)
        self.fc = nn.Linear(2*HIDDEN_SIZE, NUM_CLASS)
        self.init_weights()
        self.dropout = nn.Dropout()
    
    # 가중치 초기화
    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc.weight.data.uniform_(-initrange, initrange)
        self.fc.bias.data.zero_()
        for name, parameter in self.rnn.named_parameters():
            if 'weight' in name:
                nn.init.orthogonal_(parameter)
            elif 'bias' in name:
                nn.init.constant_(parameter, 0.01)

    # 순방향 학습 진행
    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        output, _ = self.rnn(embedded)

        return self.fc(output)
    
# 어휘사전 생성
def load_vocab(file_path):
    with open(file_path, 'rb') as f:  
        vocab = pickle.load(f)
    return vocab

vocab = load_vocab('./Vocabs/vocab_Jeolla.pkl')

# 모델 불러오기
my_model = torch.load('./Models/GRU_model1_Jeolla.pt')
mecab = Mecab()
def predict(model, text):
    text_pipeline = lambda x: vocab(x)
    with torch.no_grad():
        text = torch.tensor(text_pipeline(mecab.morphs(text)), dtype = torch.int64)
        offsets = torch.tensor([0])
        output = model(text, offsets)
        sigmoid = nn.Sigmoid()
        pred = sigmoid(output).item() 
        if pred >= 0.5: 
            result = '표준말'
        else:
            result = '전라도 사투리'
    return result

# client 요청 데이터 즉, form 데이터 저장 인스턴스
form = cgi.FieldStorage()

# 데이터 추출 / 예측 함수 실행
if 'text' in form:
    text = form.getvalue('text')
    result = predict(my_model, text)
else:
    result = "No Data"

# 브라우징 : 함수 실행
print_browser(file_path, pred = result)