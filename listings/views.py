from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .choices import bedroom_choices, price_choices, state_choices
from .models import Listing


# Create your views here.
def index(request):
    # listings=Listing.objects.all()
    # if filter of pages by date  and filter by publish date
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listing = paginator.get_page(page)
    context = {
        'listings': paged_listing
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('list_date')
    # search by keyword or word in the description
    if 'keyword' in request.GET:
        keywords = request.GET['keyword']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # filter by city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

        # filter by State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # filter by bedrooms
    # filter by price

    context = {
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'listings': queryset_list,
        'values': request.GET  # for preserve word in search page
    }
    return render(request, 'listings/search.html', context)
