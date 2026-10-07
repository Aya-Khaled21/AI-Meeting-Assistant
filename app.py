import os

from pathlib import Path
import streamlit as st

from transcription import transcribe_audio
from summary import generate_summary
from action_items import generate_action_items

from transcript_ui import render_transcript
from summary_ui import render_summary_section
from action_items_ui import render_action_items_section


# -----------------------------------------
# Page Configuration
# -----------------------------------------

st.set_page_config(
    page_title="MeetInsight AI",
    page_icon="✦",
    layout="wide",
)

# -----------------------------------------
# Load Custom CSS
# -----------------------------------------

st.html(Path("styles.css"))

# -----------------------------------------
# Session State Initialization
# -----------------------------------------

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "summary_data" not in st.session_state:
    st.session_state.summary_data = None

if "action_data" not in st.session_state:
    st.session_state.action_data = None

if "processed_file_name" not in st.session_state:
    st.session_state.processed_file_name = None

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"


# -----------------------------------------
# Sidebar Settings
# -----------------------------------------

language_col, _ = st.columns([1, 4])

with language_col:
    language = st.selectbox(
        "🌐 Output Language",
        ["English", "Arabic"],
        label_visibility="visible",
    )

st.caption(
    "The transcript remains in its original language. "
    "Only the generated meeting insights use the selected language."
)


# -----------------------------------------
# Header
# -----------------------------------------

st.html(
    """
    <div class="meet-header">

        <div class="brand-row">

            <div class="brand-icon">
                ✦
            </div>

            <div>
                <div class="brand-name">
                    MeetInsight AI
                </div>

                <div class="brand-subtitle">
                    Turn meetings into clear, actionable insights.
                </div>
            </div>

        </div>

    </div>
    """
)


# -----------------------------------------
# Upload Section
# -----------------------------------------

st.html(
    """
    <div class="hero-card">

        <div class="hero-title">
            🎙️ Analyze your meeting
        </div>

        <div class="hero-description">
            Upload an audio or video recording and let AI
            extract the most important insights.
        </div>

    </div>
    """
)

uploaded_file = st.file_uploader(
    "Choose an audio or video file",
    type=[
        "wav",
        "mp3",
        "m4a",
        "ogg",
        "mp4",
    ],
)


# -----------------------------------------
# Reset old results if a new file is uploaded
# -----------------------------------------

if uploaded_file:

    if (
        st.session_state.processed_file_name is not None
        and uploaded_file.name != st.session_state.processed_file_name
    ):
        st.session_state.transcript = None
        st.session_state.summary_data = None
        st.session_state.action_data = None
        st.session_state.processed_file_name = None


    st.success("File uploaded successfully.")

    file_extension = os.path.splitext(
        uploaded_file.name
    )[1].lower()


    # -----------------------------------------
    # Preview Uploaded Media
    # -----------------------------------------
    
    with st.expander("🎬 Preview Recording", expanded=False):
        if file_extension == ".mp4":
            st.video(uploaded_file)
        else:
            st.audio(uploaded_file)


    # -----------------------------------------
    # Generate Meeting Notes
    # -----------------------------------------

    generate_button = st.button(
        "⚡ Generate Meeting Notes",
        use_container_width=True,
    )


    if generate_button:

        try:

            # -----------------------------------------
            # Step 1: Transcription
            # -----------------------------------------

            with st.spinner("🎙️ Transcribing meeting..."):

                transcript = transcribe_audio(
                    uploaded_file
                )


            if not transcript.strip():

                st.warning(
                    "No speech was detected in the uploaded file."
                )

                st.stop()


            # -----------------------------------------
            # Step 2: Generate Summary
            # -----------------------------------------

            with st.spinner("🧠 Generating meeting summary..."):

                summary_data = generate_summary(
                    transcript,
                    language,
                )


            # -----------------------------------------
            # Step 3: Extract Action Items
            # -----------------------------------------

            with st.spinner("📋 Extracting action items..."):

                action_data = generate_action_items(
                    transcript,
                    language,
                )


            # -----------------------------------------
            # Save Results
            # -----------------------------------------

            st.session_state.transcript = transcript

            st.session_state.summary_data = summary_data

            st.session_state.action_data = action_data

            st.session_state.processed_file_name = uploaded_file.name

            st.session_state.selected_language = language


            st.success(
                "✅ Meeting analysis completed successfully."
            )


        except Exception as e:

            st.error(
                "Something went wrong while processing the meeting."
            )

            st.exception(e)


# -----------------------------------------
# Display Results
# -----------------------------------------

