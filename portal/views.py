from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserRegistrationForm, DiaryForm
from .models import Diary
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User



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
    model = Diary()
    template_name = 'portal/diary.html'
    context_object_name = 'diary_detail'
    def get_queryset(self):
        if self.request.user.has_perm('diary.add_mark'):
            return Diary.objects.all().order_by('student__username','grade')
        return Diary.objects.filter(student = self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_grade']=self.get_queryset()
        context['has_add_mark_permission'] = self.request.user.has_perm('diary.add_mark')
        if context['has_add_mark_permission']:
            context['add_mark'] = DiaryForm()
            context['add_mark'].fields['student'].queryset = User.objects.exclude(id=self.request.user.id)
        else: 
            context['add_mark'] = None
        return context
    def post(self, request, *args, **kwargs):
        form = DiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary')
        return self.render_to_response(self.get_context_data(form=form))

class GradeUpdateView(UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'portal/diary.html'
    success_url = reverse_lazy('diary')
    def form_valid(self,form):
        response = super().form_valid(form)
        return response

class GradeDeleteView(DeleteView):
    model = Diary
    template_name = 'portal/delete_grade.html'
    success_url = reverse_lazy('diary')
