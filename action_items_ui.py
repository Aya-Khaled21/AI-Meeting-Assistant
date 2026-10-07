import streamlit as st


def render_action_items_section(action_data: dict) -> None:
    """
    Render action items, deadlines, and open questions
    in the Streamlit interface.

    Args:
        action_data: Structured action items dictionary.
    """

    # Action Items
    with st.container(border=True):
        st.markdown("#### 📋 Action Items")

        action_items = action_data.get("action_items", [])

        if action_items:
            st.dataframe(
                action_items,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.write("No action items found.")

    # Open Questions
    with st.container(border=True):
        st.markdown("#### ❓ Open Questions")

        questions = action_data.get("open_questions", [])

        if questions:
            for question in questions:
                st.markdown(f"- {question}")
        else:
            st.write("No open questions found.")