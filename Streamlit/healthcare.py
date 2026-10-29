import pandas as pd
import streamlit as st
from streamlit.elements import plotly_chart
from streamlit_option_menu import option_menu
import plotly.express as px


st.set_page_config(
    page_title="HealthCare Analytics",layout="wide",page_icon="💊"
)
df=pd.read_csv("healthcare.csv")
with st.sidebar:
    selected1=option_menu("Main-Menu",["Home","Dataset","Review","HealthCare Analytics","Data Assistant","About Us"],
                         icons=["house","table","bar-chart","graph-up","robot","info-circle"],
                         menu_icon="hospital",default_index=3)

if selected1=="Home":
    st.title("Healthcare Intelligence")
    st.write("Healthcare Intelligence is the integration of advanced data analytics, clinical metrics, and operational insights to drive smarter medical ecosystems. It empowers healthcare organizations to transform raw data into predictive, actionable strategies—ultimately improving patient care quality while maximizing operational and financial efficiency")
    st.divider()
    s1,s2,s3=st.columns(3)
    s1.metric("Total Patients:",df["patient_id"].count())
    s2.metric("Total Earnings:",df["total_cost_€"].sum())
    s3.metric("Avg Rating:",f"{df["satisfaction_score"].mean():,.1f}")

    st.divider()

    pat=df["department"].value_counts().reset_index()


    st.subheader("Patient Analysis")
    q1,q2=st.columns(2)
    with q1:
        fig5 = px.bar(pat, y="department", x="count",orientation="h")
        st.plotly_chart(fig5)
    with q2:
        st.subheader("Count")
        st.dataframe(pat)
    st.info("No. Of Patients Are Almost Same Across All Departments")

    st.subheader("Length Of Stay ")
    stay=df.groupby("department")["length_of_stay_days"].mean()
    fig6=px.pie(values=stay.values,names=stay.index,hole=0.5)
    st.plotly_chart(fig6)
    st.info("Average Length Of Stay Is 3 Days")

elif selected1 =="Dataset":

    st.title("Dataset Explorer")
    st.divider()

    col1,col2,col3=st.columns(3)
    col1.metric("Total Rows:",df.shape[0])
    col2.metric("Total Columns:",df.shape[1])
    col3.metric("Missing Values:",df.isna().sum().sum())

    st.subheader("Select Column")
    selected_column=st.multiselect("Select Columns to display",df.columns,default=df.columns)
    filtered_df=df[selected_column]
    st.dataframe(filtered_df)

    if st.checkbox("Show Full Dataset"):
        st.dataframe(df)

    st.subheader("Search in Dataset")
    search_value=st.text_input("Enter Value to Search")
    if search_value:
        filtered_df=filtered_df[filtered_df.astype(str).apply(
            lambda row:row.str.contains(search_value,case=False).any(),axis=1
        )]
        st.dataframe(filtered_df)

elif selected1=="Review":
        sum1 = df["total_cost_€"].sum()

        st.header("Hospital Overview")
        st.divider()
        col1,col2 = st.columns(2)
        col1.metric("Total Patients:", df["patient_id"].sum())
        col2.metric("Revenue:",f"{sum1:,.1f}","Target:10M")
        st.divider()

        table_m=df.groupby("department").agg(
            Total_Revenue=("total_cost_€","sum"),
            No_Of_Complication=("complications", "sum"),
            Avg_Admiited_Days=("length_of_stay_days","mean"),
            Avg_Rating=("satisfaction_score","mean")
        )
        table_m["Revenue Share%"]=(table_m["Total_Revenue"]/sum1 *100)

        st.title("Hospital Info Matrix")
        st.dataframe(table_m.style.format({
            "Total_Revenue":"{:,.2f}",
            "Avg_Admiited_Days":"{:,.0f}",
            "Avg_Rating":"{:,.1f}"


        }).background_gradient(subset=["Total_Revenue"],cmap="YlOrBr"))

        st.subheader("Operational Efficiency")
        col_eff1=df.groupby("department").agg(
            Avg_Waiting_Time_In_Minutes=("wait_time_min","mean"),
            Procedure_Count=("procedures_count","sum"),
            Complication_Count=("complications","sum"),
            Readmitted_In_30Days=("readmitted_30d","sum")
        )
        st.dataframe(col_eff1.style.highlight_max(axis=0,color="#fb352b").highlight_min(axis=0,color="#2bfbbb"))

        st.title("Insights")
        st.divider()
        k1,k2,k3=st.columns(3)
        k1.metric("Avg Cost:",f"{df["total_cost_€"].mean():,.0f}€","+5% v/s Last_Year")
        k2.metric("Avg Age:",f"{df["age"].mean():,.0f}","-10% v/s Last_Year")
        k3.metric("Avg_Rating:",f"{df["satisfaction_score"].mean():,.1f}")

        if st.checkbox("Show Full Dataset"):
            st.dataframe(df)

        st.subheader("Column Statistics")
        numeric_col=df.select_dtypes(include=["int64","float64"]).columns

        if len(numeric_col) > 0:
            selected_col=st.selectbox("Select column name:",numeric_col)
            st.write(df[selected_col].describe())

