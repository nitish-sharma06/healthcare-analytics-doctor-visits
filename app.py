import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Healthcare Analytics: Doctor Visits",
    page_icon="🩺",
    layout="wide",
)

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 100
pd.set_option("display.max_columns", None)

CSV_PATH = "Healthcare_Analytics_for_Doctor_Visits.csv"


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path)
    df = raw.rename(columns={"Unnamed: 0": "patient_id"})
    return df


try:
    df = load_data(CSV_PATH)
except FileNotFoundError:
    st.error(
        f"Couldn't find `{CSV_PATH}`. Make sure the CSV is in the same folder as "
        "`app.py` (and named exactly that) before deploying."
    )
    st.stop()


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.title("🩺 Filters")

gender_options = sorted(df["gender"].dropna().unique().tolist())
gender_filter = st.sidebar.multiselect("Gender", gender_options, default=gender_options)

insurance_options = sorted(df["private"].dropna().unique().tolist())
insurance_filter = st.sidebar.multiselect(
    "Has private insurance?", insurance_options, default=insurance_options
)

illness_min, illness_max = int(df["illness"].min()), int(df["illness"].max())
illness_range = st.sidebar.slider(
    "Illness score range", illness_min, illness_max, (illness_min, illness_max)
)

st.sidebar.markdown("---")
st.sidebar.caption(f"{len(df):,} total patient records in the dataset")

filtered = df[
    df["gender"].isin(gender_filter)
    & df["private"].isin(insurance_filter)
    & df["illness"].between(illness_range[0], illness_range[1])
]

st.sidebar.markdown(f"**{len(filtered):,} records** match your filters")


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("Healthcare Analytics: Understanding Doctor Visit Patterns")
st.markdown(
    "Interactive exploration of how demographic, economic, and health-related "
    "factors relate to the number of times a patient visits a doctor."
)

if filtered.empty:
    st.warning("No records match the current filters. Adjust the filters in the sidebar.")
    st.stop()

tab_overview, tab_uni, tab_bi, tab_multi, tab_takeaways, tab_data = st.tabs(
    ["Overview", "Univariate", "Bivariate", "Multivariate", "Key Takeaways", "Raw Data"]
)


# ---------------------------------------------------------
# Overview
# ---------------------------------------------------------
with tab_overview:
    st.subheader("Dataset Snapshot")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Records (filtered)", f"{len(filtered):,}")
    c2.metric("Mean visits", f"{filtered['visits'].mean():.2f}")
    c3.metric("Median visits", f"{filtered['visits'].median():.0f}")
    c4.metric("Missing values", int(filtered.isnull().sum().sum()))

    st.markdown("#### Sample rows")
    st.dataframe(filtered.head(10), use_container_width=True)

    st.markdown("#### Summary statistics")
    st.dataframe(filtered.describe(include="all").T, use_container_width=True)

    dupes = filtered.duplicated().sum()
    st.caption(f"Duplicate rows in the filtered data: {dupes}")


# ---------------------------------------------------------
# Univariate
# ---------------------------------------------------------
with tab_uni:
    st.subheader("Univariate Analysis")
    st.caption("Looking at each variable in isolation before comparing them against each other.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Gender split**")
        fig, ax = plt.subplots(figsize=(5, 5))
        gender_counts = filtered["gender"].value_counts()
        colors = sns.color_palette("Set2", len(gender_counts))
        ax.pie(
            gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%",
            startangle=90, colors=colors, wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        )
        ax.set_title("Share of Patients by Gender")
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        st.markdown("**Age distribution**")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.histplot(filtered["age"], bins=25, kde=True, color="#4C72B0", ax=ax)
        ax.set_title("Distribution of Patient Age")
        ax.set_xlabel("Age (scaled)")
        ax.set_ylabel("Number of Patients")
        st.pyplot(fig)
        plt.close(fig)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Income distribution**")
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.histplot(filtered["income"], bins=25, kde=True, color="#55A868", ax=ax)
        ax.set_title("Distribution of Household Income")
        ax.set_xlabel("Income (scaled)")
        ax.set_ylabel("Number of Patients")
        st.pyplot(fig)
        plt.close(fig)

    with col4:
        st.markdown("**Number of doctor visits**")
        visit_counts = filtered["visits"].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.barplot(x=visit_counts.index, y=visit_counts.values, color="#C44E52", ax=ax)
        ax.set_title("How Many Times Did Patients Visit the Doctor?")
        ax.set_xlabel("Number of Visits")
        ax.set_ylabel("Number of Patients")
        st.pyplot(fig)
        plt.close(fig)
        st.caption(
            f"Median visits: {filtered['visits'].median()} | "
            f"Mean visits: {filtered['visits'].mean():.2f}"
        )

    st.markdown("**Illness score and chronic condition flags**")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.countplot(x="illness", data=filtered, color="#8172B2", ax=axes[0])
    axes[0].set_title("Illness Score Distribution")
    axes[0].set_xlabel("Illness Score")
    axes[0].set_ylabel("Number of Patients")

    chronic_share = pd.DataFrame({
        "No chronic condition": filtered["nchronic"].value_counts(normalize=True) * 100,
        "One chronic condition": filtered["lchronic"].value_counts(normalize=True) * 100,
    })
    chronic_share.plot(kind="bar", ax=axes[1], color=["#64B5CD", "#DD8452"])
    axes[1].set_title("Share of Patients Reporting Chronic Conditions")
    axes[1].set_ylabel("% of Patients")
    axes[1].set_xlabel("")
    axes[1].tick_params(axis="x", rotation=0)
    axes[1].legend(title="")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ---------------------------------------------------------
