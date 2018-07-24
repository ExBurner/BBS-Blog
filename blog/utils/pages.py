from django.core.paginator import Paginator, EmptyPage


def get_pages(request, lists):
    paginator = Paginator(lists, 10)
    try:
        current_page = int(request.GET.get("page", 1))
        page = paginator.page(current_page)
        if paginator.num_pages > 10:
            ranges = range(current_page - 4, current_page + 5)
            if current_page - 5 < 0:
                ranges = range(1, 9)
            elif current_page + 5 > paginator.num_pages:
                ranges = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            ranges = paginator.page_range
    except EmptyPage as e:
        page = paginator.page(1)

    return {"page": page, "ranges": ranges, "current_page": current_page}