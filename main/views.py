from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .models import User, Post, Rating, Auction
from django.http import HttpResponse, JsonResponse
from django.contrib import messages


class HomePageView(ListView):
    def get(self, request):
        all_posts = Post.objects.all().order_by('-id')
        param = {'posts': all_posts}
        return render(request, 'main/home.html', param)

    def post(self, request):
        user_name = request.POST['uname']
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        print(user_name)
        print(pwd1)
        print(pwd2)
        if pwd1 == pwd2:
            add_user = User(username=user_name, password=pwd1)
            add_user.save()
            messages.success(request, 'Konto zostało stworzone')
            return redirect('home')
        else:
            messages.warning(request, 'Hasła nie są takie same')
            return redirect('home')


class UploadView(ListView):
    def get(self, request, user_name):
        return render(request, 'main/upload_file.html')

    def post(self, request, user_name):
        image = request.FILES['image']
        title = request.POST['title']
        price = request.POST['price']
        description = request.POST['description']

        user_obj = User.objects.get(username=user_name)
        upload_post = Post(user=user_obj, title=title, image=image, description=description, price=price)
        upload_post.save()
        messages.success(request, 'Obraz został dodany, czekaj na potwierdzenie admina')
        return render(request, 'main/upload_file.html')


class ProfileView(ListView):
    def get(self, request, user_name):
        user_obj = User.objects.get(username=user_name)
        user_posts = user_obj.post_set.all().order_by('id')
        param = {'user_data': user_obj, 'user_posts': user_posts}
        return render(request, 'main/profile.html', param)


class DeleteView(ListView):
    model = Post

    def get(self, request, post_id):
        user = request.session['user']
        delete_post = self.model.objects.get(id=post_id)
        delete_post.delete()
        messages.success(request, 'Twój obraz został usunięty z bazy')
        return redirect(f'/profile/{user}')


class SearchView(ListView):
    def get(self, request):
        query = request.GET['query']
        search_users = User.objects.filter(username__icontains=query)
        search_title = Post.objects.filter(title__icontains=query)
        search_desc = Post.objects.filter(description__icontains=query)
        search_result = search_title.union(search_desc)
        param = {'query': query, 'search_result': search_result, 'search_users': search_users}
        return render(request, 'main/search.html', param)


class LoginView(ListView):
    def get(self, request):
        return redirect('home')

    def post(self, request):
        user_name = request.POST['uname']
        pwd = request.POST['pwd']

        user_exists = User.objects.filter(username=user_name, password=pwd).exists()
        if user_exists:
            request.session['user'] = user_name
            messages.success(request, 'Jesteś zalogowany.')
            return redirect('home')
        else:
            messages.warning(request, 'Nieprawidłowa nazwa użytkownika lub hasło')
            return redirect('home')
        return redirect('home')


class LogoutView(ListView):
    def get(self, request):
        try:
            del request.session['user']
        except:
            return redirect('home')
        return redirect('home')


class ViewImage(ListView):
    def get(self, request, post_id):
        image_info = Post.objects.get(pk=post_id)
        return render(request, 'main/image.html', {'image_info': image_info})

    def rate_image(request):
        if request.method == 'POST':
            post_id = request.POST.get('el_id')
            user_name = request.session['user']
            post_obj = Post.objects.get(pk=post_id)

            score = request.POST.get('val')
            user_obj = User.objects.get(username=user_name)
            print(post_id)
            print(score)
            print(user_obj.pk)

            rate_score = Rating(user=user_obj, post=post_obj, score=score)
            rate_score.save()
            return JsonResponse({'success': 'true', 'score': score}, safe=False)
        return JsonResponse({'success': 'false'})


class ViewAction(ListView):
    model = Auction

    def set_auction(self, request, post_id):
        param = request.POST.get('post_id')
        post_obj = Post.objects.get(pk=post_id)
        user = request.session['user']
        return render(request, 'au.html', param)













