from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Movie, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
import pymysql
import re
from django.views import generic
# Create your views here.
from django.http import HttpResponse


def pick(request):
    return render(request, 'movies/pick_movie.html')


def now_playing(request):
    def recent():
        # 写一个判断日期的函数
        pass

    movie_list = Movie.objects.order_by('-release_time')[:20] # 加'－'表示逆序

    for movie in movie_list:
        movie.name = movie.name.split(' ')[0]

    return render(request, 'movies/now_playing.html', {'movie_list': movie_list})


def detail(request, movie_id):
    # print(request.user)
    current_user = request.user

    movie = get_object_or_404(Movie, pk=movie_id)

    has_commented = False
    try:
        # 查询数据库是否存在评论记录
        my_comment = Comment.objects.get(movie_id=movie, user_id=current_user)
    except Exception as e:
        print(e) # test
        my_comment = ''
        form = CommentForm()
    else:
        has_commented = True
        form = CommentForm(instance=my_comment)
    finally:
        print(has_commented) # test


    sort = request.GET.get('sort')
    if sort == 'votes':
        # comment_set = sorted(comment_set, key=lambda m: m.thumb_ups, reverse=True)
        comment_set = movie.comment_set.order_by('-thumb_ups')[:5]
    elif sort == 'time':
        comment_set = movie.comment_set.order_by('-time')[:5]
    else: # 默认情况
        comment_set = movie.comment_set.order_by('-thumb_ups')[:5]



    context = {
        'movie': movie,
        'comment_set': comment_set,
        'form': form,
        'has_commented': has_commented,
        'my_comment': my_comment,
    }

    return render(request, 'movies/detail.html', context)


def post_comment(request, movie_id):
    if not request.user.is_authenticated:
        return redirect('/%s?next=%s' % (settings.LOGIN_URL, request.path))

    current_user = request.user
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        try: # 验证是否存在当前用户对这部电影的评论
            my_comment = Comment.objects.get(user_id=current_user, movie_id=movie.id)
        except:
            form = CommentForm(request.POST)
        else:
            form = CommentForm(request.POST, instance=my_comment)

        if form.is_valid():
            # print(form.cleaned_data['content'], username)
            comment = form.save(commit=False)
            comment.user_id = request.user
            comment.movie_id = movie
            comment.save()
            # print("评论成功")
            # request.session['has_commented'] = True
            return redirect(movie)
        else:
            comment_set = movie.comment_set.order_by('-thumb_ups')[:5]
            context = {
                'movie': movie,
                'comment_set': comment_set,
                'form': form,
            }
            # print("评论失败")
            return render(request, 'movies/detail.html', context)

    return redirect(movie)


