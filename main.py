#v7
import time
import random
from datetime import datetime

import dbattempt
import pandas as pd
import streamlit as st
container = st.empty()

def next(mode="button"):
    container.empty()
    st.session_state.page += 1
    if mode == "normal": st.rerun()
def get_id_and_order():
    # attempt
    st.session_state.columns, st.session_state.row = dbattempt.attempt(
        st.session_state.declaration_inputs, st.session_state.demography_inputs)
    st.session_state.id = st.session_state.row[0]

    # for first recall & recognition tests
    c0f = st.session_state.c0f = st.session_state.row[1]
    c1f = st.session_state.row[2] if c0f == "A" else st.session_state.row[5]
    c2fp = st.session_state.c2fp = st.session_state.row[3] if c0f == "A" else st.session_state.row[6]
    c2fn = st.session_state.c2fn = st.session_state.row[4] if c0f == "A" else st.session_state.row[7]
    c3f = st.session_state.c3f = f"{st.session_state.c0f}00"

    # for second recall & recognition tests
    c0s = st.session_state.c0s = "B" if st.session_state.row[1] == "A" else "A"
    c1s = st.session_state.row[2] if c0s == "A" else st.session_state.row[5]
    c2sp = st.session_state.c2sp = st.session_state.row[3] if c0s == "A" else st.session_state.row[6]
    c2sn = st.session_state.c2sn = st.session_state.row[4] if c0s == "A" else st.session_state.row[7]
    c3s = st.session_state.c3s = f"{st.session_state.c0s}00"

    # get the lists
    st.session_state.order = [
        f"{c0f}{c1f}{c2fp}", f"{c0f}{c1f}{c2fn}", f"{c3f}",
        f"{c0s}{c1s}{c2sp}", f"{c0s}{c1s}{c2sn}", f"{c3s}"]
    
    for k, v in zip((
        "recall0", "recall1", "recognition0", "recall2", "recall3", "recognition1"), st.session_state.order):
        with open(fr"words/{v}.txt", mode="r", encoding="UTF-8") as file:
            words = [x[:-1] if x.endswith("\n") else x for x in file.readlines()]
        random.shuffle(words)
        st.session_state[k] = words
    st.session_state[f"{c0f}_get_recognition_binary"] = [None for i in st.session_state.recognition0]
    st.session_state[f"{c0f}_get_recognition_scale"] = [None for i in st.session_state.recognition0]
    st.session_state[f"{c0s}_get_recognition_binary"] = [None for i in st.session_state.recognition1]
    st.session_state[f"{c0s}_get_recognition_scale"] = [None for i in st.session_state.recognition1]

    # informations
    print(f"Tarih:      {st.session_state.row[8]}")
    print(f"Sıralama:   {'*'.join(i for i in st.session_state.order)}")      
    print(f"ID:         {st.session_state.id}")
    time.sleep(1)
def put_declaration(inputs):
    st.session_state.vname, st.session_state.vnumber, st.session_state.gname, st.session_state.gnumber = inputs
    if (st.session_state.vname != "") and (st.session_state.vnumber != ""):
        st.session_state.declaration_inputs = inputs
        del st.session_state.warning
        next()
    else: st.session_state.warning = "Lütfen kırmızı ile işaretlenmiş alanları doldurunuz." 
def put_demography():
    for i in range(len(st.session_state.qkeys)):        
        if (st.session_state[st.session_state.qkeys[i]] == None or 
            st.session_state[st.session_state.qkeys[i]] == ""):
            if (not st.session_state.questions[i].startswith(":red[")) and (
                not st.session_state.questions[i].endswith("]")):
                st.session_state.questions[i] = ":red[" + st.session_state.questions[i] + "]"
        else: st.session_state.questions[i] = st.session_state.questions[i].replace(":red[", "").replace("]","")
    
    inputs = list()    
    for i in range(len(st.session_state.qkeys)):
        if i in (3,) and st.session_state[st.session_state.qkeys[i-1]] == "Hayır": 
            st.session_state.questions[i] = st.session_state.questions[i].replace(":red[", "").replace("]","")
            inputs.append("Hayır")
        else:inputs.append(st.session_state[st.session_state.qkeys[i]])
    
    if all(inputs) == True:
        st.session_state.demography_inputs = inputs
        del st.session_state.warning
        get_id_and_order()
        next()
    else: st.session_state.warning = "Lütfen kırmızı ile işaretlenmiş alanları doldurunuz."   
