from django.contrib import admin
from .models import (
    AuthUser, AuthGroup, AuthUserGroups, AuthUserUserPermissions,
    AuthPermission, DjangoAdminLog, DjangoContentType,
    DjangoMigrations, DjangoSession, LoginCustomuser
)

admin.site.register(AuthUser)
admin.site.register(AuthGroup)
admin.site.register(AuthUserGroups)
admin.site.register(AuthUserUserPermissions)
admin.site.register(AuthPermission)
admin.site.register(DjangoAdminLog)
admin.site.register(DjangoContentType)
admin.site.register(DjangoMigrations)
admin.site.register(DjangoSession)
admin.site.register(LoginCustomuser)
