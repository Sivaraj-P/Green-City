from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(Complaint)
admin.site.register(Queries)
admin.site.register(MyUser)

admin.site.site_header = 'Green City'                    # default: "Django Administration"
admin.site.index_title = 'ADMIN'                 # default: "Site administration"
admin.site.site_title = 'Green City'                 # default: "Site administration"



