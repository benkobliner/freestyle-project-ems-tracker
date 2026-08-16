"""Streamlit dashboard for exploring FDNY EMS incident data."""

import pandas as pd
import streamlit as st

from main import (
    get_call_type_counts,
    get_response_times,
    get_day_night_counts,
)


st.set_page_config(
    page_title="FDNY EMS Data Explorer",
    layout="wide",
)


st.title("FDNY EMS Data Explorer")

st.write(
    """
    Explore geographic and operational patterns in FDNY EMS incident
    data using live data from NYC Open Data.
    """
)


year = st.sidebar.number_input(
    "Year",
    min_value=2005,
    max_value=2025,
    value=2025,
    step=1,
)


borough = st.sidebar.selectbox(
    "Geographic Area",
    [
        "All NYC",
        "Manhattan",
        "Bronx",
        "Brooklyn",
        "Queens",
        "Staten Island",
    ],
)


scenario = st.sidebar.radio(
    "Analysis",
    [
        "Call Type by ZIP Code",
        "Response Time by ZIP Code",
        "Day vs. Night Demand",
    ],
)


if scenario == "Call Type by ZIP Code":

    st.header("EMS Call Type by ZIP Code")

    st.write(
        """
        Identify which ZIP codes generated the greatest number
        of incidents for a selected FDNY EMS call type.
        """
    )

    call_type = st.text_input(
        "Final EMS call type",
        value="DROWN",
    ).strip().upper()

    if st.button("Run Call Type Analysis"):

        with st.spinner("Querying NYC Open Data..."):

            df = get_call_type_counts(
                year=int(year),
                call_type=call_type,
                borough=borough,
            )

        if df.empty:

            st.warning(
                "No matching incidents were returned."
            )

        else:

            total_calls = int(df["call_count"].sum())

            st.metric(
                f"Total {call_type} calls",
                f"{total_calls:,}",
            )

            st.subheader("Highest-volume ZIP codes")

            display_df = df.copy()

            display_df.columns = [
                "ZIP Code",
                "EMS Calls",
            ]

            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True,
            )

            chart_df = (
                display_df.head(15)
                .set_index("ZIP Code")
            )

            st.subheader("Top 15 ZIP codes")

            st.bar_chart(
                chart_df["EMS Calls"]
            )


elif scenario == "Response Time by ZIP Code":

    st.header("EMS Response Time by ZIP Code")

    st.write(
        """
        Compare average EMS incident response times among ZIP
        codes using records FDNY identifies as having valid
        incident-response-time measurements.
        """
    )

    severity_option = st.radio(
        "Severity filter",
        [
            "All severity levels",
            "Severity levels 1-3 only",
        ],
    )

    minimum_calls = st.number_input(
        "Minimum qualifying calls per ZIP code",
        min_value=1,
        max_value=1000,
        value=50,
        step=10,
    )

    if st.button("Run Response Time Analysis"):

        high_severity_only = (
            severity_option
            == "Severity levels 1-3 only"
        )

        with st.spinner("Querying NYC Open Data..."):

            df = get_response_times(
                year=int(year),
                borough=borough,
                high_severity_only=high_severity_only,
                minimum_calls=int(minimum_calls),
            )

        if df.empty:

            st.warning(
                "No qualifying ZIP codes were returned."
            )

        else:

            st.subheader(
                "ZIP codes with longest average response times"
            )

            display_df = df[
                [
                    "zipcode",
                    "avg_response_minutes",
                    "call_count",
                ]
            ].copy()

            display_df.columns = [
                "ZIP Code",
                "Average Response Time (minutes)",
                "Qualifying Calls",
            ]

            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True,
            )

            chart_df = (
                display_df.head(15)
                .set_index("ZIP Code")
            )

            st.subheader(
                "15 longest average response times"
            )

            st.bar_chart(
                chart_df["Average Response Time (minutes)"]
            )

            st.caption(
                """
                Response time is based on
                INCIDENT_RESPONSE_SECONDS_QY and includes only
                records for which FDNY marks incident response
                time as valid.
                """
            )


elif scenario == "Day vs. Night Demand":

    st.header("Day vs. Night EMS Demand")

    st.write(
        """
        Compare EMS incident volume by ZIP code during daytime
        and nighttime hours.

        Day: 08:00-19:59

        Night: 20:00-07:59
        """
    )

    if st.button("Run Day vs. Night Analysis"):

        with st.spinner("Querying NYC Open Data..."):

            df = get_day_night_counts(
                year=int(year),
                borough=borough,
            )

        if df.empty:

            st.warning(
                "No matching incidents were returned."
            )

        else:

            pivot = df.pivot_table(
                index="zipcode",
                columns="period",
                values="call_count",
                aggfunc="sum",
                fill_value=0,
            )

            if "Day" not in pivot.columns:
                pivot["Day"] = 0

            if "Night" not in pivot.columns:
                pivot["Night"] = 0

            pivot["Total"] = (
                pivot["Day"] + pivot["Night"]
            )

            pivot["Night Share"] = (
                pivot["Night"] / pivot["Total"]
            )

            pivot = pivot.sort_values(
                "Total",
                ascending=False,
            )

            display_df = pivot.reset_index()

            display_df["Night Share"] = (
                display_df["Night Share"] * 100
            ).round(1)

            display_df.columns = [
                "ZIP Code",
                "Day Calls",
                "Night Calls",
                "Total Calls",
                "Night Share (%)",
            ]

            st.subheader(
                "Day and night EMS demand by ZIP code"
            )

            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True,
            )

            chart_df = (
                display_df.head(15)
                .set_index("ZIP Code")
            )

            st.subheader(
                "Day vs. night volume: 15 busiest ZIP codes"
            )

            st.bar_chart(
                chart_df[
                    [
                        "Day Calls",
                        "Night Calls",
                    ]
                ]
            )

            st.subheader(
                "ZIP codes with greatest nighttime share"
            )

            night_df = display_df[
                display_df["Total Calls"] >= 50
            ].sort_values(
                "Night Share (%)",
                ascending=False,
            )

            st.dataframe(
                night_df.head(15),
                hide_index=True,
                use_container_width=True,
            )


st.divider()

st.caption(
    """
    Data source: FDNY EMS Incident Dispatch Data,
    NYC Open Data. Incident locations are published at an
    aggregated geographic level to protect patient privacy.
    """
)
