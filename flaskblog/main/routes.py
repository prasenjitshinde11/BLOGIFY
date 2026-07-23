from flask import Blueprint
from flask import render_template, request, Blueprint
from flask_login import current_user
from flaskblog.models import Post, User, Comment
from flaskblog.users.forms import DeleteForm

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
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    form = DeleteForm()
    return render_template('home.html', posts=post, form=form)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/search")
def search():
    query = request.args.get('q', '').strip()
    page  = request.args.get('page', 1, type=int)
    if query:
        results = Post.query.filter(
            (Post.title.ilike(f'%{query}%')) | (Post.content.ilike(f'%{query}%'))
        ).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    else:
        results = None
    form = DeleteForm()
    return render_template('search.html', title='Search', query=query, results=results, form=form)