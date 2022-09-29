from entries.models import Like, Bookmark


def liked(request):
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user).values('entry_id')
    return {
        'liked': liked,
    }


def marked(request):
    marked = False
    if request.user.is_authenticated:
        marked = Bookmark.objects.filter(user=request.user).values('entry_id')
    return {
        'marked': marked,
    }
