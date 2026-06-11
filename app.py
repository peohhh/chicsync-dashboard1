```python
import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

st.set_page_config(
    page_title="ChicSync Dashboard",
    page_icon="🍓",
    layout="wide"
)

# ======================
# CUSTOM STYLE
# ======================

st.markdown("""
<style>
.stApp {
    background-color: #F8F1DF;
}

[data-testid="stSidebar"] {
    background-color: #F5C6CE;
}

.title-box {
    background: linear-gradient(90deg,#E98AA7,#A8C686);
    padding: 25px;
    border-radius: 20px;
    text-align:center;
    margin-bottom:20px;
}

.title-box h1,
.title-box p {
    color:white;
}

.block {
    background:white;
    padding:20px;
    border-radius:15px;
    margin-top:15px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ======================
# SESSION DATA
# ======================

if "stock" not in st.session_state:

    st.session_state.stock = pd.DataFrame({
        "Warehouse":[
            "KL Warehouse",
            "Penang Warehouse",
            "Johor Warehouse"
        ],
        "Black Satin Dress":[10,10,10],
        "White Sneakers":[15,15,15],
        "Mini Shoulder Bag":[8,8,8],
        "Status":[
            "Active",
            "Active",
            "Active"
        ]
    })

if "logs" not in st.session_state:
    st.session_state.logs = []

if "stale_reads" not in st.session_state:
    st.session_state.stale_reads = 0

df = st.session_state.stock

# ======================
# SIDEBAR
# ======================

st.sidebar.title("🍓 Control Panel")

menu = st.sidebar.radio(
    "Choose Module",
    [
        "Dashboard Overview",
        "Process & Thread",
        "Naming Service",
        "Stock Replication",
        "Consistency Analysis",
        "Fault Tolerance"
    ]
)

# ======================
# HEADER
# ======================

st.markdown("""
<div class='title-box'>
<h1>🍓 ChicSync Dashboard 🍵</h1>
<p>Distributed Fashion Stock Synchronization System</p>
</div>
""", unsafe_allow_html=True)

# ======================
# KPI
# ======================

total_stock = int(
    df["Black Satin Dress"].sum() +
    df["White Sneakers"].sum() +
    df["Mini Shoulder Bag"].sum()
)

active_nodes = len(
    df[df["Status"]=="Active"]
)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Warehouse Nodes",3)
c2.metric("Total Stock",total_stock)
c3.metric("Active Nodes",active_nodes)
c4.metric("Stale Reads",st.session_state.stale_reads)

# ======================
# DASHBOARD OVERVIEW
# ======================

if menu == "Dashboard Overview":

    st.subheader("📦 Warehouse Stock Data")

    st.dataframe(df,use_container_width=True)

    product = st.selectbox(
        "Select Product",
        [
            "Black Satin Dress",
            "White Sneakers",
            "Mini Shoulder Bag"
        ]
    )

    fig = px.bar(
        df,
        x="Warehouse",
        y=product,
        color="Status",
        text=product,
        title=f"{product} Stock by Warehouse"
    )

    st.plotly_chart(fig,use_container_width=True)

    pie_df = pd.DataFrame({
        "Product":[
            "Black Satin Dress",
            "White Sneakers",
            "Mini Shoulder Bag"
        ],
        "Total":[
            df["Black Satin Dress"].sum(),
            df["White Sneakers"].sum(),
            df["Mini Shoulder Bag"].sum()
        ]
    })

    pie = px.pie(
        pie_df,
        names="Product",
        values="Total",
        hole=0.4,
        title="Product Stock Distribution"
    )

    st.plotly_chart(pie,use_container_width=True)

# ======================
# PROCESS & THREAD
# ======================

elif menu == "Process & Thread":

    st.subheader("🧵 Process & Thread Simulation")

    if st.button("Run Simulation"):

        output = st.empty()

        logs = []

        for i in range(1,4):

            node = random.choice([
                "KL Warehouse",
                "Penang Warehouse",
                "Johor Warehouse"
            ])

            logs.append(
                f"{node} processing request {i}"
            )

            output.write(logs)

            time.sleep(0.5)

        st.success(
            "Parallel processing simulation completed."
        )

# ======================
# NAMING SERVICE
# ======================

elif menu == "Naming Service":

    st.subheader("🔎 Naming Resolution")

    services = {
        "dress.service.chicsync":"KL Warehouse",
        "shoes.service.chicsync":"Penang Warehouse",
        "bag.service.chicsync":"Johor Warehouse"
    }

    service = st.selectbox(
        "Select Service",
        list(services.keys())
    )

    if st.button("Resolve Name"):

        latency = round(
            random.uniform(0.001,0.01),
            4
        )

        st.success(
            f"Resolved to: {services[service]}"
        )

        st.info(
            f"Lookup latency: {latency}s"
        )

# ======================
# STOCK REPLICATION
# ======================

elif menu == "Stock Replication":

    st.subheader("🔄 Stock Replication")

    warehouse = st.selectbox(
        "Warehouse",
        df["Warehouse"]
    )

    product = st.selectbox(
        "Product",
        [
            "Black Satin Dress",
            "White Sneakers",
            "Mini Shoulder Bag"
        ]
    )

    qty = st.number_input(
        "New Quantity",
        min_value=0,
        max_value=100,
        value=10
    )

    consistency = st.radio(
        "Consistency Model",
        [
            "Eventual Consistency",
            "Sequential Consistency"
        ]
    )

    if st.button("Update Stock"):

        if consistency == "Sequential Consistency":

            st.session_state.stock[product] = qty

            st.session_state.stale_reads = 0

            st.success(
                "All nodes updated successfully."
            )

        else:

            idx = st.session_state.stock[
                st.session_state.stock["Warehouse"]
                == warehouse
            ].index[0]

            st.session_state.stock.loc[
                idx,
                product
            ] = qty

            st.session_state.stale_reads = 2

            st.warning(
                "Only selected node updated."
            )

        st.rerun()

# ======================
# CONSISTENCY ANALYSIS
# ======================

elif menu == "Consistency Analysis":

    st.subheader("📊 Consistency Comparison")

    analysis = pd.DataFrame({
        "Model":[
            "Eventual Consistency",
            "Sequential Consistency"
        ],
        "Stale Reads":[2,0],
        "Update Time":[4.0,0.1]
    })

    st.dataframe(
        analysis,
        use_container_width=True
    )

    fig1 = px.bar(
        analysis,
        x="Model",
        y="Stale Reads",
        title="Stale Reads Comparison"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.bar(
        analysis,
        x="Model",
        y="Update Time",
        title="Update Time Comparison"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ======================
# FAULT TOLERANCE
# ======================

elif menu == "Fault Tolerance":

    st.subheader("⚠️ Node Failure Simulation")

    node = st.selectbox(
        "Select Failed Node",
        df["Warehouse"]
    )

    if st.button("Simulate Failure"):

        st.session_state.stock.loc[
            st.session_state.stock["Warehouse"]
            == node,
            "Status"
        ] = "Down"

        st.success(
            "Traffic redirected to backup node."
        )

        st.rerun()

    if st.button("Recover Nodes"):

        st.session_state.stock["Status"] = "Active"

        st.rerun()

    status_df = (
        st.session_state.stock["Status"]
        .value_counts()
        .reset_index()
    )

    status_df.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        status_df,
        names="Status",
        values="Count",
        hole=0.4,
        title="Node Status Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
```
