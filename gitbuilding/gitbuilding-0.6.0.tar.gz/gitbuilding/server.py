"""
This module constains the flask server for viewing the documentation and for live editing.
The server is lunched with `gitbuilding serve` and runs on port 6178.
"""

import os
import shutil
import codecs
import logging
from copy import deepcopy
from tempfile import gettempdir
from uuid import uuid4 as uuid
import socket
import flask
from flask import request, jsonify
import requests
from gitbuilding import utilities
from gitbuilding.buildup import Documentation, read_directory, FileInfo
from gitbuilding.buildup.page import Page
from gitbuilding import render
from gitbuilding.config import load_config_from_file

_LOGGER = logging.getLogger('BuildUp.GitBuilding')

# This module is only the server. It makes more sense for all flask calls
# to be methods. As such disabling no-self-use
# pylint: disable=no-self-use

class GBServer(flask.Flask):
    """
    GBServer is the GitBuilding server it is a child class of flask.Flask. It can be
    used to provide a preview of the documentation and to serve the live editor.
    """

    def __init__(self, conf, handler):

        rules = render.URLRulesHTML()
        self._handler = handler
        configuration = load_config_from_file(conf)
        configuration.remove_landing_title = True
        self._license_file = utilities.handle_licenses(configuration)
        self.doc = Documentation(configuration, rules)
        file_list = read_directory('.', exclude_list=configuration.exclude)
        if self._license_file is not None:
            file_list.append(self._license_file)
        self.doc.buildall(file_list)
        self._read_config()

        # Two render objects, one for static one for live
        self.renderer = render.GBRenderer(self._config, static=False)
        # The live renderer shows the static rendering as static=False
        # is used show the header buttons.
        self.live_renderer = render.GBRenderer(deepcopy(self._config))
        self._unsaved_dropped_files = DroppedFiles()
        super(GBServer, self).__init__(__name__)

        # Define URL rules!
        self.add_url_rule("/", "render", self._render_page)
        self.add_url_rule("/-/render_markdown",
                          "live_render",
                          self._live_render,
                          methods=["POST"])
        self.add_url_rule("/<path:subpath>", "render", self._render_page)
        self.add_url_rule("/assets/<path:subpath>", "assets", self._return_assets)
        self.add_url_rule("/-/editor/", "editor", self._edit_page)
        self.add_url_rule("/-/editor/save", "save", self._save_edit, methods=["POST"])
        self.add_url_rule("/-/editor/raw", "raw", self._raw_md)
        self.add_url_rule("/-/create-homepage/", "create_homepage", self._create_homepage)
        self.add_url_rule("/-/contents-page", "contents_page", self._contents_page)

        self.add_url_rule("/<path:subpath>/-/editor/", "editor", self._edit_page)
        self.add_url_rule("/<path:subpath>/-/editor/raw", "raw", self._raw_md)
        self.add_url_rule("/<path:subpath>/-/editor/save",
                          "save",
                          self._save_edit,
                          methods=["POST"])

        self.add_url_rule("/<path:subpath>/-/editor/dropped-file",
                          "droppedfile",
                          self._dropped_file,
                          methods=["POST"])

        self.add_url_rule("/-/editor/dropped-file",
                          "droppedfile",
                          self._dropped_file,
                          methods=["POST"])

    def _read_config(self):
        """
        Reads the project data generated when converting BuildUp to markdown
        """
        self._config = self.doc.config

    def _get_docpage(self, subpath):
        """
        Gets a Page object from the Documentation object
        """
        if len(subpath) == 0:
            return None

        if subpath in self.doc.pages:
            ind = self.doc.pages.index(subpath)
            return self.doc.pages[ind]
        file_obj = FileInfo(subpath, dynamic_content=True, content='')
        return Page(file_obj, self.doc)

    def _raw_md(self, subpath=None):
        """
        Get the raw markdown for pages in the documentation
        Returns this in JSON
        """
        md = ''
        if subpath is None and request.path == "/-/editor/raw":
            if self.doc.config.landing_page is not None:
                md = self.doc.landing_page.get_raw()
                return jsonify({"md": md})
            return jsonify({"md": ""})

        if subpath+'.md' in self.doc.pages:
            page = self._get_docpage(subpath+'.md')
            if page is not None:
                md = page.get_raw()
            return jsonify({"md": md, "page": subpath})
        return jsonify({"md": "# Empty page\n\nEdit me", "page": subpath})

    def _save_edit(self, subpath=None):
        """
        Saves the edits from the live editor and full rebuilds the documentation
        """

        #removing any reference to .html as it confuses things
        if subpath is not None and os.path.splitext(subpath)[1] == '.html':
            subpath = os.path.splitext(subpath)[0]

        content = request.get_json()
        for uploaded_file in content["uploadedFiles"]:
            # Check if file is still there. It may already have been removed
            # if multiple copies of the same file were dropped.
            if self._unsaved_dropped_files.contains(uploaded_file):
                if uploaded_file in content["md"]:
                    shutil.copyfile(self._unsaved_dropped_files.get(uploaded_file),
                                    uploaded_file)
                    #Only remove if copied as multiple editors could have added same file
                    self._unsaved_dropped_files.remove(uploaded_file)

        if content["md"] is not None:

            saved = self._save_page(subpath, content["md"])

            if saved:
                self._rebuild_docs()
                return jsonify({"saved": True})
        return jsonify({"saved": False})

    def _save_page(self, subpath, md):
        if subpath is None:
            if self.doc.config.landing_page is not None:
                save_path = self.doc.landing_page.filepath
            else:
                return False
        else:
            save_path = subpath+'.md'

        utilities.make_dir_if_needed(save_path, isfile=True)
        try:
            with codecs.open(save_path, "w", encoding='utf-8') as outfile:
                outfile.write(md)
            return True
        except IOError:
            return False

    def _create_homepage(self):
        md = "# Project title\nSome text for this page"
        self._save_page('index', md)
        self._rebuild_docs()
        return flask.redirect('/-/editor/')

    def _contents_page(self):
        return self.renderer.contents_page(self.doc.output_files)

    def _rebuild_docs(self):
        file_list = read_directory('.', exclude_list=self.doc.config.exclude)
        if self._license_file is not None:
            file_list.append(self._license_file)
        self.doc.buildall(file_list)
        self._read_config()
        self.renderer.config = self._config
        self.renderer.populate_vars()

    def _dropped_file(self, subpath=None):
        """
        This gets run if a file gets dragged and dropped into the editor
        """
        files = request.files
        if subpath is None:
            folder_depth = 0
        else:
            folder_depth = len(subpath.split('/')) - 1
        out_filenames = []
        md_line = ''
        # loop through all files and save images
        for file in files:
            if files[file].mimetype.startswith("image"):
                files[file].filename = files[file].filename.replace(" ", "")
                #This is going into the markdown so we always use unix paths.
                file_path = f"images/{files[file].filename}"
                i = 0
                while os.path.exists(file_path):
                    if i == 0:
                        path_no_ext, ext = os.path.splitext(file_path)
                    i += 1
                    file_path = f'{path_no_ext}{i:03d}{ext}'

                _, ext = os.path.splitext(files[file].filename)
                temp_path = os.path.join(gettempdir(), str(uuid())+ext)
                files[file].save(temp_path)
                self._unsaved_dropped_files.add_file(file_path, temp_path)
                out_filenames.append(file_path)
                md_file_path = '../'*folder_depth + file_path
                md_line += f'![]({md_file_path})\n'
            else:
                _LOGGER.warning("Cannot upload file of mimetype: %s", files[file].mimetype)

        if len(out_filenames) > 0:
            return jsonify({"received": True,
                            "filenames": out_filenames,
                            "md_line": md_line})
        return flask.abort(405)

    def _live_render(self):
        """
        Runs the live renderer and returns the html as well as warnings
        in JSON format
        """
        content = request.get_json()
        if content["md"] is None:
            return jsonify({"html": "", "log": "", "number": 0})

        log_length = self._handler.log_length
        if not "page" in content: # Live render landing page
            if self.doc.config.landing_page is not None:
                page = self.doc.landing_page
                processed_text = page.rebuild(content["md"], '-/editor/index')
                title = page.title
                self.live_renderer.config.title = title
                self.live_renderer.populate_vars()
        else:
            page = self._get_docpage(content["page"])
            if page is None:
                return jsonify({"html": "", "log": "", "number": 0})
            processed_text = page.rebuild(content["md"], content["page"]+'/-/editor/index')

        html = self.live_renderer.render_md(processed_text,
                                            page.filepath,
                                            fullpage=False,
                                            nav=False)
        log = self._handler.log_from(log_length)

        return jsonify({"html": html,
                        "log": render.format_warnings(log),
                        "number": len(log)})

    def _edit_page(self, subpath=None):
        """
        Starts the live editor for a particular page
        """

        if (subpath is None and request.path == "/-/editor/") or os.path.splitext(subpath)[1] == '':
            self.live_renderer.config = deepcopy(self._config)
            self.live_renderer.populate_vars()

            gbpath = os.path.dirname(__file__)
            page = os.path.join(gbpath, "static", "live-editor", "index.html")
            return flask.send_file(page)

        html = self.renderer.render("<h1>Sorry. Cannot edit this file!</h1>")
        return html

    def _render_page(self, subpath=None):
        """
        Renders the static version of a page
        """
        #remove any reference to .html as it confuses things
        if subpath is not None and os.path.splitext(subpath)[1] == '.html':
            subpath = os.path.splitext(subpath)[0]

        #translated path is is the file in the buildup output
        translated_path = subpath
        if subpath == "missing":
            return self.renderer.missing_page()
        if subpath is None:
            if self.doc.config.landing_page is not None:
                translated_path = self.doc.config.landing_page
            else:
                return self.renderer.empty_homepage()
        elif os.path.splitext(subpath)[1] == '':
            translated_path = os.path.splitext(subpath)[0] + '.md'
        elif os.path.splitext(subpath)[1] == '.md':
            # Breaking this is probably excessive, it is done now to catch mistakes
            # in the link translation. Might revert later
            return flask.abort(404)

        outfile = self.doc.get_file(translated_path)

        if outfile is not None:
            if outfile.dynamic_content:
                editorbutton = bool((subpath is None) or translated_path in self.doc.pages)
                return self.renderer.render_md(outfile.content,
                                               subpath,
                                               editorbutton=editorbutton)
            return self._send_file_obj(outfile)

        if translated_path.endswith(".md"):
            outfile = self.doc.get_file(translated_path[:-2] + 'stl')
            if outfile is not None:
                return self.renderer.stl_page(outfile.path)

            return self.renderer.render_md("# Page not found\n Do you want to "
                                           f"[create it](/{subpath}/-/editor)",
                                           subpath,
                                           editorbutton=True)
        # For missing files that are not mark down check the temporary
        # files that were drag and dropped.
        temp_file = self._unsaved_dropped_files.get(subpath)
        if temp_file is not None:
            return flask.send_file(temp_file)
        # If file still missing it may be in the input directory this should only
        # happen in the live editor
        file_list = read_directory('.', exclude_list=self._config.exclude)
        if subpath in file_list:
            file_obj = file_list[file_list.index(subpath)]
            return self._send_file_obj(file_obj)
        return self._404_or_missing_image(subpath)

    def _send_file_obj(self, file_obj):
        path_on_disk = os.path.abspath(file_obj.location_on_disk)
        if os.path.exists(path_on_disk):
            return flask.send_file(path_on_disk)
        return self._404_or_missing_image(file_obj.path)

    def _404_or_missing_image(self, subpath):
        if subpath.lower().endswith((".jpg", ".jpeg", ".png", ".gif", '.svg',
                                     ".tif", ".tiff", '.webp')):
            gbpath = os.path.dirname(__file__)
            image = os.path.join(gbpath, "static", "local-server", "Missing_image.png")
            return flask.send_file(image)
        return flask.abort(404)

    def _return_assets(self, subpath):
        """
        returns file from the assets directory
        """
        page = os.path.join("assets", subpath)
        if os.path.isfile(page):
            return flask.send_file(os.path.abspath(page))

        return flask.abort(404)

    def run(self, host="localhost", port=6178): # pylint: disable=arguments-differ
        """
        Starts the flask server
        """
        try:
            # Check the server isn't already running (only needed on Windows)
            sock = socket.create_connection((host, port), timeout=0.5)
            sock.close()
            # If we have made it past this, there is a server running - so we
            # should fail
            raise ServerAlreadyRunningError(f'A server is already running on "{host}"'
                                            f' port {port}.')
        except socket.timeout:
            pass  # If we couldn't connect, ignore the error
        except ConnectionError:
            pass # If we couldn't connect, ignore the error

        super(GBServer, self).run(host, port)

