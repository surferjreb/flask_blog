from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select, update
import datetime
from app import app, db
from app.forms import BlogForm, LoginForm, UserForm, CommentForm
from app.models import User, BlogPost, Comment, admin_only


@app.route('/')
def home():
    '''Returns all DB entries and orders by date'''
    posts = []
    results = db.session.scalars(select(BlogPost)).all()
    posts = sorted(results, key=lambda x: x.date)
    return render_template('index.html', all_posts=posts)

@app.route('/<post_id>', methods=["GET", "POST"])
def show_post(post_id):
    '''Returns post entry by id'''
    form = CommentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            dt = datetime.datetime.now()
            comment = form.comment.data
            new_comment = Comment(c_author = current_user,
                                  body = comment,
                                  post_id = post_id,
                                  date = dt.strftime('%B %d, %Y'))
            db.session.add(new_comment)
            db.session.commit()

            return redirect(url_for('show_post', post_id=post_id))

    # results = db.session.scalars(select(Comment)).all()

    # comments = sorted(results, key=lambda x: x.date)
    requested_post = db.session.get(BlogPost, post_id)
    
    if requested_post:
        return render_template("post.html", post=requested_post, form=form,
                               comments=requested_post.blog_comments)
    else:
        return redirect("/")

@admin_only
@app.route("/add", methods=["GET", "POST"])
def add_post():
    form = BlogForm()
    if request.method == "POST":
        dt = datetime.datetime.now()
        new_post = BlogPost(title=f'{form.title.data}',
                            subtitle=f'{form.subtitle.data}',
                            date = dt.strftime('%B %d, %Y'),
                            body=f'{form.body.data}',
                            author=current_user,
                            img_url=f'{form.img_url.data}')
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))


    return render_template('make-post.html', form=form)

@admin_only
@app.route("/<post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.session.get(BlogPost, post_id)

    if post:
        form = BlogForm(obj=post)
        if request.method == "POST":
            # dt = datetime.datetime.now()
            db.session.execute(update(BlogPost)
                               .where(BlogPost.id == post.id)
                               .values(title=f'{form.title.data}',
                                       subtitle=f'{form.subtitle.data}',
                                       date=f'{post.date}',
                                       body=f'{form.body.data}',
                                       img_url=f'{form.img_url.data}'))
            db.session.commit()
            return redirect(f'/{post.id}')
        else:
            return render_template('edit-post.html', form=form, post=post)
    else:
        return redirect('/')
    
@admin_only
@app.route("/<post_id>/edit/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.session.get(BlogPost, post_id)

    if post:
        if request.method == "POST":
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('home'))
        flash('You are about to delete this post!')
        return render_template('delete.html', post=post)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = UserForm()

    if request.method == "POST":
        new_user = User(name = f"{form.name.data}",
                        email = f"{form.email.data}",
                        password = generate_password_hash(
                            f"{form.password.data}",
                            method='pbkdf2:sha256',
                            salt_length=8))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful', 'info')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        email = f"{form.email.data}"
        password = f"{form.password.data}"

        results = db.session.execute(db.select(User).where(User.email == email))
        user = results.scalar()

        if user == None:
            flash('Email is not registered, please check information')
            return redirect(url_for('login'))

        if check_password_hash(user.password, password):
            login_user(user)
            flash('Login Successful')
            return redirect(url_for('home'))
        else:
            flash('Password incorrect, check entered information'\
                ' and try again')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')