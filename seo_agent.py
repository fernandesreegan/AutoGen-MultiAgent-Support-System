import os
import streamlit as st
import autogen
from dotenv import load_dotenv

# Load environment variables silently from .env
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AuraDesk AI | Dynamic Multi-Agent Support",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Custom CSS for Modern Colors, Cards, & Full Word-Wrapping
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }
    .hero-banner {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.3);
    }
    .hero-banner h1 {
        color: white !important;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        color: #E0E7FF;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    .agent-card {
        background: #FFFFFF;
        border-left: 4px solid #6366F1;
        padding: 12px 14px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        word-wrap: break-word;
    }
    .agent-title {
        font-weight: 700;
        color: #312E81;
        font-size: 0.95rem;
        margin-bottom: 2px;
    }
    .agent-desc {
        font-size: 0.82rem;
        color: #64748B;
        line-height: 1.35;
    }
    .final-response-box {
        background: linear-gradient(to bottom right, #FFFFFF, #F5F3FF);
        border: 2px solid #8B5CF6;
        border-radius: 14px;
        padding: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.12);
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    .final-badge {
        display: inline-block;
        background-color: #7C3AED;
        color: white;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        transition: all 0.2s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
    }
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        font-size: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar with Dynamic Routing Team Overview
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 18px 0;">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="64" height="64" rx="16" fill="url(#logo_grad)"/>
            <path d="M20 34V30C20 23.3726 25.3726 18 32 18C38.6274 18 44 23.3726 44 30V34" stroke="white" stroke-width="3.5" stroke-linecap="round"/>
            <rect x="16" y="31" width="7" height="12" rx="3.5" fill="white"/>
            <rect x="41" y="31" width="7" height="12" rx="3.5" fill="white"/>
            <path d="M44 43C44 46.3137 41.3137 49 38 49H33" stroke="#E0E7FF" stroke-width="3" stroke-linecap="round"/>
            <circle cx="32" cy="49" r="2.5" fill="#FDE047"/>
            <defs>
                <linearGradient id="logo_grad" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#4F46E5"/>
                    <stop offset="1" stop-color="#EC4899"/>
                </linearGradient>
            </defs>
        </svg>
        <h2 style="margin: 8px 0 0 0; color: #1E1B4B; font-size: 1.35rem; font-weight: 800;">AuraDesk AI</h2>
        <span style="font-size: 0.8rem; color: #6366F1; font-weight: 600;">Smart Routing Support Studio</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🤖 Dynamic Routing Team")

    agents_info = [
        ("1. 🧭 Triage Router", "Analyzes query & dispatches to the correct expert.", "#4F46E5"),
        ("2. 💳 Billing Specialist", "Handles invoices, subscriptions, and refund requests.", "#0EA5E9"),
        ("3. 🔧 Technical Specialist", "Resolves 2FA, bugs, errors, and system glitches.", "#8B5CF6"),
        ("4. 📦 Shipping Specialist", "Tracks orders, missing items, and delivery delays.", "#F59E0B"),
        ("5. 🛡️ Policy Auditor", "Reviews tone, empathy, and company compliance.", "#10B981"),
        ("6. 🚀 Delivery Agent", "Delivers the final formatted solution.", "#EC4899"),
    ]

    for title, desc, color in agents_info:
        st.markdown(f"""
        <div class="agent-card" style="border-left-color: {color};">
            <div class="agent-title">{title}</div>
            <div class="agent-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# AutoGen Agents Initialization with Dynamic Routing
# -----------------------------------------------------------------------------
@st.cache_resource
def get_llm_config():
    return {
        "config_list": [{"model": "gpt-4o", "api_key": api_key}],
        "temperature": 0.3,
    }

def create_support_agents(llm_config):
    # 1st Agent: Intelligent Triage Router
    router_agent = autogen.ConversableAgent(
        name="Triage_Router_Agent",
        system_message=(
            "You are the Triage Router Agent. Read the customer's incoming issue carefully. "
            "Determine which specialized department agent should handle it next based on the topic:\n"
            "- If it's about money, billing, invoices, subscriptions, or refunds -> route to Billing_Specialist.\n"
            "- If it's about app errors, login issues, bugs, or 2FA -> route to Technical_Specialist.\n"
            "- If it's about package delivery, tracking, or damaged goods -> route to Shipping_Specialist.\n"
            "State your routing decision clearly so the correct expert takes over."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # Specialist 1: Billing
    billing_agent = autogen.ConversableAgent(
        name="Billing_Specialist",
        system_message=(
            "You are the Billing Specialist. Address refund inquiries, duplicate charges, and subscription rules "
            "with professional empathy and accurate company policy guidelines. Pass your drafted solution to Policy_Auditor."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # Specialist 2: Technical Support
    tech_agent = autogen.ConversableAgent(
        name="Technical_Specialist",
        system_message=(
            "You are the Technical Support Specialist. Provide step-by-step troubleshooting instructions for software bugs, "
            "login blockers, or authentication resets. Pass your drafted solution to Policy_Auditor."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # Specialist 3: Shipping & Logistics
    shipping_agent = autogen.ConversableAgent(
        name="Shipping_Specialist",
        system_message=(
            "You are the Shipping & Logistics Specialist. Handle delivery tracking issues, damaged items, and replacement policies. "
            "Pass your drafted solution to Policy_Auditor."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # Auditor Agent
    auditor_agent = autogen.ConversableAgent(
        name="Policy_Auditor",
        system_message=(
            "You are the Policy and Compliance Auditor Agent. Review the specialist's response for tone, empathy, "
            "and factual accuracy. Suggest quick improvements if needed, then pass to Customer_Delivery_Agent."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # Delivery Agent
    delivery_agent = autogen.ConversableAgent(
        name="Customer_Delivery_Agent",
        system_message=(
            "You are the Customer Delivery Agent. Perform a final format polish and present ONLY the final customer-ready reply. "
            "Conclude your final message with TERMINATE."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    return router_agent, billing_agent, tech_agent, shipping_agent, auditor_agent, delivery_agent

# -----------------------------------------------------------------------------
# Main Workspace UI
# -----------------------------------------------------------------------------
col_hero1, col_hero2 = st.columns([3, 1])

with col_hero1:
    st.markdown("""
    <div class="hero-banner">
        <h1>🎧 Intelligent Multi-Agent Support Desk</h1>
        <p>Dynamic query routing: The Triage Router analyzes your ticket and hands it directly to the right expert (Billing, Tech, or Shipping) for precise resolution.</p>
    </div>
    """, unsafe_allow_html=True)

with col_hero2:
    st.image(
        "https://img.icons8.com/fluency/240/customer-support.png",
        width=145,
    )

if "ticket_input" not in st.session_state:
    st.session_state.ticket_input = ""

st.markdown("#### 💡 Quick Sample Tickets (Test Smart Routing)")
sample_col1, sample_col2, sample_col3 = st.columns(3)

with sample_col1:
    if st.button("🔐 Tech: Lost 2FA", use_container_width=True):
        st.session_state.ticket_input = "I got a new phone and lost access to my authenticator app, so now I can't log into my account. How do I reset my two-factor authentication?"

with sample_col2:
    if st.button("💳 Billing: Refund Request", use_container_width=True):
        st.session_state.ticket_input = "I just checked my bank statement and noticed I was charged twice for my Pro subscription today ($49.99 each). Please refund the extra charge immediately!"

with sample_col3:
    if st.button("📦 Shipping: Damaged Item", use_container_width=True):
        st.session_state.ticket_input = "My order #88412 arrived today, but the box was crushed and the screen on the device is cracked. I need a replacement sent out ASAP."

st.markdown("---")

customer_query = st.text_area(
    "✍️ Customer Inquiry or Support Ticket:",
    value=st.session_state.ticket_input,
    height=120,
    placeholder="Describe the customer's issue, order number, or question here..."
)

resolve_clicked = st.button("✨ Route & Resolve Ticket", type="primary")

# -----------------------------------------------------------------------------
# Agent Execution & Results Display
# -----------------------------------------------------------------------------
if resolve_clicked:
    if not api_key:
        st.error("⚠️ OpenAI API key not found in `.env`. Please add `OPENAI_API_KEY` to your `.env` file.")
    elif not customer_query.strip():
        st.warning("⚠️ Please enter a customer inquiry or select a sample ticket above.")
    else:
        llm_config = get_llm_config()
        agents = create_support_agents(llm_config)
        router_agent, billing_agent, tech_agent, shipping_agent, auditor_agent, delivery_agent = agents

        user_proxy = autogen.UserProxyAgent(
            name="User_Proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=7,
            is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
            code_execution_config=False,
        )

        with st.spinner("🧭 Triage Router analyzing query and dispatching to the right specialist..."):
            groupchat = autogen.GroupChat(
                agents=[user_proxy, router_agent, billing_agent, tech_agent, shipping_agent, auditor_agent, delivery_agent],
                messages=[],
                max_round=7,
                speaker_selection_method="auto"  # Allows intelligent LLM-driven routing between agents
            )
            manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

            user_proxy.initiate_chat(
                manager,
                message=f"New Support Ticket: '{customer_query}'. Triage_Router_Agent, evaluate this query and route it to the correct department specialist."
            )

        st.balloons()
        st.success("✅ Ticket intelligently routed and resolved!")

        final_reply = ""
        agent_avatars = {
            "Triage_Router_Agent": "🧭",
            "Billing_Specialist": "💳",
            "Technical_Specialist": "🔧",
            "Shipping_Specialist": "📦",
            "Policy_Auditor": "🛡️",
            "Customer_Delivery_Agent": "🚀",
        }

        for msg in groupchat.messages:
            if msg.get("name") == "Customer_Delivery_Agent":
                final_reply = msg.get("content", "").replace("TERMINATE", "").strip()

        if final_reply:
            st.markdown("### 📩 Final Customer-Ready Response")
            st.markdown(f"""
            <div class="final-response-box">
                <span class="final-badge">✨ Smart-Routed & Approved</span>
                <div style="margin-top: 8px; line-height: 1.6; color: #1E293B;">
                    {final_reply.replace(chr(10), '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🔍 Behind-the-Scenes Routing & Collaboration Log")
        for msg in groupchat.messages:
            sender = msg.get("name", "System")
            content = msg.get("content", "").replace("TERMINATE", "").strip()
            if sender != "User_Proxy" and content:
                icon = agent_avatars.get(sender, "🤖")
                clean_name = sender.replace("_", " ")
                with st.expander(f"{icon} {clean_name}", expanded=False):
                    st.markdown(content)