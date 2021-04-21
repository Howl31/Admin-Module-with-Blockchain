from ..models import *
from next_prev import next_in_order, prev_in_order
import hashlib


def check_data():
    all_user_obj = UserDetail.objects.all()
    data_tampered = []
    error = 0
    for count, user in enumerate(all_user_obj):
        hash_obj = HashTable.objects.get(user=user)
        if count == 0:
            previous_hash = '0'
            hash_str = previous_hash+user.first_name+user.last_name+user.email
            current_hash = hashlib.md5(hash_str.encode()).hexdigest()
            # next_hash_obj = next_in_order(hash_obj)
            if current_hash != hash_obj.current_hash:
                error += 1
                data_tampered.append(user)
        else:
            previous_hash = prev_in_order(hash_obj).current_hash
            hash_str = previous_hash+user.first_name+user.last_name+user.email
            current_hash = hashlib.md5(hash_str.encode()).hexdigest()
            # next_hash_obj = next_in_order(hash_obj)
            if current_hash != hash_obj.current_hash:
                error += 1
                data_tampered.append(user)
    if error == 0:
        message = "safe"
    else:
        message = "tampered"
    return message





    # all_hash_objects = HashTable.objects.all()
    # count = 0
    # while count <= len(all_hash_objects):
    #     hash_obj = HashTable.objects.first()
    #     user = hash_obj.user
    #     prev_user = prev_in_order(user)
    #     if prev_user == None:
    #         previous_hash = '0'
    #         hash_str = previous_hash+user.first_name+user.last_name+user.email
    #         current_hash = hashlib.md5(hash_str.encode()).hexdigest()
    #         if current_hash == hash_obj.current_hash:
    #             message = "Data Is Safe"
    #             return message
    #         else:
    #             message = "Data Tampering Detected"
    #             return message
    #     else:
    #         previous_hash = prev_user.current_hash
    #         hash_str = previous_hash+user.first_name+user.last_name+user.email
    #         current_hash = hashlib.md5(hash_str.encode()).hexdigest()