# 기능 : main 범주의 url 라우팅
# URL : /main, /main, /main/info, /main/about, ...

from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix = '/main/')

@bp.route('about')
def main_about():
    return 'ABOUT MAIN'