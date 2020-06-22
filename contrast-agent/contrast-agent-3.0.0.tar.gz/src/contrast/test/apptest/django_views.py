# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Definitions of view functions that can be used in django app tests.
"""
import base64
import io
import json
import os
import pickle
import subprocess


import six  # pylint: disable=did-not-import-extern
from six.moves import http_client as http  # pylint: disable=did-not-import-extern
import mock
import yaml

from django import __version__ as django_version
from django.contrib.auth import logout as DjangoLogout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from pymongo import MongoClient

try:
    from app.models import Message
except ImportError:
    Message = None

from app import settings

try:
    from app.jinja2_env import environment as jinja2_environment

    JINJA_ENV = jinja2_environment()
except ImportError:
    JINJA_ENV = None


if six.PY2:
    import urllib
    import urllib2
else:
    import urllib.request

# This ends up resolving to a path relative to the apptest dir so that we don't
# have to package this data file with the contrast module.
DATA_DIR = os.path.join("..", "data")


def static_image(request):
    filename = request.GET.get("filename", "image.jpg")
    image_path = os.path.join(DATA_DIR, filename)
    with open(image_path, "rb") as image_fh:
        return StreamingHttpResponse(image_fh.readlines(), content_type="image/jpeg")


def django_autoescape(request):
    """Uses a django template with autoescaping (enabled by default)"""
    user_input = request.GET.get("user_input", "")
    return render(request, "xss.html", {"user_input": user_input}, using="django")


def django_autoescape_safe(request):
    """Uses a django template with autoescaping but marks value as safe"""
    user_input = request.GET.get("user_input", "")
    return render(
        request, "xss_autoescape_safe.html", {"user_input": user_input}, using="django"
    )


def django_no_autoescape(request):
    user_input = request.GET.get("user_input", "")
    return render(
        request, "xss_no_autoescape.html", {"user_input": user_input}, using="django"
    )


@require_http_methods(["POST"])
def file_contents(request):
    """
    This view is intended to demonstrate that simply calling request.FILES
    tracks the contents of a file because
    django.utils.datastructures.MultiValueDict __getitem__ is a source in policy.json
    """
    request.FILES["upload"]
    return render(request, "base.html")


def django_cmdi_base64_encoded(request):
    """
    Adapted from a vulnerable view in lets-be-bad-guys.
    The user_input param must base64 encoded string.
    Example: X19pbXBvcnRfXygnb3MnKS5zeXN0ZW0oJ2VjaG8gaGFja2VkJyk%3D
    this decodes to "__import__('os').system('echo hacked')"
    """
    user_input = six.ensure_str(request.GET.get("user_input", None))

    # provide altchars to ensure a call to str.translate()
    decoded_input = base64.b64decode(user_input, altchars="-_")

    eval(decoded_input)

    return render(
        request, "cmdi.html", {"result": "decoded input: {}".format(decoded_input)}
    )


def create_url_definition(name, view):
    if django_version < "2":
        from django.conf.urls import url

        urlpath = url(r"^{}/$".format(name), view, name=name)
    else:
        from django.urls import path

        urlpath = path("{}/".format(name), view, name=name)
    return urlpath


def nosqli(request):
    if request.method == "GET":
        return render(request, "nosqli.html")
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        with_kwarg = request.POST.get("with_kwarg", str(False)) == str(True)
        if user_input:
            try:
                method = request.environ["method_to_test"]
            except KeyError:
                raise Exception(
                    "Must indicate which pymongo collection method to test."
                )

            data = run_pymongo(method, user_input, with_kwarg)
            result = [x for x in data]
        else:
            result = "no user input"
        return render(request, "nosqli.html", {"result": result})


@csrf_exempt
def untrusted_yaml(request):
    """
    !!map {
      ? !!str "goodbye"
      : !!python/object/apply:subprocess.check_output [
        !!str "ls",
      ],
    }
    """
    user_input = request.GET.get("user_input", "")
    load_all = request.environ.get("load_all", False)

    if user_input:
        if load_all:
            # load_all returns a generator so we need to force the load
            list(yaml.load_all(user_input))
        else:
            yaml.load(user_input)

    return render(
        request, "deserialization_yaml.html", {"user_input": "ud", "result": "res"}
    )


def run_pymongo(method, user_input, with_kwarg):
    """
    :param method: Pymongo Collection method to run
    :param user_input: input to pass in to method to run
    :return: any data returned from pymongo query
    """
    client = MongoClient()
    db = client.pymongo_test_db

    data = []
    if method == "find":
        data = (
            db.posts.find(filter={"title": user_input})
            if with_kwarg
            else db.posts.find({"title": user_input})
        )
    elif method == "insert_one":
        new_record = json.loads(user_input)
        db.posts.insert_one(document=new_record) if with_kwarg else db.posts.insert_one(
            new_record
        )
    elif method == "insert_many":
        if with_kwarg:
            db.posts.insert_many(documents=[{"whatever": user_input}])
        else:
            db.posts.insert_many([{"whatever": user_input}])
    elif method == "update":
        record = {"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}

        db.posts.insert_one(record)
        db.posts.update_one(record, {"$set": {"title": user_input}})
    elif method == "delete":
        db.posts.delete_one({"whatever": user_input})
    else:
        raise Exception("Pymongo query for method {} not implemented".format(method))

    return data


def xss(request):
    user_input = request.GET.get("user_input", "")
    should_escape = request.environ.get("django_escape", False)

    if should_escape:
        from django.utils.html import escape

        user_input = escape(user_input)
    return render(request, "xss.html", {"user_input": user_input})


def raw_xss(request):
    """Test reflected-xss detection without using a template engine"""
    user_input = request.GET.get("user_input", "")
    return HttpResponse("<p>Looks like xss: " + user_input + "</p>")


def raw_xss_streaming(request):
    user_input = request.GET.get("user_input", "")
    return StreamingHttpResponse(["<p>Looks like xss: " + user_input + "</p>"])


def xss_csv(request):
    user_input = request.GET.get("user_input", "")
    response = HttpResponse(content_type="text/csv")

    # write a csv-like response because agent currently does not support propagation thru the csv module
    response.write(",".join(["First row", user_input, "Bar", "Baz"]))
    return response


def render_to_response(filename, context=None):
    if context is None:
        context = {}
    template = JINJA_ENV.get_template(filename)
    return HttpResponse(template.render(**context))


def xss_jinja(request):
    user_input = request.GET.get("user_input", "")
    return render_to_response("xss.html", {"user_input": user_input})


def xss_mako(request):
    user_input = request.GET.get("user_input", "")

    return render(
        template_name="xss.html",
        context={"user_input": user_input},
        request=request,
        using="mako",
    )


def xss_cookie(request):
    cookie = request.COOKIES["user_input"]
    return render(request, "xss.html", {"user_input": cookie})


@csrf_exempt
def cmd_injection(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", None)
    elif request.method == "GET":
        user_input = request.GET.get("user_input", None)
    else:
        user_input = None

    try:
        process = subprocess.Popen(
            user_input,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            close_fds=True,
        )

        stdout, _ = process.communicate()

        result = stdout
    except Exception as e:
        result = str(e)

    return render(request, "cmdi.html", {"result": str(result)})


@require_http_methods(["POST"])
@csrf_exempt
def cmdi_file(request):
    """
    This view is intended to replicate (more-or-less) the SQLi vuln in djangoat
    """
    uploaded_file = request.FILES["upload"]
    data_path = os.path.join(settings.MEDIA_ROOT, "data")

    # Tests string propagation through os.path methods
    full_file_name = os.path.join(data_path, uploaded_file.name)
    content = ContentFile(uploaded_file.read())
    default_storage.save(full_file_name, content)

    bak_file_path = full_file_name + ".bak"
    # This is really cheesy isn't it?
    os.system("cp {} {}".format(full_file_name, bak_file_path))

    return render(request, "cmdi.html")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def untrusted_pickle(request):
    """
    Passes untrusted input to pickle

    GET uses pickle.loads with the encoded parameter
    POST users pickle.load with a stream built from the parameter
    """
    result = ""

    if request.method == "GET":
        user_input = request.GET.get("user_input", "")
        user_input = user_input.encode("utf-8")

        if user_input:
            try:
                result = pickle.loads(user_input)
            except Exception as e:
                result = str(e)

    elif request.method == "POST":
        user_input = request.POST.get("user_input", "")
        user_input = io.BytesIO(six.ensure_binary(user_input))

        if user_input:
            try:
                result = pickle.load(user_input)
            except Exception as e:
                result = str(e)

    return render(
        request, "deserialization.html", {"user_input": "ud", "result": result}
    )


@require_http_methods(["GET"])
def stream_source(request):
    """
    Emulates the case where a stream is marked as a source
    """
    user_input = b"\x80\x03]q\x00(K\x01K\x02K\x03e."  # [1, 2, 3]
    stream = io.BytesIO(user_input)

    try:
        # This is artificial and would never happen inside a real app, but it
        # allows us to test the case where a stream is treated as a source
        stream.cs__source = True
        result = pickle.load(stream)
    except Exception as e:
        result = str(e)

    return render(
        request, "deserialization.html", {"user_input": "ud", "result": result}
    )


def ssrf_dynamic(request):
    """
    This is a POST endpoint, and the sub-requests are "sent" (mocked) as GET requests.
    This is to prevent interning. If we use GET for the first request, we end up tracking
    every instance of the string `'GET'`. This includes literals.

    Before we understood this, we were seeing lots of duplicate SSRF events reported here.
    One event was due to the URL and the other was due to the request method.
    """
    url = request.POST.get("url")
    path = request.POST.get("path")
    hostname = request.POST.get("hostname")
    module = request.POST.get("module")
    method = request.POST.get("method")
    use_https = request.POST.get("use_https", str(False)) == str(True)
    trusted_url = "http://python.org"
    with_kwarg = request.POST.get("with_kwarg", str(False)) == str(True)
    result = None

    http_client_class = http.HTTPSConnection if use_https else http.HTTPConnection

    try:
        # python 2 modules
        if module == "urllib":
            result = (
                urllib.urlopen(url=url) if with_kwarg else urllib.urlopen(url)
            ).getcode()
        elif module == "urllib2_str":
            result = (
                urllib2.urlopen(url=url) if with_kwarg else urllib2.urlopen(url)
            ).getcode()
        elif module == "urllib2_obj":
            req = urllib2.Request(url)
            result = (
                urllib2.urlopen(url=req) if with_kwarg else urllib2.urlopen(req)
            ).getcode()
        # python 3 modules
        elif module == "urllib.request_str":
            result = (
                urllib.request.urlopen(url=url)
                if with_kwarg
                else urllib.request.urlopen(url)
            ).getcode()
        elif module == "urllib.request_obj":
            req = urllib.request.Request(url)
            result = (
                urllib.request.urlopen(url=req)
                if with_kwarg
                else urllib.request.urlopen(req)
            ).getcode()
        elif module == "HTTPConnection.request":
            conn = http_client_class(trusted_url, 80)
            # Don't want to create a real connection
            conn._create_connection = mock.MagicMock()
            conn.request("GET", path)
        elif module == "HTTPConnection.request-method":
            conn = http_client_class(trusted_url, 80)
            # Don't want to create a real connection
            conn._create_connection = mock.MagicMock()
            conn.request(method, trusted_url)
        elif module == "HTTPConnection.putrequest":
            conn = http_client_class(trusted_url, 80)
            # Don't want to create a real connection
            conn._create_connection = mock.MagicMock()
            conn.putrequest(method="GET", url=path) if with_kwarg else conn.putrequest(
                "GET", path
            )
        elif module == "HTTPConnection.putrequest-method":
            conn = http_client_class(trusted_url, 80)
            # Don't want to create a real connection
            conn._create_connection = mock.MagicMock()
            conn.putrequest(
                method=method, url=trusted_url
            ) if with_kwarg else conn.putrequest(method, trusted_url)
        elif module == "HTTPConnection.__init__":
            conn = (
                http_client_class(host=hostname)
                if with_kwarg
                else http_client_class(hostname)
            )
    except Exception as e:
        result = str(e)

    return render(request, "ssrf.html", {"user_input": url, "result": result})


def unvalidated_redirect(request):
    user_input = request.GET.get("user_input", "/cmdi/")
    permanent = request.GET.get("permanent", False)
    return redirect(user_input, permanent=permanent)


@require_http_methods(["GET"])
def two_vulns(request):
    """
    This view contains two vulnerabilities.
    """
    user_input = request.GET.get("user_input", "")

    try:
        # First vulnerability: cmd-injection
        subprocess.Popen(
            user_input,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            close_fds=True,
        )
    except Exception:
        pass

    # Second vulnerability: reflected-xss
    return HttpResponse("<p>{}</p>".format(user_input))


def untrusted_exec(request):
    user_input = request.GET.get("user_input", "1 + 2")
    exec (user_input)
    # This is xss too...
    return HttpResponse("<p>executed statement: {}</p>".format(user_input))


def untrusted_execfile(request):
    user_input = request.GET.get("user_input", "attack.py")

    try:
        execfile(user_input)
    except Exception:
        pass

    # This is xss too...
    return HttpResponse("<p>executed statement: {}</p>".format(user_input))


def logout(request):
    DjangoLogout(request)
    return render(request, "logout.html")


def get_dynamic_source(request, request_dict, source):
    user_input = ""

    if source == "parameter":
        user_input = request_dict.get("user_input")
    elif source == "body":
        user_input = request.body
    elif source == "host":
        user_input = request.get_host()
    elif source == "port":
        user_input = request.get_port()
    elif source == "raw_uri":
        user_input = request.get_raw_uri()
    elif source == "files" and request.method == "POST":
        file_stream = request.FILES.get("user_input")
        user_input = file_stream.read()
    elif source == "full_path":
        user_input = request.get_full_path()
    elif source == "full_path_info":
        user_input = request.get_full_path_info()
    elif source == "scheme":
        user_input = request.scheme
    elif source == "encoding":
        user_input = request.encoding
    elif source == "referer_header":
        user_input = (
            request.headers["Referer"] if six.PY3 else request.META["HTTP_REFERER"]
        )

    return user_input


def dynamic_sources(request):
    request_dict = request.POST if request.method == "POST" else request.GET
    source = request_dict.get("source", "")
    user_input = get_dynamic_source(request, request_dict, source)

    if isinstance(user_input, bytes):
        # TODO: PYT-714 be able to remove this conversion when .format can propagate tags
        user_input = str(user_input)

    os.system("echo {}".format(user_input))

    return HttpResponse("<p>tested sources </p>")


def cookie_source(request):
    user_input = request.COOKIES["user_input"]
    os.system("echo {}".format(user_input))

    return HttpResponse("<p>echoed cookie: {}</p>".format(user_input))


def header_source(request):
    use_environ = request.environ.get("use_environ", False)

    if use_environ:
        user_input = request.environ.get("HTTP_TEST_HEADER")
    else:
        user_input = (
            request.headers["Test-Header"]
            if six.PY3
            else request.META["HTTP_TEST_HEADER"]
        )

    os.system("echo {}".format(user_input))

    return HttpResponse("<p>echoed header: {}</p>".format(user_input))


def header_key_source(request):
    use_environ = request.environ.get("use_environ", False)

    if use_environ:
        keys = request.environ.keys()
    else:
        keys = request.headers.keys() if six.PY3 else request.META.keys()

    user_input = list(keys)[0]
    os.system("echo {}".format(user_input))

    return HttpResponse("<p>echoed header key: {}</p>".format(user_input))


def stored_xss(request):
    user_input = request.GET.get("user_input", "hello")
    test_type = request.GET.get("test_type")

    if test_type == "create_method":
        msg = Message.objects.create(name=user_input)
    elif test_type == "init_direct":
        msg = Message(name=user_input)
        msg.save()
    elif test_type == "filter":
        _ = Message.objects.create(name=user_input)
        msgs = Message.objects.filter(name=user_input)
        msg = msgs[0]
    elif test_type == "multi-column":
        msg = Message.objects.create(name=user_input, content=user_input)
    else:
        raise Exception("Pass a test_type to test")

    html = "<p>Looks like xss: " + msg.name + "</p>"
    return HttpResponse(html)


def get_apptest_urls():
    # New url/views should be added to this list
    url_mappings = [
        ("static-image", static_image),
        ("xss-autoescape", django_autoescape),
        ("xss-autoescape-safe", django_autoescape_safe),
        ("xss-no-autoescape", django_no_autoescape),
        ("file-contents", file_contents),
        ("cmdi", cmd_injection),
        ("cmdi-base64-encoded", django_cmdi_base64_encoded),
        ("cmdi-file", cmdi_file),
        ("nosqli", nosqli),
        ("stream-source", stream_source),
        ("cookie-source", cookie_source),
        ("header-source", header_source),
        ("header-key-source", header_key_source),
        ("untrusted-yaml", untrusted_yaml),
        ("untrusted-pickle", untrusted_pickle),
        ("xss", xss),
        ("xss-jinja", xss_jinja),
        ("xss-mako", xss_mako),
        ("xss-cookie", xss_cookie),
        ("raw-xss", raw_xss),
        ("xss-csv", xss_csv),
        ("raw-xss-streaming", raw_xss_streaming),
        ("logout", logout),
        ("ssrf-dynamic", ssrf_dynamic),
        ("unvalidated-redirect", unvalidated_redirect),
        ("two-vulns", two_vulns),
        ("untrusted-exec", untrusted_exec),
        ("untrusted-execfile", untrusted_execfile),
        ("dynamic-sources", dynamic_sources),
        ("stored-xss", stored_xss),
    ]

    return [create_url_definition(name, view) for name, view in url_mappings]
