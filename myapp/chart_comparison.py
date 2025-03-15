import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.http import HttpResponse
from .models import RealMeasurement, PredictedMeasurement


def generate_average_comparison_chart():
    # Get all real and predicted measurements
    real_measurements = RealMeasurement.objects.all()
    predicted_measurements = PredictedMeasurement.objects.all()

    # Use the first real measurement to get the field names (excluding id and image_name)
    fields = [field.name for field in RealMeasurement._meta.fields if field.name not in ["id", "image_name"]]

    real_averages = []
    predicted_averages = []

    for field in fields:
        real_values = [getattr(rm, field) for rm in real_measurements]
        predicted_values = [getattr(pm, field) for pm in predicted_measurements]

        real_avg = sum(real_values) / len(real_values) if real_values else 0
        predicted_avg = sum(predicted_values) / len(predicted_values) if predicted_values else 0

        real_averages.append(real_avg)
        predicted_averages.append(predicted_avg)

    # Prepare data for Seaborn
    data = {
        "Measurement": fields * 2,
        "Average Value (cm)": real_averages + predicted_averages,
        "Type": ["Average Real"] * len(fields) + ["Average Predicted"] * len(fields)
    }

    # Plotting with Seaborn
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 8))

    sns.barplot(data=data, x="Measurement", y="Average Value (cm)", hue="Type", palette=["#8884d8", "#82ca9d"])
    plt.title("Real vs Predicted Measurements", fontsize=16)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Measurement", fontsize=14)
    plt.ylabel("Value (cm)", fontsize=14)

    # Save the chart to a BytesIO object
    chart_buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(chart_buffer, format='png')
    chart_buffer.seek(0)
    plt.close()

    # Return the image as a response
    return HttpResponse(chart_buffer.getvalue(), content_type='image/png')
