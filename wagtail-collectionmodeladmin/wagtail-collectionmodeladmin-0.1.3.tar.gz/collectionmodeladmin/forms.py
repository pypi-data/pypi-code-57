def get_permission_panel():

    return collection_member_permission_formset_factory(
    VideoModal,
    [
        ('add_videomodal', _("Add"), _("Add/edit video modals you own")),
        ('change_videomodal', _("Edit"), _("Edit any video modal")),
    ],
    'videomodal/permissions/includes/videomodal_permission_formset.html'
)