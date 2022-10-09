from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# 创建一个蓝图
simple_page = Blueprint('simple_page', __name__, template_folder='templates')
# admin = Blueprint('admin', __name__, static_folder='static')
# 一个蓝图可以通过 static_folder 关键字参数提供一个指向文件系统上文件夹的路径，来暴露一个带有静态文件的文件夹。这可以是一个绝对路径，也可以是相对于蓝图文件夹的路径:
# 默认情况下，路径最右边的部分就是它在 web 上所暴露的地址。因为这里这个文件夹 叫做 static ，它会在 蓝图 + /static 的位置上可用。也就是说，蓝图为 /admin 把静态文件夹注册到 /admin/static 。
# 生成url：url_for('admin.static', filename='style.css')

# 像常规的应用一样，蓝图被设想为包含在一个文件夹中。当多个蓝图源于同一个文件 夹时，可以不必考虑上述情况，但也这通常不是推荐的做法。

@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)


# 从蓝图中获取当前的应用对象
from flask import current_app
@simple_page.route('/current_app')
def index():
    return render_template(current_app.config['INDEX_TEMPLATE'])