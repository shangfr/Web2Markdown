# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:56:50 2022

@author: 86155
"""

import requests
from urllib.parse import urlparse
from markdownify import markdownify
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
   page_title="Auto TypeSetting App",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)


def local_css(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown('<style>{}</style>'.format(f.read()),
                    unsafe_allow_html=True)

@st.cache
def get_html(url):
    r = requests.get(url)

    if r.status_code == 200:
        if r.encoding == "ISO-8859-1":
            html_d = r.text.encode("ISO-8859-1").decode("utf-8")
        else:
            html_d = r.text  # utf-8编码直接用，

        return html_d
    else:
        return None

@st.cache
def save_md(name, md_d):
    with open(f"{name}.md", 'w', encoding='utf-8') as f:
        f.write(md_d)

  
def show_markdown(html_d):
    md_data = markdownify(html_d)
    netloc = url_p.netloc
    scheme = url_p.scheme
    md_d = md_data.replace("](/", f"]({scheme}://{netloc}/")
    st.markdown(md_d)
    save_md("test", md_d)


local_css("./css/mystyle.css")

url = st.text_input(
    '输入网址：', 'http://yxgzal.cast.org.cn/art/2022/10/8/art_1751_199004.html')

url_p = urlparse(url)


tab1, tab2, tab3 = st.tabs(["排版前", "排版后", "资料"])

with tab1:
    st.header("排版前")
    components.iframe(url,height=1600,scrolling=True)
    
with tab2:
    st.header("排版后")
    html_d = get_html(url)
    
    
    if html_d:
        md_d = markdownify(html_d)
        netloc = url_p.netloc
        scheme = url_p.scheme
        md_d = md_d.replace("](/", f"]({scheme}://{netloc}/")
        md_d = md_d.replace("\n\n\n\n\n", "\n\n").replace("\n\n\n\n", "\n\n").replace("\n\n\n", "\n\n")
        with st.expander("手动修改"):
            txt = st.text_area('Text to analyze', md_d,height=500)
        st.markdown(txt)
        save_md("./output/test", txt)




