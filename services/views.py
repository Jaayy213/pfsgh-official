from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ServiceRequestForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import ServiceRequest


def service_request_view(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

            # --- 1. Admin Email Notification ---
            admin_subject = f"New Service Request: {instance.ref_number}"
            admin_message = f"""
New Service Request Received!

Reference: {instance.ref_number}
Service Choice: {instance.get_service_choice_display()}
Client Name: {instance.full_name_or_company}
Phone: {instance.phone}
Email: {instance.email}
Address: {instance.business_address}
Registration Status: {instance.registration_status}

Preferred Start Date: {instance.preferred_start_date}
Target Completion Date: {instance.target_completion_date}
Indicative Budget: {instance.indicative_budget}
            """
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.PFS_NOTIFY_EMAIL],
                fail_silently=False,
            )

            # --- 2. Client Auto-Confirmation Email ---
            client_subject = f"PFS Service Request Confirmation - [{instance.ref_number}]"
            client_message = f"""
Hello {instance.full_name_or_company},

Thank you for contacting Pneuma Food Scientifics (PFS).

We have received your service request ({instance.ref_number}). Our team is reviewing your specifications and will contact you shortly.

If you have urgent questions, feel free to reach out directly via phone or WhatsApp at 020 793 5696 / +233 24 104 3139.

Best regards,
Pneuma Food Scientifics
            """

            send_mail(
                subject=client_subject,
                message=client_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=True,
            )

            return render(request, 'services/request_success.html', {'ref_number': instance.ref_number})
    else:
        initial_service = request.GET.get('service', 'A').upper()
        if initial_service not in ['A', 'B', 'C']:
            initial_service = 'A'
        form = ServiceRequestForm(initial={'service_choice': initial_service})

    return render(request, 'services/request_form.html', {'form': form})


@staff_member_required
def service_request_dashboard(request):
    """List all submitted requests with search and filter options"""
    requests_list = ServiceRequest.objects.all().order_by('-created_at')
    
    # Optional Filters
    service_filter = request.GET.get('service')
    if service_filter:
        requests_list = requests_list.filter(service_choice=service_filter)
        
    search_query = request.GET.get('q')
    if search_query:
        requests_list = requests_list.filter(
            full_name_or_company__icontains=search_query
        ) | requests_list.filter(ref_number__icontains=search_query)

    context = {
        'service_requests': requests_list,
        'total_count': requests_list.count(),
    }
    return render(request, 'blog/dashboard/services.html', context)


@staff_member_required
def service_request_detail(request, pk):
    """View full submission details"""
    service_req = get_object_or_404(ServiceRequest, pk=pk)
    return render(request, 'blog/dashboard/services_detail.html', {'req': service_req})


@staff_member_required
def service_request_delete(request, pk):
    """Delete a service request"""
    service_req = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        ref = service_req.ref_number
        service_req.delete()
        messages.success(request, f"Service Request {ref} deleted successfully.")
        return redirect('service_request_dashboard')
    return render(request, 'blog/dashboard/services_confirm_delete.html', {'req': service_req})