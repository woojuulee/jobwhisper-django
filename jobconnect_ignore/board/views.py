import json

from django.http import Http404
# from .forms import BoardForm
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Board, Comment
from .forms import CommentForm



def board_index(request):
    board_list = Board.objects.all()
    paginator = Paginator(board_list, 20)  # 페이지당 20개 아이템으로 페이지네이션

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'board/index.html', {'page': page})




def board_detail(request, board_id):
    board = Board.objects.get(pk=board_id)

    board_history = request.session.get('board_history')
    if not board_history:
        request.session['board_history'] = []
    request.session['board_history'] += [board_id]

    # if not (board and board.is_active):
    #     return Http404("요청하신 페이지가 없습니다.")

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comment(
                content=data['content'],
                board_id=board_id
            ).save()
            return redirect(reverse('board:detail',
                                    kwargs={'board_id': board_id}))

    
    # 코멘트에 대한 페이지네이션
    comments = Comment.objects.filter(board=board).order_by('-id')  # 최신 댓글이 위에 오도록
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



    return resp


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

