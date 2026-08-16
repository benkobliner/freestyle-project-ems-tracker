"""Streamlit dashboard for exploring FDNY EMS incident data."""

import streamlit as st

from main import (
    get_call_type_counts,
    get_response_times,
    get_held_incident_rates,
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
        "Held Incidents by ZIP Code",
    ],
)


if scenario == "Call Type by ZIP Code":

    st.header("EMS Call Type by ZIP Code")

    st.write(
        """
        Identify which ZIP codes generated the greatest number
        of incidents for a selected FDNY EMS final call type.
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


elif scenario == "Held Incidents by ZIP Code":

    st.header("Held EMS Incidents by ZIP Code")

    st.write(
        """
        Compare the percentage of EMS incidents marked as held
        in the FDNY EMS Incident Dispatch Data.

        The public NYC Open Data metadata identifies HELD_INDICATOR
        as a Y/N field but does not provide a detailed operational
        definition. This dashboard therefore reports the field
        descriptively rather than assigning a specific cause to
        held status.
        """
    )

    severity_option = st.radio(
        "Severity filter",
        [
            "All severity levels",
            "Severity levels 1-3 only",
        ],
        key="held_severity",
    )

    minimum_calls = st.number_input(
        "Minimum qualifying calls per ZIP code",
        min_value=1,
        max_value=5000,
        value=100,
        step=50,
        key="held_minimum",
    )

    if st.button("Run Held Incident Analysis"):

        high_severity_only = (
            severity_option
            == "Severity levels 1-3 only"
        )

        with st.spinner("Querying NYC Open Data..."):

            df = get_held_incident_rates(
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

            total_calls = int(
                df["total_calls"].sum()
            )

            total_held = int(
                df["held_calls"].sum()
            )

            overall_rate = (
                total_held / total_calls * 100
                if total_calls
                else 0
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Qualifying EMS Incidents",
                f"{total_calls:,}",
            )

            col2.metric(
                "Held Incidents",
                f"{total_held:,}",
            )

            col3.metric(
                "Held Percentage",
                f"{overall_rate:.2f}%",
            )

            st.subheader(
                "ZIP codes with highest held percentage"
            )

            display_df = df[
                [
                    "zipcode",
                    "total_calls",
                    "held_calls",
                    "held_percentage",
                ]
            ].copy()

            display_df.columns = [
                "ZIP Code",
                "Total Calls",
                "Held Calls",
                "Held Percentage",
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
                "Top 15 ZIP codes by held percentage"
            )

            st.bar_chart(
                chart_df["Held Percentage"]
            )

            st.caption(
                """
                ZIP codes below the selected minimum call volume
                are excluded to reduce the influence of very small
                sample sizes.
                """
            )


st.divider()

st.caption(
    """
    Data source: FDNY EMS Incident Dispatch Data,
    NYC Open Data. Incident locations are published at an
    aggregated geographic level to protect patient privacy.
    """
)
