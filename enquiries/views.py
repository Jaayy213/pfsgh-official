from django.shortcuts import render, redirect
from .forms import EnquiryForm
from .models import Enquiry
import openpyxl
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def enquiry_view(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("enquiry_success")
    else:
        form = EnquiryForm()

    context = {
        "form": form,
    }

    return render(request, "enquiries/enquiry_form.html", context)


def enquiry_success(request):
    return render(request, "enquiries/success.html")


def enquiry_dashboard(request):
    enquiries = Enquiry.objects.all().order_by("-created_at")

    # Filtering
    services = Enquiry.SERVICE_CHOICES
    selected_service = request.GET.get('service', '')
    if selected_service:
        enquiries = enquiries.filter(service_required=selected_service)

    context = {
        "enquiries": enquiries,
        'services': services,
        'selected_service': selected_service,
    }

    return render(request, "blog/dashboard/enquiries.html", context)


def export_enquiries(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Enquiries"

    # Headers
    headers = [
        "First Name",
        "Last Name",
        "Company",
        "Service",
        "Phone",
        "Email",
        "Region",
        "Address",
        "Social Platform",
        "Social Handle",
        "Other Enquiry",
        "Date",
    ]

    ws.append(headers)

    # Data
    for enquiry in Enquiry.objects.all():
        ws.append([
            enquiry.first_name,
            enquiry.last_name,
            enquiry.company_name,
            enquiry.get_service_required_display(),
            enquiry.phone_number,
            enquiry.region,
            enquiry.email,
            enquiry.address,
            enquiry.get_social_platform_display() if enquiry.social_platform else "",
            enquiry.social_handle,
            enquiry.other_enquiry,
            enquiry.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    # Response
    response = HttpResponse(
        content_type="application/ms-excel"
    )
    response["Content-Disposition"] = 'attachment; filename="enquiries.xlsx"'

    wb.save(response)
    return response


@require_POST
def update_enquiry_status(request):
    enquiry_id = request.POST.get("enquiry_id")
    new_status = request.POST.get("status")

    if not enquiry_id or not new_status:
        return JsonResponse({"success": False, "message": "Missing data."})

    try:
        enquiry = Enquiry.objects.get(id=enquiry_id)
        enquiry.status = new_status
        enquiry.save()
        return JsonResponse({"success": True, "status": new_status})
    except Enquiry.DoesNotExist:
        return JsonResponse({"success": False, "message": "Enquiry not found."})