def del_comment(request, movie_id, comment_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    try:
        comment = get_object_or_404(Comment, pk=comment_id)
    except:
        pass
    else:
        comment.delete()

    return redirect(movie)


def explore(request):
    # 获取标签和排序方式
    tag = request.GET.get('tag', '热门')
    sort = request.GET.get('sort', 'recommend')
    # print(tag, sort)

    if sort == 'recommend':
        sort_value = '-heat'
    elif sort == 'time':
        sort_value = '-release_time'
    elif sort == 'rank':
        sort_value = '-rating'

    limit = 20 # 每页显示的数量

    # 取页码以及翻页类型
    # 当前页面若取不到，则默认第一页
    # 注意这里 page 参数对应的值在前端
    current_p = int(request.GET.get('page', '1'))
    page_type = request.GET.get('page_type', '')

    if page_type == 'previous':
        current_p -= 1
    elif page_type == 'next':
        current_p += 1
    print('当前页数', current_p) #test

    previous_page = True
    next_page = True
    start_pos = (current_p - 1) * limit
    end_pos = start_pos + limit


    if tag == '热门':
        # 计算该类别的电影数量
        movie_num = Movie.objects.all().order_by('-heat').count()
        if sort == 'recommend':
            try:
                movie_list = Movie.objects.all().order_by('-heat')[start_pos:end_pos]
            except Exception as e:  # 最后一页可能取不到那么多
                print(e)
                movie_list = Movie.objects.all().order_by('-heat')[start_pos:]
        elif sort == 'time':
            try:
                movie_list = Movie.objects.all().order_by('-heat')[start_pos:end_pos]
            except Exception as e:  # 最后一页可能取不到那么多
                print(e)
                movie_list = Movie.objects.all().order_by('-heat')[start_pos:]
            movie_list = sorted(movie_list, key=lambda m: m.release_time, reverse=True)
        elif sort == 'rank':
            try:
                movie_list = Movie.objects.all().order_by('-heat')[start_pos:end_pos]
            except Exception as e:  # 最后一页可能取不到那么多
                print(e)
                movie_list = Movie.objects.all().order_by('-heat')[start_pos:]
            movie_list = sorted(movie_list, key=lambda m: m.rating, reverse=True)
    elif tag == '最新':
        # 需设置 radio 不可选
        movie_num = Movie.objects.all().order_by('-release_time').count()
        try:
            movie_list = Movie.objects.all().order_by('-release_time')[start_pos:end_pos]
        except Exception as e:  # 最后一页可能取不到那么多
            print(e)
            movie_list = Movie.objects.all().order_by('-release_time')[start_pos:]
    else: # 处理除'最新'，'热门'以外的标签
        movie_num = Movie.objects.filter(genre__icontains=tag).order_by(sort_value).count()
        try:
            movie_list = Movie.objects.filter(genre__icontains=tag).order_by(sort_value)[start_pos:end_pos]
        except Exception as e:  # 最后一页可能取不到那么多
            print(e)
            movie_list = Movie.objects.filter(genre__icontains=tag).order_by(sort_value)[start_pos:]

    # 判断是否有上下页
    if start_pos <= 0:
        previous_page = False
    if end_pos > movie_num:
        next_page = False

    # test
    # print('previous_page:', previous_page)
    # print('next_page:', next_page)
    # print('start_pos', start_pos)
    # print('end_pos', end_pos)

    for movie in movie_list:
        movie.name = movie.name.split(' ')[0]

    # paginator
    # limit = 15
    # paginator = Paginator(movie_list, limit)
    # page = request.GET.get('page')
    # print('当前页数', page)
    # movies = paginator.get_page(page)

    context = {
        'movie_list': movie_list,
        'tag': tag,
        'sort': sort,
        'previous_page': previous_page,
        'next_page': next_page,
        'current_p': current_p,
        'page_type': page_type,
    }

    return render(request, 'movies/pick_movie.html', context)


def index(request):


    # 正在上映
    now_playing = Movie.objects.order_by('-release_time')[:20]
    for movie in now_playing:
        movie.name = movie.name.split(' ')[0]

    limit = 5
    paginator1 = Paginator(now_playing, limit)
    now_playing_page = request.GET.get('now_playing_page')
    now_playing = paginator1.get_page(now_playing_page)

    # 热门电影
    hot_list = Movie.objects.order_by('-heat')[:20]
    for movie in hot_list:
        movie.name = movie.name.split(' ')[0]

    paginator2 = Paginator(hot_list, limit)
    hot_page = request.GET.get('hot_page')
    hot_list = paginator2.get_page(hot_page)

    # 口碑榜
    rating_list = Movie.objects.order_by('-rating')[:20]
    for movie in rating_list:
        movie.name = movie.name.split(' ')[0]

    paginator2 = Paginator(rating_list, limit)
    rating_page = request.GET.get('rating_page')
    rating_list = paginator2.get_page(rating_page)

    context = {
        'movie_list1': now_playing,
        'hot_list': hot_list,
        'rating_list': rating_list,
        'now_playing_page': now_playing_page,
        'hot_page': hot_page,
        'rating_page': rating_page,
    }

    return render(request, 'movies/index.html', context)


def all_comments(request, movie_id):

    current_user = request.user
    movie = get_object_or_404(Movie, pk=movie_id)

    # 排序方式
    sort = request.GET.get('sort')
    # 获取页码以及翻页类型
    current_p = int(request.GET.get('page', '1'))
    page_type = request.GET.get('page_type', '')

    limit = 20  # 每页显示的数量
    # 判断翻页类型
    if page_type == 'previous':
        current_p -= 1
    elif page_type == 'next':
        current_p += 1

    previous_page = True
    next_page = True
    start_pos = (current_p - 1) * limit
    end_pos = start_pos + limit

    comment_num = movie.comment_set.count()
    if sort == 'votes':
        try:
            comment_set = movie.comment_set.order_by('-thumb_ups')[start_pos:end_pos]
        except Exception as e:
            print(e)
            comment_set = movie.comment_set.order_by('-thumb_ups')[start_pos:]
    elif sort == 'time':
        try:
            comment_set = movie.comment_set.order_by('-time')[start_pos:end_pos]
        except Exception as e:
            print(e)
            comment_set = movie.comment_set.order_by('-time')[start_pos:]
    else: # 默认排序
        try:
            comment_set = movie.comment_set.order_by('-thumb_ups')[start_pos:end_pos]
        except Exception as e:
            print(e)
            comment_set = movie.comment_set.order_by('-thumb_ups')[start_pos:]

    # 判断是否有上下页
    if start_pos <= 0:
        previous_page = False
    if end_pos > comment_num:
        next_page = False

    if request.method == 'POST':
        # 若方法为 post，检查权限
        if not request.user.is_authenticated:  # 检查评论权限
            return redirect('/%s?next=%s' % (settings.LOGIN_URL, request.path))

        try: # 验证是否存在当前用户对这部电影的评论
            my_comment = Comment.objects.get(user_id=current_user, movie_id=movie.id)
        except:
            form = CommentForm(request.POST)
        else:
            form = CommentForm(request.POST, instance=my_comment)

        if form.is_valid():
            # print(form.cleaned_data['content'], username)
            comment = form.save(commit=False)
            comment.user_id = request.user
            comment.movie_id = movie
            comment.save()
            # print("评论成功")
            return HttpResponseRedirect(reverse('movies:all_comments', args=[movie.id]))
        else: # 数据验证未通过，用已填的数据重新渲染表单
            context = {
                'movie': movie,
                'comment_set': comment_set,
                'form': form,
                'current_p': current_p,
                'page_type': page_type,
                'previous_page': previous_page,
                'next_page': next_page,
            }
            return render(request, 'reviews/all_comments.html', context)
    else: # 不是 post 方法
        try:
            my_comment = Comment.objects.get(user_id=current_user, movie_id=movie.id)
        except:
            form = CommentForm()
        else:
            form = CommentForm(instance=my_comment)

        context = {
            'movie': movie,
            'comment_set': comment_set,
            'form': form,
            'current_p': current_p,
            'page_type': page_type,
            'previous_page': previous_page,
            'next_page': next_page,
        }

        return render(request, 'reviews/all_comments.html', context)


def reviews(request):
    # 排序方式
    sort = request.GET.get('sort')
    # 取页码以及翻页类型
    # 当前页面若取不到，则默认第一页
    # 注意这里 page 参数对应的值在前端
    current_p = int(request.GET.get('page', '1'))
    page_type = request.GET.get('page_type', '')
    limit = 20  # 每页显示的数量

    # 判断翻页类型
    if page_type == 'previous':
        current_p -= 1
    elif page_type == 'next':
        current_p += 1

    previous_page = True
    next_page = True
    start_pos = (current_p - 1) * limit
    end_pos = start_pos + limit

    comment_num_limit = 100
    # 判断是否有上下页
    if start_pos <= 0:
        previous_page = False
    if end_pos >= comment_num_limit:
        next_page = False

    # 因为数据库里一定有超过 100 条评论，而此处最多只显示 100 条评论，所以不需要使用 try 语句
    if sort == 'votes':
        comment_set = Comment.objects.order_by('-thumb_ups')[start_pos:end_pos]

    elif sort == 'time':
        comment_set = Comment.objects.order_by('-time')[start_pos:end_pos]
    else: # 默认排序方式
        comment_set = Comment.objects.order_by('-thumb_ups')[start_pos:end_pos]

    context = {
        'comment_set': comment_set,
        'next_page': next_page,
        'previous_page': previous_page,
        'current_p': current_p,
        'page_type': page_type,
        'sort': sort,
    }

    return render(request, 'reviews/top_reviews.html', context)


def subject_search(request):
    search_text = request.GET.get('search_text')

    connection = pymysql.connect(
        host='localhost',
        user='abc',
        password='123',
        db='Vent',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try: # 模糊检索
        with connection.cursor() as cursor:
            sql = "select `id` from `movies_movie` where `name` like %s"
            param = '%' + search_text + '%'
            cursor.execute(sql, (param))
            result = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        connection.close()

    try:
        movie_ids = [ i['id'] for i in result ]
    except Exception as e:
        print(e)
    else:
        movie_set = []
        for id in movie_ids:
            movie = Movie.objects.get(pk=id)
            movie_set.append(movie)

        for movie in movie_set:
            movie.star = movie.star[:40]
        # print(movie_set) # test

        context = {
            'search_text': search_text,
            'movie_set': movie_set,
        }

        return render(request, 'movies/search_result.html', context)


def like_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'login': 0,
        })
        # return redirect('/%s?next=%s' % (settings.LOGIN_URL, request.path))

    # 获取评论id
    # comment_id = request.GET.get('comment_id') # GET 写法
    comment_id = request.POST['comment_id'] # POST 写法
    # 从数据库中获取评论对象
    comment = get_object_or_404(Comment, pk=comment_id)
    # 获取当前登录用户
    current_user = request.user

    connection = pymysql.connect(
        host='localhost',
        user='abc',
        password='123',
        db='Vent',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `movies_like` WHERE `comment_id` = %s and `user_id` = %s"
            params = [comment_id, current_user.id]
            cursor.execute(sql, (params))
            result = cursor.fetchall()
    except Exception as e:
        print(e)
    else:
        if result == (): # 该用户还未对这条评论点赞
            has_commented  = 0 # 前端标记
            comment.thumb_ups += 1 # 该条评论的点赞数 ＋ 1
            comment.save()
            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `movies_like` (`comment_id`, `user_id`) VALUES (%s, %s)"
                    params = [comment_id, current_user.id]
                    cursor.execute(sql, (params))
                connection.commit() # 提交修改
            except Exception as e:
                print(e)
        else:
            has_commented = 1

        context = {
            'thumb_ups': comment.thumb_ups,
            'has_commented': has_commented,
        }

        return JsonResponse(context)
    finally:
        connection.close()









