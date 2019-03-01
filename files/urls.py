from django.conf.urls import url

from files.views import UploadFileAPIView

urlpatterns = [
    url(r'v1/uploadmedia/', UploadFileAPIView.as_view()),
    ]