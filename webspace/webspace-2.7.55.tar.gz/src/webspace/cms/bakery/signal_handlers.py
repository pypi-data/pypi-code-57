from wagtail.core.signals import page_published, page_unpublished


def handle_publish(sender, instance, **kwargs):
    from .abstract import WagtailPageBakeryModel
    if isinstance(instance, WagtailPageBakeryModel):
        instance.build()


def handle_unpublish(sender, instance, **kwargs):
    #  from .abstract import WagtailPageBakeryModel
    #  if isinstance(instance, WagtailPageBakeryModel):
    #    instance.unbuild()
    pass


def register_signal_handlers():
    page_published.connect(
        handle_publish, dispatch_uid='wagtailbakery_page_published')
    page_unpublished.connect(
        handle_unpublish, dispatch_uid='wagtailbakery_page_unpublished')