def attention_button(i, mode):
    st.session_state.attention[i] = "🟢" if mode == True else "🔴"
def recall_instructions(i):
    if i < 2: instruction = f'<div style="text-align: center; font-size: 36px; padding-top: 128px">{st.session_state.instructions[i] if st.session_state.order[i][1] != 2 else st.session_state.instructions[i][115:]}</div>'
    elif i == 2: instruction = f'<div style="text-align: center; font-weight: bold; font-size: 24px; padding-top: 6px;">{st.session_state.instructions[i]}</div>'
    elif i == 3: instruction = f'<div style="text-align: center; font-size: 36px; padding-top: 128px">{st.session_state.instructions[i]}</div>'
    duration = 15 if i != 2 else 60

    if i == 2:
        if "start" not in st.session_state:
            st.session_state.anumbers = [i for i in range(280,10,-3)]
            st.session_state.aoptions = [random.choice((True,False)) for i in range(90)]
            st.session_state.attention = [" " for i in range(90)]
            st.session_state.atrue = [f"atrue{i}" for i in range(90)]
            st.session_state.afalse = [f"afalse{i}" for i in range(90)]
            st.session_state.start = datetime.now()
        
        with container.container():
            st.markdown(instruction,  unsafe_allow_html=True)
            st.markdown(f'<div style="text-align: center; font-weight: bold; font-size: 24px; padding-top: 6px;">{" "}</div>',  unsafe_allow_html=True)
            for i in range(90):
                columns = st.columns(4)
                columns[0].markdown(f'<div style="text-align: right; font-weight: bold; font-size: 24px;">{st.session_state.attention[i]}</div>', unsafe_allow_html=True)
                columns[1].markdown(f'<div style="text-align: center; font-weight: bold; font-size: 24px;">{st.session_state.anumbers[i] if st.session_state.aoptions[i] == True else st.session_state.anumbers[i]-1}</div>', unsafe_allow_html=True)
                columns[2].button("Doğru", key=st.session_state.atrue[i], on_click=attention_button, args=(i, True if st.session_state.aoptions[i] == True else False))
                columns[3].button("Yanlış", key=st.session_state.afalse[i], on_click=attention_button, args=(i, False if st.session_state.aoptions[i] == True else True))

        while (datetime.now() - st.session_state.start).total_seconds() < duration: time.sleep(1)
        else:
            time.sleep(2)
            del st.session_state.anumbers
            del st.session_state.aoptions
            del st.session_state.attention
            del st.session_state.atrue
            del st.session_state.afalse
            del st.session_state.start
            next("normal")

    else:
        with container:
            st.markdown(instruction,  unsafe_allow_html=True)
            time.sleep(duration)
        next("normal")
def recall_show_words(words):
    with container:
        for word in words:
            st.markdown(f'<div style="text-align: center; font-size: 128px; padding-top: 256px">{word}</div>', unsafe_allow_html=True)
            time.sleep(2)
    next("normal")
