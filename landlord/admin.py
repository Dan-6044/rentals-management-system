from django.contrib import admin
from .models import Landlord

@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)


from django.contrib import admin
from .models import Property, PropertyImage, PropertyVideo

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # This will add a form for adding one image by default

class PropertyVideoInline(admin.TabularInline):
    model = PropertyVideo
    extra = 1  # This will add a form for adding one video by default

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_name', 'user', 'property_type', 'location', 'longitude', 'rent', 'agency', 'contact')
    list_filter = ('property_type', 'location', 'rent')
    search_fields = ('property_name', 'location', 'user__username')
    ordering = ('rent',)

    # Add inlines for images and videos
    inlines = [PropertyImageInline, PropertyVideoInline]

admin.site.register(Property, PropertyAdmin)


