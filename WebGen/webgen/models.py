from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self):
		super().save()

		img = Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

class About(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name=models.CharField(max_length=250)
	def __str__(self):
		return self.name

class Course(models.Model):
	course_title = models.CharField(max_length=20)
	content = models.TextField()
	teacher = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.course_title

	def get_absolute_url(self):
		return reverse('course-detail', kwargs={'pk': self.pk})
# Create your models here.
