from django.db import models

# Create your models here.
class OnspaceUser(models.Model):
    username = models.CharField(max_length=64, verbose_name = '사용자명')
    useremail = models.EmailField(max_length=128, verbose_name = '사용자 이메일')
    password = models.CharField(max_length=64, verbose_name = '비밀번호')
    subscription = models.BooleanField(default=False, verbose_name = '구독여부')
    registered_dttm = models.DateTimeField(auto_now_add = True, verbose_name='등록시간')

    def __str__(self):
        return self.username

    class Meta:
        db_table = "Onspace_user"
        verbose_name = "온스페이스 사용자"
        verbose_name_plural = "온스페이스 사용자"