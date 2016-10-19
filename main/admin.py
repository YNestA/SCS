from django.contrib import admin
from models import *

# Register your models here.

class CollegeAdmin(admin.ModelAdmin):
    filter_horizontal = ("majors",)

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("groups","user_permissions",)

def user_unicode(self):
    return ' | '.join([self.common_user_profile.name,self.username])

User.__unicode__=user_unicode

admin.site.register(Major)
admin.site.register(College,CollegeAdmin)
admin.site.register(Category)
admin.site.register(Term)
admin.site.register(CourseLocationTime)
admin.site.register(Course)
admin.site.register(SelectRecord)
admin.site.register(CommonUserProfile)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(SystemNotify)