def recall_get_words(key):
    if "start" not in st.session_state:
        st.session_state.recall = list() 
        st.session_state.start = datetime.now()
    
    with container.container():
        st.markdown("""<style> 
        [data-baseweb="textarea"] {
        border-bottom-color: #000000; border-top-color: #000000; border-right-color: #000000; border-left-color: #000000;
        border-bottom-width: 2px; border-top-width: 2px; border-right-width: 2px; border-left-width: 2px;}
        [data-baseweb="textarea"] > [data-baseweb="base-input"] > textarea { height: 72px;  font-size: 2rem;}
        .st-emotion-cache-f4ro0r { align-items: center;}
        </style>""", unsafe_allow_html=True)
        st.markdown(f'<div style="color:red; font-size: 16px; font-weight: bold; text-align: left;">"ENTER" tuşuna bastığınızda yazdığınız kelime ekrandan kaybolacak ve kaydedilecektir.</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:red; font-size: 16px; font-weight: bold; text-align: left;">Bitirmek için formun sonundaki "Tamamladım" tuşuna basınız.</div>', unsafe_allow_html=True)
        st.chat_input("", key=f"{key}RECALLINPUT")
        st.session_state.recall.append(st.session_state[f"{key}RECALLINPUT"])
        st.button("Tamamladım", key=f"{key}RECALLPOST", on_click=recall_save_words, args=(key,), use_container_width=True)
    
    while (datetime.now() - st.session_state.start).total_seconds() <= 180:
        st.session_state.duration = (datetime.now() - st.session_state.start).total_seconds()
        time.sleep(1)
    else: recall_save_words(key, "timeout")
def recall_save_words(key, mode="button"):
    st.session_state.recall = ",".join([i for i in st.session_state.recall if i != None])
    dbattempt.put("observations", f"{key}RECALLRESULTS", (st.session_state.recall, st.session_state.id))
    dbattempt.put("observations", f"{key}RECALLDURATION", (st.session_state.duration, st.session_state.id))
    del st.session_state.duration
    del st.session_state.recall
    del st.session_state.start
    next(mode="normal" if mode=="timeout" else "button")
def distractor_clear():
    with container:
        st.markdown("""---""")
    time.sleep(1)
    next("normal")
def distractor_start():
    if "start" not in st.session_state:
        st.session_state.doptions = list()
        for i in range(10, len(st.session_state.countries)-10):
            st.session_state.doptions.append(sorted([st.session_state.cities[i-5], st.session_state.cities[i-10], st.session_state.cities[i], st.session_state.cities[i+5], st.session_state.cities[i+10]], key=lambda x: random.random()))
        st.session_state.dscore = 0
        st.session_state.start = datetime.now()    

   
    with container.container():
        row0 = st.container()
        row0.markdown(f'<div style="text-align: center; font-weight: bold; font-size: 18px; padding-top: 6px;">Lütfen beş dakika içerisinde aşağıdaki ülkelerin başkentlerini işaretleyiniz.</div>', unsafe_allow_html=True)
        
        row1 = st.container()
        columns1 = row1.columns(2)
        counter = columns1[0].empty()
        score = columns1[1].empty()
        
        row2 = st.container()
        row2.markdown("""<style> p { font-size: 18px !important; } </style> """, unsafe_allow_html=True)
        columns2 = row2.columns(3)

    for i in range(3):
        with columns2[i]:
            for i in range(10+(i*25), 35+(i*25)): st.radio(
                f"({i-9}) {st.session_state.countries[i]}",
                st.session_state.doptions[i-10],
                index=None, key=f"distractor{i}",
                on_change=distractor_change)
       
    while (datetime.now() - st.session_state.start).total_seconds() < 300:
        st.session_state.dduration = 300 - round((datetime.now() - st.session_state.start).total_seconds())
        counter.markdown(f'<div style="text-align: center; font-weight: bold; font-size: 24px; padding-top: 6px;">{st.session_state.dduration} saniyeniz kaldı.</div>', unsafe_allow_html=True)
        score.markdown(f'<div style="text-align: center; font-weight: bold; font-size: 24px; padding-top: 6px;">{st.session_state.dscore} puan kazandınız.</div>', unsafe_allow_html=True)
        time.sleep(0.1)
    else:
        time.sleep(2)
        del st.session_state.dduration
        del st.session_state.dscore
        del st.session_state.doptions
        del st.session_state.start
        next("normal")
def distractor_change():
    st.session_state.dscore = 0
    for i in range(10,85):
        if st.session_state.cities[i] == st.session_state[f"distractor{i}"]:
            st.session_state.dscore += 10
