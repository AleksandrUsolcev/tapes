from django.contrib import admin

from .models import Tape, Entry, Comment, Subscribe, Like, Bookmark


class TapeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        'created',
    )


class EntryAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class SubscribeAdmin(admin.ModelAdmin):
    pass


class LikeAdmin(admin.ModelAdmin):
    pass


class BookmarkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tape, TapeAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
