import sublime
import requests
import sublime_plugin
import io


SERVATOR_API_UPLOAD_ENDPOINT = 'http://serve.janitorrb.com/api/upload'


class ServatorCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        f = self.get_content_byffer()
        filename = "index.html"
        files = {'serve': (filename, f, 'text/html')}
        response = requests.post(SERVATOR_API_UPLOAD_ENDPOINT, files=files)
        if response.ok:
            serve_url = response.json()['result']['serve_url']
            sublime.set_clipboard(serve_url)
            sublime.status_message("Serve: " + serve_url)

    def get_content_byffer(self):
        content = self.get_view_content()
        f = io.StringIO()
        f.write(content)
        f.seek(0)
        return f

    def get_view_content(self):
        # from https://github.com/Paaskehare/pastebin-sublime-plugin/blob/master/pastebin.py
        content = u''
        # loop over the selections in the view:
        for region in self.view.sel():
            if not region.empty():
                # be sure to insert a newline if we have multiple selections
                if content:
                    content += FileForm.NEWLINE
                content += self.view.substr(region)
        # if we havent gotten data from selected text,
        # we assume the entire file should be pasted:
        if not content:
            content += self.view.substr(sublime.Region(0, self.view.size()))
        return content