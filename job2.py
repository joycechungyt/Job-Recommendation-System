import streamlit as st
import pandas as pd
import pickle
def correct_type(s):
    make_str = str(s)
    remove_hyphen = make_str.replace("-", "")
    remove_slash = remove_hyphen.replace("/", "")
    return remove_slash.lower()
def recommend(choice):
    job_index = sample[sample["user"] == choice].index[0]
    job_index = sample.index.get_loc(job_index)
    distances = similarity[job_index]
    jobs_list = sorted(list(enumerate(distances)), reverse=True, key=lambda e: e[1])[1:11]

    jobs = []
    company = []
    city = []
    state = []
    for i in jobs_list:
        jobs.append(sample_csv.iloc[i[0]]["Position"])
        company.append(sample_csv.iloc[i[0]]["Company"])
        city.append(sample_csv.iloc[i[0]]["City"])
        state.append(sample_csv.iloc[i[0]]["State.Name"])
    return jobs, company, city, state

data = pickle.load(open("sample_dict.pkl", "rb"))
sample = pd.DataFrame(data)
similarity = pickle.load(open("similarity.pkl", "rb"))
sample_csv = pd.read_csv("sample_csv.csv")

st.title("Hiring Portal")

pos = st.selectbox("Select Title", ["Which kind of Job are you looking for?"] + list(sample_csv["Position"].unique()))

col1, col2 = st.columns(2)
with col1:
    specific_states = sample_csv[sample_csv["Position"] == pos]
    sta = st.selectbox("Available State", sorted(list(specific_states["State.Name"].unique())))
with col2:
    specific_cities = specific_states[specific_states["State.Name"] == sta]
    ci = st.selectbox("Available City", sorted(list(specific_cities["City"].unique())))

col3, col4 = st.columns(2)
with col3:
    et = st.selectbox("Available Employment Type", list(specific_cities["Employment.Type"].unique()))
with col4:
    er = st.selectbox(" Required Education", list(specific_cities["Education.Required"].unique()))

try:
    if st.button("Search Jobs", use_container_width = True):
        inp_pos = correct_type(pos).lower()
        inp_sta = sta.replace(" ", "").lower()
        inp_ci = ci.replace(" ", "").lower()
        inp_et = correct_type(et).lower()
        inp_er = er.replace(" ", "").lower()

        inp_user = inp_pos + " " + inp_ci + " " + inp_sta + " " + inp_et + " " + inp_er

        rec_jobs, rec_company, rec_city, rec_state = recommend(inp_user)

        rec_data = {"Jobs" : rec_jobs, "Company" : rec_company, "City" : rec_city, "State" : rec_state}
        rec_df = pd.DataFrame(rec_data)
        rec_df.index = rec_df.index + 1

        st.table(rec_df)
except:
    st.error("Please select Job Title")