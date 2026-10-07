import streamlit as st


def render_transcript(transcript: str) -> None:
    """
    Render the meeting transcript.
    """

    with st.expander("📄 Transcript", expanded=False):

        st.caption(
            "Generated transcript from the meeting recording"
        )

        if transcript:
            st.text_area(
                "Transcript",
                value=transcript,
                height=400,
                label_visibility="collapsed",
            )
        else:
            st.write(
                "No transcript available."
            )