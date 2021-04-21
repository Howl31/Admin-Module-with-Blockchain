from django.shortcuts import render, redirect
from .models import UserDetail, HashTable
import hashlib
from next_prev import next_in_order, prev_in_order
from .blockchain import data_tamper

# Create your views here.


def home(request):
    user_data = UserDetail.objects.all()
    msg = data_tamper.check_data()
    return render(request, 'home.html', {'users': user_data, 'msg': msg})


def user_details(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_objects = UserDetail.objects.all()
        if len(user_objects) == 0:
            previous_hash = '0'
            current_hash_str = previous_hash+first_name+last_name+email
            current_hash = hashlib.md5(current_hash_str.encode()).hexdigest()
            user = UserDetail.objects.create(email=email, first_name=first_name, last_name=last_name)
            HashTable.objects.create(previous_hash=previous_hash, user=user, current_hash=current_hash)
            HashTable.objects.create(previous_hash=current_hash)
        else:
            hash_obj = HashTable.objects.last()
            previous_hash = hash_obj.previous_hash
            current_hash_str = previous_hash+first_name+last_name+email
            current_hash = hashlib.md5(current_hash_str.encode()).hexdigest()
            user = UserDetail.objects.create(email=email, first_name=first_name, last_name=last_name)
            hash_obj.user = user
            hash_obj.current_hash = current_hash
            hash_obj.save()
            HashTable.objects.create(previous_hash=current_hash)
    return render(request, 'user_form.html')


def update_details(request, pk):
    user_to_update = UserDetail.objects.get(id=pk)
    user = UserDetail.objects.get(id=pk)
    suppose = 'true'
    print("level 1")
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        print("user saved")
        while suppose == "true":
            hash_obj = HashTable.objects.get(user=user)
            prev_hash_obj = prev_in_order(hash_obj)
            if prev_hash_obj != None:
                # print("hi")
                prev_hash = prev_hash_obj.current_hash
                hash_str = prev_hash+user.first_name+user.last_name+user.email
                current_hash = hashlib.md5(hash_str.encode()).hexdigest()
                print(hash_obj.user, prev_hash, current_hash, " ", hash_str)
                hash_obj.previous_hash = prev_hash
                hash_obj.current_hash = current_hash
                hash_obj.save()
                print("hash object saved in not first node")
                user = next_in_order(user)
                # print(user)
                if user == None:
                    print(" false in not first node")
                    suppose = "false"
            else:
                # print('no prev')
                prev_hash = "0"
                hash_str = prev_hash+user.first_name+user.last_name+user.email
                current_hash = hashlib.md5(hash_str.encode()).hexdigest()
                print(hash_obj, prev_hash, current_hash, " ", hash_str)
                hash_obj.previous_hash = prev_hash
                hash_obj.current_hash = current_hash
                hash_obj.save()
                print("hash object saved in first node")
                user = next_in_order(user)
                # print(user)
                if user == None:
                    print(" false in first node")
                    suppose = "false"

        # updating last hash object
        last_hash_obj = HashTable.objects.last()
        prev_hash_of_last = prev_in_order(last_hash_obj).current_hash
        last_hash_obj.previous_hash = prev_hash_of_last
        last_hash_obj.save()
        print("last hash saved")
        return redirect('home')
    return render(request, 'update_detail.html', {'user': user_to_update})