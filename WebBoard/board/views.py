from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render

from board.models import Board


# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    keyword = request.GET.get('keyword', '')
#     qry = "SELECT (@R := @R+1) rownum, A.* \
#              FROM web_test.board_board A, (SELECT @R := 0) B \
#             ORDER BY id DESC"
#     boardList = Board.objects.raw(qry)
    boardList = Board.objects.order_by('-id')
    
    rowCount = 10       # 한페이지에 출력하는 row 수
    paging = 3          # 한페이지에 표시할 페이지 범위
    
    if len(keyword) > 0 :
        boardList = boardList.filter(Q (title__icontains=keyword) | Q (content__icontains=keyword))
        
    paginator = Paginator(boardList, rowCount)
    try:
        bList = paginator.page(page)
    except PageNotAnInteger:
        bList = paginator.page(1)
    except EmptyPage:
        bList = paginator.page(paginator.num_pages)
    
    start_index = (paging*int((bList.number-1)/paging))+1
    end_index = paging*(int((bList.number-1)/paging)+1)+1
    if end_index > len(paginator.page_range):
        end_index = len(paginator.page_range)+1
    page_range = range(start_index,end_index)

    return render(request, 'list.html', {'boardList':bList, 'keyword':keyword, 'page_range':page_range})


def write_form(request):
    page = request.GET.get('page', 1)
    return render(request, 'write.html', {'page':page})


def write(request):
    moObj = Board ( 
                title = request.POST.get('title'),
                content = request.POST.get('content')
            )
    moObj.save()
    return HttpResponseRedirect('/')


def view(request, bData_id):
    page = request.GET.get('page', 1)
    keyword = request.GET.get('keyword', '')
    try:
        bData = Board.objects.get(pk=bData_id)
    except Board.DoesNotExist:
        raise Http404('찾을 수 없습니다.')
       
    return render(request, 'view.html', {'bData':bData, 'page':page, 'keyword':keyword})


def modify_form(request, bData_id):
    page = request.GET.get('page', 1)
    
    try:
        bData = Board.objects.get(pk=bData_id)
    except Board.DoesNotExist:
        raise Http404('찾을 수 없습니다.')
       
    return render(request, 'modify.html', {'bData':bData, 'page':page})


def modify(request, bData_id):
    page = request.GET.get('page', 1)
    
    try:
        bData = Board.objects.get(pk=bData_id)
    except Board.DoesNotExist:
        raise Http404('찾을 수 없습니다.')
    
    bData.title = request.POST['title']
    bData.content = request.POST['content']
    bData.save()
    
    return render(request, 'view.html', {'bData':bData, 'page':page})


def delete(request, bData_id):
    try:
        bData = Board.objects.get(pk=bData_id)
    except Board.DoesNotExist:
        raise Http404('찾을 수 없습니다.')
    
    bData.delete()
    
    return HttpResponseRedirect('/')



