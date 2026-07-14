import streamlit as st

HEALTH_COLORS = {
    "Healthy": "#2ca02c",
    "Good": "#2ca02c",
    "Warning": "#ff7f0e",
    "Fair": "#1f77b4",
    "Critical": "#d62728",
    "Poor": "#ff7f0e",
    "High Risk": "#d62728"
}

DARK_HEALTH_COLORS = {
    "Healthy": "#00ff88",
    "Good": "#00ff88",
    "Warning": "#ffb300",
    "Fair": "#00e5ff",
    "Critical": "#ff2d55",
    "Poor": "#ffb300",
    "High Risk": "#ff2d55"
}


def get_plotly_template():
    theme = st.session_state.get("theme", "light")
    if theme == "dark":
        return {
            "template": "plotly_dark",
            "font": {"family": "sans serif"},
            "hoverlabel": {"font": {"family": "sans serif"}},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
        }
    else:
        return {
            "template": "plotly_white",
            "font": {"family": "sans serif"},
            "hoverlabel": {"font": {"family": "sans serif"}},
        }


def apply_theme(fig):
    theme = st.session_state.get("theme", "light")
    config = get_plotly_template()
    fig.update_layout(**config)
    if theme == "dark":
        fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)")
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig
