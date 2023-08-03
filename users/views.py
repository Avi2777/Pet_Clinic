from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from users.forms import CustomUserChangeForm

User = get_user_model()


# --- Profile Update View ---
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('core:dashboard')

    def get_object(self):
        # Fetch the user instance based on the provided 'pk' (user ID) in the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)

    def get(self, request, *args, **kwargs):
        # Save the previous URL in the session
        request.session['previous_url'] = request.META.get('HTTP_REFERER', self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile updated successfully.')  # Optional: Show success message
        return redirect(self.get_success_url())

    def get_success_url(self):
        # Return the previous URL saved in the session or the default success URL
        return self.request.session.get('previous_url', self.success_url)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/profile_delete.html'
    success_url = reverse_lazy('core:dashboard')

    def get_object(self, queryset=None):
        # Fetch the user instance based on the provided 'pk' (user ID) in the URL
        pk = self.kwargs.get('pk')
        return get_user_model().objects.get(pk=pk)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect(self.success_url)
        else:
            # Delete the user and redirect to the success URL
            return self.delete(request, *args, **kwargs)