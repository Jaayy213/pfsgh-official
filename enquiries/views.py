from django.shortcuts import render, redirect, get_object_or_404
from .forms import EnquiryForm, EnquiryCommentForm
from .models import Enquiry, EnquiryComment
import openpyxl
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count



def is_staff_user(user):
    return user.is_active and user.is_staff


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



@login_required
@user_passes_test(is_staff_user)
def enquiry_dashboard(request):
    base_enquiries = Enquiry.objects.all()
    total_count = base_enquiries.count()

    # Initialize ALL statuses to 0
    statuses_dict = dict(Enquiry.STATUS_CHOICES)
    all_status_counts = {key: 0 for key in statuses_dict.keys()}
    
    # Populate actual status counts
    status_queryset = base_enquiries.values('status').annotate(total=Count('id'))
    for item in status_queryset:
        if item['status'] in all_status_counts:
            all_status_counts[item['status']] = item['total']

    # KPI Card metrics
    new_count = all_status_counts.get('new', 0)
    contacted_count = all_status_counts.get('contacted', 0)
    paid_count = all_status_counts.get('paid', 0)
    closed_count = all_status_counts.get('closed', 0)

    contacted_pct = round((contacted_count / total_count * 100)) if total_count else 0
    paid_pct = round((paid_count / total_count * 100)) if total_count else 0
    closed_pct = round((closed_count / total_count * 100)) if total_count else 0

    # Build List for Status Breakdown
    status_stats = []
    for key, label in Enquiry.STATUS_CHOICES:
        cnt = all_status_counts[key]
        pct = round((cnt / total_count * 100)) if total_count else 0
        status_stats.append({
            'key': key,
            'label': label,
            'count': cnt,
            'pct': pct
        })

    status_stats.sort(key=lambda x: x['count'], reverse=True)

    # Initialize ALL services to 0
    services_dict = dict(Enquiry.SERVICE_CHOICES)
    all_service_counts = {key: 0 for key in services_dict.keys()}

    # Populate actual service counts
    service_queryset = base_enquiries.values('service_required').annotate(total=Count('id'))
    for item in service_queryset:
        if item['service_required'] in all_service_counts:
            all_service_counts[item['service_required']] = item['total']

    # Build List for Service Breakdown
    service_stats = []
    for key, label in Enquiry.SERVICE_CHOICES:
        cnt = all_service_counts[key]
        pct = round((cnt / total_count * 100)) if total_count else 0
        service_stats.append({
            'key': key,
            'label': label,
            'count': cnt,
            'pct': pct
        })

    service_stats.sort(key=lambda x: x['count'], reverse=True)

    # Filter Table Results
    filtered_enquiries = base_enquiries.order_by("-created_at")
    selected_service = request.GET.get('service', '')
    selected_status = request.GET.get('status', '')

    if selected_service:
        filtered_enquiries = filtered_enquiries.filter(service_required=selected_service)
    if selected_status:
        filtered_enquiries = filtered_enquiries.filter(status=selected_status)

    # --- PAGINATION ---
    paginator = Paginator(filtered_enquiries, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "enquiries": page_obj,
        "page_obj": page_obj,
        "services": Enquiry.SERVICE_CHOICES,
        "statuses": Enquiry.STATUS_CHOICES,
        "selected_service": selected_service,
        "selected_status": selected_status,
        "total_count": total_count,
        "new_count": new_count,
        "contacted_count": contacted_count,
        "paid_count": paid_count,
        "closed_count": closed_count,
        "contacted_pct": contacted_pct,
        "paid_pct": paid_pct,
        "closed_pct": closed_pct,
        "status_stats": status_stats,
        "service_stats": service_stats,
    }

    return render(request, "blog/dashboard/enquiries.html", context)


@login_required
@user_passes_test(is_staff_user)
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


@login_required
@user_passes_test(is_staff_user)
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



@login_required
@user_passes_test(is_staff_user)
def create_comment(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk)

    form = EnquiryCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.enquiry = enquiry
        comment.author = request.user
        comment.save()

        context = {
            "enquiry": enquiry,
        }

        html = render(request, "blog/dashboard/partials/enquiry_comments.html", context).content.decode()

        return JsonResponse({
            "success": True,
            "html": html,
        })
    return JsonResponse({
        "success": False,
        "errors": form.errors,
    })


@login_required
@user_passes_test(is_staff_user)
def update_comment(request, pk):
    comment = get_object_or_404(EnquiryComment, pk=pk)

    form = EnquiryCommentForm(request.POST, instance=comment)

    if form.is_valid():
        form.save()

        context = {
            "enquiry": comment.enquiry
        }

        html = render(request, "blog/dashboard/partials/enquiry_comments.html", context).content.decode()

        return JsonResponse({
            "success": True,
            "html": html,
        })
    return JsonResponse({
        "success": False,
        "errors": form.errors,
    })


@login_required
@user_passes_test(is_staff_user)
def delete_comment(request, pk):
    comment = get_object_or_404(EnquiryComment, pk=pk)

    enquiry = comment.enquiry
    comment.delete()

    context = {
        "enquiry": enquiry,
    }

    html = render(
        request,
        "blog/dashboard/partials/enquiry_comments.html", context).content.decode()

    return JsonResponse({
        "success": True,
        "html": html,
    })