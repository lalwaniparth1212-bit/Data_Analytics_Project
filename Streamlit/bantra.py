from email.policy import default
from unittest import case

import pandas as pd
from streamlit import set_page_config
from streamlit.source_util import page_icon_and_name
from streamlit_option_menu import option_menu
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Urban-Traffic",
    layout="wide",
    page_icon="🚗"

)
df=pd.read_csv("Banglore_traffic.csv")

with st.sidebar:
    selected=option_menu("Main-Menu",["Home","Dataset","Assesment","Traffic-Analytics",
                                      "Data-Assistant","About-Us"],icons=["house","table","bar-chart","graph-up",
                                      "robot","info-circle"],menu_icon="car-front",default_index=4)

if selected=="Home":
    st.header("Urban Traffic")
    st.write("This project is an in-depth analysis of urban traffic patterns designed to evaluate vehicular flow, identify systemic bottlenecks, and diagnose the root causes of commuter congestion across the regional transit network. The ultimate goal is to provide city planners and traffic engineers with the empirical foundation needed to optimize signal timings, enhance intersection safety, and implement targeted infrastructure upgrades")
    st.divider()
    s1,s2,s3,s4=st.columns(4)
    s1.metric("Total Traffic Volume:",f"{df["Traffic_Volume"].sum():,.1f}")
    s2.metric("Average Speed:",f"{df["Average Speed"].mean():,.1f}")
    s3.metric("Avg Travel Time Index:",f"{df["Travel Time Index"].mean():,.2f}")
    s4.metric("Environmental Impact:",f"{df["Environmental Impact"].mean():,.2f}")
    st.divider()


    st.subheader("Area Wise Average Traffic Volume")
    tv=df.groupby("Area Name")["Traffic_Volume"].mean().reset_index()
    fig1=px.bar(tv,x="Area Name",y="Traffic_Volume",color="Traffic_Volume")
    st.plotly_chart(fig1)

    st.subheader("Total Volume")
    tv2 = df.groupby("Area Name")["Traffic_Volume"].sum()
    st.dataframe(tv2)

elif selected=="Dataset":
    st.header("Dataset")
    st.divider()
    q1,q2,q3=st.columns(3)
    q1.metric("Total Rows:",df.shape[0])
    q2.metric("Total Columns:",df.shape[1])
    q3.metric("Total Missing Values:",df.isna().sum().sum())

    st.subheader("Select Columns")

    selected_col=st.multiselect("Select Columns To Display",df.columns,default=df.columns)
    filtered=df[selected_col]
    st.dataframe(filtered)

    if st.checkbox("Show Full Dataset"):
        st.dataframe(df)

    st.subheader("Search in Dataset")
    search_i=st.text_input("Enter Your Value")
    if search_i:
        filtered=filtered[filtered.astype(str).apply(
            lambda row:row.str.contains(search_i,case=False).any(),axis=1
        )]
        st.dataframe(filtered)

