def can_user_modify_dataset(user, dataset):
    return dataset.is_public is False and dataset.user == user or user.is_superuser


def can_user_modify_annotation_set(user, annotation_set):
    is_owner = annotation_set.dataset.is_public is False and annotation_set.dataset.user == user
    is_admin = user.is_superuser

    return is_owner or is_admin
