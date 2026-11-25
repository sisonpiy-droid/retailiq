import os
import shutil

# 1. Update app.py
with open("app.py", "r", encoding="utf-8") as f:
    text = f.read()

# Update Styling and Tabs
new_style = """
st.markdown(\"""
<style>
    .stApp {background-color: #F8F9FA;}
    h1, h2, h3, h4, h5, h6, p, span {color: #0F172A; font-family: 'Inter', sans-serif;}
    .metric-card {background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-top: 4px solid #2563EB;}
    .answer-card {background: white; padding: 24px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); margin-top: 20px;}
    .stButton>button {background-color: #2563EB; color: white; border-radius: 8px; font-weight: 600; border: none;}
    .stButton>button:hover {background-color: #1D4ED8;}
</style>
\""", unsafe_allow_html=True)
"""
text = text.replace('st.markdown("""\n<style>\n    .main {background-color: #f8f9fa;}\n    h1, h2, h3 {color: #1f2937; font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif;}\n    .metric-card {background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-top: 4px solid #3b82f6;}\n    .answer-card {background: white; padding: 24px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); margin-top: 20px;}\n</style>\n""", unsafe_allow_html=True)', new_style)

# We remove the sidebar navigation and replace with tabs
sidebar_orig = """with st.sidebar:
    st.markdown(f"### {st.session_state.username.capitalize()}")
    st.write(f"**Role:** {user['role'].title()}\\n\\n**Stores:** {', '.join(stores)}")
    st.divider()
    page = st.radio("Navigation", ["Overview", "Ask RetailIQ", "Evaluation"])
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()"""

sidebar_new = """with st.sidebar:
    st.markdown(f"### {st.session_state.username.capitalize()}")
    st.write(f"**Role:** {user['role'].title()}\\n\\n**Stores:** {', '.join(stores)}")
    st.divider()
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Ask RetailIQ", "Analytics", "History", "System Health"])
"""
text = text.replace(sidebar_orig, sidebar_new)

# Replace conditions based on `page == ` with `with tabX:`
text = text.replace('if page == "Overview":', 'with tab1:\n')
text = text.replace('elif page == "Ask RetailIQ":', 'with tab2:\n')
text = text.replace('elif page == "Evaluation":', 'with tab5:\n')

text = text.replace('st.title("Executive Overview")', '    st.title("Executive Overview")')
# Since replacing everything correctly for indentation is hard via simple replace, let's just do a clean regex or line-by-line shift
lines = text.split('\\n')
inside_tab1 = False
inside_tab2 = False
inside_tab5 = False
new_lines = []
for line in lines:
    if line.startswith('with tab1:'):
        inside_tab1 = True
        new_lines.append(line)
        continue
    elif line.startswith('with tab2:'):
        inside_tab1 = False
        inside_tab2 = True
        new_lines.append(line)
        continue
    elif line.startswith('with tab5:'):
        inside_tab2 = False
        inside_tab5 = True
        new_lines.append(line)
        continue
    
    if inside_tab1 or inside_tab2 or inside_tab5:
        # indent by 4 spaces
        if line.strip() != "":
            new_lines.append("    " + line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

text = "\\n".join(new_lines)

# Fill tabs 3 and 4 with simple placeholders to prevent errors
tab34_content = """
with tab3:
    st.title("Analytics")
    st.write("Deeper dive analytics to come.")

with tab4:
    st.title("History")
    if st.session_state.history:
        for h in st.session_state.history:
            st.write(f"Q: {h['q']}")
    else:
        st.write("No history.")
"""
text = text + tab34_content

with open("app.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated UI in app.py")
