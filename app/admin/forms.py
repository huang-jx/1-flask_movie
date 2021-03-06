from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

from app.models import Admin


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label='账号',
        validators=[
            DataRequired()
        ],
        description='账号',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号！'
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired()
        ],
        description='密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码！'
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            'class': 'btn btn-primary btn-block btn-flat'
        }
    )
    accept_tos = BooleanField(
        label='I accept the TOS',
        validators=[
            DataRequired()
        ]
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在！')


class TagForm(FlaskForm):
    name = StringField(
        label='标签名称',

        description='标签',
        validators=[
            DataRequired()
        ],
        render_kw={
            'class': 'form-control',
            'id': 'input_name',
            'placeholder': '请输入标签名称!',
        }
    )
    submit = SubmitField(
        label='添加',
        render_kw={
            'class': 'btn btn-primary'
        }
    )
