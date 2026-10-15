from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserRegistrationForm, DiaryForm, AddSubjectForm
from .models import Diary, Accounts, Subject
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied



def home(request):
    return render(request,"portal/home.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request,"portal/register.html",{"form": form})

class DiaryView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = 'portal/diary.html'
    context_object_name = 'diary_detail'
    add_perm = 'portal.add_diary'

    def can_add(self):
        return self.request.user.has_perm(self.add_perm)

    def build_form(self, data=None):
        form = DiaryForm(data)
        form.fields['student'].queryset = Accounts.objects.exclude(user=self.request.user)
        return form

    def get_queryset(self):
        qs = Diary.objects.select_related('student', 'subject')
        if self.can_add():
            return qs.order_by('student__name', 'grade')
        return qs.filter(student__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        can_add = self.can_add()
        context['has_add_mark_permission'] = can_add
        context['add_mark'] = (
            kwargs.get('add_mark_form') or self.build_form()
        ) if can_add else None
        return context

    def post(self, request, *args, **kwargs):
        if not self.can_add():
            raise PermissionDenied

        form = self.build_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary')

        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(add_mark_form=form))

class GradeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'portal.change_diary'
    model = Diary
    form_class = DiaryForm
    template_name = 'portal/diary.html'
    success_url = reverse_lazy('diary')
    def form_valid(self,form):
        response = super().form_valid(form)
        return response

class GradeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'portal.delete_diary'
    model = Diary
    template_name = 'portal/delete_grade.html'
    success_url = reverse_lazy('diary')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
  
        account, created = Accounts.objects.get_or_create(
            user=self.request.user,
            defaults={'name': self.request.user.username, 'secondname': ''}
        )
        context['account'] = account

        if self.request.user.has_perm('portal.add_subject'):
            context['has_add_subject_permission'] = True
        else:
            context['has_add_subject_permission'] = False
            
        return context

class AddSubjectView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'portal.add_subject'
    model = Subject
    form_class = AddSubjectForm
    template_name = 'portal/subject.html'
    success_url = reverse_lazy('diary')