def recognition_get_words(key, k):
    if "warning" not in st.session_state:
        st.session_state.warning = ""
    if "start" not in st.session_state:
        st.session_state.recognitionb = [None for i in st.session_state[f"recognition{k}"]]
        st.session_state.recognitions = [None for i in st.session_state[f"recognition{k}"]]
        st.session_state.start = datetime.now()
    
    with container.container():
        st.markdown("""<style> p { font-size: 18px !important; } </style> """, unsafe_allow_html=True)
        row0 = st.container()
        row1 = st.container()
    
    # instructions
    with row0:
        for i in range(len(st.session_state.instructions[4:])):
            if i == 0: st.markdown(f'<div style="text-align: justify; font-size: 18px;">{st.session_state.instructions[4+i]}</div>', unsafe_allow_html=True)
            else:
                if i == 1: st.markdown(f'<div style="text-align: justify; font-weight: bold; font-size: 18px; padding-top: 12px;">{st.session_state.instructions[4+i]}</div>', unsafe_allow_html=True)
                else: st.markdown(f'<div style="text-align: justify; font-weight: bold; font-size: 18px;">{st.session_state.instructions[4+i]}</div>', unsafe_allow_html=True)

    # radio buttons
    binary = list()
    scale = list()
    with row1:   
        for i in range(len(st.session_state[f"recognition{k}"])):
            row = row1.container()
            with row:
                st.markdown("""---""", unsafe_allow_html=True) 
                columns = st.columns((1,1,2))
                with columns[0]:
                    st.markdown(f'<div style="color:red; font-size: 1px; text-align: center; padding-top: 36px; padding-bottom: 36px;"> </div>', unsafe_allow_html=True)
                    st.markdown(st.session_state[f"recognition{k}"][i])
                with columns[1]:
                    binary.append(
                        st.radio(st.session_state[f"recognition{k}"][i],
                                options=st.session_state.recognition_options[:2],
                                index=st.session_state.recognition_options[:2].index(st.session_state.recognitionb[i]) if st.session_state.recognitionb[i] != None else None,
                                horizontal=False, label_visibility="hidden"))
                with columns[2]:
                    scale.append(
                        st.radio(st.session_state[f"recognition{k}"][i],
                                options=st.session_state.recognition_options[2:],
                                index=st.session_state.recognition_options[2:].index(st.session_state.recognitions[i]) if st.session_state.recognitions[i] != None else None,
                                horizontal=False, label_visibility="hidden"))
        st.markdown(f'<div style="color:red; font-size: 24px; text-align: center; padding-top: 12px;">{st.session_state.warning}</div>', unsafe_allow_html=True)
        st.button("Tamamladım", key=f"{key}_post_recall", on_click=recognition_save_words, args=(key,k,binary,scale), use_container_width=True)
def recognition_save_words(key, k, binary,scale):    
    st.session_state.duration = (datetime.now() - st.session_state.start).total_seconds()
    st.session_state.recognitionb = binary
    st.session_state.recognitions = scale
    if all(binary) == True and all(scale) == True:
        words = ",".join([i.replace(":red[", "").replace("]","") for i in st.session_state[f"recognition{k}"]])
        binary = ",".join(["1" if i.replace(":red[", "").replace("]","") == st.session_state.recognition_options[0] else "0" for i in binary])
        scale = ",".join([i.replace(":red[", "").replace("]","")[1] for i in scale])
        dbattempt.put("observations", f"{key}RECOGNITIONWORDS", (words, st.session_state.id))
        dbattempt.put("observations", f"{key}RECOGNITIONBINARY", (binary, st.session_state.id))
        dbattempt.put("observations", f"{key}RECOGNITIONSCALE", (scale, st.session_state.id))
        dbattempt.put("observations", f"{key}RECOGNITIONDURATION", (st.session_state.duration, st.session_state.id))
        del st.session_state.duration
        del st.session_state.recognitions
        del st.session_state.recognitionb
        del st.session_state.start
        del st.session_state.warning
        next()
    else:
        for i in range(len(st.session_state[f"recognition{k}"])):
            if binary[i] == None or scale[i] == None:
                if not st.session_state[f"recognition{k}"][i].startswith(":red[") and not st.session_state[f"recognition{k}"][i].endswith("]"):
                    st.session_state[f"recognition{k}"][i] = ":red[" + st.session_state[f"recognition{k}"][i] + "]"
            else: st.session_state[f"recognition{k}"][i] = st.session_state[f"recognition{k}"][i].replace(":red[", "").replace("]","")
        st.session_state.warning = "Lütfen kırmızı ile işaretlenmiş alanları doldurunuz."

