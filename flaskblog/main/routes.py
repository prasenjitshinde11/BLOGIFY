from flask import Blueprint
from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flaskblog.users.forms import DeleteForm

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home(): 
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    form =  DeleteForm()
    return render_template('home.html', posts=post, form=form)

@main.route("/about")
def about():
    return render_template('about.html', title='About')