elif selected1=="HealthCare Analytics":

    st.title("Healthcare Dashboard")
    s1,s2=st.tabs(["Patients","Revenue"])
    with s1:
        st.subheader("Department wise Patients")
        fig1 = px.sunburst(df, path=["department", "gender"])
        fig1.update_layout(height=500)
        st.plotly_chart(fig1,use_container_width=True)
        st.info("Both Gender Are Almost Same Across All Department")

    with s2:
        st.subheader("Department wise Revenue")
        rev=df.groupby("department")["total_cost_€"].sum().reset_index()
        fig2=px.bar(rev,x="department",y="total_cost_€",color="department")
        st.plotly_chart(fig2)

    st.divider()
    st.subheader("Readmission Rate")
    readm=df["readmitted_30d"].value_counts()
    fig3=px.pie(values=readm.values,names=readm.index)
    st.plotly_chart(fig3)
    st.success("Almost 80% Of People Recoverd Fully")

    s3,s4=st.tabs(["Waiting time","Age"])
    with s3:
        st.subheader("Waiting Time Analysis")
        fig4=px.box(df,x="department",y="wait_time_min",color="department")
        st.plotly_chart(fig4)
        st.info("Average Waiting Time For Patients is almost 30 Minutes ")

    with s4:
        st.subheader("Age Analysis")
        fig7 = px.box(df["age"])
        st.plotly_chart(fig7)
        st.info("Average Age of Person Is 53")


    s5,s6=st.tabs(["Condition","Admission"])
    with s5:
        st.subheader("Patient Condition Chronic(1) Or Not(0)")
        cc = df["chronic_condition"].value_counts()
        fig10 = px.pie(values=cc.values, names=cc.index,hole=0.5,color_discrete_sequence=["#21DE34","#E60B0B"])
        st.plotly_chart(fig10)

    with s6:
        st.subheader("Patient Admission Type")
        at = df["admission_type"].value_counts()
        fig11 = px.pie(values=at.values, names=at.index,color_discrete_sequence=["#E60B0B","#21DE34"])
        st.plotly_chart(fig11)
    st.divider()


    st.subheader("Patient Rating Distribution")
    fig15=px.histogram(df["satisfaction_score"])
    st.plotly_chart(fig15)
    st.divider()

elif selected1=="Data Assistant":
    st.title("Data Assistant")
    st.divider()

    st.write("Ask Questions and Get Visual Analytics")
    user_q=st.text_input("Ask Me Question")

    if user_q:
        q=user_q.lower()

        if "age" in q:
            fig7=px.box(df["age"])
            st.plotly_chart(fig7)
            st.info("Average Age of Person Is 53")

        elif "patients" in q:
            pat=df["department"].value_counts()
            fig8=px.pie(values=pat.values,names=pat.index)
            st.plotly_chart(fig8)
            st.info(f"Total No. Of Patients : {df["patient_id"].count()}")

        elif "gender" in q:
            gen=df["gender"].value_counts()
            fig9=px.pie(values=gen.values,names=gen.index)
            st.plotly_chart(fig9)

        elif "hi" in q or "hello" in q or "hey" in q :
            st.write("Hello How Can I Help You")

        elif "chronic condition" in q:
            cc=df["chronic_condition"].value_counts()
            fig10=px.pie(values=cc.values,names=cc.index)
            st.plotly_chart(fig10)

        elif "admission type" in q:
            at=df["admission_type"].value_counts()
            fig11=px.pie(values=at.values,names=at.index)
            st.plotly_chart(fig11)

        elif "waiting time" in q:
            fig12=px.box(df,x="department",y="wait_time_min",color="department")
            st.plotly_chart(fig12)

        elif "rating" in q:
            fig13=px.box(df,x="department",y="satisfaction_score",color="department")
            st.plotly_chart(fig13)

        elif "revenue" in q:
            rev=df.groupby("department")["total_cost_€"].sum()
            fig14=px.bar(x=rev.index,y=rev.values)
            st.plotly_chart(fig14)

        elif "how are you" in q:
            st.write("I Am Good,How Can I Help?")

elif selected1=="About Us":
    st.header("HealthCare Intelligence")
    st.subheader("Description")
    st.write("Healthcare Intelligence is the integration of advanced data analytics, clinical metrics, and operational insights to drive smarter medical ecosystems. It empowers healthcare organizations to transform raw data into predictive, actionable strategies—ultimately improving patient care quality while maximizing operational and financial efficiency")
    st.divider()

    st.subheader("Technologies Used")
    st.write("""
     - Pandas
    
     - Plotly
    
     - Matplotlib

     - Streamlit

     - Streamlit_Option_Menu""")