# initializing
if "page" not in st.session_state:
    st.session_state.page = 0

    # declarations
    with open(r"forms/declaration.txt", mode="r", encoding="UTF-8") as file:
        declaration = [x[:-1] if x.endswith("\n") else x for x in file.readlines()]
    titles = [declaration[x] for x in range(len(declaration)) if x % 2 == 0]
    descriptions = [declaration[x] for x in range(len(declaration)) if x % 2 == 1]
    st.session_state.declarations = tuple(zip(titles, descriptions))
    st.session_state.vname = st.session_state.vnumber = ""
    st.session_state.gname = st.session_state.gnumber = ""

    # demography
    with open(r"forms/demography.txt", mode="r", encoding="UTF-8") as file:
        demography = [x[:-1] if x.endswith("\n") else x for x in file.readlines()]
    st.session_state.questions = [demography[x] for x in range(len(demography)) if x % 4 == 0]
    st.session_state.qkeys = [demography[x] for x in range(len(demography)) if x % 4 == 1]              
    st.session_state.qtypes = [demography[x] for x in range(len(demography)) if x % 4 == 2]
    st.session_state.qoptions = [demography[x].split(",") for x in range(len(demography)) if x % 4 == 3]
    for k in st.session_state.qkeys: st.session_state[k] = None

    # instructions
    with open(r"forms/instructions.txt", mode="r", encoding="UTF-8") as file:
        st.session_state.instructions = [x[:-1] if x.endswith("\n") else x for x in file.readlines()]
    
    # recognition options
    st.session_state.recognition_options = [
    "GÖRDÜM", "GÖRMEDİM",
    "(1) Gördüğüme eminim",
    "(2) Gördüğümü düşünüyorum ama emin değilim",
    "(3) Görmediğimi düşünüyorum ama emin değilim",
    "(4) Görmediğime eminim"]

    #distractor
    st.session_state.cc = pd.read_excel(r"forms/capitalcities.xlsx")
    st.session_state.cities = st.session_state.cc["City"].values.tolist()
    st.session_state.countries = st.session_state.cc["Country"].values.tolist()

    # start
    time.sleep(1)
# for declaration & demography forms
if st.session_state.page == 0:
    if "warning" not in st.session_state: st.session_state.warning = ""
    containers = container.container()
    
    # header
    header = "BİLGİLENDİRİLMİŞ GÖNÜLLÜ OLUR FORMU"
    row0 = containers.container()
    # declarations
    row1 = containers.container()
    # inputs
    inputs, labels = [], [
        "Gönüllü Adı Soyadı:", "Gönüllü Telefon Numarası:",
        "(Var ise) Vasi Adı Soyadı:", "(Var ise) Vasi Telefon Numarası:"]      
    row2 = containers.container()
    columns = row2.columns(2)

    # create
    with row0: 
        st.markdown(f'<div style="font-size: 28px; font-weight: bold; text-align: center;">{header}</div>', unsafe_allow_html=True)
    with row1:
        for d in range(len(st.session_state.declarations)):
            st.markdown(f'<div style="font-size: 20px; font-weight: bold; text-align: left; padding-top: 12px;">{st.session_state.declarations[d][0]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size: 16px; text-align: justify; padding-top: 12px;">{st.session_state.declarations[d][1]}</div>', unsafe_allow_html=True)
        st.markdown("""---""", unsafe_allow_html=True)
    with row2:
        st.markdown("""<style>
        p { font-size: 16px !important; }
        input { font-size: 16px !important; } 
        </style> """,
        unsafe_allow_html=True)
    with columns[0]:
        inputs.append(st.text_input(f":{'black' if st.session_state.warning == '' else 'red'}[{labels[0]}]", value=st.session_state.vname))
        inputs.append(st.text_input(f":{'black' if st.session_state.warning == '' else 'red'}[{labels[1]}]", value=st.session_state.vnumber))
    with columns[1]:
        inputs.append(st.text_input(labels[2], value=st.session_state.gname))
        inputs.append(st.text_input(labels[3], value=st.session_state.gnumber))  
    with row2:
        st.markdown(f'<div style="color:red; font-size: 24px; text-align: center; padding-top: 12px;">{st.session_state.warning}</div>', unsafe_allow_html=True)
        st.button("Onaylıyorum", on_click=put_declaration, args=(inputs,), use_container_width=True)
