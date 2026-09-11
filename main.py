import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("영화의 일별 관객 수가 시간에 따라 어떻게 변했는지 살펴봅니다.")


# ============================================================
# 1. 데이터 불러오기
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜: YYYYMMDD → 실제 날짜
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce",
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # 날짜 기준으로 정렬
    df = df.sort_values(["날짜", "순위"]).reset_index(drop=True)

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.info("인터넷 연결이나 데이터 주소를 확인해 주세요.")
    st.stop()


# ============================================================
# 데이터 확인
# ============================================================

if df.empty:
    st.warning("불러온 데이터가 없습니다.")
    st.stop()


# ============================================================
# 그래프 1. 영화별 날짜에 따른 일관객 변화
# ============================================================

st.divider()

st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 수 변화를 "
    "선 그래프로 확인할 수 있습니다."
)

# 영화 목록
movie_list = (
    df["영화명"]
    .dropna()
    .astype(str)
    .drop_duplicates()
    .sort_values()
    .tolist()
)

if not movie_list:
    st.warning("선택할 수 있는 영화가 없습니다.")
    st.stop()


selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list,
)


# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

movie_df = movie_df.sort_values("날짜")


# Plotly 그래프
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
)


# 마우스를 올렸을 때 날짜와 관객 수가 나오도록 설정
fig.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    height=500,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# ============================================================
# 이 그래프로 알 수 있는 것
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "영화의 일별 관객 수가 날짜에 따라 어떻게 증가하거나 감소했는지 "
    "확인할 수 있습니다."
)


# ============================================================
# 2. 앞으로 추가할 그래프
# ============================================================

st.divider()

st.header("📊 그래프 2. 다음 그래프")

st.write(
    "앞으로 새로운 그래프를 이 구역에 추가할 수 있습니다."
)

st.info(
    "예: 순위 변화, 누적관객 변화, 스크린 수 변화, "
    "상영횟수 변화 등의 그래프를 추가할 수 있습니다."
)


# ============================================================
# 3. 앞으로 추가할 그래프
# ============================================================

st.divider()

st.header("📊 그래프 3. 다음 그래프")

st.write(
    "추가 그래프를 위한 공간입니다."
)


# ============================================================
# 데이터 정보
# ============================================================

with st.expander("📋 데이터 정보 보기"):
    st.write(f"전체 데이터 행 수: **{len(df):,}개**")

    if df["날짜"].notna().any():
        min_date = df["날짜"].min().strftime("%Y-%m-%d")
        max_date = df["날짜"].max().strftime("%Y-%m-%d")

        st.write(f"데이터 기간: **{min_date} ~ {max_date}**")

    st.write(f"영화 종류: **{df['영화명'].nunique():,}개**")

    st.dataframe(
        df.head(20),
        use_container_width=True,
    )
