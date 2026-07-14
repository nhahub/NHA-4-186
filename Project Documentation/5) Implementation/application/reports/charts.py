import plotly.express as px
from application.reports.theme import HEALTH_COLORS, apply_theme


def create_health_status_chart(df):
    if df.empty:
        return None
    fig = px.pie(
        df, names="health_status", values="total",
        title="Health Status Distribution",
        hole=0.4, color="health_status",
        color_discrete_map=HEALTH_COLORS
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    apply_theme(fig)
    return fig


def create_prediction_trend_chart(df):
    if df.empty:
        return None
    fig = px.line(
        df, x="day", y="total",
        markers=True, title="Prediction Trend Over Time",
        line_shape='spline'
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Predictions"
    )
    apply_theme(fig)
    return fig


def create_maintenance_type_chart(df):
    if df.empty:
        return None
    fig = px.bar(
        df, x="maintenance_type", y="total",
        title="Maintenance Type Distribution",
        color="maintenance_type"
    )
    fig.update_layout(
        xaxis_title="Maintenance Type",
        yaxis_title="Count",
        showlegend=False
    )
    apply_theme(fig)
    return fig


def create_engineer_activity_chart(df):
    if df.empty:
        return None
    fig = px.bar(
        df, x="Engineer_Name",
        y=["Predictions_Count", "Maintenance_Count"],
        barmode="group",
        title="Engineer Activity Overview",
        labels={'value': 'Count', 'variable': 'Activity Type', 'Engineer_Name': 'Engineer'},
        color_discrete_sequence=['#1f77b4', '#2ca02c']
    )
    apply_theme(fig)
    return fig


def create_critical_engines_chart(df):
    if df.empty:
        return None
    fig = px.bar(
        df, x="predicted_rul", y="engine_id",
        color="health_status", orientation="h",
        title="Critical Engines by Remaining Useful Life (RUL)",
        labels={'engine_id': 'Engine ID', 'predicted_rul': 'Predicted RUL', 'health_status': 'Status'},
        color_discrete_map=HEALTH_COLORS
    )
    fig.update_layout(
        xaxis_title="Predicted RUL",
        yaxis_title="Engine ID",
        yaxis_type='category'
    )
    apply_theme(fig)
    return fig
