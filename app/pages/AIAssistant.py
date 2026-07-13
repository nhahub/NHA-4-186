import streamlit as st
import sys
from pathlib import Path
from utils.path_setup import *
from utils.styles import inject_global_css
from utils.sidebar import render_sidebar

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from ai.rag import RAGEngine

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
)

inject_global_css()
render_sidebar()

st.markdown("""
<style>
.settings-section {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.settings-section h4 {
    color: #00e5ff;
    margin: 0 0 0.8rem 0;
    font-size: 0.9rem;
}
.chat-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    border: 1px solid rgba(0, 229, 255, 0.2);
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1rem;
}
.chat-header h2 {
    margin: 0;
    color: #fff;
    font-size: 1.3rem;
}
.chat-header p {
    margin: 0;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.85rem;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(46, 204, 113, 0.2);
    border: 1px solid rgba(46, 204, 113, 0.3);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    color: #2ecc71;
    margin-left: auto;
}
.status-dot {
    width: 6px;
    height: 6px;
    background: #2ecc71;
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.welcome-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin: 1.5rem 0;
    border: 1px solid rgba(0, 229, 255, 0.2);
}
.welcome-card h2 { color: #00e5ff; margin: 0 0 0.5rem 0; }
.welcome-card p { color: rgba(255, 255, 255, 0.8); margin: 0; }
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1.5rem;
}
.feature-card {
    background: rgba(0, 229, 255, 0.05);
    border: 1px solid rgba(0, 229, 255, 0.15);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    transition: all 0.3s ease;
}
.feature-card:hover {
    background: rgba(0, 229, 255, 0.1);
    border-color: rgba(0, 229, 255, 0.3);
}
.feature-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.feature-title { color: #00e5ff; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.3rem; }
.feature-desc { color: rgba(255, 255, 255, 0.6); font-size: 0.7rem; margin: 0; }
.stChatMessage {
    border-radius: 16px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.source-context {
    background: rgba(0, 0, 0, 0.3);
    border-left: 3px solid #00e5ff;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin-top: 0.8rem;
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.7);
}
.source-context strong { color: #00e5ff; }
.engine-status-card {
    background: rgba(46, 204, 113, 0.1);
    border: 1px solid rgba(46, 204, 113, 0.2);
    border-radius: 8px;
    padding: 0.8rem;
}
.engine-status-card strong { color: #2ecc71; }
.engine-status-card p { color: rgba(255,255,255,0.7); font-size: 0.85rem; margin: 0.3rem 0 0 0; }
.role-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 229, 255, 0.1);
    border: 1px solid rgba(0, 229, 255, 0.2);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    color: #00e5ff;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Please login first to access the AI Assistant.")
    st.stop()

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "top_k" not in st.session_state:
    st.session_state.top_k = 3
if "show_sources" not in st.session_state:
    st.session_state.show_sources = True
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Maintenance Engineer"

col_settings, col_chat = st.columns([1, 2], gap="medium")

with col_settings:
    st.markdown("### ⚙️ Engine Configuration")

    with st.expander("🔗 Connection", expanded=(st.session_state.rag_engine is None)):
        groq_api_key = st.text_input(
            "Groq API Key",
            value="",
            type="password",
            help="Get your key from console.groq.com",
            key="groq_key",
        )
        llm_model = st.text_input(
            "LLM Model",
            value="llama-3.3-70b-versatile",
            help="Groq-hosted model for response generation",
            key="llm_model",
        )

    with st.expander("📚 Knowledge Base", expanded=True):
        knowledge_path = st.text_input(
            "Knowledge Base File",
            value=str(ROOT / "data" / "knowledge_base.txt"),
            help="Path to your maintenance knowledge base text file",
            key="kb_path",
        )
        top_k = st.slider(
            "Top-K Retrieval",
            1, 10, st.session_state.top_k,
            help="Number of relevant chunks to retrieve",
            key="top_k_slider",
        )
        st.session_state.top_k = top_k

    with st.expander("👤 Assistant Role", expanded=True):
        role = st.selectbox(
            "Select your role",
            ["Maintenance Engineer", "Field Monitoring Worker", "General User"],
            index=["Maintenance Engineer", "Field Monitoring Worker", "General User"].index(
                st.session_state.selected_role
            ),
            help="Choose your role for tailored responses",
            key="role_select",
        )
        st.session_state.selected_role = role

        role_descriptions = {
            "Maintenance Engineer": "Technical, evidence-based responses with sensor references and thresholds.",
            "Field Monitoring Worker": "Plain-language status with traffic-light indicators and actionable checklists.",
            "General User": "High-level summaries with optional deeper technical dives.",
        }
        st.caption(role_descriptions[role])

    with st.expander("⚙️ Options", expanded=False):
        st.session_state.show_sources = st.checkbox(
            "Show Source Context",
            value=st.session_state.show_sources,
            help="Display the retrieved context chunks with responses",
            key="show_src",
        )

    if st.button("🚀 Load / Reload RAG Engine", type="primary", width="stretch"):
        with st.spinner("Loading embedding model and building vector index..."):
            try:
                engine = RAGEngine(
                    knowledge_path=knowledge_path,
                    groq_api_key=groq_api_key,
                    llm_model=llm_model,
                )
                n_chunks = engine.load()
                st.session_state.rag_engine = engine
                st.success(f"✅ RAG engine loaded! {n_chunks} chunks indexed.")
                st.rerun()
            except Exception as e:
                import traceback
                st.error(f"❌ Failed to load RAG engine: {e}")
                st.code(traceback.format_exc())

    if st.session_state.rag_engine is not None:
        st.markdown("---")
        st.markdown("""
        <div class="engine-status-card">
            <strong>✅ Engine Active</strong>
            <p>Ready to assist with turbofan maintenance queries</p>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.chat_history:
        st.markdown("---")
        if st.button("🗑️ Clear Chat History", type="secondary", width="stretch"):
            st.session_state.chat_history = []
            st.rerun()

with col_chat:
    status_badge = ""
    if st.session_state.rag_engine is not None:
        status_badge = '<span style="background:rgba(46,204,113,0.2);border:1px solid rgba(46,204,113,0.3);border-radius:20px;padding:0.25rem 0.7rem;font-size:0.75rem;color:#2ecc71;">● Active</span>'

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#1e3a5f 0%,#0d2137 100%);padding:1rem 1.5rem;border-radius:12px;border:1px solid rgba(0,229,255,0.2);margin-bottom:1rem;"><h2 style="margin:0;color:#fff;font-size:1.3rem;">🤖 TurboMind AI Assistant {status_badge}</h2><p style="margin:0.3rem 0 0 0;color:rgba(255,255,255,0.7);font-size:0.85rem;">Your intelligent maintenance companion powered by Groq</p></div>',
        unsafe_allow_html=True,
    )

    role_icons = {
        "Maintenance Engineer": "🔧",
        "Field Monitoring Worker": "👷",
        "General User": "👤",
    }
    st.markdown(
        f'<p style="background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.2);border-radius:20px;padding:0.3rem 0.8rem;font-size:0.8rem;color:#00e5ff;display:inline-block;">{role_icons[st.session_state.selected_role]} Responding as: <strong>{st.session_state.selected_role}</strong></p>',
        unsafe_allow_html=True,
    )

    if st.session_state.rag_engine is None:
        st.markdown("""
        <div class="welcome-card">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔧</div>
            <h2>Welcome to TurboMind</h2>
            <p>Configure and load the RAG engine in the settings panel to start chatting about turbofan engine maintenance.</p>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🔍</div>
                    <div class="feature-title">Smart Search</div>
                    <div class="feature-desc">AI-powered retrieval from maintenance docs</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💡</div>
                    <div class="feature-title">Expert Answers</div>
                    <div class="feature-desc">Context-aware responses from your knowledge base</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">RUL Estimation</div>
                    <div class="feature-desc">Remaining useful life analysis</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    with st.container():
        if not st.session_state.chat_history:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.5);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                <h3 style="color: rgba(255,255,255,0.7);">Start a Conversation</h3>
                <p style="color: rgba(255,255,255,0.5);">Ask anything about turbofan engine maintenance</p>
            </div>
            """, unsafe_allow_html=True)

            suggestion_cols = st.columns(3)
            suggestions = [
                "What are common engine degradation modes?",
                "Explain sensor readings S01-S21",
                "How to estimate RUL?",
            ]
            for i, suggestion in enumerate(suggestions):
                with suggestion_cols[i]:
                    if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                        st.session_state.chat_history.append({"role": "user", "content": suggestion})
                        st.rerun()
        else:
            for msg in st.session_state.chat_history:
                msg_role = msg["role"]
                content = msg["content"]
                sources = msg.get("sources", None)

                if msg_role == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(content)
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(content)
                        if sources and st.session_state.show_sources:
                            with st.expander("📎 Retrieved Sources", expanded=False):
                                for i, source in enumerate(sources, 1):
                                    st.markdown(
                                        f"""
                                        <div class="source-context">
                                            <strong>Chunk {i}</strong><br>
                                            {source[:300]}...
                                        </div>
                                        """,
                                        unsafe_allow_html=True,
                                    )

    if prompt := st.chat_input("Ask about turbofan engines, sensors, RUL..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🔍 Searching knowledge base..."):
                try:
                    sources = st.session_state.rag_engine.search(query=prompt, k=st.session_state.top_k)

                    with st.spinner("🧠 Generating response..."):
                        response = st.session_state.rag_engine.generate(
                            query=prompt,
                            k=st.session_state.top_k,
                            max_tokens=4096,
                            role=st.session_state.selected_role,
                        )
                except Exception as e:
                    response = f"❌ Error generating response: {e}"
                    sources = None

            st.markdown(response)

            if sources and st.session_state.show_sources:
                with st.expander("📎 Retrieved Sources", expanded=False):
                    for i, source in enumerate(sources, 1):
                        st.markdown(
                            f"""
                            <div class="source-context">
                                <strong>Chunk {i}</strong><br>
                                {source[:300]}...
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "sources": sources if "sources" in locals() else None,
        })
