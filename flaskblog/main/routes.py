from flask import Blueprint, render_template
from flask_login import current_user
from flaskblog.models import Post, User, Comment
from flaskblog.users.forms import DeleteForm
from flaskblog.utils import get_page

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # Show welcome landing page for visitors who aren't logged in
    if not current_user.is_authenticated:
        total_users = User.query.count()
        total_posts = Post.query.count()
        total_comments = Comment.query.count()
        return render_template('welcome.html',
                               total_users=total_users,
                               total_posts=total_posts,
                               total_comments=total_comments)

    # Logged-in users see the regular post feed
    page = get_page()
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    form = DeleteForm()
    return render_template('home.html', posts=post, form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')