elif selected=="Assesment":
    st.header("Traffic Overview")

    w1,w2,w3=st.columns(3)
    w1.metric("Road Utilization:",f"{df["Road Capacity Utilization"].mean():,.1f}%","+10% vs LastYear")
    w2.metric("Total Incidents:",df["Incident Reports"].sum(),"+5%  vs LastYear",delta_color="inverse")
    w3.metric("Public Transport Usage:",f"{df["Public Transport Usage"].mean():,.1f}%")

    st.divider()

    urb_matrix=df.groupby("Area Name").agg(
        Traffic_Volume=("Traffic_Volume","mean"),
        Total_Incidents=("Incident Reports","sum"),
        Travel_Index=("Travel Time Index","mean")
    )
    st.dataframe(urb_matrix.style.format({
        "Traffic_Volume":"{:,.2f}",
        "Travel_Index":"{:,.1f}"
    }).background_gradient(subset=["Traffic_Volume"],cmap="Blues"))
    st.info("Travel Time Is 30% More Than Usual Time")
    st.divider()

    tab1,tab2,tab3,tab4=st.tabs(["Infrastructure","Environment","Weather","Traffic"])
    with tab1:
        st.subheader("Condition Of Infrastructure")
        urb_matrix2=df.groupby("Area Name").agg(
            Road_Capacity=("Road Capacity Utilization","mean"),
            Signal_Compliance=("Traffic Signal Compliance","mean"),
            Congestion_Level=("Congestion Level","mean")
        )
        st.dataframe(urb_matrix2.style.format({
            "Road_Capacity":"{:,.2f}%",
            "Signal_Compliance":"{:,.2f}%",
            "Congestion_Level":"{:,.2f}%"
        }).highlight_max(axis=0,color="#2bfbbb").highlight_min(axis=0,color="#fb352b"))
        st.warning("Electronic City Needs Improvement")
    st.divider()
    with tab2:
        st.header("Effect On Environment")
        urb_matrix3 = df.groupby("Area Name").agg(
            Public_Transport_Usage=("Public Transport Usage", "mean"),
            Pedestrian_and_Cyclist_Count=("Pedestrian and Cyclist Count", "mean"),
            Environmental_Impact=("Environmental Impact", "mean")
        )
        st.dataframe(urb_matrix3.style.format({
            "Public_Transport_Usage": "{:,.1f}%",
            "Pedestrian_and_Cyclist_Count": "{:,.0f}",
            "Environmental_Impact": "{:,.2f}"
        }).background_gradient(subset=["Environmental_Impact"], cmap="RdYlGn"))
        st.warning("Only 45% of People Use Public Transport")
    with tab3:
        st.subheader("Weather Condition")
        wc = df["Weather Conditions"].value_counts()
        fig2 = px.pie(values=wc.values, names=wc.index)
        st.plotly_chart(fig2)
    with tab4:
        st.subheader("Area Wise Traffic")
        fig8=px.bar(df,x="Area Name",y="Traffic_Volume",color="Area Name")
        st.plotly_chart(fig8)



    st.header("Insights")
    c1,c2,c3=st.columns(3)
    c1.metric("Average Traffic Volume",f"{df["Traffic_Volume"].mean():,.2f}","+10% vs LastYear",delta_color="inverse")
    c2.metric("Average Speed",f"{df["Average Speed"].mean():,.1f}","-5% vs LastYear")
    c3.metric("Environmental Impact",f"{df["Environmental Impact"].mean():,.1f}","+10% vs LastYear",delta_color="inverse")

    st.subheader("Column Statistics")
    numeric_column=df.select_dtypes(include=["int64","float64"]).columns

    if len(numeric_column) > 0:
        selected_column=st.selectbox("Select Column",numeric_column)
        st.write(df[selected_column].describe())

elif selected=="Traffic-Analytics":
    st.header("Dashboard")
    s1,s2,s3=st.tabs(["Avg Speed","Condition","Incidents"])
    with s1:
        st.subheader("Area Wise Average Speed")
        fig3 = px.box(df, x="Area Name", y="Average Speed", color="Area Name")
        st.plotly_chart(fig3)
    with s2:
        st.subheader("Area Wise Condition")
        fig4=px.bar(df,x="Area Name",y=["Road Capacity Utilization","Congestion Level"],barmode="group")
        st.plotly_chart(fig4)
    with s3:
        inc=df.groupby("Area Name")["Incident Reports"].sum()
        st.subheader("Area Wise Incidents")
        fig5=px.pie(values=inc.values,names=inc.index,hole=0.5)
        st.plotly_chart(fig5)
    st.divider()

    st.subheader("Traffic Distribution")
    fig10=px.treemap(df,path=["Area Name","Road/Intersection Name"],
                     values="Traffic_Volume",
                     color="Area Name",
                     color_continuous_scale="Turbo"
                     )
    st.plotly_chart(fig10)
    st.divider()


    st.subheader("Environmental Impact v/s Public Transport Usage")
    fig6=px.bar(df,x="Area Name",y=["Public Transport Usage","Environmental Impact"],barmode="group")
    st.plotly_chart(fig6,use_container_width=True)
    st.divider()

    ratio=df["Roadwork and Construction Activity"].value_counts()
    st.subheader("Construction Ratio")
    fig7=px.bar(x=ratio.index,y=ratio.values)
    st.plotly_chart(fig7)
    st.divider()

    st.subheader("Environmental Impact Frequency")
    fig9=px.histogram(df["Environmental Impact"])
    st.plotly_chart(fig9)
    st.divider()

