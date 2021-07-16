import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'moxing.settings'

if __name__ == '__main__':

    subject, from_email, to = '来自www.liufengblog.com的测试邮件', '2432920243@qq.com', '15518615671@163.com'
    text_content = '欢迎访问www.liufengblog.com，这里是流风的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.liufengblog.com" target=blank>www.liujiangblog.com</a>，这里是流风的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()