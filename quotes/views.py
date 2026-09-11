import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import QuoteRequest
from .forms import QuoteRequestForm

logger = logging.getLogger(__name__)


def is_staff_user(user):
    return user.is_active and user.is_staff


# --- PUBLIC API ROUTE ---

@require_POST
def submit_quote(request):
    form = QuoteRequestForm(request.POST)

    if form.is_valid():
        quote = form.save()

        # Build notification email content
        services_list = ", ".join(quote.services)
        subject = f"New Quote Request: {quote.first_name} {quote.last_name} ({quote.company})"
        message = (
            f"You have received a new quote request.\n\n"
            f"--- CONTACT INFORMATION ---\n"
            f"Name: {quote.first_name} {quote.last_name}\n"
            f"Email: {quote.email}\n"
            f"Phone: {quote.phone}\n"
            f"Company: {quote.company}\n"
            f"Industry: {quote.get_industry_display() if quote.industry else 'N/A'}\n\n"
            f"--- SERVICES NEEDED ---\n"
            f"{services_list}\n\n"
            f"--- PROJECT DETAILS ---\n"
            f"Description:\n{quote.project_description}\n\n"
            f"Timeline: {quote.get_timeline_display() if quote.timeline else 'N/A'}\n"
            f"Budget: {quote.get_budget_display() if quote.budget else 'N/A'}\n"
            f"Priority: {quote.get_priority_display() if quote.priority else 'N/A'}\n\n"
            f"Additional Info:\n{quote.additional_info or 'None'}\n"
        )

        try:
            recipient = getattr(settings, 'ADMIN_EMAIL_NOTIFICATION', settings.DEFAULT_FROM_EMAIL)
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification for Quote ID {quote.id}: {e}")

        return JsonResponse({
            'success': True,
            'message': 'Your quote request has been successfully submitted.'
        })

    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)


# --- ADMIN DASHBOARD CRUD VIEWS ---

@login_required
@user_passes_test(is_staff_user)
def quote_dashboard(request):
    """List all quote requests with filtering and search."""
    quotes = QuoteRequest.objects.all()

    # Filters
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    search_query = request.GET.get('q')

    if status_filter == 'processed':
        quotes = quotes.filter(is_processed=True)
    elif status_filter == 'pending':
        quotes = quotes.filter(is_processed=False)

    if priority_filter in ['low', 'medium', 'high']:
        quotes = quotes.filter(priority=priority_filter)

    if search_query:
        quotes = quotes.filter(
            first_name__icontains=search_query
        ) | quotes.filter(
            last_name__icontains=search_query
        ) | quotes.filter(
            company__icontains=search_query
        ) | quotes.filter(
            email__icontains=search_query
        )

    context = {
        'quotes': quotes,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search_query': search_query,
        'total_quotes': QuoteRequest.objects.count(),
        'pending_quotes': QuoteRequest.objects.filter(is_processed=False).count(),
        'processed_quotes': QuoteRequest.objects.filter(is_processed=True).count(),
    }
    return render(request, 'blog/dashboard/quotes.html', context)


@login_required
@user_passes_test(is_staff_user)
def quote_detail(request, pk):
    """View full details of a specific quote request."""
    quote = get_object_or_404(QuoteRequest, pk=pk)

    context = {
        'quote': quote,
    }
    return render(request, 'blog/dashboard/quote_detail.html', context)


@login_required
@user_passes_test(is_staff_user)
@require_POST
def toggle_quote_processed(request, pk):
    """Toggle the processed status of a quote request."""
    quote = get_object_or_404(QuoteRequest, pk=pk)
    quote.is_processed = not quote.is_processed
    quote.save()
    status_str = "processed" if quote.is_processed else "pending"
    messages.success(request, f"Quote request from {quote.first_name} ({quote.email}) marked as {status_str}.")
    return redirect(request.META.get('HTTP_REFERER', 'quote_dashboard'))


@login_required
@user_passes_test(is_staff_user)
@require_POST
def delete_quote(request, pk):
    """Delete a quote request."""
    quote = get_object_or_404(QuoteRequest, pk=pk)
    quote.delete()
    messages.success(request, f"Quote request from {quote.first_name} ({quote.email}) deleted successfully.")
    return redirect('quote_dashboard')