if st.session_state.page == 1:
    if "warning" not in st.session_state: st.session_state.warning = ""
    form = container.form("form_demography")
    
    js = '''<script>
        var body = window.parent.document.querySelector(".main");
        console.log(body);
        body.scrollTop = 0;
    </script>'''
    st.components.v1.html(js)

    # create
    with form:
        st.markdown("""<style>
        p { font-size: 16px !important; }
        input { font-size: 16px !important; } 
        </style> """,
        unsafe_allow_html=True)
        for q in range(len(st.session_state.questions)):
            if st.session_state.qtypes[q] == "0": st.text_input(
                label=st.session_state.questions[q],
                key=st.session_state.qkeys[q],
                value=st.session_state[st.session_state.qkeys[q]])
            if st.session_state.qtypes[q] == "1": st.number_input(
                label=st.session_state.questions[q],
                key=st.session_state.qkeys[q],
                value=st.session_state[st.session_state.qkeys[q]],
                min_value=0, step=1)
            if st.session_state.qtypes[q] == "2": st.radio(
                label=st.session_state.questions[q],
                key=st.session_state.qkeys[q],
                options=st.session_state.qoptions[q],
                index=st.session_state.qoptions[q].index(st.session_state[st.session_state.qkeys[q]]) if st.session_state[st.session_state.qkeys[q]] != None else None,
                horizontal=True)
        st.markdown(f'<div style="color:red; font-size: 24px; text-align: center; padding-top: 12px;">{st.session_state.warning}</div>', unsafe_allow_html=True)
        st.form_submit_button("Onayla", on_click=put_demography, use_container_width=True)
    
# for first recall test show
elif st.session_state.page == 2: recall_instructions(0)
elif st.session_state.page == 3: recall_show_words(st.session_state.recall0)
elif st.session_state.page == 4: recall_instructions(1)
elif st.session_state.page == 5: recall_show_words(st.session_state.recall1)
# for first recall test input 
elif st.session_state.page == 6: recall_instructions(2)
elif st.session_state.page == 7: recall_instructions(3)
elif st.session_state.page == 8: recall_get_words(st.session_state.c0f)
# for first recognition test
elif st.session_state.page == 9: recognition_get_words(st.session_state.c0f, 0)
# distractor part
elif st.session_state.page == 10: distractor_clear()
elif st.session_state.page == 11: distractor_start()
elif st.session_state.page == 12: distractor_clear()
# for second recall test show
elif st.session_state.page == 13: recall_instructions(0)
elif st.session_state.page == 14: recall_show_words(st.session_state.recall2)
elif st.session_state.page == 15: recall_instructions(1)
elif st.session_state.page == 16: recall_show_words(st.session_state.recall3)
# for second recall test input 
elif st.session_state.page == 17: recall_instructions(2)
elif st.session_state.page == 18: recall_instructions(3)
elif st.session_state.page == 19: recall_get_words(st.session_state.c0s)
# for second recognition test
elif st.session_state.page == 20: recognition_get_words(st.session_state.c0s, 1)
# thank you
elif st.session_state.page == 21:
    msg = "Deneyimize katıldığınız için teşekkür ederiz."
    with container: st.markdown(f'<div style="text-align: center; font-weight: bold; font-size: 36px; padding-top: 256px;">{msg}</div>', unsafe_allow_html=True)
