from django.db import models

# Create your models here.

class Ceshi(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=128)
    sex = models.CharField(max_length=32,choices=gender)
    phone = models.CharField(max_length=30,blank=True,null=True)

    class Meta:
        db_table = 'ceshi'






class tian1(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    sex = models.CharField(max_length=32,choices=gender)
    email = models.EmailField(unique=True,null=True)
    phone = models.CharField(max_length=30,blank=True,null=True)
    c_time = models.DateTimeField(auto_now_add=True,null=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-c_time']
        db_table = 'tian1'
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('tian1', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:

        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"
