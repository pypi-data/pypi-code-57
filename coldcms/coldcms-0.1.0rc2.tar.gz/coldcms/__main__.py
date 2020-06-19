if __name__ == "__main__":

    import os

    import django  # noqa
    from coldcms.wsgi import application
    from django.core.management import call_command
    from django.conf import settings
    from waitress import serve
    from whitenoise import WhiteNoise

    print(" ------------------------------------------------------ ")
    print("| ColdCMS quick launch                                 |")
    print("| This will start a WhiteNoise server                  |")
    print("| You can have better performance with an Nginx server |")
    print(" ------------------------------------------------------ ")

    print("App loading...")
    print("This can take a few seconds")

    os.environ["DJANGO_SETTINGS_MODULE"] = "coldcms.settings.production"

    django.setup()

    if os.environ.get("RUN_DJANGO_MIGRATION") != "0":
        call_command("migrate", no_input=True, verbosity=0)

    if os.environ.get("SETUP_INITIAL_DATA") != "0":
        print("Setting up initial data on your website...")
        call_command("setup_initial_data", "--noconfirm")

    if os.environ.get("CREATE_SUPERUSER") != "0":
        print("Create your admin data")
        call_command("createsuperuser")

    # starting app
    wsgiapp = WhiteNoise(application, root=settings.STATIC_ROOT, prefix="static")

    print("HTTP service listening on port 8080...")
    print("Go to http://localhost:8080")
    serve(wsgiapp, host="0.0.0.0", port=8080, _quiet=True)
