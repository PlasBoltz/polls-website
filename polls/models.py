from binascii import Error
from datetime import datetime
from inspect import Attribute
from tkinter import CASCADE

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_admin = models.BooleanField(default = False)
    display_name = models.CharField(max_length=24, default="User"+str(id))
    posts = models.TextField(default = "")

    def get_username(self):
        return self.user.username

    def set_username(self, new_username):
        self.user.username = new_username

    def get_password(self):
        return self.user.password
    
    def set_password(self, new_password):
        self.user.password = new_password

    def get_display_name(self):
        return self.display_name
    
    def set_display_name(self, new_display_name):
        self.display_name = new_display_name

    def get_posts(self):
        return [Post.objects.get(pk=int(i)) for i in self.posts.split()]

    def add_post(self, post):
        self.posts += " " + str(post.id)
    
    def delete(self, post):
        posts = self.posts.split()
        posts.delete(str(post.id))
        self.posts = " ".join(posts)



    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)

    time_published = models.DateTimeField(auto_now_add=True, blank=True)
    raw_title = models.TextField(max_length=256)
    raw_content  =models.TextField(max_length=8192)
    meta_tags = models.TextField()
    is_viewable = models.BooleanField(default = True)
    comments = models.TextField()
    
    @classmethod
    def create(cls, author):
        post = cls(author = author)
        return post

    @property
    def title(self):
        if self.is_viewable:
            return self.raw_title
        else:
            return "[removed]"

    @property
    def content(self):
        if self.is_viewable:
            return self.raw_content
        else:
            return "[removed]"

    def get_author(self):
        return self.author

    def set_author(self, new_author: Profile):
        self.author = new_author
    
    def get_title(self):
        return self.raw_title

    def set_title(self, new_title):
        self.raw_title = new_title
    
    def get_meta_tags(self):
        return self.meta_tags

    def add_meta_tag(self, tag):
        self.meta_tags = self.meta_tags + " " + tag
    
    def delete_meta_tag(self, tag):
        tags = self.meta_tags.split() #splits the metatags into a list by spaces
        tags = tags.remove(tag) #remove has built in error handeling
        self.meta_tags = " ".join(tags) #joins tags into string by spaces

    def get_content(self):
        return self.raw_content
    
    def set_content(self, new_content):
        self.raw_content = new_content

    @property
    def get_comments(self):
        ids = self.comments.split()
        c = [Comment.objects.get(pk=int(i)) for i in ids]
        return c

    @property
    def get_width(self):
        return 48*len(self.get_comments)+10*(len(self.get_comments)-1)

    def add_comment(self, new_comment):
        new_comment_id = new_comment.id
        self.comments += " " + str(new_comment_id)

    def delete_comment(self, target_comment):
        ids = self.cmments.split()
        ids.remove(str(target_comment.id))
        self.comments = " ".join(ids)
    
    def get_viewable(self):
        return self.is_viewable
    
    def set_viewable(self, new_v :bool):
        self.is_viewable = new_v

class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)

    time_published = models.DateTimeField(auto_now_add=True, blank=True)
    raw_content = models.TextField(max_length=1024)
    comments = models.TextField()
    is_viewable = models.BooleanField(default = True)

    @classmethod
    def create(cls, author):
        comment = cls(author = author)
        return comment

    def get_author(self):
        return self.author

    def set_author(self, new_author: Profile):
        self.author = new_author

    def get_content(self):
        return self.raw_content
    
    def set_content(self, new_content):
        self.raw_content = new_content

    @property
    def content(self):
        if self.is_viewable:
            return self.raw_content
        else:
            return "[removed]"

    @property
    def get_comments(self):
        ids = self.comments.split()
        c = [Comment.objects.get(pk=int(i)) for i in ids]
        return c

    @property
    def get_width(self):
        return 48*len(self.get_comments)+22*(len(self.get_comments)-1)

    def add_comment(self, new_comment):
        new_comment_id = new_comment.id
        self.comments += " " + str(new_comment_id)

    def delete_comment(self, target_comment):
        ids = self.cmments.split()
        ids.remove(str(target_comment.id))
        self.comments = " ".join(ids)
    
    def get_viewable(self):
        return self.is_viewable
    
    def set_viewable(self, new_v :bool):
        self.is_viewable = new_v

