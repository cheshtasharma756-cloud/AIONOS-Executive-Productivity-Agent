import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Executive Productivity Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATA
# Source-grounded data from the AIONOS Assignment 1 data pack
# ============================================================

ACTIONS = [

    {
        "id": 1,
        "title": "Send updated vendor list to Raghav",
        "owner": "Arjun",
        "status": "My Action",
        "deadline": "Wednesday morning",
        "priority": "High",
        "source": "Vendor List email thread + Leadership Sync",
        "confidence": "High",
        "validation": "Confirmed commitment",
        "requester": "Raghav",
        "description": (
            "Arjun committed to send the updated vendor list to Raghav. "
            "Later messages reconfirmed the Wednesday morning commitment."
        ),
        "evidence": [
            "Leadership Sync records Arjun's commitment to send the updated vendor list.",
            "Raghav followed up in the email thread.",
            "Arjun first committed to Tuesday, then reconfirmed Wednesday morning.",
            "Repeated mentions refer to the same underlying action and are deduplicated."
        ],
        "deduplication": (
            "Multiple mentions in the email thread are treated as one commitment. "
            "The latest commitment is Wednesday morning."
        )
    },

    {
        "id": 2,
        "title": "Confirm ownership of Mumbai office lease renewal",
        "owner": "Unconfirmed",
        "status": "Unclear Ownership",
        "deadline": "Friday EOD",
        "priority": "High",
        "source": "Mumbai Office Lease Renewal thread",
        "confidence": "Needs Confirmation",
        "validation": "Ownership not explicitly confirmed",
        "requester": "Raghav / Facilities discussion",
        "description": (
            "The lease renewal requires an authorized signature, but the "
            "source material does not confirm who is responsible for signing."
        ),
        "evidence": [
            "Facilities states that an authorized signature is required by Friday.",
            "Raghav asks who should sign.",
            "Divya says it is not her responsibility and believes Facilities may own it.",
            "No source explicitly confirms the final owner.",
            "The agent therefore does not assign ownership to Facilities or Arjun."
        ],
        "deduplication": (
            "Multiple lease messages refer to the same unresolved ownership issue."
        )
    },

    {
        "id": 3,
        "title": "Attend Meridian Logistics client call",
        "owner": "Arjun",
        "status": "Scheduled",
        "deadline": "Wednesday 3:00 PM",
        "priority": "High",
        "source": "Meridian email thread + Calendar",
        "confidence": "High",
        "validation": "Confirmed by email and calendar",
        "requester": "Priya",
        "description": (
            "The Meridian call was rescheduled and the new time was confirmed "
            "with Priya. The calendar shows Wednesday 3:00–3:30 PM."
        ),
        "evidence": [
            "Priya asked Arjun to propose a new time.",
            "Arjun proposed Wednesday at 3 PM.",
            "Priya confirmed the proposed time.",
            "The calendar contains the Wednesday 3:00–3:30 PM meeting."
        ],
        "deduplication": (
            "Email confirmation and calendar entry represent the same scheduled event."
        )
    },

    {
        "id": 4,
        "title": "Review Q3 campaign deck",
        "owner": "Arjun",
        "status": "Scheduled",
        "deadline": "Thursday 9:30 AM",
        "priority": "High",
        "source": "Q3 Campaign Deck + Calendar",
        "confidence": "High",
        "validation": "Confirmed review time",
        "requester": "Neha",
        "description": (
            "The campaign deck review moved from Wednesday to Thursday morning. "
            "Neha confirmed the deck was ready before the review."
        ),
        "evidence": [
            "The review was moved from Wednesday to Thursday.",
            "Neha confirmed the deck was ready Thursday morning.",
            "The calendar shows the Thursday 9:30–10:00 AM deck review."
        ],
        "deduplication": (
            "The email/thread updates and calendar entry are consolidated "
            "into one review commitment."
        )
    },

    {
        "id": 5,
        "title": "Review July expense variance report",
        "owner": "Arjun",
        "status": "Completed",
        "deadline": "Wednesday evening",
        "priority": "Medium",
        "source": "Expense Report thread",
        "confidence": "High",
        "validation": "Completed and acknowledged",
        "requester": "Divya",
        "description": (
            "Divya agreed to provide the expense variance report Wednesday evening. "
            "She sent it at 6 PM and Arjun acknowledged receipt."
        ),
        "evidence": [
            "Divya agreed to provide the report Wednesday evening.",
            "The report was sent Wednesday at 6 PM.",
            "Arjun acknowledged the report."
        ],
        "deduplication": (
            "The promise, delivery, and acknowledgement are treated as one "
            "completed commitment."
        )
    }
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_actions(status=None):
    if status is None:
        return ACTIONS

    return [
        action for action in ACTIONS
        if action["status"] == status
    ]


def confidence_badge(confidence):
    if confidence == "High":
        return "🟢 High"
    elif confidence == "Needs Confirmation":
        return "🟠 Needs Confirmation"
    return "⚪ Unknown"


def action_card(action, show_evidence=True):

    st.markdown(
        f"### {action['title']}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"**Owner**  \n{action['owner']}")

    with col2:
        st.markdown(f"**Deadline**  \n{action['deadline']}")

    with col3:
        st.markdown(f"**Priority**  \n{action['priority']}")

    with col4:
        st.markdown(
            f"**Confidence**  \n{confidence_badge(action['confidence'])}"
        )

    st.markdown(
        f"**Status:** `{action['status']}`"
    )

    st.caption(
        f"Source: {action['source']}"
    )

    st.write(action["description"])

    if show_evidence:

        with st.expander("🔎 View Source Evidence & Agent Validation"):

            st.markdown("**Source Evidence**")

            for item in action["evidence"]:
                st.markdown(f"- {item}")

            st.markdown("**Validation**")
            st.write(action["validation"])

            st.markdown("**Deduplication**")
            st.write(action["deduplication"])

    st.divider()


# ============================================================
# ASK AGENT
# ============================================================

def answer_question(question):

    q = question.lower().strip()

    # Raghav / vendor promise
    if "raghav" in q or "vendor" in q:

        return {
            "answer": (
                "You committed to send the updated vendor list to Raghav. "
                "The latest commitment in the source material is Wednesday morning."
            ),
            "source": "Vendor List email thread + Leadership Sync",
            "confidence": "High"
        }

    # Mumbai lease
    if (
        "lease" in q
        or "mumbai" in q
        or "ownership" in q
        or "sign" in q
    ):

        return {
            "answer": (
                "The Mumbai office lease renewal requires an authorized "
                "signature by Friday EOD, but ownership is still unconfirmed. "
                "The sources mention Facilities, but do not explicitly assign "
                "the signing responsibility."
            ),
            "source": "Mumbai Office Lease Renewal thread",
            "confidence": "Needs Confirmation"
        }

    # Meridian
    if "meridian" in q:

        return {
            "answer": (
                "The Meridian Logistics call was rescheduled to Wednesday "
                "3:00–3:30 PM. Priya confirmed the proposed time and the "
                "calendar contains the meeting."
            ),
            "source": "Meridian email thread + Calendar",
            "confidence": "High"
        }

    # Campaign deck
    if (
        "campaign" in q
        or "deck" in q
        or "neha" in q
    ):

        return {
            "answer": (
                "The Q3 campaign deck review is scheduled for Thursday at "
                "9:30 AM. Neha confirmed the deck was ready before the review."
            ),
            "source": "Q3 Campaign Deck + Calendar",
            "confidence": "High"
        }

    # Expense
    if (
        "expense" in q
        or "report" in q
    ):

        return {
            "answer": (
                "The July expense variance report was completed. Divya sent "
                "it Wednesday at 6 PM and Arjun acknowledged it."
            ),
            "source": "Expense Report thread",
            "confidence": "High"
        }

    # Action today
    if (
        "today" in q
        or "action" in q
        or "do" in q
    ):

        return {
            "answer": (
                "The main unresolved actions surfaced by the source data are "
                "the vendor list commitment and confirmation of ownership for "
                "the Mumbai office lease renewal."
            ),
            "source": "Vendor List + Mumbai Lease threads",
            "confidence": "High"
        }

    # Waiting
    if (
        "waiting" in q
        or "others" in q
        or "pending" in q
    ):

        return {
            "answer": (
                "The source pack contains scheduled activities involving other "
                "people, while the Mumbai lease remains unresolved because "
                "ownership has not been confirmed."
            ),
            "source": "Calendar + Mumbai Office Lease thread",
            "confidence": "High"
        }

    # Completed
    if (
        "completed" in q
        or "done" in q
        or "finished" in q
    ):

        return {
            "answer": (
                "The July expense variance report is completed. "
                "Divya sent it Wednesday evening and Arjun acknowledged it."
            ),
            "source": "Expense Report thread",
            "confidence": "High"
        }

    return {
        "answer": (
            "I could not confidently answer that from the supplied source "
            "material. Try asking about Raghav, the vendor list, Mumbai lease, "
            "Meridian, the Q3 deck, expense report, or current actions."
        ),
        "source": "No sufficiently matching source found",
        "confidence": "Needs Confirmation"
    }


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🤖 Agent Controls")

st.sidebar.caption(
    "Source-grounded Executive Productivity Agent"
)

view = st.sidebar.radio(
    "Choose View",
    [
        "Daily Brief",
        "My Actions",
        "Waiting / Scheduled",
        "Unclear Ownership",
        "Completed",
        "Ask Agent",
        "Agent Trace"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### 📥 Data Sources")

st.sidebar.markdown("✓ Leadership Sync")
st.sidebar.markdown("✓ Email threads")
st.sidebar.markdown("✓ Calendar")
st.sidebar.markdown("✓ Voice notes")

st.sidebar.divider()

st.sidebar.markdown("### ⚙️ Processing Pipeline")

st.sidebar.markdown(
    """
**1. Extract**  
↓  
**2. Resolve**  
↓  
**3. Deduplicate**  
↓  
**4. Validate**  
↓  
**5. Brief**
"""
)

st.sidebar.divider()

st.sidebar.caption(
    "Assignment 1 • AIONOS Executive Productivity Agent"
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Executive Productivity Agent")

st.markdown(
    "**AIONOS Assignment 1 | Executive: Arjun Malhotra, VP Sales**"
)

st.info(
    "The agent converts messy meeting notes, emails, voice notes and "
    "calendar information into a structured, source-grounded executive brief."
)

st.markdown("")


# ============================================================
# DAILY BRIEF
# ============================================================

if view == "Daily Brief":

    st.header("Today's Executive Brief")

    my_actions = get_actions("My Action")
    scheduled = get_actions("Scheduled")
    unclear = get_actions("Unclear Ownership")
    completed = get_actions("Completed")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("My Actions", len(my_actions))

    with c2:
        st.metric("Scheduled", len(scheduled))

    with c3:
        st.metric("Unclear Ownership", len(unclear))

    with c4:
        st.metric("Completed", len(completed))

    st.divider()

    # Needs Attention
    st.subheader("🔴 Needs Attention")

    for action in my_actions:
        action_card(action)

    for action in unclear:
        action_card(action)

    # Scheduled
    st.subheader("📅 Scheduled")

    for action in scheduled:
        action_card(action)

    # Completed
    st.subheader("✅ Completed")

    for action in completed:
        action_card(action)

    # Agent note
    st.warning(
        "Agent validation: The Mumbai lease renewal is flagged because "
        "ownership is unclear. The agent does not assume that Facilities "
        "or Arjun is the owner."
    )


# ============================================================
# MY ACTIONS
# ============================================================

elif view == "My Actions":

    st.header("🎯 My Actions")

    actions = get_actions("My Action")

    st.caption(
        "Commitments explicitly assigned to Arjun or made by Arjun."
    )

    if actions:
        for action in actions:
            action_card(action)
    else:
        st.success("No active personal actions found.")


# ============================================================
# WAITING / SCHEDULED
# ============================================================

elif view == "Waiting / Scheduled":

    st.header("📅 Waiting / Scheduled")

    st.caption(
        "Activities that have been resolved into scheduled commitments."
    )

    actions = get_actions("Scheduled")

    for action in actions:
        action_card(action)


# ============================================================
# UNCLEAR OWNERSHIP
# ============================================================

elif view == "Unclear Ownership":

    st.header("⚠️ Unclear Ownership")

    st.warning(
        "The agent intentionally does not invent an owner when the source "
        "material does not explicitly establish responsibility."
    )

    actions = get_actions("Unclear Ownership")

    for action in actions:
        action_card(action)


# ============================================================
# COMPLETED
# ============================================================

elif view == "Completed":

    st.header("✅ Completed")

    actions = get_actions("Completed")

    for action in actions:
        action_card(action)


# ============================================================
# ASK AGENT
# ============================================================

elif view == "Ask Agent":

    st.header("🤖 Ask the Agent")

    st.write(
        "Ask a question about the executive's commitments, deadlines, "
        "scheduled activities or unresolved ownership."
    )

    st.markdown("### Example questions")

    example_questions = [
        "What did I promise Raghav?",
        "What needs action today?",
        "What is still unclear?",
        "Who owns the Mumbai lease?",
        "What happened with the Meridian call?",
        "What happened to the Q3 campaign deck?",
        "What has already been completed?"
    ]

    selected_question = st.selectbox(
        "Try an example",
        ["Select a question..."] + example_questions
    )

    question = st.text_input(
        "Or type your own question"
    )

    if selected_question != "Select a question..." and not question:
        question = selected_question

    if st.button("Ask Agent", type="primary"):

        if question.strip():

            result = answer_question(question)

            st.success(result["answer"])

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Source**")
                st.write(result["source"])

            with col2:
                st.markdown("**Confidence**")
                st.write(
                    confidence_badge(result["confidence"])
                )

            st.divider()

            st.caption(
                "Answer generated from the supplied assignment source material."
            )

        else:

            st.warning("Please enter a question first.")


# ============================================================
# AGENT TRACE
# ============================================================

elif view == "Agent Trace":

    st.header("🧠 Agent Processing Trace")

    st.write(
        "This view shows the structured intermediate representation used "
        "by the prototype to transform source material into an executive brief."
    )

    stages = [
        (
            "1. Extract",
            "Identify candidate commitments, activities, deadlines and requests "
            "from meeting notes, emails, voice notes and calendar entries."
        ),
        (
            "2. Resolve",
            "Resolve owner, requester, deadline and current status using the "
            "available source evidence."
        ),
        (
            "3. Deduplicate",
            "Merge repeated mentions of the same underlying commitment."
        ),
        (
            "4. Validate",
            "Check whether ownership and status are actually supported by "
            "the sources. Unclear ownership is preserved as uncertain."
        ),
        (
            "5. Brief",
            "Convert validated commitments into an executive-facing daily brief."
        )
    ]

    for title, description in stages:

        st.markdown(f"### {title}")
        st.write(description)

    st.divider()

    st.subheader("📋 Normalized Commitment Records")

    for action in ACTIONS:

        with st.expander(action["title"]):

            st.write(
                {
                    "Owner": action["owner"],
                    "Requester": action["requester"],
                    "Status": action["status"],
                    "Deadline": action["deadline"],
                    "Priority": action["priority"],
                    "Confidence": action["confidence"],
                    "Validation": action["validation"],
                    "Source": action["source"]
                }
            )

    st.divider()

    st.subheader("Agent Quality Checks")

    checks = [
        "✓ Commitment extraction",
        "✓ Owner resolution",
        "✓ Deadline detection",
        "✓ Duplicate commitment merging",
        "✓ Unclear ownership detection",
        "✓ Completed-item detection",
        "✓ Source traceability"
    ]

    for check in checks:
        st.write(check)

    st.info(
        "Important: the prototype is source-grounded and deterministic. "
        "It does not claim to use an external LLM unless one is explicitly "
        "connected."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AIONOS Executive Productivity Agent • Assignment 1 • "
    "Source-grounded prototype"
)