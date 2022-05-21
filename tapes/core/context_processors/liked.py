from tape.models import Like


def liked(request):
    liked = []
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user).values('entry_id')
        for i in range(len(likes)):
            liked.append(likes[i]['entry_id'])
    return {
        'liked': liked,
    }
