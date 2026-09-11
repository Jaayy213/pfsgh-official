from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RSVPForm
from django.contrib import messages
from django.db.models import Q
from .models import RSVP
from django.contrib.auth.decorators import login_required, user_passes_test


# Event RSVP page
def product_launch(request):
    context = {

    }
    return render(request, 'main/product_launch.html', context)



# RSVP Form Submission
def rsvp_view(request):
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            rsvp = form.save()
            if rsvp.attendance == 'yes':
                messages.success(
                    request,
                    f"Thank you, {rsvp.first_name}! Your seat for the PFS Product Launch has been reserved successfully.",
                )
            else:
                messages.info(
                    request,
                    f"Thank you, {rsvp.first_name}. We have recorded your response and hope to see you at future events.",
                )
            return redirect('rsvp_submit')
        else:
            messages.error(
                request,
                "There was an issue processing your submission. Please check the form fields and try again.",
            )
    else:
        form = RSVPForm()

    context = {
        'form': form,
    }

    return render(request, 'main/product_launch.html', context)


def is_staff_user(user):
    return user.is_active and user.is_staff


@login_required
@user_passes_test(is_staff_user)
def rsvp_dashboard(request):
    """ Custom Admin Dashboard to list, search, and filter RSVPs """
    query = request.GET.get('q', '')
    attendance_filter = request.GET.get('attendance', '')

    rsvps = RSVP.objects.all()

    # Search functionality
    if query:
        rsvps = rsvps.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query) |
            Q(phone__icontains=query)
        )

    # Filter functionality
    if attendance_filter in ['yes', 'no']:
        rsvps = rsvps.filter(attendance=attendance_filter)

    # Counts for summary metrics
    total_rsvps = RSVP.objects.count()
    attending_count = RSVP.objects.filter(attendance='yes').count()
    declined_count = RSVP.objects.filter(attendance='no').count()

    context = {
        'rsvps': rsvps,
        'query': query,
        'attendance_filter': attendance_filter,
        'total_rsvps': total_rsvps,
        'attending_count': attending_count,
        'declined_count': declined_count,
    }
    return render(request, 'blog/dashboard/rsvp_dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
def rsvp_edit(request, pk):
    """ View to edit a single RSVP entry """
    rsvp = get_object_or_404(RSVP, pk=pk)
    
    if request.method == 'POST':
        form = RSVPForm(request.POST, instance=rsvp)
        if form.is_valid():
            form.save()
            messages.success(request, f"RSVP for {rsvp.first_name} {rsvp.last_name} updated successfully.")
            return redirect('rsvp_dashboard')
    else:
        form = RSVPForm(instance=rsvp)

    context = {
        'form': form,
        'rsvp': rsvp,
    }

    return render(request, 'blog/dashboard/rsvp_edit.html', context)


@login_required
@user_passes_test(is_staff_user)
def rsvp_delete(request, pk):
    """ View to delete an RSVP entry """
    rsvp = get_object_or_404(RSVP, pk=pk)
    if request.method == 'POST':
        name = f"{rsvp.first_name} {rsvp.last_name}"
        rsvp.delete()
        messages.warning(request, f"RSVP record for {name} has been deleted.")
        return redirect('rsvp_dashboard')

    context = {
        'rsvp': rsvp,
    }
    
    return render(request, 'blog/dashboard/rsvp_confirm_delete.html', context)