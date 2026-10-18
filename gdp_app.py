import re
from io import StringIO

import requests as rq
import bs4
import pandas as pd
import plotly.express as px
import streamlit as st

HEADERS = {"User-Agent": "Mozilla/5.0 (student homework project)"}


def clean_text(s):
    """Remove footnotes like [n 1] from a name."""
    s = re.sub(r"\[.*?\]", "", str(s))
    return s.strip()


def clean_number(s):
    """Turn text like '552,325 (2024)' into 552325. Dashes become NaN (missing)."""
    s = re.sub(r"\[.*?\]", "", str(s))
    s = re.sub(r"\(.*?\)", "", s)
    s = s.replace(",", "")
    return pd.to_numeric(s, errors="coerce")


@st.cache_data
def load_data():
    # --- Today's GDP table ---
    current_url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    page = rq.get(current_url, headers=HEADERS)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})
    for table in tables:
        if "Country/Territory" in table.get_text():
            gdp_table = table
            break

    current = pd.read_html(StringIO(str(gdp_table)))[0]
    current.columns = ["Country", "IMF", "WorldBank", "UN"]

    gdp = pd.DataFrame({
        "Country":   current["Country"].map(clean_text),
        "IMF":       current["IMF"].map(clean_number),
        "WorldBank": current["WorldBank"].map(clean_number),
        "UN":        current["UN"].map(clean_number),
    })
    gdp = gdp[gdp["Country"] != "World"]

    old_url = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_GDP_(nominal)&oldid=1187446467"
    old_page = rq.get(old_url, headers=HEADERS)
    old = pd.read_html(StringIO(old_page.text), match="region")[0]

    regions = pd.DataFrame({
        "Country": old.iloc[:, 0].map(clean_text),
        "Region":  old.iloc[:, 1].map(clean_text),
    })
    regions = regions[regions["Country"] != "World"]

    gdp = pd.merge(gdp, regions, on="Country", how="left")

    extra_regions = {
        "Channel Islands": "Europe",
        "Isle of Man": "Europe",
        "Faroe Islands": "Europe",
        "Guam": "Oceania",
        "Northern Mariana Islands": "Oceania",
        "American Samoa": "Oceania",
        "U.S. Virgin Islands": "Americas",
        "Saint Martin": "Americas",
    }
    gdp["Region"] = gdp["Region"].fillna(gdp["Country"].map(extra_regions))
    return gdp


st.title("GDP by Region")

gdp = load_data()

source = st.radio("Choose who reported the GDP numbers:",
                  ["IMF", "UN", "World Bank"], horizontal=True)

column = {"IMF": "IMF", "UN": "UN", "World Bank": "WorldBank"}[source]

plot_data = gdp.dropna(subset=[column]).sort_values(column, ascending=False)

fig = px.bar(
    plot_data,
    x="Region",
    y=column,
    color="Country",
    hover_name="Country",
    title=f"Nominal GDP by region ({source} numbers)",
    labels={column: "GDP (millions of US$)"},
    height=650,
)
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)