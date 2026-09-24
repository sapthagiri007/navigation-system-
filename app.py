import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="Underwater Domain Awareness", page_icon="🌊", layout="wide")

st.markdown("""
<style>
.stApp{background:#06111b;color:#e8f7ff}
.block-container{padding-top:1rem;max-width:100%}
.card,.alert-card,.ok-card{border:1px solid #17465a;border-radius:8px;padding:12px;background:rgba(5,22,34,.78)}
.alert-card{border-color:#e22b2b;background:rgba(80,8,8,.30)}
.ok-card{border-color:#1f8a54;background:rgba(8,65,37,.22)}
.metric-label{font-size:12px;color:#8eabb8}
.metric-value{font-size:22px;font-weight:700}
.pipeline{border:1px solid #126078;border-radius:8px;padding:10px;text-align:center;min-height:105px;background:#071a27}
</style>
""", unsafe_allow_html=True)

if "objects" not in st.session_state:
    st.session_state.objects = pd.DataFrame([
        {"ID":"T-01","Classification":"Possible Submarine","Latitude":11.02,"Longitude":77.05,"Depth":312,"Speed":12.4,"Confidence":92,"Threat":"HIGH","Status":"ALERT"},
        {"ID":"T-02","Classification":"Ship","Latitude":11.08,"Longitude":77.22,"Depth":35,"Speed":8.1,"Confidence":96,"Threat":"LOW","Status":"NORMAL"},
        {"ID":"T-03","Classification":"Marine Animal","Latitude":10.90,"Longitude":77.00,"Depth":72,"Speed":4.3,"Confidence":88,"Threat":"LOW","Status":"NORMAL"},
    ])
df=st.session_state.objects

# Header
a,b,c,d=st.columns([4,1.2,1.2,1.7])
with a:
    st.markdown("## 🌊 UNDERWATER DOMAIN AWARENESS")
    st.markdown("### <span style='color:#00d9ff'>INTELLIGENT TRACKING & DECISION SUPPORT SYSTEM</span>",unsafe_allow_html=True)
with b:
    st.markdown("<div class='card'><div class='metric-label'>SYSTEM STATUS</div><div class='metric-value' style='color:#32d583'>● OPERATIONAL</div></div>",unsafe_allow_html=True)
with c:
    st.markdown("<div class='card'><div class='metric-label'>ACTIVE SENSORS</div><div class='metric-value' style='color:#32d583'>4/4</div></div>",unsafe_allow_html=True)
