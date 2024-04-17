from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.utils import timezone
from django.contrib.auth import authenticate, login
import json

from django.http import Http404
# from .forms import BoardForm
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Board, Comment, User
from .forms import CommentForm

from django.db.models import Count, Avg

from django.db.models import Subquery
from django.contrib.auth.models import User, UserManager


def board_index(request):
    # 회사별 평균평점 계산
    avg = Comment.objects.values('board').annotate(avg_rating=Avg('star'))

    # 정렬
    sort = request.GET.get('sort') # 쿼리스트링은 GET으로 받아온다.
    # if sort == 'comments':  # 리뷰 많은 순
    #     content_list = Comment.objects.values('board').annotate(
    #         review_count=Count('id')).order_by('-review_count')

    if sort == 'salary':  # 높은 연봉순
        board_list = Board.objects.all().order_by('-salary')

    elif sort == 'comments':  # 리뷰 많은순
        # a = Board.objects.all().select_related('comment_set')
        # print(a)
        # Board.objects.raw("")
        # b = Comment.objects.values('board_id').annotate(
        #     review_count=Count('board_id')
        # ).order_by('-review_count')

        # print(b)
        # Board.objects.annotate(
        #     review_count=
        # )

        # board = Board.objects.select_related('comment_set')
        # .annotate(
        #     review_count=Count('board_id')
        # ).order_by('review_count')
        # print(board.query)

        a = Comment.objects.values('board').annotate(
            review_count=Count('id')).order_by('-review_count')
        # print(a)

        li = []
        board_list = []
        for i in a:
            li.append(i['board'])
        # print(li)

        for j in li:
            board_list.append(Board.objects.get(id=j))

    else:
        sort == 'basic'
        board_list = Board.objects.all()

    paginator = Paginator(board_list, 20)  # 페이지당 20개 아이템으로 페이지네이션

    page_number = request.GET.get('page', '')
    page = paginator.get_page(page_number)

    return render(request, 'board/index.html', {'page': page, 'avg': avg, 'sort': sort})


def board_detail(request, board_id):
    board = Board.objects.get(pk=board_id)

    board_history = request.session.get('board_history')
    if not board_history:
        request.session['board_history'] = []
    request.session['board_history'] += [board_id]

    # if not (board and board.is_active):
    #     return Http404("요청하신 페이지가 없습니다.")

    form = CommentForm()

    # if request.method == 'POST':
    #    form = CommentForm(request.POST)
    #    if form.is_valid():
    #        data = form.cleaned_data
    #        Comment(
    #            content=data['content'],
    #            board_id=board_id
    #        ).save()
    #        return redirect(reverse('board:detail',
    #                                kwargs={'board_id': board_id}))

    # 코멘트에 대한 페이지네이션
    comments = Comment.objects.filter(
        board=board).order_by('-id')  # 최신 댓글이 위에 오도록
    paginator = Paginator(comments, 10)  # 페이지당 10개의 코멘트

    page_number = request.GET.get('page', 1)  # URL의 page 파라미터 값을 가져옵니다
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # page 파라미터가 정수가 아니면 첫 번째 페이지를 보여줍니다
        page = paginator.page(1)
    except EmptyPage:
        # 페이지의 범위를 벗어나면 마지막 페이지를 보여줍니다
        page = paginator.page(paginator.num_pages)

    # render 메서드의 context 파라미터에 page를 추가합니다
    return render(request, "board/detail.html", {'board': board, 'form': form, 'page': page})

    


def board_comment(request, board_id):
    board = Board.objects.get(pk=board_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid:
            temp = form.save(commit=False)
            temp.board = board
            temp.save()
            return redirect(reverse('board:detail', kwargs={'board_id': board_id}))
    else:
        form = CommentForm()
        return render(request, 'board/comment.html', {'board': board, 'form': form})


def board_write(request):
    form = BoardForm()
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('board:index'))

    return render(request,
                  "board/write.html",
                  {'form': form})


def board_edit(request, board_id):
    board = Board.objects.get(id=board_id)
    form = BoardForm(initial={
        'title': board.title,
        'content': board.content,
        'author': board.author
    })
    if request.method == 'POST':
        form = BoardForm(request.POST)

        if form.is_valid():
            board.title = form.cleaned_data['title']
            board.content = form.cleaned_data['content']
            board.author = form.cleaned_data['author']
            board.save()
            return redirect(reverse('board:detail', kwargs={
                'board_id': board_id
            }))
    return render(request,
                  "board/edit.html",
                  {'form': form})


def board_delete(request, board_id):
    board = Board.objects.get(id=board_id)
    board.is_delete = True
    board.save()
    return redirect(reverse('board:index'))

# import 코드 섞여서 그냥 다 보내요!


# from .forms import BoardForm


def board_register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('board:index'))
    return render(request, 'board/register.html', {'form': form})


def board_login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('board:index')
        else:
            messages.error(request, '로그인에 실패했습니다. 사용자 이름 또는 비밀번호를 확인해 주세요.')

    return redirect('board:index')


class board_logout(LogoutView):
    # 로그아웃 후 리디렉션 URL 설정
    next_page = reverse_lazy('board:index')
