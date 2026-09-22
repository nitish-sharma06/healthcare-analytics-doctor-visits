# Healthcare Analytics: Understanding Doctor Visit Patterns

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://healthcare-analytics-doctor-visits-geauvqwfkjj58bqqzezbqz.streamlit.app/)

Exploratory data analysis of a patient-level healthcare dataset, examining how demographic, economic, and health-related factors relate to the number of doctor visits.

**🔗 Live App:** https://healthcare-analytics-doctor-visits-geauvqwfkjj58bqqzezbqz.streamlit.app/

## Overview

This project explores the **Doctor Visits** dataset to understand what drives patients to visit the doctor more or less often. The analysis follows a standard EDA workflow: data loading and inspection, univariate analysis, bivariate analysis, and multivariate analysis, ending in a set of key takeaways.

## Files

| File | Description |
|---|---|
| `1776250375-P2-Healthcare_Analytics_for_Doctor_Visits.csv` | Raw dataset — 5,190 patient records with 12 variables (visits, gender, age, income, illness score, insurance status, chronic condition flags, etc.) |
| `Healthcare_Analytics_for_Doctor_Visits_Completed.ipynb` | Jupyter Notebook with the full analysis: data cleaning checks, distributions, correlations, and visualizations |
| `Healthcare_Analytics_for_Doctor_Visits_Presentation_1.pptx` | Slide deck summarizing the methodology and key findings |
| `app.py` | Streamlit app — interactive version of the analysis, deployed live above |
| `requirements.txt` | Python dependencies needed to run `app.py` |

## Dataset

The dataset contains 5,190 records with the following fields:

- **visits** — number of doctor visits
- **gender** — patient gender
- **age** — patient age (scaled)
- **income** — patient income (scaled)
- **illness** — illness severity score
- **reduced** — days of reduced activity due to illness
- **health** — general health score
- **private** — whether the patient has private health insurance
- **freepoor** — free healthcare coverage due to low income
- **freerepat** — free healthcare coverage (repatriation/veteran status)
- **nchronic** — presence of a chronic condition (non-limiting)
- **lchronic** — presence of a chronic condition (limiting)

The dataset is clean — no missing values and no duplicate rows.

## Analysis Structure

1. **Loading the Data** — import and initial inspection
2. **First Look: Structure & Data Types** — data types, missing values, duplicates
3. **Univariate Analysis** — individual variable distributions (gender split, age, income, visits, illness/chronic flags)
4. **Bivariate Analysis** — visits vs. gender, insurance status, illness score, and correlation among numeric variables
5. **Multivariate Analysis** — combined effects (chronic condition × gender, age × visits by insurance, income quartiles × illness level)
6. **Key Takeaways** — summary of findings

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/healthcare-analytics-doctor-visits.git
   cd healthcare-analytics-doctor-visits
   ```
2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   ```
3. Launch the notebook:
   ```bash
   jupyter notebook Healthcare_Analytics_for_Doctor_Visits_Completed.ipynb
   ```

## Key Findings

- The dataset is clean, with no missing values or duplicate rows across all 5,190 patient records.
- **Illness score has the strongest relationship with doctor visits** among the numeric variables examined — sicker patients visit the doctor more often, matching intuition.
- Patients **with private insurance tend to average more visits** than those without, suggesting insurance coverage may reduce a barrier to seeking care.
- **Gender differences in average visits are modest**, though the variance differs slightly between groups.
- Higher illness scores drive up visit counts **across every income quartile**, but the effect isn't perfectly uniform — a deeper statistical test (e.g. ANOVA or Poisson regression on `visits`) is a natural next step.

## Tools Used

- Python (pandas, numpy, matplotlib, seaborn)
- Jupyter Notebook
- Microsoft PowerPoint (for the summary presentation)

## Author

Nitish Sharma
