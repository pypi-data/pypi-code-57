import random


def ImageUploadDestination(instance, filename):
    if filename:
        get_extension = filename.split('.')[-1]
        get_filename = random.randint(0, 1000000000000)
        new_filename = f"IMG{get_filename}.{get_extension}"
        return(f'djangopost/{instance.author.id}_{instance.author.username}/{new_filename}')