# Bivariate
# ---------------------------------------------------------
with tab_bi:
    st.subheader("Bivariate Analysis")
    st.caption("Comparing `visits` against other variables to look for patterns.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Average visits by gender**")
        gender_visits = filtered.pivot_table(
            index="gender", values="visits", aggfunc=["count", "mean", "median"]
        )
        gender_visits.columns = ["count", "mean_visits", "median_visits"]
        st.dataframe(gender_visits, use_container_width=True)

        fig, ax = plt.subplots(figsize=(6, 5))
        sns.barplot(x=gender_visits.index, y=gender_visits["mean_visits"], color="#4C72B0", ax=ax)
        ax.set_title("Average Doctor Visits by Gender")
        ax.set_xlabel("Gender")
        ax.set_ylabel("Mean Number of Visits")
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        st.markdown("**Average visits by insurance status**")
        insurance_visits = filtered.groupby("private")["visits"].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.barplot(x=insurance_visits.index, y=insurance_visits.values, color="#55A868", ax=ax)
        ax.set_title("Average Doctor Visits: Private Insurance vs. None")
        ax.set_xlabel("Has Private Insurance?")
        ax.set_ylabel("Mean Number of Visits")
        st.pyplot(fig)
        plt.close(fig)
        st.dataframe(insurance_visits.rename("mean_visits"), use_container_width=True)

    st.markdown("**Illness score vs. doctor visits**")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.regplot(
        x="illness", y="visits", data=filtered,
        x_jitter=0.15, y_jitter=0.15,
        scatter_kws={"alpha": 0.15, "color": "#C44E52", "s": 15},
        line_kws={"color": "black", "linewidth": 2},
        ax=ax,
    )
    ax.set_title("Illness Score vs. Doctor Visits (with trend line)")
    ax.set_xlabel("Illness Score")
    ax.set_ylabel("Number of Visits")
    st.pyplot(fig)
    plt.close(fig)
    st.caption(f"Correlation (illness, visits): {round(filtered['illness'].corr(filtered['visits']), 3)}")

    st.markdown("**Correlation among numeric variables**")
    numeric_cols = ["visits", "age", "income", "illness", "reduced", "health"]
    corr = filtered[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation Heatmap: Numeric Variables")
    st.pyplot(fig)
    plt.close(fig)


# ---------------------------------------------------------
# Multivariate
# ---------------------------------------------------------
with tab_multi:
    st.subheader("Multivariate Analysis")
    st.caption("Combining two or more factors at once to see whether relationships change across subgroups.")

    st.markdown("**Visits by chronic condition and gender**")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(x="nchronic", y="visits", hue="gender", data=filtered, ax=ax)
    ax.set_title("Doctor Visits by Chronic Condition Status and Gender")
    ax.set_xlabel("Has a Non-Chronic Condition?")
    ax.set_ylabel("Number of Visits")
    ax.legend(title="Gender")
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("**Age vs. visits, colored by insurance status**")
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(
        x="age", y="visits", hue="private", style="gender",
        data=filtered, alpha=0.6, palette="Set1", ax=ax,
    )
    ax.set_title("Age vs. Doctor Visits, by Insurance Status and Gender")
    ax.set_xlabel("Age (scaled)")
    ax.set_ylabel("Number of Visits")
    st.pyplot(fig)
    plt.close(fig)

    st.markdown("**Average visits across income quartiles and illness levels**")
    try:
        working = filtered.copy()
        working["income_quartile"] = pd.qcut(
            working["income"], 4, labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"], duplicates="drop"
        )
        pivot = working.pivot_table(index="income_quartile", columns="illness", values="visits", aggfunc="mean")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
        ax.set_title("Average Visits by Income Quartile and Illness Score")
        ax.set_xlabel("Illness Score")
        ax.set_ylabel("Income Quartile")
        st.pyplot(fig)
        plt.close(fig)
    except ValueError:
        st.info("Not enough varied income data in the current filter selection to compute quartiles.")


# ---------------------------------------------------------
# Key Takeaways
# ---------------------------------------------------------
with tab_takeaways:
    st.subheader("Key Takeaways")
    st.markdown(
        """
- The dataset is clean: **no missing values and no duplicate rows** across 5,190 patient records.
- **Illness score has the strongest relationship with doctor visits** of the numeric
  variables examined, which matches intuition — sicker patients visit the doctor more often.
- Patients **with private insurance tend to average more visits** than those without,
  suggesting insurance coverage may reduce a barrier to seeking care.
- **Gender differences in average visits are modest**, though the spread (variance) differs
  slightly between groups.
- Combining **income and illness** shows that higher illness scores drive up visit counts
  across every income quartile, but the effect is not perfectly uniform — worth a deeper
  statistical test (e.g. ANOVA or a Poisson regression on `visits`) as a next step.
        """
    )


# ---------------------------------------------------------
# Raw Data
# ---------------------------------------------------------
with tab_data:
    st.subheader("Raw / Filtered Data")
    st.dataframe(filtered, use_container_width=True)
    st.download_button(
        "Download filtered data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_doctor_visits.csv",
        mime="text/csv",
    )

st.markdown("---")
st.caption("Built with Streamlit · Data: Doctor Visits healthcare dataset")