class ServerAlreadyRunningError(Exception):
    """
    Custom exception for if the GitBuilding server is already running.
    """

class DevServer(GBServer):
    """
    Child class of GBServer, this server allows hot-reloading of live-editor for
    development.
    """

    def __init__(self, conf, handler):

        super(DevServer, self).__init__(conf, handler)

        self.add_url_rule("/static/live-editor/<path:subpath>",
                          "dev_editor_static",
                          self._dev_editor_static)
        self.add_url_rule("/static/<path:subpath>",
                          "dev_other_static",
                          self._dev_other_static)
        self.add_url_rule("/sockjs-node/<path:subpath>",
                          "dev_editor_sockjs",
                          self._dev_editor_sockjs)

        self.add_url_rule("/__webpack_dev_server__/<path:subpath>",
                          "dev_editor_webpack",
                          self._dev_editor_webpack)

    def _edit_page(self, subpath=None):
        """
        Starts the live editor for a particular page
        """
        if (subpath is None and request.path == "/-/editor/") or os.path.splitext(subpath)[1] == '':
            self.live_renderer.config = deepcopy(self._config)
            self.live_renderer.populate_vars()

            url = "http://localhost:8080/static/live-editor/"
            try:
                req = requests.get(url)
            except requests.exceptions.RequestException:
                msg = (f"ERROR: Could not connect to live-editor dev server"
                       f" on '{url}', did you forget to start it?")
                return flask.abort(flask.Response(msg, status=500))
            return req.text
        html = self.renderer.render("<h1>Sorry. Cannot edit this file!</h1>")
        return html

    def _dev_editor_static(self, subpath):
        url = "http://localhost:8080/static/live-editor/" + subpath
        try:
            req = requests.request(flask.request.method, url)
        except requests.exceptions.RequestException:
            msg = (f"ERROR: Could not connect to live-editor dev server for '{url}',"
                   " did you forget to start it?")
            return flask.abort(flask.Response(msg, status=500))
        return req.text

    def _dev_editor_sockjs(self, subpath):
        url = ("http://localhost:8080/sockjs-node/"
               + subpath
               + flask.request.query_string.decode())
        try:
            req = requests.request(flask.request.method, url)
        except requests.exceptions.RequestException:
            msg = (f"ERROR: Could not connect to live-editor dev server for '{url}',"
                   " did you forget to start it?")
            return flask.abort(flask.Response(msg, status=500))
        return req.text

    def _dev_editor_webpack(self, subpath):
        url = ("http://localhost:8080/__webpack_dev_server__/"
               + subpath
               + flask.request.query_string.decode())
        try:
            req = requests.request(flask.request.method, url)
        except requests.exceptions.RequestException:
            msg = (f"ERROR: Could not connect to live-editor dev server for '{url}',"
                   " did you forget to start it?")
            return flask.abort(flask.Response(msg, status=500))
        return req.text

    def _dev_other_static(self, subpath):
        return flask.send_from_directory("static", subpath)

