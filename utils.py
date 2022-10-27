# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:21:12 2022

@author: shangfr
"""
import base64
import hashlib
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from markdownify import markdownify
import streamlit as st


def txt2md5(dtxt):
    md5_value = hashlib.md5(str(dtxt).encode("utf-8")).hexdigest()
    return md5_value


def splash_get(url):
    script = """
    splash:go(args.url)
    splash:wait(1)
    return splash:html()
    """
    resp = requests.post('http://39.101.187.7:8012/run', json={
        'lua_source': script,
        'url': url
    })
    return resp


def tidy_img(md):
    img_path = re.findall('http.*?jpe?g|http.*?png', md)

    for path in img_path:
        r = requests.get(path)
        file_suffix = r.headers['Content-Type'].split("/")[1]
        path_file = "./img/{}.{}".format(txt2md5(path), file_suffix)
        with open(path_file, 'wb') as f:
            f.write(r.content)

        md = md.replace(path, path_file)
    return md


@st.cache
def get_html(url, render_service=False):

    url_p = urlparse(url)

    if render_service:
        r = splash_get(url)
    else:
        r = requests.get(url)

    if r.status_code == 200:
        if r.encoding == "ISO-8859-1":
            html_d = r.text.encode("ISO-8859-1").decode("utf-8")
        else:
            html_d = r.text  # utf-8编码直接用，

        soup = BeautifulSoup(html_d, 'lxml')

        html_d = str(soup.body)
        if html_d:
            md_d = markdownify(
                html_d, strip=['a'], heading_style='ATX').strip()
            netloc = url_p.netloc
            scheme = url_p.scheme
            md_d = md_d.replace("](/", f"]({scheme}://{netloc}/")
            md_d = re.sub('\n+', '\n', md_d).replace("\n", "\n\n")

            md = tidy_img(md_d)
            return md


def convert_img(image):
    with image.open() as image_bytes:
        img_bytes = image_bytes.read()
        encoded_src = base64.b64encode(img_bytes).decode("ascii")
        file_suffix = image.content_type.split("/")[1]
        path_file = "./img/{}.{}".format(txt2md5(encoded_src), file_suffix)
        with open(path_file, 'wb') as f:
            f.write(img_bytes)

    return {"src": path_file}


def word2md(docx_file):
    import mammoth

    # with open("VPN使用文档.docx", "rb") as docx_file:

    result = mammoth.convert_to_html(
        docx_file, convert_image=mammoth.images.img_element(convert_img))
    html = result.value  # The generated HTML

    # 转化HTML为Markdown
    md = markdownify(html, heading_style='ATX')

    return md


def path2base64(path):
    with open(path, "rb") as f:
        byte_data = f.read()
    base64_str = base64.b64encode(byte_data).decode("ascii")  # 二进制转base64
    return base64_str


def st_markdown(md):
    img_path = re.findall('\./.*?jpe?g|\./.*?png', md)

    for path in img_path:
        md = md.replace(path, 'data:image/png;base64,'+path2base64(path))

    st.markdown(md)
