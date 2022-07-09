from django.contrib import admin

from talks.models import Talk
from tape.models import Tape, Entry, Subscribe, Like, Bookmark


class TapeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        'created',
    )


class EntryAdmin(admin.ModelAdmin):
    pass


class TalkAdmin(admin.ModelAdmin):
    pass


class SubscribeAdmin(admin.ModelAdmin):
    pass


class LikeAdmin(admin.ModelAdmin):
    pass


class BookmarkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tape, TapeAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Talk, TalkAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
