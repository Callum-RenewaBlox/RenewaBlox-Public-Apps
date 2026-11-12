"""Electricity Portrait, by RenewaBlox — an anonymised church charity.

Fourteen months of half-hourly meter readings for a church charity, told in
plain English for its leaders, in three tabs: Charity consumption (a donut of
business against charity use, opened first), Electricity portrait (the
findings in full) and the June 2027 simulation. The page names no client,
address or meter number: it is the anonymised edition of a client analysis,
deployed at electricity-portrait.streamlit.app.

Self-contained: reads ``electricity_portrait.html`` (hand-authored; Inter, the
wordmark and the meter data inlined, no CDN, no requests) and renders it via
``st.iframe``, where its charts and tooltips run. No database, no secrets.

Public tool. Run locally:  streamlit run app_electricity_portrait.py
"""
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="RenewaBlox — Electricity Portrait",
    page_icon=":material/electric_bolt:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# The page is the whole app: strip Streamlit's chrome and padding so it fills
# the viewport and scrolls inside its own frame, keeping its header pinned.
st.markdown(
    """
    <style>
      [data-testid="stHeader"], [data-testid="stToolbar"],
      [data-testid="stDecoration"], [data-testid="stStatusWidget"],
      [data-testid="stBottomBlockContainer"], footer {display:none !important;}
      [data-testid="stAppViewContainer"] {overflow:hidden !important;}
      /* stMain scrolls by default and reserves a scrollbar gutter, which would
         leave a dead strip down the right-hand edge of a full-bleed page */
      [data-testid="stMain"] {overflow:hidden !important; height:100dvh !important;}
      [data-testid="stMain"] .block-container,
      [data-testid="stMainBlockContainer"], .block-container {
          padding:0 !important; margin:0 !important; max-width:100% !important;}
      [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockBorderWrapper"] {
          gap:0 !important;}
      [data-testid="stElementContainer"], [data-testid="element-container"] {
          width:100% !important;}
      [data-testid="stIFrame"] {
          height:100dvh !important; width:100% !important; display:block; border:0;}
      html, body, .stApp {overflow:hidden !important; background:#f4f8fa !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Read the page fresh on every run (Streamlit re-runs this script but can keep
# imported modules cached, so reading here keeps it current after a redeploy).
PAGE = (Path(__file__).resolve().parent / "electricity_portrait.html").read_text(
    encoding="utf-8")

# Nothing after the iframe: it owns the full 100dvh and stMain is
# overflow:hidden, so anything rendered below it could never be scrolled to.
st.iframe(PAGE, height=900)
