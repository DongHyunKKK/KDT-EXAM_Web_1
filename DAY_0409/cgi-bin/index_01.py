# 모듈 로딩
import cgi

# web 인코딩 설정
# import sys, codecs
# sys.stdout = codecs.getwriter(encoding = 'utf-8')(sys.stdout.detach())

# web 브라우저 화면 출력 코드
def print_browser(result = ''):
    # HTML 파일 읽기 -> body 문자열
    file_name = './html/test.html'
    with open(file_name, mode = 'r', encoding = 'utf-8') as f:
        web_string = f.read()
        # HTML Header
        print('Content-Type : text/html; charset = utf-8;')  # charset는 한글 깨지면 필요 
        print()
        # HTML Body
        print(web_string.format(result))


# client 요청 데이터 즉, form 데이터 저장 인스턴스
form = cgi.FieldStorage()

# 데이터 추출
if 'data' in form:
    result = form.getvalue(key = 'data')
else:
    result = 'No Data'

print_browser(result)