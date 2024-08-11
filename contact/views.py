from django.shortcuts import render, redirect
from store.models import Product, ReviewRating
from .forms import ContactForm
from .models import Contact
from django.core.mail import EmailMessage
from django.contrib import messages
from django.template.loader import render_to_string
import mengcraft.settings


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = Contact()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.contact_note = form.cleaned_data['contact_note']

            #message to Meng
            mail_subject_admin = f'You received a message from {data.name}'
            message_admin = render_to_string("contact/contact_form_admin.html", {
                "name": data.name,
                "email": data.email,
                "contact_note": data.contact_note,
            })
            to_email = mengcraft.settings.EMAIL_HOST_USER
            send_email = EmailMessage(mail_subject_admin, message_admin, to=[to_email])
            send_email.send()

            #message to user

            mail_subject_user = "Thank your for your message - Mengcraft"
            message_user = render_to_string("contact/contact_form_user.html", {
                "name": data.name,
                "contact_note": data.contact_note
            })
            user_email = data.email
            send_email = EmailMessage(mail_subject_user, message_user, to=[user_email])
            send_email.send()

            messages.success(request, "Thank you for your message. We will be back to you shortly")
            return redirect('contact')
        else:
            return redirect('contact')

    return render(request, "contact/contact.html")
