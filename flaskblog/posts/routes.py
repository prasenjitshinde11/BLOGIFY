from flask import (render_template, url_for, flash,  
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post , Comment
from flaskblog.posts.forms import PostForm, commentForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new",methods=['GET', 'POST'])
@login_required
def new_post():
     form = PostForm()
     if form.validate_on_submit():
         post= Post(title=form.title.data, content=form.content.data, author=current_user)
         db.session.add(post)
         db.session.commit()
         flash('Your post has been created! ', 'success')
         return redirect(url_for('main.home'))
     return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>",methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = commentForm()
    
    if form.validate_on_submit():
        comment = Comment(body=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('post.html', title='New POst', post=post, form=form)


@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
        
    if form.validate_on_submit():
        post.title =  form.title.data
        post.content =  form.content.data
        db.session.commit()
        flash('Your post has been updated','succces')
        return redirect(url_for('posts.post', post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content 

    return render_template('create_post.html', title='update Post', form=form, legend='Update Post')


comments = {}

@posts.route("/post/<string:title>", methods=["GET", "POST"])
def post_detail(title):
    post = next((p for p in post if p['title'] == title), None)

    if title not in comments:
        comments[title] = []

    if request.method == "POST":
        comment = request.form.get("comment")
        if comment:
            comments[title].append(comment)

    return render_template(
        "post.html",
        post=post,
        comments=comments[title]
    )


@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))
