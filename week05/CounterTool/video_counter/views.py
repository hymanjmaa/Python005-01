from django.shortcuts import render
from django_redis import get_redis_connection
redis_conn = get_redis_connection("default")


def video_detail(request):
    videos = [1001, 1002, 1003, 1004, 1005]
    return render(request, 'video.html', locals())


def click_video(request):
    vid = request.GET.get('vid')
    res = counter(vid).decode()
    return render(request, 'video_counter_res.html', locals())


def counter(video_id: int):
    redis_conn.incr(f'{video_id}', amount=1)
    c_num = redis_conn.get(f"{video_id}")
    return c_num
