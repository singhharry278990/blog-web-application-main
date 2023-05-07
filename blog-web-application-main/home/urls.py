from django.urls import path
from .views import *
from  middleware.middleware import CustomMiddleware

urlpatterns = [
    path('', home, name="home"),
    path('reset/', reset_password_page, name="reset_password"),
    path('login/', CustomMiddleware(login_view), name="login_view"),
    path('register/', register_view, name="register_view"),
    path('add-blog/', add_blog, name="add_blog"),
    path('blog-detail/<slug>', blog_detail, name="blog_detail"),
    path('see-blog/', see_blog, name="see_blog"),
    path('blog-delete/<id>', blog_delete, name="blog_delete"),
    path('blog-update/<slug>/', blog_update, name="blog_update"),
    path('logout-view/', logout_view, name="logout_view"),
    path('verify/<token>/', verify, name="verify"),
    path('otp/<id>', otp_page, name="otp"),
    path('thank-you/', thsnk_you_page, name="thank-you"),
    path('suspened/', suspened_page, name="suspened"),
    path('suspened/view-edit/', user_profile, name='view-edit')
   
]