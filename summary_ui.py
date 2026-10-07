import streamlit as st


def render_summary_section(summary_data: dict) -> None:
    """
    Render the summary-related sections of the meeting insights UI.

    Sections:
    - Meeting Summary
    - Key Discussion Points
    - Decisions

    Args:
        summary_data: Dictionary returned by generate_summary().
    """

    # Meeting Summary
    with st.container(border=True):
        st.markdown("#### 📌 Meeting Summary")

        summary = summary_data.get("summary", "")

        if summary:
            st.write(summary)
        else:
            st.write("No summary available.")

    # Key Discussion Points
    with st.container(border=True):
        st.markdown("#### 🗣️ Key Discussion Points")

        key_points = summary_data.get("key_points", [])

        if key_points:
            for point in key_points:
                st.markdown(f"- {point}")
        else:
            st.write("No key discussion points available.")

    # Decisions
    with st.container(border=True):
        st.markdown("#### ✅ Decisions")

        decisions = summary_data.get("decisions", [])

        if decisions:
            for decision in decisions:
                st.markdown(f"- {decision}")
        else:
            st.write("No decisions available.")