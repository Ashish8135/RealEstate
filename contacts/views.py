from django.contrib import messages
# from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect

# Create your views here.
from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/'+listing_id)

        contacts = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message,
                           user_id=user_id)
        contacts.save()
        # Send mail
        send_mail(
            'Property listing inquiry',
            'There has been inquiry for ' + listing + '.please sign to this link for complete your profile',
            'ashish.shaivya10@gmail.com',
            [realtor_email,'amitsin403@gmail.com','vishalsah09@gmail.com','anitajoshi4846@gmail.com'],
            fail_silently=False
        )

        messages.success(request, "Thank You ! Your request has been submitted ,a realtor will get back to you soon")
        # return redirect('/listings/')
        return render(request, 'contact/Thank.html')
