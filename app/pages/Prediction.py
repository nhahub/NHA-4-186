import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
import sys
from pathlib import Path
from utils.path_setup import *
from utils.styles import inject_global_css, status_badge_html
from utils.sidebar import render_sidebar
from application.reports.export import export_prediction_pdf

if "batch_result" not in st.session_state:
    st.session_state.batch_result = None

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from application.prediction.service import PredictionService

st.set_page_config(
    page_title="Prediction",
    page_icon="🔮",
    layout="wide"
)

inject_global_css()
render_sidebar()

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login first")
    st.stop()

@st.cache_resource
def load_service():
    return PredictionService()

service = load_service()

st.markdown(
    '<div class="main-header"><h1>🔮 Prediction Module</h1><p>Predict Remaining Useful Life (RUL) for aircraft engines</p></div>',
    unsafe_allow_html=True,
)

if "result" not in st.session_state:
    st.session_state.result = None

prediction_mode = st.radio(
    "Choose Prediction Mode",
    ["Manual Prediction", "CSV Upload"],
    horizontal=True,
)

DEFAULT_SENSORS = {
    "op_setting_1": 0.0, "op_setting_2": 0.0,
    "sensor_2": 642.7, "sensor_3": 1590.5, "sensor_4": 1408.9,
    "sensor_6": 21.6, "sensor_7": 553.4, "sensor_8": 2388.1,
    "sensor_9": 9065.4, "sensor_11": 47.5, "sensor_12": 521.4,
    "sensor_13": 2388.1, "sensor_14": 8143.9, "sensor_15": 8.44,
    "sensor_17": 393.2, "sensor_20": 38.8, "sensor_21": 23.3,
}

SENSOR_RANGES = {
    "op_setting_1": (-0.006, 0.006, 0.0001),
    "op_setting_2": (-0.001, 0.001, 0.0001),
    "sensor_2": (641.0, 645.0, 0.1),
    "sensor_3": (1570.0, 1610.0, 0.5),
    "sensor_4": (1380.0, 1440.0, 0.5),
    "sensor_6": (21.6, 21.62, 0.001),
    "sensor_7": (550.0, 557.0, 0.1),
    "sensor_8": (2387.5, 2388.5, 0.01),
    "sensor_9": (8990.0, 9140.0, 1.0),
    "sensor_11": (46.5, 48.5, 0.05),
    "sensor_12": (519.0, 524.0, 0.1),
    "sensor_13": (2387.5, 2388.5, 0.01),
    "sensor_14": (8080.0, 8210.0, 1.0),
    "sensor_15": (8.3, 8.6, 0.005),
    "sensor_17": (388.0, 398.0, 0.1),
    "sensor_20": (38.2, 39.4, 0.02),
    "sensor_21": (22.9, 23.7, 0.01),
}