with d:
    st.markdown("<div class='alert-card'><b style='color:#ff4545'>⚠ SUBMARINE ALERT</b><br>1 CONTACT</div>",unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎛 SIMULATION CONTROLS")
    live=st.toggle("Live Tracking",False)
    interval=st.selectbox("Update Interval (sec)",[1,2,3,5],index=1)
    threshold=st.slider("Alert Confidence Threshold (%)",50,99,80)
    st.markdown("## 🖥 DISPLAY OPTIONS")
    st.checkbox("Show Track Labels",True)
    st.checkbox("Show Sensor Range",True)
    st.checkbox("Show Track History",True)
    st.markdown("## 📡 SENSOR STATUS")
    for n in ["SONAR Array","Sonobuoy Network","Hydrophone","Ocean Current Sensor"]:
        st.markdown(f"**◉ {n}** &nbsp; <span style='color:#32d583'>ONLINE</span>",unsafe_allow_html=True)
    st.markdown("## 🗺 LEGEND")
    st.markdown("🔴 Possible Submarine<br>🟨 Ship<br>🔵 Marine Animal<br>⚪ Background / Noise",unsafe_allow_html=True)
    st.info("Software prototype using simulated sensor data for academic demonstration.")

if live:
    rng=np.random.default_rng(int(time.time())%100000)
    for i in df.index:
        df.loc[i,"Latitude"]+=rng.normal(0,.0012)
        df.loc[i,"Longitude"]+=rng.normal(0,.0015)
    st.session_state.objects=df

left,right=st.columns([1.15,1.85])
with left:
    st.markdown("### 📍 TACTICAL TRACKING MAP" + ("  🟢 LIVE" if live else ""))
    m=df[["Latitude","Longitude"]].rename(columns={"Latitude":"lat","Longitude":"lon"})
    st.map(m,zoom=8,height=390)
    st.caption("SIMULATED COORDINATES • Academic prototype")
with right:
    st.markdown("### 🎯 CONTACTS - CLASSIFICATION SUMMARY")
    table=df.copy()
    table["Classification Confidence"]=table["Confidence"].astype(str)+"%"
    table["Threat Level"]=table["Threat"]+" ("+table["Status"]+")"
    table=table[["ID","Classification","Classification Confidence","Latitude","Longitude","Threat Level","Status"]]
    st.dataframe(table,use_container_width=True,hide_index=True,height=250)
    st.markdown(f"""<div class='card'><b style='color:#00d9ff'>ⓘ ALERT RULE:</b>
    Alert is generated <b>ONLY</b> when the contact is classified as
    <b style='color:#ff4545'>POSSIBLE SUBMARINE</b> and its classification confidence
    is above the selected threshold ({threshold}%).</div>""",unsafe_allow_html=True)
    sub=df[df["Classification"]=="Possible Submarine"].iloc[0]
    if int(sub["Confidence"])>=threshold:
        st.markdown(f"""<div class='alert-card'><h3 style='color:#ff4545'>⚠ POSSIBLE SUBMARINE DETECTED</h3>
        <b>Contact ID:</b> {sub["ID"]}<br><b>Classification Confidence:</b> {sub["Confidence"]}% |
        <b>Threshold:</b> {threshold}%<br><b>Threat Level:</b> HIGH<br>
        <b>Time:</b> {datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")}</div>""",unsafe_allow_html=True)
    else:
        st.markdown("<div class='ok-card'><h3>🟢 NO HIGH-CONFIDENCE SUBMARINE ALERT</h3>Continue monitoring.</div>",unsafe_allow_html=True)

st.divider()
x1,x2,x3=st.columns([1.5,1.5,1])
with x1:
    st.markdown("### 🔊 SENSOR SIGNAL ANALYSIS — T-01")
    x=np.linspace(0,10,300); rng=np.random.default_rng(5)
    y=np.sin(2*np.pi*1.2*x)+.30*np.sin(2*np.pi*5*x)+.22*rng.normal(size=len(x))
    st.line_chart(pd.DataFrame({"Acoustic Signal":y},index=x),height=230)
    st.caption("Signal Type: Acoustic | Sensor: SONAR Array | Frequency Band: 1–10 kHz")
with x2:
    st.markdown("### 📊 CLASSIFICATION CONFIDENCE — T-01")
    conf=pd.DataFrame({"Class":["Possible Submarine","Ship","Marine Animal","Background/Noise"],"Confidence":[92,4,3,1]}).set_index("Class")
    st.bar_chart(conf,y="Confidence",height=230)
    st.caption("Confidence is for the predicted class, not submarine probability.")
with x3:
    st.markdown("### 📋 TRACK INFORMATION — T-01")
    st.markdown(f"""**Speed** &nbsp; {sub["Speed"]:.1f} knots<br>
    **Direction** &nbsp; 128° SE<br>**Depth** &nbsp; {sub["Depth"]} m<br>
    **Last Updated** &nbsp; {datetime.now().strftime("%I:%M:%S %p")}<br>
    **Track Quality** &nbsp; <span style='color:#32d583'>GOOD</span>""",unsafe_allow_html=True)

st.divider()
st.markdown("### 🔄 PROCESSING PIPELINE")
steps=[("📡","1. SENSOR DATA<br>COLLECTION","SONAR, Sonobuoys, Hydrophones"),("🔗","2. DATA FUSION","Multi-sensor synchronization"),("〰","3. NOISE REDUCTION","Filtering & noise removal"),("📊","4. FEATURE EXTRACTION","MFCC, Spectrogram, Time-Frequency"),("🧠","5. AI/ML CLASSIFIER","Classification prediction"),("⚠","6. DECISION & ALERT","Class + confidence → Alert")]
cols=st.columns(6)
for col,(icon,title,desc) in zip(cols,steps):
    with col: st.markdown(f"<div class='pipeline'><div style='font-size:23px'>{icon}</div><b>{title}</b><br><small>{desc}</small></div>",unsafe_allow_html=True)

st.markdown("<p style='text-align:center;color:#00d9ff'>Underwater Domain Awareness Prototype System | Academic Demonstration Only</p>",unsafe_allow_html=True)
if live:
    time.sleep(interval)
    st.rerun()
