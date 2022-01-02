import uuid
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import models
from sorl.thumbnail import get_thumbnail, delete

User = get_user_model()


def image_directory_path(instance, filename):
    return f'images/pictures/{str(uuid.uuid4())}.{filename.split(".")[-1]}'


class Post(models.Model):
    owner = models.ForeignKey(User, verbose_name='オーナー', on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)
    is_publish = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # photo = models.ImageField(upload_to=image_directory_path, verbose_name='投稿画像', blank=True, null=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        owner = self.owner
        updated_at = self.updated_at
        return f"{owner}/{updated_at}"


class Picture(models.Model):
    picture = models.ImageField(upload_to=image_directory_path)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # main_flag = models.BooleanField(default=False, verbose_name='メイン画像')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_pictures'

    def save(self, *args, **kwargs):
        super(Picture, self).save(*args, **kwargs)
        temp_img_name = self.picture.name
        if self.picture.width > 1000 or self.picture.height > 1000:
            new_width = 1000
            new_height = 1000

            resized = get_thumbnail(self.picture, "{}x{}".format(new_width, new_height))
            name = resized.name.split('/')[-1]  # 結局上で定義したUUIDの名前になるのでこれは仮の名前
            self.picture.save(name, ContentFile(resized.read()), True)
            try:
                delete(temp_img_name)
            except ObjectDoesNotExist:  # ここの例外は自身のものに変える
                pass

    def __str__(self):
        return f'{self.pk} : {self.picture.name}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'


class Comment(models.Model):
    text = models.TextField(verbose_name='コメント', max_length=1024)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='投稿日時', auto_now_add=True)

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return self.text