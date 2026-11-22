from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.auth import auth_bp
from app.auth.forms import LoginForm
from app.models.admin_user import AdminUser


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField, SubmitField
    from wtforms.validators import DataRequired, Length

    # Solo se permite crear el primer admin; después el registro queda cerrado.
    if AdminUser.query.first() is not None:
        flash('El registro está cerrado: ya existe un administrador.', 'danger')
        return redirect(url_for('auth.login'))

    class RegisterForm(FlaskForm):
        username = StringField('Usuario', validators=[DataRequired(), Length(min=3)])
        password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
        submit = SubmitField('Crear Admin')

    form = RegisterForm()
    if form.validate_on_submit():
        existing = AdminUser.query.filter_by(username=form.username.data).first()
        if existing:
            flash('Ese usuario ya existe', 'danger')
        else:
            from app.extensions import db
            user = AdminUser(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Admin creado correctamente. Inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('admin/login.html', form=form, register_mode=True, can_register=True)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            # Evita redirecciones abiertas: solo rutas internas.
            if not next_page or not next_page.startswith('/') or next_page.startswith('//'):
                next_page = url_for('admin.dashboard')
            return redirect(next_page)
        flash('Usuario o contraseña incorrectos', 'danger')
    can_register = AdminUser.query.first() is None
    return render_template('admin/login.html', form=form, can_register=can_register)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))