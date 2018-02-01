from django.contrib import admin

# Register your models here.
from .models import ToolShareUser
from toolsharesite.models import Tool, Category

class shareToolUserAdmin(admin.ModelAdmin):
    list_display = ['username','zip']

admin.site.register(ToolShareUser,shareToolUserAdmin)

class ToolAdmin(admin.ModelAdmin):
    list_disply = ['name','owner']
    
admin.site.register(Tool,ToolAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_disply = ['id','type']
    
admin.site.register(Category,CategoryAdmin)