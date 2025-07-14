from datetime import datetime
from functools import wraps


from flask_login import login_user, current_user, logout_user, login_required

from forms import SignupForm, LoginForm, AdForm, CourseForm
from extensions import app,db
from models import User,Ad,Course,FavoriteAd,FavoriteCourse
from flask import render_template, redirect, url_for, flash, request, abort

import time
from werkzeug.utils import secure_filename
import os

@app.route('/')
def home():
    return render_template('home.html')
admin_emails = ["elene.example@example.com", "nika.example@example.com"]


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.email == form.email.data) | (User.username == form.username.data)
        ).first()
        if existing_user:
            flash(" ელ.ფოსტა ან მომხმარებლის სახელი უკვე დარეგისტრირებულია. გთხოვთ გაიაროთ ავტორიზაცია.", "warning")
            return redirect(url_for('login'))


        role = 'admin' if form.email.data in admin_emails else 'guest'

        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            birthday=form.birthday.data,
            gender=form.gender.data,
            country=form.country.data,
            role=role
        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("რეგისტარცია წარმატებულია! გთხოვთ გაიაროთ ავტორიზაცია.", "success")
        return redirect(url_for('login'))

    if form.errors:
        flash(f"Form errors: {form.errors}", "danger")

    return render_template("signup.html", form=form)






@app.route('/login' , methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)

            if user.email in admin_emails and user.role != 'admin':
                user.role = 'admin'
                db.session.commit()
            flash(f"მოგესალმებით, {user.username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("არასწორი ელ.ფოსტა ან პაროლი.", "danger")

    if form.errors:
        flash(f"Form errors: {form.errors}", "danger")

    return render_template("login.html", form=form)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function






@app.route('/logout')
def logout():
    logout_user()
    flash("თქვენ აქაუნთი დატოვეთ.", "info")
    return redirect(url_for('home'))

@app.route('/ads')
def ads():

    ads_list = Ad.query.order_by(Ad.date_posted.desc()).all()
    if current_user.is_authenticated:
        user_fav_ad_ids = [f.ad_id for f in FavoriteAd.query.filter_by(user_id=current_user.id).all()]
    else:
        user_fav_ad_ids = []
    return render_template('ads.html', ads=ads_list,user_fav_ad_ids=user_fav_ad_ids)
@app.route('/ads/new', methods=['GET','POST'])
@login_required
def new_ad():
    form = AdForm()
    if form.validate_on_submit():
        ad = Ad(title=form.title.data,
                description=form.description.data,
                contact_info=form.contact_info.data,
                author=current_user)
        db.session.add(ad)
        db.session.commit()
        flash('თქვენი განცხადება აიტვირთა', 'success')
        return redirect(url_for('ads'))
    return render_template('create_ad.html', form=form)
@app.route('/ads/delete/<int:ad_id>',methods=['POST'])
@login_required
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.author != current_user and current_user.role != 'admin':
        abort(403)
    db.session.delete(ad)
    db.session.commit()
    flash('თქვენი განცხადება წაიშალა.', 'info')
    return redirect(url_for('ads'))
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin/page')
@login_required
@admin_required
def admin_page():
    users = User.query.all()
    return render_template('admin_page.html', users=users, admin_emails=admin_emails)


@app.route('/admin/promote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash(f"{user.username} უკვე ადმინია.", "info")
    else:
        user.role = 'admin'
        db.session.commit()
        flash(f"{user.username} გახდეს ადმინი.", "success")

    return redirect(url_for('admin_page'))
@app.route('/admin/demote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def demote_user(user_id):
    user = User.query.get_or_404(user_id)


    if user.email in admin_emails:
        flash("თქვენ არ შეგიძლიათ მენეჯერის დაქვეითება.", "danger")
        return redirect(url_for('admin_page'))


    if current_user.email not in admin_emails:
        flash("მხოლოდ მენეჯერს შეუძლია ადმინის დაქვეითება.", "danger")
        return redirect(url_for('admin_page'))

    if user.role == 'admin':
        user.role = 'guest'
        db.session.commit()
        flash(f"{user.username} დაბრუნდა როგორც მომხმარებელი.", "warning")
    else:
        flash(f"{user.username} არ არის ადმინი.", "info")

    return redirect(url_for('admin_page'))
@app.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)


    if user.role == 'admin':
        flash("ადმინის წაშლა არ შეგიძლიათ.", "danger")
        return redirect(url_for('admin_page'))

    db.session.delete(user)
    db.session.commit()
    flash(f"{user.username} deleted.", "success")

    return redirect(url_for('admin_page'))


@app.route('/courses')
def courses():
    courses = Course.query.all()
    if current_user.is_authenticated:
        user_fav_course_ids = [f.course_id for f in FavoriteCourse.query.filter_by(user_id=current_user.id).all()]
    else:
        user_fav_course_ids = []

    return render_template('courses.html', courses=courses,user_fav_course_ids=user_fav_course_ids)




@app.route('/courses/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_course():
    form = CourseForm()

    if form.validate_on_submit():
        image = form.image_file.data

        if image and image.filename:
            filename = secure_filename(image.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            image_path = os.path.join(app.root_path, 'static/course_images', unique_filename)
            image.save(image_path)
        else:
            unique_filename = 'default.jpg'


        course = Course(
            title=form.title.data,
            description=form.description.data,

            image_file=unique_filename
        )

        db.session.add(course)
        db.session.commit()

        flash('ახალი კურსი დაემატა წარმატებით!', 'success')
        return redirect(url_for('courses'))

    return render_template('add_course.html', form=form)

@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)


    return render_template('course_detail.html', course=course)

@app.route('/courses/delete/<int:course_id>',methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if  current_user.role != 'admin':
        abort(403)
    db.session.delete(course)
    db.session.commit()
    flash('თქვენი კურსი წაიშალა.', 'info')
    return redirect(url_for('courses'))

@app.route('/favorite_course/<int:course_id>', methods=['POST'])
@login_required
def favorite_course(course_id):
    existing = FavoriteCourse.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if existing:
        db.session.delete(existing)
    else:
        fav = FavoriteCourse(user_id=current_user.id, course_id=course_id)
        db.session.add(fav)
    db.session.commit()
    return redirect(url_for('courses'))
@app.route('/favorite_ad/<int:ad_id>', methods=['POST'])
@login_required
def favorite_ad( ad_id):
    existing = FavoriteAd.query.filter_by(user_id=current_user.id, ad_id=ad_id).first()
    if existing:
        db.session.delete(existing)
    else:
        fav = FavoriteAd(user_id=current_user.id, ad_id=ad_id)
        db.session.add(fav)
    db.session.commit()
    return redirect( url_for('ads'))
