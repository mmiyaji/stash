#!/usr/bin/env python
# encoding: utf-8
"""
upload.py

Created by mmiyaji on 2012-07-14.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from __future__ import with_statement
from views import *
import simplejson, re, urllib
from django import forms
# from scan import Scanner
WEBSITE = 'http://ruhenheim.org/'
MIN_FILE_SIZE = 1 # bytes
MAX_FILE_SIZE = 20000000 # bytes
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES
THUMBNAIL_MODIFICATOR = '=s80' # max width / height
EXPIRATION_TIME = 300 # seconds
def get_authors(str):
    reg = "\[(.*)\]"
    p = re.compile(reg, re.M)
    a = p.findall(str)
    authors = {}
    for i in a:
        aa = i.split(",")
        for j in aa:
            authors[j.strip()] = True
    return authors
def get_tags(str):
    reg = "\((.*)\)"
    p = re.compile(reg, re.M)
    a = p.findall(str)
    authors = {}
    for i in a:
        aa = i.split(",")
        for j in aa:
            authors[j.strip()] = True
    return authors
class UploadHandler(object):
    def __init__(self, request):
        """
        Arguments:
        - `request`:
        """
        self._request = request
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def uploadGET(self):
        """
        Page to upload images.
        Case of GET REQUEST '/upload/'
        """
        temp_values = Context()
        download_script = open(os.path.join(self.BASE_DIR, 'templates/component/download_script.html')).read()
        upload_script = open(os.path.join(self.BASE_DIR, 'templates/component/upload_script.html')).read()
        temp_values = {
            "target":"upload",
            "title":"Upload form",
            "tags":Tag.get_all(),
            "download_script":download_script,
            "upload_script":upload_script,
            }
        # logger.debug(download_script)
        return render_to_response('upload/index.html',temp_values,
                                  context_instance=RequestContext(self._request))

    def uploadPOST(self):
        """
        Page to upload images.
        Case of POST REQUEST '/upload/'
        """
        # print "aaaaaaaaa",self._request.POST, self._request.FILES
        results = []
        blob_keys = []
        allcaption = ""
        if self._request.POST.has_key('allcaption'):
            allcaption = self._request.POST['allcaption']
        allcomment = ""
        if self._request.POST.has_key('allcomment'):
            allcomment = self._request.POST['allcomment']
        alltag = None
        if self._request.POST.has_key('alltag'):
            alltag = self._request.POST.getlist('alltag')
        for fieldStorage in self._request.FILES.getlist('files'):
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = re.sub(r'^.*\\', '',
                                    fieldStorage.name)
            # print result['name']
            result['type'] = fieldStorage.content_type
            # print result['type']
            if self.validate(result):
                image_url = os.path.join(settings.MEDIA_URL, 'tmp', result['name'])
                # print image_url
                destination = open(image_url.encode("utf-8"), 'wb+')
                for chunk in fieldStorage.chunks():
                    destination.write(chunk)
                    destination.close()
                published_at = datetime.datetime.now()
                entry = Entry.get_by_pub_and_name(published_at, result["name"])
                if entry:
                    result['already'] = True
                else:
                    entry = Entry()
                if allcaption:
                    entry.caption = allcaption
                if allcomment:
                    entry.comment = allcomment
                entry.published_at = published_at
                # name = force_unicode(entry.published_at.strftime((smart_str("%Y%m%d%H%M%S_"+str(entry.id).zfill(5)+"."+result['name'].split(".")[-1]))))
                name = force_unicode(result['name'])
                entry.title = name
                entry.filetype = result['type']
                entry.original_title = result['name']
                entry.save(isFirst = True)
                # entry.authors.clear()
                # if result['type'] == "application/pdf":
                #     image_url = os.path.join(settings.MEDIA_URL, 'tmp', result['name'])
                #     commands.getoutput("convert '%s[0]' -resize 600x800 '%s.png'" % (image_url.encode("utf-8"), image_url.encode("utf-8")))
                #     image = File(open(image_url.encode("utf-8")+".png"))
                #     print image,image.size,name
                #     entry.image = image
                # else:
                #     entry.image = File(open(os.path.join(settings.MEDIA_URL, 'images', 'noimage.png')))
                entry.file = fieldStorage
                authors = get_authors(name)
                for a in authors.keys():
                    author = Author.get_by_name(a)
                    if not author:
                        author = Author()
                        author.name = a
                        author.save()
                    entry.authors.add(author)
                entry.tag.clear()
                tags = get_tags(name)
                for t in tags.keys():
                    tag = Tag.get_by_name(t)
                    if not tag:
                        tag = Tag()
                        tag.name = t
                        tag.save()
                    entry.tag.add(tag)
                if alltag:
                    for t in alltag:
                        tt = Tag.get_by_id(t)
                        entry.tag.add(tt)
                        # tags += "%s," % tt.name
                entry.save()
        return HttpResponseRedirect("/upload/")

        # s = simplejson.dumps(self.handle_upload(), separators=(',',':'))
        # if self._request.POST.has_key('redirect'):
        #     redirect = self._request.POST('redirect') or None
        #     if redirect:
        #         return HttpResponseRedirect(str(
        #                 redirect.replace('%s', urllib.quote(s, ''), 1)
        #                 ))
        # # if 'application/json' in self._request.headers.get('Accept'):
        # #     self.response.headers['Content-Type'] = 'application/json'
        # # self.response.write(s)
        # print "simple json ",s
        # return HttpResponse(s, mimetype = "application/json",)
    # def initialize(self, request, response):
    #     super(UploadHandler, self).initialize(request, response)
    #     self.response.headers['Access-Control-Allow-Origin'] = '*'
    #     self.response.headers[
    #         'Access-Control-Allow-Methods'
    #         ] = 'OPTIONS, HEAD, GET, POST, PUT, DELETE'

    def validate(self, file):
        # if file['size'] < MIN_FILE_SIZE:
        #     file['error'] = 'minFileSize'
        # elif file['size'] > MAX_FILE_SIZE:
        #     file['error'] = 'maxFileSize'
        # elif not ACCEPT_FILE_TYPES.match(file['type']):
        #     file['error'] = 'acceptFileTypes'
        # else:
        #     return True
        # return False
        return True

    def get_file_size(self, file):
        file.seek(0, 2) # Seek to the end of the file
        size = file.tell() # Get the position of EOF
        file.seek(0) # Reset the file position to the beginning
        return size

    def handle_upload(self):
        results = []
        blob_keys = []
        allcaption = ""
        if self._request.POST.has_key('allcaption'):
            allcaption = self._request.POST['allcaption']
        allcomment = ""
        if self._request.POST.has_key('allcomment'):
            allcomment = self._request.POST['allcomment']
        alltag = None
        if self._request.POST.has_key('alltag'):
            alltag = self._request.POST.getlist('alltag')
        for fieldStorage in self._request.FILES.getlist('files[]'):
            if type(fieldStorage) is unicode:
                continue
            result = {}
            result['name'] = re.sub(r'^.*\\', '',
                                    fieldStorage.name)
            # print result['name']
            result['type'] = fieldStorage.content_type
            # print result['type']
            # result['size'] = self.get_file_size(fieldStorage.file)
            # result['size']
            if self.validate(result):
                image_url = os.path.join(settings.MEDIA_URL, 'tmp', result['name'])
                destination = open(image_url, 'wb+')
                for chunk in fieldStorage.chunks():
                    destination.write(chunk)
                    destination.close()
                # scan = Scanner(image_url)
                # exif = scan.scanExif()
                # zimage = scan.scanQR()
                exif = None
                published_at = None
                orientation = 0
                published_at = datetime.datetime.now()
                # try:
                #     if exif:
                #         if exif.has_key(36867):
                #             # DateTimeOriginal
                #             published_at = date_validate(exif[36867], "%Y:%m:%d %H:%M:%S")
                #         elif exif.has_key(36868):
                #             # DateTimeDigitized
                #             published_at = date_validate(exif[36868], "%Y:%m:%d %H:%M:%S")
                #         elif exif.has_key(306):
                #             # DateTime
                #             published_at = date_validate(exif[306], "%Y:%m:%d %H:%M:%S")
                #         else:
                #             # now
                #             published_at = datetime.datetime.now()
                #     else:
                #         published_at = datetime.datetime.now()
                # except:
                #     published_at = datetime.datetime.now()
                # try:
                #     if exif.has_key(274):
                #         orientation = int(exif[274])
                # except:
                #     pass
                authors = []
                # if zimage:
                #     for i in zimage:
                #         if "QRCODE" == str(i.type):
                #             # ","がひとつ以上あれば旧式のQRコード
                #             if i.data.count(",") < 1: # 新バージョンのQRコード．学生IDのみ入力されている
                #                 element = ["do-ele","",i.data,""]
                #             else: # 旧バージョンのQRコード．"do-ele",氏名,学生ID,nickname,passwd
                #                 element = i.data.split(",")
                #             author = Author.get_by_student_id(element[2])
                #             if not author:
                #                 author = Author()
                #                 author.student_id = element[2].replace("　"," ").strip()
                #                 # 学籍番号の最初4桁を入学年度として扱う
                #                 adate = None
                #                 try:
                #                     # せめて数字かどうかチェック それ以外なら今日の日付を入力
                #                     ayear = int(element[2].replace("　"," ").strip()[:4])
                #                     adate = date_validate(str(ayear)+"-04-01")
                #                 except:
                #                     pass
                #                 if not adate:
                #                     adate = datetime.datetime.now()
                #                 author.admitted_at = adate
                #                 author.name = element[1].replace("　"," ").strip()
                #                 author.nickname = element[3].replace("　"," ").strip()
                #                 author.save()
                #             authors.append(author)
                entry = Entry.get_by_pub_and_name(published_at, result["name"])
                if entry:
                    result['already'] = True
                else:
                    entry = Entry()
                if allcaption:
                    entry.caption = allcaption
                if allcomment:
                    entry.comment = allcomment
                if orientation:
                    entry.orientation = orientation
                entry.published_at = published_at
                name = force_unicode(entry.published_at.strftime((smart_str("%Y%m%d%H%M%S_"+str(entry.id).zfill(5)+"."+result['name'].split(".")[-1]))))
                entry.title = name
                # entry.image = fieldStorage
                entry.original_title = result['name']
                entry.save()
                # entry.authors.clear()
                for a in authors:
                    entry.authors.add(a)
                entry.tag.clear()
                tags = ""
                if alltag:
                    for t in alltag:
                        tt = Tag.get_by_id(t)
                        entry.tag.add(tt)
                        tags += "%s," % tt.name
                entry.save()
                result['title'] = name
                result['authors'] = serializers.serialize("json", entry.authors.all())
                if len(entry.authors.all()):
                    result['author'] = {'name':entry.authors.all()[0].name,
                                        'student_id':entry.authors.all()[0].author_id,
                                        'admitted_year':entry.authors.all()[0].admitted_at.year}
                result['published_at'] = entry.published_at.strftime("%Y-%m-%d %H:%M:%S")
                result['uuid'] = "aa"
                result['caption'] = entry.caption
                result['comment'] = entry.comment
                result['tag'] = tags
                result['update_type'] = 'UPDATE'
                result['update_url'] = "http://%s/entry/%s/update/" % (self._request.get_host(), 1)
                result['delete_type'] = 'DELETE'
                result['delete_url'] = "http://%s/entry/%s/delete/" % (self._request.get_host(), 1)
                if (IMAGE_TYPES.match(result['type'])):
                    try:
                        result['url'] = "http://"+self._request.get_host()+"/media/"+entry.name
                        result['thumbnail_url'] = "http://"+self._request.get_host()+"/media/"+ "a"
                    except: # Could not get an image serving url
                        pass
                if not 'url' in result:
                    result['url'] = "http://"+self._request.get_host()+"/media/"+"a"
                    result['thumbnail_url'] = "http://"+self._request.get_host()+"/media/"+"a"
            results.append(result)
        return results

@csrf_protect
def home(request):
    """
    URL REQUEST '/upload/'
    """
    request_type = request.method
    logger.debug(request_type)
    uhandler = UploadHandler(request)
    if request_type == 'GET':
        return uhandler.uploadGET()
    elif request_type == 'OPTION' or request_type == 'HEAD':
        # connection test
        return HttpResponse("OK")
    elif request_type == 'POST':
        return uhandler.uploadPOST()
    # elif request_type == 'DELETE':
    else:
        return uhandler.uploadGET()

def main():
    """
    write tests
    """
    pass

if __name__ == '__main__':
    main()

