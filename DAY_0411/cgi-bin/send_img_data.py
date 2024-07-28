# 모듈 로딩
import cgi, cgitb, sys, codecs, datetime

cgitb.enable()

# WEB 인코딩 설정
sys.stdout = codecs. getwriter(encoding = 'utf-8')(sys.stdout.detach())

# 웹 페이지의 form 태그 내의 input 태그 입력값 가져와서 저장하고 있는 인스턴스
form = cgi.FieldStorage()

# 클라이언트의 요청 데이터 추출
if 'img_file' in form and 'message' in form:
    fileitem = form['img_file']  # form.getvalue(key = 'img_file')
    
    # 서버에 이미지 파일 저장
    # ext = '.' + fileitem.filename.rsplit('.')[-1]
    img_file = fileitem.filename

    suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
    
    save_path = f'./image/{suffix}_{img_file}'
    with open(save_path, mode = 'wb') as f:
        f.write(fileitem.file.read())

    img_path = f'../image/{suffix}_{img_file}'
    msg = form.getvalue('message')
else:
    img_path = 'None'
    msg = 'None'

# 요청에 대한 응답 HTML
print('Content-Type : text/html; charset = utf-8')  # HTML is following
print()  # 무조건 한줄 띄어야 함
print('<TITLE>CGI script output</TITLE>')
print('<h1>This is my fisrt CGI script</h1>')
print(f'Hello, world!')
print(f'<img src={img_path}>')
print(f'<h3>{img_path}</h3>')
print(f'<h3>{msg}</h3>')