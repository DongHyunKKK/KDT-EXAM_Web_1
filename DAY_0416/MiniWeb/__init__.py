# 모듈 로딩
from flask import Flask, render_template

# 애플리케이션 팩토리 함수
def create_app():
    myapp = Flask(import_name = __name__)

    # bp 등록
    from .views import main_views
    myapp.register_blueprint(blueprint = main_views.bp)

    return myapp

# # 전역변수
# myapp = Flask(import_name = __name__)

# # 사용자 요청 URL 처리 기능 => 라우팅(Routing)
# # 형식 : @Flask_instance_name.route(URL 문자열)

# # 웹 서버의 첫 페이지 : http://127.0.0.1:5000/
# @myapp.route('/')
# def index_page():
#     #return "<h3><font color = 'red'>My Web Index Page</font></h3>"
#     return render_template('tem.html')
# # 사용자마다 페이지 반환
# # 사용자 페이지 URL: http://127.0.0.1:5000/<username>
# @myapp.route('/<name>')
# def username(name):
#     return f'username : {name}'

# @myapp.route('/name')  # '/name/'인 경우 주소창에 /를 생략해서 적어도 된다. 
# def hello():
#     return 'Name Name'

# @myapp.route('/<int:number>')
# def show_number(number):
#     return f'Select Number : {number}'

# @myapp.route('/user_info2')
# def user_login2():
#     return myapp.redirect('/')

# # 실행 제어
# if __name__ == '__main__':
#     # Flask 웹 서버 구동
#     myapp.run(debug = True)