elif selected=="Data-Assistant":
    st.header("Data Assistant")
    st.write("Ask Questions About the Dataset")
    user_in=st.text_input("Ask Me Questions")
    if user_in:
        q=user_in.lower()
        if "traffic" in q:
            st.subheader("Area Wise Volume")
            fig10=px.bar(df,x="Area Name",y="Traffic_Volume",color="Area Name")
            st.plotly_chart(fig10)
            st.warning("Indiranagar & Koramangala has the most Traffic")
            st.subheader("Road/Intersection Wise Volume")
            fig11=px.bar(df,y="Road/Intersection Name",x="Traffic_Volume",orientation="h")
            st.plotly_chart(fig11)

        if "environment" in q:
            st.subheader("Environmental Impact Frequency")
            fig9 = px.histogram(df["Environmental Impact"])
            st.plotly_chart(fig9)

        if "incident" in q:
            st.subheader("Area Wise Incidents")
            ir=df.groupby("Area Name")["Incident Reports"].sum()
            fig12=px.bar(x=ir.index,y=ir.values,color=ir.values)
            st.plotly_chart(fig12)
            st.error("Indiranagar and M.G Road has the Most No. Of Incidents")
            st.dataframe(ir)

        if "weather" in q:
            st.subheader("Weather Condition")
            wc = df["Weather Conditions"].value_counts()
            fig19 = px.pie(values=wc.values, names=wc.index)
            st.plotly_chart(fig19)

        if "pedestrian" in q:
            st.subheader("Pedestrian and Cyclist Count")
            pcc=df.groupby("Area Name")["Pedestrian and Cyclist Count"].sum()
            fig13=px.bar(x=pcc.index,y=pcc.values,color=pcc.index)
            st.plotly_chart(fig13)
            st.dataframe(pcc)

        if "parking" in q:
            st.subheader("Parking Usage")
            pu=df.groupby("Area Name")["Parking Usage"].sum()
            fig14=px.bar(x=pu.index,y=pu.values,color=pu.values)
            st.plotly_chart(fig14)

        if "public transport" in q:
            st.subheader("Public Transport Usage")
            pt=df.groupby("Area Name")["Public Transport Usage"].sum()
            fig15=px.bar(x=pt.index,y=pt.values,color=pt.index)
            st.plotly_chart(fig15)

        if "signal" in q:
            st.subheader("Traffic Signal Compliance")
            ts=df.groupby("Area Name")["Traffic Signal Compliance"].sum()
            fig16=px.bar(x=ts.index,y=ts.values,color=ts.index)
            st.plotly_chart(fig16)
            st.info("Electronic City has the lowest Signal Compliance")

        if "condition" in q:
            st.subheader("Road Capacity Utilization v/s Congestion Level")
            rcu=df.groupby("Area Name")["Road Capacity Utilization"].mean()
            cl=df.groupby("Area Name")["Congestion Level"].mean()
            fig17=px.bar(x=rcu.index,y=[rcu.values,cl.values],barmode="group")
            st.plotly_chart(fig17)

        if "speed" in q:
            st.subheader("Area Wise Average Speed")
            fig18 = px.box(df, x="Area Name", y="Average Speed", color="Area Name")
            st.plotly_chart(fig18)

        if "index" in q:
            st.subheader("Travel Time Index")
            tti=df.groupby("Area Name")["Travel Time Index"].mean()
            st.dataframe(tti.style.format({
                "Travel Time Index":"{:,.1f}"
            }))

elif selected=="About-Us":
    st.header("Urban Traffic")
    st.subheader("Description")
    st.write("This project is an in-depth analysis of urban traffic patterns designed to evaluate vehicular flow, identify systemic bottlenecks, and diagnose the root causes of commuter congestion across the regional transit network. The ultimate goal is to provide city planners and traffic engineers with the empirical foundation needed to optimize signal timings, enhance intersection safety, and implement targeted infrastructure upgrades")
    st.divider()

    st.subheader("Technologies Used")
    st.write("""
     - Pandas

     - Matplotlib
     
     - Plotly

     - Streamlit

     - Streamlit_Option_Menu""")
