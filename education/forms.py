from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from modelsArticle import Article

class ArticleForm(FlaskForm):
    article = Article()
    title = StringField(validators=[DataRequired(),Length(1,64)])
    author = StringField(validators=None)
    tag = SelectField(choices=article.tags)
    flag = SelectField(choices=article.flags)
    txt_markdown = TextAreaField() # markdown编辑器
    submit = SubmitField()

    def object_to_form(self,article):
        self.title.data = article.title
        self.author.data = article.author
        self.tag.data = article.tag
        self.flag.data = article.flag
        self.txt_markdown.data = article.txt_markdown
    
    def get_title_label(self):
        return 'TITLE:'
    def get_author_label(self):
        return 'AUTHOR:'
    def get_tag_label(self):
        return 'TAG:'
    def get_flag_label(self):
        return 'FLAG:'
    def get_txt_markdown_label(self):
        return 'MARKDOWN'
    def get_submit_label(self):
        return 'SUBMIT'


class LoginForm(FlaskForm):
    account = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField()

    def get_account_label(self):
        # 重构flask_wtf中的属性函数，原属性函数的label包含<>html标记，现直接返回字符串
        return 'ACCOUNT:'

    def get_password_label(self):
        return 'PASSWORD:'

    def get_remember_me_label(self):
        return 'renmember me?'

    def get_submit_label(self):
        return 'LOGIN'

class SearchForm(FlaskForm):
    key_word = StringField(validators=[DataRequired()])
    submit = SubmitField()

    def get_submit_label(self):
        return 'SEARCH'

class AddAdminForm(FlaskForm):
    account = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    password_verify = PasswordField(validators=[DataRequired(), EqualTo('password')])
    phone = StringField(validators=[Length(11)])
    email = StringField(validators=[Email()])
    info = StringField(validators=None)
    submit = SubmitField()

    def get_account_label(self):
        return 'ACCOUNT'

    def get_password_label(self):
        return 'PASSWORD'

    def get_password_verify_label(self):
        return 'REPEAT PASSWORD'

    def get_phone_label(self):
        return 'PHONE'

    def get_email_label(self):
        return 'EMAIL'

    def get_info_label(self):
        return 'INFO'

    def get_submit_label(self):
        return 'ADD ADMIN'

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired()])
    new_password_verify = PasswordField(validators=[DataRequired()])
    submit = SubmitField()

    def get_old_password_label(self):
        return 'OLD PASSWORD'
    
    def get_new_password_label(self):
        return 'NEW PASSWORD'

    def get_new_password_verify_label(self):
        return 'REPEAT PASSWORD'

    def get_submit_label(self):
        return 'UPDATE'

class ChangePhoneForm(FlaskForm):
    new_phone = StringField(validators=[DataRequired(), Length(11)])
    submit = SubmitField()

    def get_new_phone_label(self):
        return 'NEW PHONE'

    def get_submit_label(self):
        return 'UPDATE'
    
class ChangeEmailForm(FlaskForm):
    new_email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField()

    def get_new_email_label(self):
        return 'NEW EMAIL'

    def get_submit_label(self):
        return 'UPDATE'
    
class ChangeInfoForm(FlaskForm):
    new_info = StringField(validators=[DataRequired()])
    submit = SubmitField()

    def get_new_info_label(self):
        return 'NEW INFO'

    def get_submit_label(self):
        return 'UPDATE'