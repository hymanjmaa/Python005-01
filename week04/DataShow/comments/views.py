from django.shortcuts import render
from .models import Comment
from pathlib import Path
import json

p = Path(__file__)
base_path = p.resolve().parent
# Create your views here.


def show_comments(request):

    comment_count = Comment.objects.all().count()
    if comment_count == 0:
        with open(base_path.as_posix() + '/static/comments.json', 'r') as f:
            records = f.read()
            record_l = json.loads(records)
            for r in record_l:
                comment = Comment(content=r['content'],
                                  star=int(r['star'])/10,
                                  pub_time=r['pub_time'])
                comment.save()

    conditions = {'star__gt': 3}
    comments = Comment.objects.filter(**conditions).all()

    return render(request, 'comments.html', locals())


def search_comments(request):
    q = request.GET.get('q')

    if q in ['', None]:
        comments = Comment.objects.all()
    else:
        conditions = {'content__icontains': q}
        comments = Comment.objects.filter(**conditions).all()

    return render(request, 'comments.html', locals())