if prediction_mode == "Manual Prediction":
    with st.container(border=True):
        st.markdown('<div class="section-title">Engine Information</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        engine_id = col1.number_input("Engine ID", min_value=1, value=1, step=1)
        lo, hi, step = SENSOR_RANGES["op_setting_1"]
        op1 = col2.number_input("Operating Setting 1", value=DEFAULT_SENSORS["op_setting_1"], min_value=lo, max_value=hi, step=step, format="%.4f", help=f"Valid range: {lo} to {hi}")
        lo, hi, step = SENSOR_RANGES["op_setting_2"]
        op2 = col2.number_input("Operating Setting 2", value=DEFAULT_SENSORS["op_setting_2"], min_value=lo, max_value=hi, step=step, format="%.4f", help=f"Valid range: {lo} to {hi}")

    with st.container(border=True):
        st.markdown('<div class="section-title">Sensor Measurements</div>', unsafe_allow_html=True)
        sensor_data = {"op_setting_1": op1, "op_setting_2": op2}
        sensor_numbers = [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 20, 21]
        cols = st.columns(3)
        for i, sensor in enumerate(sensor_numbers):
            key = f"sensor_{sensor}"
            lo, hi, step = SENSOR_RANGES[key]
            sensor_data[key] = cols[i % 3].number_input(
                f"Sensor {sensor}", value=DEFAULT_SENSORS[key], min_value=lo, max_value=hi, step=step,
                format="%.4f", key=key, help=f"Valid range: {lo} to {hi}"
            )

    if st.button("🚀 Predict RUL", width='stretch'):
        with st.spinner("Running prediction with SHAP explanation..."):
            result = service.predict_single(
                sensor_data=sensor_data,
                user_id=st.session_state.user["id"],
                engine_id=engine_id
            )
        st.session_state.result = result

        if result["success"]:
            status = result["status"]

            with st.container(border=True):
                m1, m2 = st.columns(2)
                m1.metric("Predicted RUL", f"{result['predicted_rul']:.2f} Cycles")
                health = result["predicted_rul"]
                if health > 80:
                    m2.markdown(f"**Health Status**<br>{status_badge_html('Healthy')}", unsafe_allow_html=True)
                elif health > 30:
                    m2.markdown(f"**Health Status**<br>{status_badge_html('Warning')}", unsafe_allow_html=True)
                else:
                    m2.markdown(f"**Health Status**<br>{status_badge_html('Critical')}", unsafe_allow_html=True)

                if status["color"] == "success":
                    st.success(f"{status['icon']} {status['message']}")
                elif status["color"] == "warning":
                    st.warning(f"{status['icon']} {status['message']}")
                else:
                    st.error(f"{status['icon']} {status['message']}")

                st.info(f"💡 Recommended Action: {status['action']}")

            with st.container(border=True):
                st.subheader("📄 Prediction Report")
                report_df = pd.DataFrame({
                    "Field": ["Engine ID", "Predicted RUL", "Health Status", "Recommended Action"],
                    "Value": [str(engine_id), str(round(result["predicted_rul"], 2)), status["status"], status["action"]]
                })
                st.table(report_df)

                pdf = export_prediction_pdf({
                    "engine_id": engine_id,
                    "predicted_rul": round(result["predicted_rul"], 2),
                    "health_status": status["status"],
                    "prediction_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                })
                st.download_button(
                    "📄 Download PDF Report", data=pdf,
                    file_name=f"Prediction_Report_{engine_id}.pdf",
                    mime="application/pdf", width='stretch'
                )
        else:
            st.error(result["message"])

elif prediction_mode == "CSV Upload":
    with st.container(border=True):
        st.markdown('<div class="section-title">Upload NASA Test File</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv"])

        if uploaded_file is not None:
            columns = [
                "unit", "cycle", "op_setting_1", "op_setting_2", "op_setting_3",
                "sensor_1", "sensor_2", "sensor_3", "sensor_4", "sensor_5",
                "sensor_6", "sensor_7", "sensor_8", "sensor_9", "sensor_10",
                "sensor_11", "sensor_12", "sensor_13", "sensor_14", "sensor_15",
                "sensor_16", "sensor_17", "sensor_18", "sensor_19", "sensor_20", "sensor_21"
            ]
            df = pd.read_csv(uploaded_file, sep=r"\s+", header=None, names=columns, engine="python")

            st.markdown("#### Preview")
            st.dataframe(df.head(), width='stretch')

            if st.button("🚀 Predict CSV", width='stretch'):
                with st.spinner("Running batch prediction on uploaded data..."):
                    result = service.predict_batch(df, user_id=st.session_state.user["id"])

                st.session_state.batch_result = result
                if result["success"]:
                    st.toast("✅ Batch prediction completed!", icon="✅")

                    with st.container(border=True):
                        st.subheader("Results")
                        st.dataframe(result["results"], width='stretch')
                        csv = result["results"].to_csv(index=False).encode("utf-8")
                        st.download_button(
                            "📥 Download Prediction Results", data=csv,
                            file_name="batch_predictions.csv", mime="text/csv",
                            width='stretch'
                        )
                else:
                    st.error(result["message"])

if (
    prediction_mode == "Manual Prediction"
    and st.session_state.result is not None
    and st.session_state.result["success"]
):
    with st.container(border=True):
        explanation = st.session_state.result["explanation"]
        st.subheader("📊 SHAP Explanation")

        tab1, tab2 = st.tabs(["📈 Waterfall", "📊 Feature Importance"])

        with tab1:
            with st.spinner("Generating SHAP waterfall plot..."):
                shap.plots.waterfall(explanation["shap_values"][0], show=False)
                fig = plt.gcf()
                fig.set_size_inches(10, 6)
                st.pyplot(fig)
                plt.close(fig)

        with tab2:
            with st.spinner("Generating SHAP feature importance..."):
                shap.plots.bar(explanation["shap_values"], show=False)
                fig = plt.gcf()
                fig.set_size_inches(10, 6)
                st.pyplot(fig)
                plt.close(fig)
