from tape.models import Like, Bookmark


def liked(request):
    liked = []
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user).values('entry_id')
        for i in range(len(likes)):
            liked.append(likes[i]['entry_id'])
    return {
        'liked': liked,
    }


def marked(request):
    marked = []
    if request.user.is_authenticated:
        marks = Bookmark.objects.filter(user=request.user).values('entry_id')
        for i in range(len(marks)):
            marked.append(marks[i]['entry_id'])
    return {
        'marked': marked,
    }
