# 기능 : main 범주의 url 라우팅
# URL : /main, /main, /main/info, /main/about, ...

from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix = '/')

@bp.route('/')
def main_about():
    return render_template('DH.html')


    

   
         
    