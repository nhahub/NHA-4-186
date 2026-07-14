import pandas as pd
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
# ======================================================
# Export DataFrame to CSV
# ======================================================

def export_to_csv(df):
    """
    Convert a pandas DataFrame to CSV bytes.
    Used with Streamlit download_button().
    """

    return df.to_csv(
        index=False
    ).encode("utf-8")


# ======================================================
# Export DataFrame to Excel
# ======================================================

def export_to_excel(df):
    """
    Convert a pandas DataFrame to an Excel file in memory.
    """

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Report"
        )

    output.seek(0)

    return output.getvalue()


# ======================================================
# Export Multiple Reports to Excel
# ======================================================

def export_multiple_reports(report_dict):
    """
    Export multiple DataFrames into one Excel workbook.

    Parameters
    ----------
    report_dict : dict
        {
            "Predictions": predictions_df,
            "Maintenance": maintenance_df,
            "Critical": critical_df
        }
    """

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        for sheet_name, dataframe in report_dict.items():

            dataframe.to_excel(
                writer,
                sheet_name=sheet_name[:31],   # Excel sheet name limit
                index=False
            )

    output.seek(0)

    return output.getvalue()
# ======================================================
# Export Prediction Report to PDF
# ======================================================

def export_prediction_pdf(prediction):
    """
    prediction : dict
    """

    output = BytesIO()

    doc = SimpleDocTemplate(output)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "AI Predictive Maintenance Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    table_data = [

        ["Field", "Value"],

        ["Engine ID", prediction["engine_id"]],

        ["Predicted RUL", prediction["predicted_rul"]],

        ["Health Status", prediction["health_status"]],

        ["Prediction Date", prediction["prediction_date"]]

    ]

    table = Table(table_data, colWidths=[180, 250])

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0,0), (-1,0), 8),

            ("ALIGN", (0,0), (-1,-1), "CENTER")

        ])

    )

    elements.append(table)

    doc.build(elements)

    pdf = output.getvalue()

    output.close()

    return pdf