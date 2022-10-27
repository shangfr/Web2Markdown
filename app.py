# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:56:50 2022

@author: shangfr
"""
import streamlit as st
import streamlit.components.v1 as components
from utils import get_html,word2md,st_markdown


st.set_page_config(
    page_title="Auto TypeSetting App",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded",
)


def save_file(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        f.write(data)


def read_file(name):
    with open(name, 'r', encoding='utf-8') as f:
        data_f = f.read()
    return data_f


def rep_word(str1, rep_txt):
    rep_w = rep_txt.replace('，', ',').replace('；', ';').split(';')
    for w in rep_w:
        if w:
            wab = w.split(',')
            if len(wab) == 2:
                str1 = str1.replace(wab[0], wab[1])
    return str1


def change_callback():
    for key in st.session_state.keys():
        del st.session_state[key]


def text_callback():
    st.session_state['key02'] = st.session_state['key01']


def local_css(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown('<style>{}</style>'.format(f.read()),
                    unsafe_allow_html=True)


local_css("./css/mystyle.css")

col1, col2, col3, col4 = st.columns([5,2,1,1])
uploaded_file = st.file_uploader("Choose a file", on_change=change_callback)
if uploaded_file is not None:
    md_d = word2md(uploaded_file)
else:
    # UI

    url_p = 'http://yxgzal.cast.org.cn/art/2022/10/8/art_1751_199004.html'
    url = col1.text_input('输入网址：', url_p, on_change=change_callback)
    col4.info('')
    render_service = col4.checkbox('渲染服务', on_change=change_callback)
    
    md_d = get_html(url, render_service)

if 'key02' in st.session_state:
    md_doc = st.session_state['key02']
else:
    md_doc = md_d

n0 = md_doc.count('\n')
n1 = int(len(md_doc)/20)
n01 = max(n0, n1)

tool_opt = ['查看', '排版', '样式']
tool = col2.selectbox('功能', options=tool_opt)

if tool == tool_opt[0]:
    tool2 = col3.selectbox('排版', options=['后', '前'])
    if tool2 == '前':
        components.iframe(url, height=(n01+10)*23, scrolling=True)
    else:
        st_markdown(md_doc)

elif tool == tool_opt[1]:
    rep_txt = col3.text_input('替换', '')
    if rep_txt:
        print(rep_txt)
        md_doc = rep_word(md_doc, rep_txt)
        st.session_state['key02'] = md_doc

    col01, col02 = st.columns(2)
    with col01:
        st.header("Markdown编辑")
        md_doc_e = st.text_area('', md_doc, height=n01*23,
                                key='key01', on_change=text_callback)
    with col02:
        st.header("Markdown渲染")
        st_markdown(md_doc_e)
    save_file("./output/test.md", md_doc_e)

elif tool == tool_opt[2]:
    css_p = 'css/mystyle.css'
    css_f = read_file(css_p)
    n02 = css_f.count('\n')
    css_t = st.text_area('CSS', css_f, height=n02*23)
    save_file(css_p, css_t)