class DroppedFiles:
    """
    Pretty simple class for handling the files dropped into the editor. This
    could be handled with a list of dictionaries but the syntax for checking
    and finding the correct file gets really ugly.
    """

    def __init__(self):
        self._files = []

    def add_file(self, output_file, temp_file):
        """
        Add a dropped file to be tracked. Inputs are the filename in the
        output, and the temporary filename
        """
        if not self.contains(output_file):
            self._files.append({'output_path':output_file,
                                'temp_path':temp_file})

    @property
    def _out_paths(self):
        return [fdict['output_path'] for fdict in self._files]

    def get(self, filename):
        """
        Get the temp file for location for `filename`. Returns None if the
        filename does not exist
        """

        out_paths = self._out_paths
        if filename in out_paths:
            return self._files[out_paths.index(filename)]['temp_path']
        return None

    def contains(self, filename):
        """
        Returns true if `filename` is listed as an output filename.
        """
        return self.get(filename) is not None

    def remove(self, filename):
        """
        Removes the record for the dropped file and deletes the temporary file
        from disk
        """
        out_paths = self._out_paths
        if filename in out_paths:
            ind = out_paths.index(filename)
            temp_file = self._files[ind]['temp_path']
            os.remove(temp_file)
            self._files.pop(ind)
            return True
        return False
