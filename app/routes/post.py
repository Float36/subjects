from flask import Blueprint, render_template, request, redirect, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from ..extensions import db
from ..forms import StudentForm, TeacherForm
from ..models.post import Post
from ..models.user import User

post = Blueprint('post', __name__)

@post.route('/', methods=['POST', 'GET'])
def all():
    form = TeacherForm()
    form.teacher.choices = [t.name for t in User.query.filter_by(status='teacher')]

    if request.method == "POST":
        teacher = request.form.get('teacher')
        teacher_id = User.query.filter_by(name=teacher).first().id
        posts = Post.query.filter_by(teacher=teacher_id).order_by(Post.date.desc()).all()
    else:
        posts = Post.query.order_by(Post.date.desc()).limit(20).all()
    return render_template('post/all.html', posts=posts, user=User, form=form)

@post.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():
    form = StudentForm()
    form.student.choices = [s.name for s in User.query.filter_by(status='user')]
    if request.method == 'POST':
        subject = request.form.get('subject')
        student = request.form.get('student')
        student_id = User.query.filter_by(name=student).first().id

        post = Post(teacher=current_user.id, subject=subject, student=student_id)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
    else:
        return render_template('post/create.html', form=form)


@post.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    post = Post.query.get(id)

    if post.author.id == current_user.id:
        form = StudentForm()
        form.student.data = User.query.filter_by(id=post.student).first().name
        form.student.choices = [s.name for s in User.query.filter_by(status='user')]
        if request.method == 'POST':
            post.subject = request.form.get('subject')
            student = request.form.get('student')

            post.student = User.query.filter_by(name=student).first().id

            try:
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(str(e))
        else:
            return render_template('post/update.html', post=post, form=form)
    else:
        abort(403)


@post.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    post = Post.query.get(id)
    if post.author.id == current_user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return str(e)
    else:
        abort(403)

