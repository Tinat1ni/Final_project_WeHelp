from django.views.generic import TemplateView, UpdateView, FormView, ListView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from post.models import Post
from .models import Profile
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.conf import settings
import random
from .forms import  VerificationForm, RegistrationForm
from post.forms import PostForm
import requests
from .tasks import send_post_choice_email, send_welcome_email


class HomeView(TemplateView):
    template_name = 'index.html'

class RegisterView(FormView):
    template_name = 'new_registration.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']

        confirmation_code = random.randint(100000, 999999)

        registration_data = {
            'phone_number': phone_number,
            'username': username,
            'password': password,
            'email': email
        }
        self.request.session['registration_data'] = registration_data
        self.request.session['confirmation_code'] = confirmation_code

        self.send_confirmation_sms(phone_number, confirmation_code)

        messages.success(self.request, 'კოდი გამოგზავნილია')

        return redirect('user:verify_code')

    def send_confirmation_sms(self, phone_number, confirmation_code):
        username = 'tinatingagnidze'
        password = 'mU2xVloUZv'
        client_id = 1088
        service_id = 2967

        url = 'https://bi.msg.ge/sendsms.php'

        params = {
            'username': username,
            'password': password,
            'client_id': client_id,
            'service_id': service_id,
            'to': phone_number,
            'text': f'თქვენი კოდი: {confirmation_code} ',
            'utf': 1,
            'result': 'json'
        }

        try:
            response = requests.get(url, params=params)

            response_data = response.json()

            if response_data.get('error'):
                raise ValueError(f'SMS API Error: {response_data['error']}')

            code = response_data.get('code', '')
            if code != 0:
                raise ValueError(f'SMS not sent: {response_data}')
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'Failed to send SMS: {str(e)}')

    def form_invalid(self, form):
        return super().form_invalid(form)


class VerificationView(FormView):
    template_name = 'verification_form.html'
    form_class = VerificationForm

    def form_valid(self, form):
        entered_code = form.cleaned_data['confirmation_code']

        correct_code = self.request.session.get('confirmation_code')

        if str(entered_code) == str(correct_code):
            registration_data = self.request.session.get('registration_data')
            if registration_data:
                User = get_user_model()

                user = User.objects.create_user(
                    username=registration_data['username'],
                    email=registration_data['email'],
                    password=registration_data['password']
                )
                user.phone_number = registration_data['phone_number']
                user.save()

                send_welcome_email.delay(
                    user_email=user.email,
                    username=user.username,
                )

                del self.request.session['registration_data']
                del self.request.session['confirmation_code']

                return redirect('user:login')

        else:
            messages.error(self.request, 'კოდი არასწორია')
            return super().form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ChoosePostView(LoginRequiredMixin, View):
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        volunteer_profile = request.user.profile

        if post.author == request.user:
            messages.error(request, 'თქვენ ვერ აირჩევთ საკუთარ პოსტს.')
            return redirect('post:detail', pk=post.pk)

        volunteer_profile.chosen_posts.add(post)

        subject = f'თქვენ აირჩიეთ პოსტი: {post.title}'
        message = f'პოსტის ავტორი: {post.author.username}\nტელეფონის ნომერი: {post.author.phone_number} '
        recipient_email = request.user.email

        subject_for_author = 'თქვენი პოსტი აირჩია მოხალისემ'
        author_message = f"თქვენი პოსტი '{post.title}' აირჩია მოხალისემ: {request.user.username}.\n შეგახსენებთ, მოხალისის მიერ დახმარების გაწევის შემდეგ მონიშნეთ პოსტი როგორც დასრულებული"
        recipient_email_author = post.author.email

        send_post_choice_email.delay(subject, message, recipient_email)
        send_post_choice_email.delay(subject_for_author, author_message, recipient_email_author)


        messages.success(request, 'თქვენ აირჩიეთ პოსტი')
        return redirect('post:detail', pk=post.pk)


class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            if self.request.user.is_authenticated:
                category = self.request.GET.get('category',
                                                'user_posts')
                if category == 'chosen_posts':
                    posts = self.request.user.profile.chosen_posts.all().order_by('-created_at')
                else:
                    posts = Post.objects.filter(author=self.request.user).select_related('author').order_by('-created_at')

                context['posts'] = posts
                context['category'] = category
            else:
                context['posts'] = []
                context['category'] = 'user_posts'

            return context

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')

        if post_id and action:
            post = get_object_or_404(Post, id=post_id, author=request.user)

            if action == 'delete':
                post.delete()
            elif action == 'mark_completed' and not post.completed:
                post.completed = True
                post.save()

        return redirect('user:profile')


class PostEditView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, id=self.kwargs['pk'], author=self.request.user)


