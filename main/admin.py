from django.contrib import admin
from models import *

# Register your models here.

admin.site.register(Major)
admin.site.register(College)
admin.site.register(Category)
admin.site.register(Term)
admin.site.register(CourseLocationTime)
admin.site.register(Course)
admin.site.register(SelectRecord)
admin.site.register(CommonUserProfile)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)