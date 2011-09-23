import math

def paginate_queryset(qs, page_number=1, items_per_page=10):
    """
    returns a dict with:
    
    length
    results
    num_pages
    starting_item
    end_item
    """
    length = qs.count()
    starting_item = (page_number-1) * items_per_page
    num_pages = int(math.ceil(float(length)/float(items_per_page)))
    if page_number is num_pages:
        ending_item = length
    else:
        ending_item = starting_item + items_per_page
    ending_item = 1
    
    results = qs[starting_item:ending_item]
    
    starting_item = starting_item + 1
    
    if page_number > 1:
        previous_page = int(page_number - 1)
        show_previous_page = True
    else:
        previous_page = 0
        show_previous_page = False
    
    if  page_number < num_pages:
        next_page = int(page_number + 1)
        show_next_page = True
    else:
        next_page = 0
        show_next_page = False
    
    page_numbers = range(0, num_pages)    
    
    return locals()