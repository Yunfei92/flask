from flask import Flask,render_template,redirect,request,url_for,flash,Blueprint,g
from flask_login import login_user,logout_user,login_required,current_user

from start import login_manager
from modelsAdmin import Admin
from modelsArticle import Article
from modelsSPEA import WebsiteInfo,UpdateInfo,IndexImax,NoticeBoard
from forms import ArticleForm,LoginForm,SearchForm,AddAdminForm,ChangePasswordForm,ChangePhoneForm,ChangeEmailForm,ChangeInfoForm

views_blueprint = Blueprint('views_blueprint', __name__)

def new_render_template(template_name_or_list, **context):
    # 重写渲染函数，在新函数中做传递search_form参数和提交判定
    search_form = SearchForm()
    notice_board = NoticeBoard()
    notice_board.get_notice_board()
    if search_form.validate_on_submit():
        return redirect(url_for('views_blueprint.search_by_key_word', key_word=search_form.key_word.data))
    return render_template(template_name_or_list, **context, search_form=search_form, notice_board=notice_board)

@views_blueprint.route('/', methods=['GET','POST'])
def index():
    article = Article()
    article_notice_list = article.search_by_tag('NOTICE')
    print(article_notice_list)
    article_show_list = article.search_by_tag('SHOW')
    print(article_show_list)
    article_exp_list = article.search_by_tag('EXP')
    print(article_exp_list)
    index_imax = IndexImax()
    index_imax.get_index_imax()
    return new_render_template('index.html', article_notice_list=article_notice_list, article_show_list=article_show_list, article_exp_list=article_exp_list, index_imax=index_imax, page_title='INDEX')

@views_blueprint.app_errorhandler(404)
def page_not_found(e):
    return new_render_template('404.html', page_title='404_page_not_found'),404

@views_blueprint.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        admin = Admin()
        if admin.verify_login(login_form):
            login_user(admin, login_form.remember_me.data)
            flash('ADMIN LOGIN SUCCESS!')
            return redirect(request.args.get('next') or url_for('views_blueprint.index'))
        else:
            flash('ADMIN LOGIN FAIL! PLEASE CHECK YOUR ACCOUNT AND PASSWORD!')
    return new_render_template('login.html', form=login_form, page_title='ADMIN LOGIN')

@views_blueprint.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('ADMIN LOGOUT!')
    return redirect(url_for('views_blueprint.index'))

@views_blueprint.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    admin = current_user
    admin_list = admin.search_all()
    add_admin_form = AddAdminForm()
    change_password_form = ChangePasswordForm()
    change_phone_form = ChangePhoneForm()
    change_email_form = ChangeEmailForm()
    change_info_form = ChangeInfoForm()
    if add_admin_form.validate_on_submit():
        admin.add_new_admin(add_admin_form)
        flash('ADD ADMIN SUCCESS!')
        return redirect(url_for('views_blueprint.admin'))
    if change_password_form.validate_on_submit():
        admin.change_password(change_password_form)
        flash('CHANGE PASSWORD SUCCESS!')
        return redirect(url_for('views_blueprint.admin'))
    if change_phone_form.validate_on_submit():
        admin.change_phone(change_phone_form)
        flash('CHANGE PHONE SUCCESS!')
        return redirect(url_for('views_blueprint.admin'))
    if change_email_form.validate_on_submit():
        admin.change_email(change_email_form)
        flash('CHANGE EMIAL SUCCESS!')
        return redirect(url_for('views_blueprint.admin'))
    if change_info_form.validate_on_submit():
        admin.change_info(change_info_form)
        flash('CHANGE INFO SUCCESS!')
        return redirect(url_for('views_blueprint.admin'))
    return new_render_template('admin.html', admin_list=admin_list, change_password_form=change_password_form, change_phone_form=change_phone_form, change_email_form=change_email_form, change_info_form=change_info_form, add_admin_form=add_admin_form, page_title='ADMIN')

@views_blueprint.route('/admin/article_list/<admin_id>', methods=['GET','POST'])
@login_required
def get_article_list_by_admin_id(admin_id):
    admin = Admin()
    print("333333333333333333")
    admin.get_admin_object(admin_id)
    print('222222222222222222')
    print(admin.id)
    article = Article()
    article_list = article.search_by_admin_id(admin.id)
    return new_render_template('article_list.html', article_list=article_list, page_title=admin.get_account())

@views_blueprint.route('/new_article',methods=['GET','POST'])
@login_required
def new_article():
    article_form = ArticleForm()
    if article_form.validate_on_submit():
        article = Article()
        article.form_to_object(article_form)
        article.new_article(current_user.id)
        flash('文章提交成功')
        return redirect(url_for('views_blueprint.get_article_by_id',article_id=article.id))
    return new_render_template('edit_article.html', form=article_form, page_title='NEW ARTICLE')

@views_blueprint.route('/edit_article/<article_id>',methods=['GET','POST'])
@login_required
def edit_article(article_id):
    article = Article()
    article.search_by_id(article_id)
    article_form = ArticleForm()
    if article_form.validate_on_submit():
        article.form_to_object(article_form)
        article.update_article()
        flash('文章更新成功')
        return redirect(url_for('views_blueprint.get_article_by_id',article_id=article.id))
    article_form.object_to_form(article) # ??此行语句位置对功能实现有重大影响
    return new_render_template('edit_article.html', form=article_form, page_title='EDIT ARTICLE')

@views_blueprint.route('/delete_article/<article_id>',methods=['GET','POST'])
@login_required
def delete_article(article_id):
    article = Article()
    article.search_by_id(article_id)
    message = article.delete_article()
    flash(message)
    return redirect(url_for('views_blueprint.show_article_list'))

@views_blueprint.route('/show_article_list', methods=['GET','POST'])
@login_required
def show_article_list():
    article = Article()
    article_list = article.search_all()
    return new_render_template('article_list.html', article_list=article_list, page_title='ARTICLE LIST')

@views_blueprint.route('/article/website_info', methods=['GET','POST'])
def website_info():
    website_info = WebsiteInfo()
    website_info.get_website_info()
    return new_render_template('article.html', article=website_info)

@views_blueprint.route('/article/update_info', methods=['GET','POST'])
def update_info():
    update_info = UpdateInfo()
    update_info.get_update_info()
    return new_render_template('article.html', article=update_info)

@views_blueprint.route('/article/<article_id>', methods=['GET','POST'])
def get_article_by_id(article_id):
    article = Article()
    article.search_by_id(article_id)
    return new_render_template('article.html', article=article)

@views_blueprint.route('/article_list/<article_tag>', methods=['GET','POST'])
def get_article_list_by_tag(article_tag):
    article = Article()
    article_list = article.search_by_tag(article_tag)
    return new_render_template('article_list.html', article_list=article_list, page_title=article_tag)

@views_blueprint.route('/search/<key_word>', methods=['GET','POST'])
def search_by_key_word(key_word):
    article = Article()
    article_list = article.search_by_key_word(key_word)
    return new_render_template('article_list.html', article_list=article_list, page_title='SEARCH：'+key_word)

@views_blueprint.route('/article/set_spea/<article_id>/<spea_name>', methods=['GET','POST'])
def set_spea(article_id, spea_name):
    article = Article()
    article.search_by_id(article_id)
    article.set_spea(spea_name)
    flash('SET' + spea_name + 'SUCCESS')
    return redirect(request.args.get('next') or url_for('views_blueprint.index'))

@views_blueprint.route('/test',methods=['GET','POST'])
def test():
    return new_render_template('test.html')



if __name__=='__main__':
    article = Article()
    article.search_by_id('20170507193843')