if (
    st.session_state.transcript
    and st.session_state.summary_data
    and st.session_state.action_data
):

    # Get results from session state
    transcript = st.session_state.transcript
    summary_data = st.session_state.summary_data
    action_data = st.session_state.action_data

    # -----------------------------------------
    # Meeting Statistics
    # -----------------------------------------

    word_count = len(transcript.split())

    action_count = len(
        action_data.get("action_items", [])
    )

    decision_count = len(
        summary_data.get("decisions", [])
    )

    question_count = len(
        action_data.get("open_questions", [])
    )

    st.html(
        f"""
        <div style="
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin: 1.5rem 0;
        ">

            <div class="stat-card">
                <div class="stat-label">
                    Words
                </div>

                <div class="stat-value">
                    {word_count:,}
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-label">
                    Action Items
                </div>

                <div class="stat-value">
                    {action_count}
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-label">
                    Decisions
                </div>

                <div class="stat-value">
                    {decision_count}
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-label">
                    Open Questions
                </div>

                <div class="stat-value">
                    {question_count}
                </div>
            </div>

        </div>
        """
    )

    st.divider()

    # -----------------------------------------
    # Main Content
    # -----------------------------------------

    st.html(
        """
        <div class="section-title">
            ✨ Meeting Analysis
        </div>
        """
    )
    left_column, right_column = st.columns(
        [1, 1.6],
        gap="large",
    )


    # -----------------------------------------
    # Left Column - Transcript
    # -----------------------------------------

    with left_column:

        render_transcript(
            st.session_state.transcript
        )


    # -----------------------------------------
    # Right Column - Meeting Insights
    # -----------------------------------------

    with right_column:

        st.markdown("### ✨ Meeting Insights")

        render_summary_section(
            st.session_state.summary_data
        )

        render_action_items_section(
            st.session_state.action_data
        )


    # -----------------------------------------
    # Download Notes
    # -----------------------------------------

    st.divider()


    summary_data = st.session_state.summary_data

    action_data = st.session_state.action_data

    transcript = st.session_state.transcript

    selected_language = st.session_state.selected_language


    # -----------------------------------------
    # Dynamic Download Titles
    # -----------------------------------------

    if selected_language == "Arabic":

        notes_title = "🤖 مساعد اجتماعات بالذكاء الاصطناعي - ملاحظات الاجتماع"

        summary_title = "📌 ملخص الاجتماع"

        key_points_title = "🗣️ نقاط النقاش الرئيسية"

        decisions_title = "✅ القرارات"

        action_items_title = "📋 المهام"

        open_questions_title = "❓ الأسئلة المفتوحة"

        transcript_title = "📄 النص المفرغ"

    else:

        notes_title = "🤖 AI Meeting Assistant - Meeting Notes"

        summary_title = "📌 Meeting Summary"

        key_points_title = "🗣️ Key Discussion Points"

        decisions_title = "✅ Decisions"

        action_items_title = "📋 Action Items"

        open_questions_title = "❓ Open Questions"

        transcript_title = "📄 Transcript"


    # -----------------------------------------
    # Build Downloadable Markdown
    # -----------------------------------------

    notes_content = f"# {notes_title}\n\n"


    notes_content += f"## {summary_title}\n\n"

    notes_content += (
        summary_data.get(
            "summary",
            "No summary available.",
        )
        + "\n\n"
    )


    notes_content += f"## {key_points_title}\n\n"

    for point in summary_data.get(
        "key_points",
        [],
    ):

        notes_content += f"- {point}\n"

    notes_content += "\n"


    notes_content += f"## {decisions_title}\n\n"

    decisions = summary_data.get(
        "decisions",
        [],
    )

    if decisions:

        for decision in decisions:

            notes_content += f"- {decision}\n"

    else:

        notes_content += "No decisions found.\n"

    notes_content += "\n"


    notes_content += f"## {action_items_title}\n\n"

    action_items = action_data.get(
        "action_items",
        [],
    )

    if action_items:

        notes_content += (
            "| Person | Task | Deadline |\n"
        )

        notes_content += (
            "|---|---|---|\n"
        )


        for item in action_items:

            person = item.get(
                "person",
                "Not specified",
            )

            task = item.get(
                "task",
                "Not specified",
            )

            deadline = item.get(
                "deadline",
                "Not specified",
            )


            notes_content += (
                f"| {person} | {task} | {deadline} |\n"
            )

    else:

        notes_content += "No action items found.\n"

    notes_content += "\n"


    notes_content += f"## {open_questions_title}\n\n"

    questions = action_data.get(
        "open_questions",
        [],
    )

    if questions:

        for question in questions:

            notes_content += f"- {question}\n"

    else:

        notes_content += "No open questions found.\n"

    notes_content += "\n"


    notes_content += f"## {transcript_title}\n\n"

    notes_content += transcript


    # -----------------------------------------
    # Download Button
    # -----------------------------------------

    st.download_button(
        label="📥 Download Meeting Notes",
        data=notes_content,
        file_name="meeting_notes.md",
        mime="text/markdown",
        use_container_width=True,
    )
    
    st.html(
    """
    <div class="footer">
        MeetInsight AI · Built with Python, Streamlit & Gemini
    </div>
    """
)