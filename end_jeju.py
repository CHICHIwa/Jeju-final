import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
from plotly.graph_objs import Figure
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.statespace.sarimax import SARIMAXResultsWrapper
import pickle
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly

# 타이틀, 아이콘, 레이아웃 설정
st.set_page_config(
    page_title="제주도 여행 계획의 A to Z - 데이터 기반 관광형태 분석",
    page_icon="🍊",
    layout="wide"
)

# CSS를 사용하여 전체 페이지의 배경 이미지 설정
def set_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdN82HY%2FbtsGK99f1pm%2FdW4DfXw42gpvIxOQon7RRK%2Fimg.webp");
            background-size: cover;
            background-position: center center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_image()  # 배경 이미지 함수 호출



# 대시보드에 페이지 제목 설정
def add_page_title():
    st.title("🍊제주도 관광 데이터 분석 Final-Project🍊")
    
    
# Page 클래스 정의 / 각 페이지 나타내고 제목, 내용,데이터프레임, 그래프, 이미지를 속성으로 가짐
class Page:
    def __init__(self, title, content, dfs=None, graphs=None, images=None, df_titles=None, graph_descriptions=None):
        self.title = title
        self.content = content
        self.dfs = dfs if dfs is not None else []
        self.graphs = graphs if graphs is not None else []
        self.images = images if images is not None else []
        self.df_titles = df_titles if df_titles is not None else []
        self.graph_descriptions = graph_descriptions if graph_descriptions is not None else []


def add_future_plans_page():
    st.write("""
    ## 향후 계획
    ### 호텔 데이터를 이용한 군집분석, 식당 추천 시스템
    """)
    
    # 이미지 파일을 로드합니다 (로컬 경로를 사용)
    image = Image.open("Jeju/Bye.png")
    
    # 이미지를 스트림릿 페이지에 표시
    st.image(image, caption='한라산의 울림, 바다의 속상임 - 제주도에서 휴식을 즐겨보세요')
       
# def show_pages(pages):
#     for page in pages:
#         if isinstance(page, Page):
#             st.write(f"# {page.title}")
#             st.write(page.content)
#             for i, df in enumerate(page.dfs):
#                 if df is not None:
#                     st.write(f"> **{page.df_titles[i]}**" if i < len(page.df_titles) else "> **Data**")
#                     st.dataframe(df, use_container_width=True)
            
#             # "관광 현황 분석" 페이지에 대한 특별한 레이아웃 처리
#             if page.title == "관광 현황 분석":
#                 # 첫 번째 그래프는 전체 너비로 표시
#                 if page.graphs:
#                     if isinstance(page.graphs[0], Figure):
#                         st.plotly_chart(page.graphs[0], use_container_width=True)
#                         if len(page.graph_descriptions) > 0:
#                             st.write(page.graph_descriptions[0])  # 첫 번째 그래프의 설명 추가
#                     else:
#                         st.error("Invalid graph object detected.")

#                 # 그 이후 그래프를 두 개씩 나열
#                 col_index = 0
#                 cols = [None, None]  # 두 개의 열을 위한 임시 리스트
#                 for i, graph in enumerate(page.graphs[1:]):  # 첫 번째 그래프를 제외하고 시작
#                     if col_index == 0:
#                         cols = st.columns(2)  # 두 열 생성
#                     if isinstance(graph, Figure):
#                         cols[col_index].plotly_chart(graph, use_container_width=True)
#                         if i + 1 < len(page.graph_descriptions):  # 설명이 있으면 출력
#                             cols[col_index].write(page.graph_descriptions[i + 1])
#                     else:
#                         cols[col_index].error("Invalid graph object detected.")
                    
#                     col_index = (col_index + 1) % 2  # 0, 1, 0, 1, ...으로 변경하여 열을 번갈아 선택
#             else:
#                 # 다른 페이지들은 모든 그래프를 두 개씩 나열
#                 col_index = 0
#                 cols = [None, None]
#                 for i, graph in enumerate(page.graphs):
#                     if col_index == 0:
#                         cols = st.columns(2)
#                     if isinstance(graph, Figure):
#                         cols[col_index].plotly_chart(graph, use_container_width=True)
#                         if i < len(page.graph_descriptions):  # 설명이 있으면 출력
#                             cols[col_index].write(page.graph_descriptions[i])
#                     else:
#                         cols[col_index].error("Invalid graph object detected.")
                    
#                     col_index = (col_index + 1) % 2

#         elif isinstance(page, Section):
#             st.write(f"## {page.title}")
#         else:
#             st.warning("Unknown page type!")

def show_pages(pages):
    for page in pages:
        if isinstance(page, Page):
            st.write(f"# {page.title}")
            st.write(page.content)
            for i, df in enumerate(page.dfs):
                if df is not None:
                    st.write(f"> **{page.df_titles[i]}**" if i < len(page.df_titles) else "> **Data**")
                    st.dataframe(df, use_container_width=True)
            
            # "관광 현황 분석" 페이지에 대한 특별한 레이아웃 처리
            if page.title in ["관광 현황 - 동반자 유형별 분석", "농협카드 - 시계열 모델링"]:
                # 첫 번째 그래프는 전체 너비로 표시
                if page.graphs:
                    if isinstance(page.graphs[0], Figure):
                        st.plotly_chart(page.graphs[0], use_container_width=True)
                        if len(page.graph_descriptions) > 0:
                            st.write(page.graph_descriptions[0])  # 첫 번째 그래프의 설명 추가
                    else:
                        st.error("Invalid graph object detected.")

                # 그 이후 그래프를 두 개씩 나열
                col_index = 0
                cols = [None, None]  # 두 개의 열을 위한 임시 리스트
                for i, graph in enumerate(page.graphs[1:]):  # 첫 번째 그래프를 제외하고 시작
                    if col_index == 0:
                        cols = st.columns(2)  # 두 열 생성
                    if isinstance(graph, Figure):
                        cols[col_index].plotly_chart(graph, use_container_width=True)
                        if i + 1 < len(page.graph_descriptions):  # 설명이 있으면 출력
                            cols[col_index].write(page.graph_descriptions[i + 1])
                    else:
                        cols[col_index].error("Invalid graph object detected.")
                    
                    col_index = (col_index + 1) % 2  # 0, 1, 0, 1, ...으로 변경하여 열을 번갈아 선택
                   
            elif page.title == "분류별 추천 관광지":
                for graph in page.graphs:
                    if isinstance(graph, folium.Map):
                        folium_static(graph, width=1000, height=800)
                    else:
                        st.error("Invalid graph object detected for the map display.")
            elif page.title == "향후 계획":
                add_future_plans_page()                  
            else:
                # 다른 페이지들은 모든 그래프를 두 개씩 나열
                col_index = 0
                cols = [None, None]
                for i, graph in enumerate(page.graphs):
                    if col_index == 0:
                        cols = st.columns(2)
                    if isinstance(graph, Figure):
                        cols[col_index].plotly_chart(graph, use_container_width=True)
                        if i < len(page.graph_descriptions):  # 설명이 있으면 출력
                            cols[col_index].write(page.graph_descriptions[i])
                    else:
                        cols[col_index].error("Invalid graph object detected.")
                    
                    col_index = (col_index + 1) % 2

        elif isinstance(page, Section):
            st.write(f"## {page.title}")
        else:
            st.warning("Unknown page type!")
            

class Section:
    def __init__(self, title):
        self.title = title
        
        
# 원본 데이터 로딩
df_1 = pd.read_csv("Jeju/데이터/제주 동반자 유형별 여행 계획 데이터2023.csv")
df_2 = pd.read_csv("Jeju/데이터/제주 무장애 관광지 입장 데이터2023.csv") 
df_3 = pd.read_csv("Jeju/데이터/SNS 제주 관광 키워드별 수집 통계_월2023.csv") 
df_4 = pd.read_csv("Jeju/데이터/제주 관광수요예측 데이터_비짓제주 로그 데이터 월2023.csv")
df_5 = pd.read_csv("Jeju/데이터/제주관광공사 관광 소비행태 데이터 카드사 음식 급상승 데이터.csv")
df_6 = pd.read_csv("Jeju/데이터/Consumption status by date_Jeju(2123).csv")
df_7 = pd.read_csv("Jeju/데이터/종합맵.csv")
####################################################################

cl_nm_counts = pd.read_csv("Jeju/시각화/cl_nm_counts.csv")
df_top_keywords = pd.read_csv("Jeju/시각화/df_top_keywords.csv")
df_top_CNTNTSs = pd.read_csv("Jeju/시각화/df_top_CNTNTSs.csv")
Sum_df = pd.read_csv("Jeju/시각화/Sum_df.csv")
sorted_group_df = pd.read_csv("Jeju/시각화/sorted_group_df.csv")


###################################################################
def format_period(period):
    year, month = divmod(period, 100)
    return f"{year}년 {month}월"

fig1 = go.Figure()

# Add a trace for each investigation period
for 조사기간 in cl_nm_counts['조사기간'].unique():
    filtered_df = cl_nm_counts[cl_nm_counts['조사기간'] == 조사기간]
    fig1.add_trace(
        go.Bar(
            visible=False,
            name=f"조사기간: {format_period(조사기간)}",
            x=filtered_df['동반자유형'],
            y=filtered_df['비율(%)']
        )
    )

# Make the first trace visible
fig1.data[0].visible = True

# Create sliders
steps = []
for i, 조사기간 in enumerate(cl_nm_counts['조사기간'].unique()):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig1.data)},
              {"title": f"조사기간: {format_period(조사기간)}"}],  # layout attribute
        label=format_period(조사기간)  # slider label
    )
    step["args"][0]["visible"][i] = True  # Toggle visibility of the i'th trace
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "조사기간 선택: "},
    pad={"t": 50},
    steps=steps
)]

# Annotations for data source
annotations = [dict(
    text="자료 출처: 제주관광공사",  # Replace with the actual source
    showarrow=False,
    xref="paper",
    yref="paper",
    x=0,
    y=-0.1,
    xanchor="left",
    yanchor="top",
    font=dict(size=12)
)]

# Update layout for Y-axis title and sliders
fig1.update_layout(
    yaxis_title='비율(%)',
    sliders=sliders,
    title="조사기간별 동반자유형 분석",
    annotations=annotations
)
####
fig2 = go.Figure()

# Add a pie chart for each companion type
for i, cl_nm in enumerate(df_top_keywords['동반자유형'].unique()):
    df_filtered = df_top_keywords[df_top_keywords['동반자유형'] == cl_nm]
    keywords = df_filtered['키워드'].tolist()
    frequencies = df_filtered['빈도'].tolist()

    fig2.add_trace(
        go.Pie(
            labels=keywords,
            values=frequencies,
            name=cl_nm,
            visible=(i == 0)  # Only the first companion type is visible initially
        )
    )

# Create slider steps
steps = []
for i, cl_nm in enumerate(df_top_keywords['동반자유형'].unique()):
    step = dict(
        method='update',
        args=[{'visible': [(j == i) for j in range(len(df_top_keywords['동반자유형'].unique()))]},
              {'title': f'동반자 유형: {cl_nm}'}],
        label=cl_nm
    )
    steps.append(step)

fig2.update_layout(
    sliders=[dict(
        active=0,
        currentvalue={'prefix': '동반자 유형: '},
        steps=steps
    )],
    annotations=[dict(
        text="자료 출처: 제주관광공사",
        showarrow=False,
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.2,
        xanchor="center",
        yanchor="top",
        font=dict(size=12)
    )],
    title="동반자 유형별 상위 키워드 분석"
)
####
fig3 = go.Figure()

# Add a pie chart for each companion type
for i, cl_nm in enumerate(df_top_CNTNTSs['동반자유형'].unique()):
    df_filtered = df_top_CNTNTSs[df_top_CNTNTSs['동반자유형'] == cl_nm]
    keywords = df_filtered['콘텐츠'].tolist()
    frequencies = df_filtered['빈도'].tolist()

    fig3.add_trace(
        go.Pie(
            labels=keywords,
            values=frequencies,
            name=cl_nm,
            visible=(i == 0)  # Only the first companion type is visible initially
        )
    )

# Create slider steps
steps = []
for i, cl_nm in enumerate(df_top_CNTNTSs['동반자유형'].unique()):
    step = dict(
        method='update',
        args=[{'visible': [(j == i) for j in range(len(df_top_CNTNTSs['동반자유형'].unique()))]},
              {'title': f'동반자 유형: {cl_nm}'}],
        label=cl_nm
    )
    steps.append(step)

fig3.update_layout(
    sliders=[dict(
        active=0,
        currentvalue={'prefix': '동반자 유형: '},
        steps=steps
    )],
    annotations=[dict(
        text="자료 출처: 제주관광공사",
        showarrow=False,
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.2,
        xanchor="center",
        yanchor="top",
        font=dict(size=12)
    )],
    title="동반자 유형별 상위 콘텐츠 분석"
)
############################
fig4 = px.line(Sum_df, x='방문기간', y='입장인원수', color='관광지명', 
              title='방문기간별 관광지 입장인원수',
              labels={'방문기간': '방문 기간', '입장인원수': '입장 인원수', '관광지명': '관광지 명'})

# Update graph layout
fig4.update_layout(
    xaxis_title='방문 기간',
    yaxis_title='입장 인원수',
    legend_title='관광지'
)
############################
fig5 = go.Figure()

unique_entry_types = sorted_group_df['입장구분명'].unique()

# Add a bar for each entry type
for entry_type in unique_entry_types:
    filtered_df = sorted_group_df[sorted_group_df['입장구분명'] == entry_type]
    fig5.add_trace(
        go.Bar(
            x=filtered_df['관광지명'],
            y=filtered_df['입장인원수'],
            name=entry_type,
            visible=False  # Start with all bars hidden, will enable visibility below
        )
    )

# Setup buttons for the interactive component
buttons = []
for i, entry_type in enumerate(unique_entry_types):
    visibility = [False] * len(unique_entry_types)
    visibility[i] = True
    buttons.append(
        dict(
            label=entry_type,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{entry_type} - 관광지별 입장인원수"}]
        )
    )

# Configure layout with buttons
fig5.update_layout(
    updatemenus=[{
        "buttons": buttons,
        "direction": "down",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "x": 0.1,
        "xanchor": "left",
        "y": 1.15,
        "yanchor": "top"
    }],
    title=f"{unique_entry_types[0]} - 관광지별 입장인원수"
)

# Initially set the first dataset to visible
fig5.data[0].visible = True
#####################################################
year_df = pd.read_csv("Jeju/시각화/year_df.csv")
year_df2 = pd.read_csv("Jeju/시각화/year_df2.csv")
sns_df = pd.read_csv("Jeju/시각화/sns_df.csv")
sns_df2 = pd.read_csv("Jeju/시각화/sns_df2.csv")
top_seasons = pd.read_csv("Jeju/시각화/top_seasons.csv")
top10_classification_df = pd.read_csv("Jeju/시각화/top10_classification_df.csv")
############################################################
year_df['게시년월'] = year_df['게시년월'].astype(str)

fig6 = go.Figure()

# Get unique months from DataFrame
unique_months = year_df['게시년월'].unique()

# Add data for each month and search term to the graph, initially hidden
for month in unique_months:
    for spot in year_df[year_df['게시년월'] == month]['검색어명'].unique():
        filtered_df = year_df[(year_df['게시년월'] == month) & (year_df['검색어명'] == spot)]
        fig6.add_trace(
            go.Bar(
                x=[spot],
                y=filtered_df['검색어언급수'],
                name=spot,
                visible=False,  # initially all traces are hidden
                legendgroup=month,  # group by month for toggling
                legendgrouptitle_text=month  # show month as group title
            )
        )

# Create buttons for each month to toggle visibility
buttons = []

for i, month in enumerate(unique_months):
    visibility = [(m.legendgroup == month) for m in fig6.data]  # check each trace's group

    buttons.append(
        dict(
            label=month,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{month} - 검색어별 언급수"}]
        )
    )

# Add dropdown menu with buttons to the layout
fig6.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.15,
        yanchor="top"
    )],
    title=f"{unique_months[0]} - 검색어별 언급수"
)

# Set the visibility of the first month's data as default
for trace in fig6.data:
    trace.visible = trace.legendgroup == unique_months[0]
######################################################
year_df2['게시년월'] = year_df2['게시년월'].astype(str)

fig7 = go.Figure()

# Create unique months from the DataFrame
unique_months = year_df2['게시년월'].unique()

# Add traces for each month and keyword, initially hidden
for month in unique_months:
    for spot in year_df2[year_df2['게시년월'] == month]['대표키워드명'].unique():
        filtered_df = year_df2[(year_df2['게시년월'] == month) & (year_df2['대표키워드명'] == spot)]
        fig7.add_trace(
            go.Bar(
                x=[spot],
                y=filtered_df['대표키워드언급수'],
                name=spot,
                visible=False,  # initially all traces are hidden
                legendgroup=month,  # group by month for toggling
                legendgrouptitle_text=month  # show month as group title
            )
        )

# Create buttons for each month to toggle visibility
buttons = []

for i, month in enumerate(unique_months):
    visibility = [month == trace.legendgroup for trace in fig7.data]  # adjust visibility based on group

    buttons.append(
        dict(
            label=month,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{month} - 키워드별 언급수"}]
        )
    )

# Add dropdown menu with buttons to the layout
fig7.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.15,
        yanchor="top"
    )],
    title=f"{unique_months[0]} - 키워드별 언급수"
)

# Set the visibility of the first month's data as default
for trace in fig7.data:
    trace.visible = trace.legendgroup == unique_months[0]
#########################################################
fig8 = go.Figure()

# Get unique source categories from DataFrame
unique_sources = sns_df['출처분류명'].unique()

# Add bars for each source and search term, initially hidden
for source in unique_sources:
    for spot in sns_df[sns_df['출처분류명'] == source]['검색어명'].unique():
        filtered_df = sns_df[(sns_df['출처분류명'] == source) & (sns_df['검색어명'] == spot)]
        fig8.add_trace(
            go.Bar(
                x=[spot],
                y=filtered_df['검색어언급수'],
                name=spot,
                visible=False,  # initially all traces are hidden
                legendgroup=source,  # group by source for toggling
                legendgrouptitle_text=source  # show source as group title
            )
        )

# Create buttons for each source to toggle visibility
buttons = []

for i, source in enumerate(unique_sources):
    visibility = [trace.legendgroup == source for trace in fig8.data]  # adjust visibility based on group

    buttons.append(
        dict(
            label=source,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{source} - 검색어별 언급수"}]
        )
    )

# Add dropdown menu with buttons to the layout
fig8.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.15,
        yanchor="top"
    )],
    title=f"{unique_sources[0]} - 검색어별 언급수"
)

# Set the visibility of the first source category as default
for trace in fig8.data:
    trace.visible = trace.legendgroup == unique_sources[0]
#########################################################
fig9 = go.Figure()

# Get unique source categories from DataFrame
unique_sources = sns_df2['출처분류명'].unique()

# Add bars for each source and keyword, initially hidden
for source in unique_sources:
    for keyword in sns_df2[sns_df2['출처분류명'] == source]['대표키워드명'].unique():
        filtered_df = sns_df2[(sns_df2['출처분류명'] == source) & (sns_df2['대표키워드명'] == keyword)]
        fig9.add_trace(
            go.Bar(
                x=[keyword],
                y=filtered_df['대표키워드언급수'],
                name=keyword,
                visible=False,  # initially all traces are hidden
                legendgroup=source,  # group by source for toggling
                legendgrouptitle_text=source  # show source as group title
            )
        )

# Create buttons for each source to toggle visibility
buttons = []

for i, source in enumerate(unique_sources):
    visibility = [(trace.legendgroup == source) for trace in fig9.data]  # adjust visibility based on group

    buttons.append(
        dict(
            label=source,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{source} - 대표키워드별 언급수"}]
        )
    )

# Add dropdown menu with buttons to the layout
fig9.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.15,
        yanchor="top"
    )],
    title=f"{unique_sources[0]} - 대표키워드별 언급수"
)

# Set the visibility of the first source category as default
for trace in fig9.data:
    trace.visible = trace.legendgroup == unique_sources[0]
###############################################################
fig10 = go.Figure()

# Get unique season categories from DataFrame
unique_sources = top_seasons['계절'].unique()

# Add bars for each season and location, initially hidden
for source in unique_sources:
    for keyword in top_seasons[top_seasons['계절'] == source]['지역명'].unique():
        filtered_df = top_seasons[(top_seasons['계절'] == source) & (top_seasons['지역명'] == keyword)]
        fig10.add_trace(
            go.Bar(
                x=[keyword],
                y=filtered_df['전체조회'],
                name=keyword,
                visible=False,  # initially all traces are hidden
                legendgroup=source,  # group by season for toggling
                legendgrouptitle_text=source  # show season as group title
            )
        )

# Create buttons for each season to toggle visibility
buttons = []

for i, source in enumerate(unique_sources):
    visibility = [(trace.legendgroup == source) for trace in fig10.data]  # adjust visibility based on group

    buttons.append(
        dict(
            label=source,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{source} - 계절별 검색어 언급수"}]
        )
    )

# Add dropdown menu with buttons to the layout
fig10.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.3,
        yanchor="top"
    )],
    title=f"{unique_sources[0]} - 계절별 검색어 언급수"
)

# Set the visibility of the first season's data as default
for trace in fig10.data:
    trace.visible = trace.legendgroup == unique_sources[0]
###########################################################
fig11 = go.Figure()

# Get unique classification names from DataFrame
unique_sources = top10_classification_df['분류명'].unique()

# Add bars for each classification and keyword, initially hidden
for source in unique_sources:
    for keyword in top10_classification_df[top10_classification_df['분류명'] == source]['지역명'].unique():
        filtered_df = top10_classification_df[(top10_classification_df['분류명'] == source) & (top10_classification_df['지역명'] == keyword)]
        fig11.add_trace(
            go.Bar(
                x=[keyword],
                y=filtered_df['전체조회'],
                name=keyword,
                visible=False,  # initially all traces are hidden
                legendgroup=source,  # group by classification for toggling
                legendgrouptitle_text=source  # show classification as group title
            )
        )

# Create buttons for each classification to toggle visibility
buttons = []

for i, source in enumerate(unique_sources):
    visibility = [(trace.legendgroup == source) for trace in fig11.data]  # adjust visibility based on group

    buttons.append(
        dict(
            label=source,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{source} - 분류별 검색어 언급수"}]
        )
    )

# Add dropdown menu with buttons to the layout
fig11.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        direction="down",
        pad={"r": 10, "t": 10},
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.3,
        yanchor="top"
    )],
    title=f"{unique_sources[0]} - 분류별 검색어 언급수"
)

# Set the visibility of the first classification's data as default
for trace in fig11.data:
    trace.visible = trace.legendgroup == unique_sources[0]
###################################################################
region_consumption_sorted1 = pd.read_csv("Jeju/시각화/region_consumption_sorted1.csv")
region_variation_sorted = pd.read_csv("Jeju/시각화/region_variation_sorted.csv")
top_local_sales_cleaned = pd.read_csv("Jeju/시각화/top_local_sales_cleaned.csv")
top_foreign_sales_cleaned = pd.read_csv("Jeju/시각화/top_foreign_sales_cleaned.csv")
sorted_grouped_df = pd.read_csv("Jeju/시각화/sorted_grouped_df.csv")
time_df = pd.read_csv("Jeju/시각화/time_df.csv")
#######################################################################
region_consumption_sorted1['년'] = region_consumption_sorted1['년'].astype(str)

fig12 = go.Figure()

# 고유 '년' 목록 생성
unique_years = region_consumption_sorted1['년'].unique()

# 모든 '년' 및 '지역명'에 대해 트레이스 추가
for year in unique_years:
    for region in region_consumption_sorted1[region_consumption_sorted1['년'] == year]['지역명'].unique():
        filtered_df = region_consumption_sorted1[(region_consumption_sorted1['년'] == year) & (region_consumption_sorted1['지역명'] == region)]
        fig12.add_trace(
            go.Bar(
                x=filtered_df['지역명'],
                y=filtered_df['전체매출금액비율'],
                name=f"{year} - {region}",
                visible=False, # initially all traces are hidden
                customdata=[year] * len(filtered_df)
            )
        )

# Button creation logic
buttons = []

for i, year in enumerate(unique_years):
    visibility = [year == trace.customdata[0] for trace in fig12.data]
    buttons.append(
        dict(
            label=year,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{year}년 지역별 전체매출금액비율"}]
        )
    )

# Update button layout
fig12.update_layout(
    updatemenus=[{
        "buttons": buttons,
        "direction": "down",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "x": 0.1,
        "xanchor": "left",
        "y": 1.15,
        "yanchor": "top"
    }],
    title=f"{unique_years[0]}년 지역별 전체매출금액비율"
)

# Set initial visibility
initial_year = unique_years[0]
for trace in fig12.data:
    trace.visible = trace.customdata[0] == initial_year
#################################################################################
region_variation_sorted['년'] = region_variation_sorted['년'].astype(str)

fig13 = go.Figure()

# Create a list of unique years
unique_years = region_variation_sorted['년'].unique()

# Add a bar for each year and region, initially hidden
for year in unique_years:
    for region in region_variation_sorted[region_variation_sorted['년'] == year]['지역명'].unique():
        filtered_df = region_variation_sorted[(region_variation_sorted['년'] == year) & (region_variation_sorted['지역명'] == region)]
        fig13.add_trace(
            go.Bar(
                x=filtered_df['지역명'],
                y=filtered_df['변화율'],
                name=f"{year} - {region}",
                visible=False,  # initially all traces are hidden
                customdata=[year] * len(filtered_df)
            )
        )

# Create buttons for interactivity
buttons = []

for i, year in enumerate(unique_years):
    visibility = [year == trace.customdata[0] for trace in fig13.data]
    buttons.append(
        dict(
            label=year,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{year}년 지역별 변화율"}]
        )
    )

# Apply updated button logic
fig13.update_layout(
    updatemenus=[{
        "buttons": buttons,
        "direction": "down",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "x": 0.1,
        "xanchor": "left",
        "y": 1.15,
        "yanchor": "top"
    }],
    title=f"{unique_years[0]}년 지역별 변화율"
)

# Set initial visibility based on the first year
initial_year = unique_years[0]
for trace in fig13.data:
    trace.visible = trace.customdata[0] == initial_year
###########################################################################
top_local_sales_cleaned['년'] = top_local_sales_cleaned['년'].astype(str)

fig14 = go.Figure()

# Create a list of unique years
unique_years = top_local_sales_cleaned['년'].unique()

# Add a bar for each year and business name, initially hidden
for year in unique_years:
    for region in top_local_sales_cleaned[top_local_sales_cleaned['년'] == year]['상호명'].unique():
        filtered_df = top_local_sales_cleaned[(top_local_sales_cleaned['년'] == year) & (top_local_sales_cleaned['상호명'] == region)]
        fig14.add_trace(
            go.Bar(
                x=[region],  # x-axis is the business name
                y=filtered_df['제주도민매출금액비율'],  # y-axis is the sales ratio
                name=region,
                visible=False,  # initially all traces are hidden
                customdata=[year] * len(filtered_df)
            )
        )

# Create buttons for interactivity
buttons = []

for i, year in enumerate(unique_years):
    visibility = [year == trace.customdata[0] for trace in fig14.data]
    buttons.append(
        dict(
            label=year,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{year}년 상호별 제주도민매출금액비율"}]
        )
    )

# Apply updated button logic
fig14.update_layout(
    updatemenus=[{
        "buttons": buttons,
        "direction": "down",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "x": 0.1,
        "xanchor": "left",
        "y": 1.15,
        "yanchor": "top"
    }],
    title=f"{unique_years[0]}년 상호별 제주도민매출금액비율"
)

# Set initial visibility based on the first year
initial_year = unique_years[0]
for trace in fig14.data:
    trace.visible = trace.customdata[0] == initial_year
#############################################################
top_foreign_sales_cleaned['년'] = top_foreign_sales_cleaned['년'].astype(str)

fig15 = go.Figure()

# Create a list of unique years
unique_years = top_foreign_sales_cleaned['년'].unique()

# Add a bar for each year and business name, initially hidden
for year in unique_years:
    for region in top_foreign_sales_cleaned[top_foreign_sales_cleaned['년'] == year]['상호명'].unique():
        filtered_df = top_foreign_sales_cleaned[(top_foreign_sales_cleaned['년'] == year) & (top_foreign_sales_cleaned['상호명'] == region)]
        fig15.add_trace(
            go.Bar(
                x=[region],  # x-axis is the business name
                y=filtered_df['외지인매출금액비율'],  # y-axis is the non-resident sales ratio
                name=region,
                visible=False,  # initially all traces are hidden
                customdata=[year] * len(filtered_df)
            )
        )

# Create buttons for interactivity
buttons = []

for i, year in enumerate(unique_years):
    visibility = [year == trace.customdata[0] for trace in fig15.data]
    buttons.append(
        dict(
            label=year,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"{year}년 상호별 외지인매출금액비율"}]
        )
    )

# Apply updated button logic
fig15.update_layout(
    updatemenus=[{
        "buttons": buttons,
        "direction": "down",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "x": 0.1,
        "xanchor": "left",
        "y": 1.15,
        "yanchor": "top"
    }],
    title=f"{unique_years[0]}년 상호별 외지인매출금액비율"
)

# Set initial visibility based on the first year
initial_year = unique_years[0]
for trace in fig15.data:
    trace.visible = trace.customdata[0] == initial_year
##############################################################
fig16 = px.scatter(sorted_grouped_df,
                 x="전체매출금액비율",
                 y="전체매출수비율",
                 animation_frame="지역명",
                 animation_group="소분류명",
                 size="전체매출금액비율",
                 color="소분류명",
                 hover_name="소분류명",
                 log_x=True,
                 log_y=True,
                 size_max=55,
                 range_x=[0.01, 12],
                 range_y=[0.005, 65])

# Remove animation play and pause buttons, as Streamlit does not support them directly
fig16["layout"].pop("updatemenus")
##################################################################
# Create figure
fig17 = go.Figure()

# Get unique categories from DataFrame
categories = time_df['중분류명'].unique()

# Add data for each category to the graph
for category in categories:
    category_df = time_df[time_df['중분류명'] == category]
    fig17.add_trace(go.Scatter(x=category_df['분석년월'], y=category_df['외지인매출금액비율'], name=category))

# Set the title
fig17.update_layout(title_text="식품별 소비량 변화")

# Add range slider
fig17.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)
##################################################3
Consumption_status_by_date_NH = pd.read_csv("Jeju/데이터/Consumption status by date_Jeju(2123).csv", parse_dates=['승인일자'], index_col='승인일자')
Consumption_status_by_date_NH['이용건수_전체'] = Consumption_status_by_date_NH['이용건수_전체'] * 1000
Consumption_status_by_date_NH['이용금액_전체'] = Consumption_status_by_date_NH['이용금액_전체'] * 1000000
Consumption_status_by_date_NH['이용건수_개인'] = Consumption_status_by_date_NH['이용금액_전체'] * 1000
Consumption_status_by_date_NH['이용금액_개인'] = Consumption_status_by_date_NH['이용금액_전체'] * 1000000
Consumption_status_by_date_NH['이용건수_법인'] = Consumption_status_by_date_NH['이용금액_전체'] * 1000
Consumption_status_by_date_NH['이용금액_법인'] = Consumption_status_by_date_NH['이용금액_전체'] * 1000000
####################################

#계절성 분석
# Assuming 'Consumption_status_by_date_NH' is pre-loaded with your data
consumption_data = Consumption_status_by_date_NH['이용금액_전체']

# Perform seasonal decomposition
result = seasonal_decompose(consumption_data, model='additive', period=365)

# Convert the seasonal component to a DataFrame and reset index to 'date'
seasonal_df = pd.DataFrame(result.seasonal).reset_index()
seasonal_df.columns = ['date', 'seasonal']  # Rename columns appropriately

# Visualize the seasonal component using Plotly Express
fig18 = px.line(seasonal_df, x='date', y='seasonal', title='Seasonal Component of Consumption',
              labels={'seasonal': 'Seasonality'}, template='plotly_dark')
############################################

#추세 분석
Consumption_status_by_date_NH['7_day_rolling_avg'] = Consumption_status_by_date_NH['이용금액_전체'].rolling(window=7).mean()
Consumption_status_by_date_NH['30_day_rolling_avg'] = Consumption_status_by_date_NH['이용금액_전체'].rolling(window=30).mean()

# Create a figure using Plotly graph objects
fig19 = go.Figure()

# Add traces for the original data and the rolling averages
fig19.add_trace(go.Scatter(x=Consumption_status_by_date_NH.index, y=Consumption_status_by_date_NH['이용금액_전체'], mode='lines', name='Original'))
fig19.add_trace(go.Scatter(x=Consumption_status_by_date_NH.index, y=Consumption_status_by_date_NH['7_day_rolling_avg'], mode='lines', name='7 Day Rolling Average'))
fig19.add_trace(go.Scatter(x=Consumption_status_by_date_NH.index, y=Consumption_status_by_date_NH['30_day_rolling_avg'], mode='lines', name='30 Day Rolling Average'))

# Update the layout of the figure
fig19.update_layout(
    title='Daily 이용금액_전체 with Rolling Average',
    xaxis_title='Date',
    yaxis_title='Consumption',
    template='plotly_dark'
)
#################################################
nlags = int(len(Consumption_status_by_date_NH) * 0.1) 
#정상성 분석
acf_values = acf(Consumption_status_by_date_NH['이용금액_전체'], fft=False, nlags=nlags)  # Ensure the column name is correct

# Create a list of lag values
lags = list(range(len(acf_values)))

# Create a Plotly figure
fig20 = go.Figure()
fig20.add_trace(go.Scatter(x=lags, y=acf_values, mode='lines+markers', name='ACF'))

# Update the layout of the figure
fig20.update_layout(
    title='Autocorrelation Function',
    xaxis_title='Lags',
    yaxis_title='ACF',
    template='plotly_dark'
)
######################################################

#노이즈 분석
rolling_window = 7  # For example, using 12 points for moving average was mentioned
Consumption_status_by_date_NH['smoothed'] = Consumption_status_by_date_NH['이용금액_전체'].rolling(window=rolling_window).mean()

# Create a Plotly figure
fig21 = go.Figure()

# Add trace for original data
fig21.add_trace(go.Scatter(
    x=Consumption_status_by_date_NH.index,  # Or you might use a 'Date' column if available
    y=Consumption_status_by_date_NH['이용금액_전체'],
    mode='lines',
    name='Original Data'
))

# Add trace for smoothed data
fig21.add_trace(go.Scatter(
    x=Consumption_status_by_date_NH.index,  # Or 'Date' column
    y=Consumption_status_by_date_NH['smoothed'],
    mode='lines',
    name='Smoothed Data',
    line=dict(color='red')
))

# Update the layout of the figure
fig21.update_layout(
    title='Time Series with Smoothing',
    xaxis_title='Time',
    yaxis_title='Value',
    template='plotly_dark'
)
###########################
combined_df = pd.read_csv("Jeju/데이터/종합맵.csv")

def create_map(df):
    # 제주도 중심 좌표
    jeju_center = [33.3617, 126.5292]
    map_jeju = folium.Map(location=jeju_center, zoom_start=10)

    # 분류에 따른 색상 지정
    marker_colors = {
        '반려견 동반 관광지': 'blue',
        '마을 관광자원': 'green',
        '안전여행 스탬프 관광지': 'red'
    }

    # 데이터프레임의 각 행에 대해 마커 추가
    for idx, row in df.iterrows():
        # 지정되지 않은 분류는 회색으로 표시
        icon_color = marker_colors.get(row['분류'], 'gray')
        popup_text = f"<strong>{row['관광지명']}</strong><br>{row['주소']}</strong><br>{row['관광지분류']}</strong><br>{row['관광지설명']}"
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=icon_color)
        ).add_to(map_jeju)

    return map_jeju
##############################

#모델링 시각화
pred_summary = pd.read_csv("Jeju/시각화/pred_summary.csv")
########################################
fig22 = go.Figure()

fig22.add_trace(go.Scatter(
    x=pred_summary.index,  # 이 부분은 실제 데이터의 인덱스를 사용해야 합니다.
    y=pred_summary['mean'],  # 실제 데이터의 평균 예측값
    mode='lines',
    name='Predicted Mean'
))

# 신뢰 구간을 채워진 영역으로 추가
fig22.add_trace(go.Scatter(
    x=pred_summary.index.tolist() + pred_summary.index[::-1].tolist(),
    y=pred_summary['mean_ci_lower'].tolist() + pred_summary['mean_ci_upper'][::-1].tolist(),
    fill='toself',
    fillcolor='rgba(0,100,80,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    name='Confidence Interval'
))

fig22.update_layout(
    title='6-Month Sales Forecast for Jeju',
    xaxis_title='Date',
    yaxis_title='Sales Amount',
    legend_title='Legend'
)
#############################################
Consumption_status_by_date_NH2 = pd.read_csv("Jeju/데이터/Consumption status by date_Jeju(2123).csv")
Consumption_status_by_date_NH2['ds'] = pd.to_datetime(Consumption_status_by_date_NH2['승인일자'], format='%Y%m%d')
Consumption_status_by_date_NH2['y'] = Consumption_status_by_date_NH2['이용금액_전체']
prophet_data = Consumption_status_by_date_NH2[['ds', 'y']]

def load_model():
    # 여기에 모델 피팅 코드
    model = Prophet()
    model.fit(prophet_data)
    return model

def make_forecast(model):
    future = model.make_future_dataframe(periods=180)
    forecast = model.predict(future)
    return forecast

model = load_model()
forecast = make_forecast(model)

# 예측 그래프 표시
fig23 = plot_plotly(model, forecast)

# 컴포넌트별 시각화
components_fig = plot_components_plotly(model, forecast)
################################
#마무리











# 페이지 및 섹션 정의
pages = [
    Page("개요", 
         """
         ### 프로젝트 목표
         - 목적 정의: 제주도 관광 데이터를 활용하여 관광객의 소비 패턴 분석, 인기 관광지 동향 파악 등의 분석을 진행.
         - 이해관계자: 제주도 관광청, 여행 사업자, 관광객 등
         
         ### 데이터 소스
         - 데이터 종류: 동반자 유형별 여행 데이터, 무장애 관광지 입장 데이터, 카드사 음식 결제 데이터, 일자별 소비현황 데이터, 맵 데이터 등
         - 데이터 수집 방법: 제주 관광공사, KDX 한국데이터거래소, 제주데이터허브
         
         ### 분석 구성
         - 관광 현황 분석, 키워드 분석, 소비현황 분석, 농협카드 매출 시계열 분석, 분류별 맵
         - 시간의 흐름에 따른 전세가와 여론 분석
         
         ### 사용할 도구와 기술
         - Pandas, plotly, folium, streamlit, SARIMAX, Prophet 등

         ### 향후 계획
         - 제주도 내의 호텔과 연관한 식당 추천 시스템, 추가적인 분석과 머신러닝 사용
         
         """
    ),
    Page("데이터 소개", 
         """
         ### 데이터 샘플 
         
         """,
         dfs=[df_1, df_2, df_3, df_4, df_5, df_6, df_7],
         df_titles=["제주 동반자 유형별 여행 계획 데이터2023", "제주 무장애 관광지 입장 데이터2023",
                    "SNS 제주 관광 키워드별 수집 통계_월(22~23)", "제주 관광수요예측 데이터_비짓제주 로그 데이터 월2023",
                    "제주관광공사 관광 소비행태 데이터 카드사 음식 급상승 데이터", "[NH농협카드] 일자별 소비현황_제주",
                    "제주도 맵 데이터(관광자원, 반려경 동반 관광지, 안전여행 스탬프 관광지)"]

    ),
    Page("관광 현황 - 동반자 유형별 분석", 
         """
         ### 동반자 유형에 따른 제주도 관광

         """,
         graphs=[fig1, fig2, fig3],
         graph_descriptions=[
             "2023년 동안 방문한 관광객의 동반자 유형을 분석한 결과, 1월부터 9월까지는 주로 가족 단위 관광객이 많았으며, 9월부터 12월까지는 친구와 함께 방문한 관광객이 더 많았습니다.",
             "키워드 분석 결과, 모든 유형의 관광객 사이에서 '휴식과 치유 여행'이 가장 인기 있는 키워드였습니다. 부모와 함께 여행한 관광객은 '식도락 여행'을 선호했고, 아이나 커플과 함께한 관광객은 '레저와 체험'을 즐겼습니다. 또한 친구와 함께하거나 혼자 방문한 관광객에게는 '천천히 걷기'가 다음으로 인기 있는 키워드였습니다.",
             "콘텐츠 분석 결과, 성산일출봉과 섭지코지는 대부분의 동반자 유형이 선호하는 콘텐츠였습니다. 친구와 함께한 관광객은 협재해수욕장을, 부모와 함께한 관광객은 쇠소깍을, 아이와 함께한 관광객은 아쿠아플라넷 제주를, 커플 관광객은 월정리해변을, 개인 관광객은 해양도립공원을 선호했습니다."
         ]
         
    ),
    Page("관광 현황 - 관광지 입장 분석", 
         """
         ### 무장애 관광지 입장 현황

         """,
         graphs=[fig4, fig5],
         graph_descriptions=[
             "천지연폭포의 경우, 1월부터 4월까지 관광객 수가 급증한 후, 그 이후로는 방문객 수가 현저히 감소하는 추세를 확인할 수 있습니다. 반면, 정방폭포와 천제연폭포는 이렇게 급격한 변동을 보이지 않습니다. 해안가 관광지는 입장인원 변동이 심한 편이며, 다른 관광지들은 대체로 비슷한 수준의 방문객을 유지하고 있습니다.",
             "경로, 유아, 장애인 방문객 모두 폭포를 가장 많이 방문한 것으로 확인되었습니다."
         ]
         
    ),    
    Page("키워드 - SNS 분석", 
         """
         ### SNS별 제주도관련 글 분석
         """,
         graphs=[fig6, fig7, fig8, fig9],
         graph_descriptions=[
             "성산일출봉이 눈에 띄게 많은 검색 수를 기록하고 있는 것을 확인할 수 있습니다.",
             "제주도 관련 글에서는 2022년 이후로 '산방산 맛집'이라는 키워드가 자주 등장하고 있습니다.",
             "SNS별로 검색어 차이는 존재하지만, 성산일출봉은 여전히 눈에 띄는 검색량을 기록하고 있습니다.",
             "네이버 블로그에서는 '맛집' 키워드가 인기를 끌었고, 인스타그램에서는 관광지에 대한 언급이 많았습니다. 트위터에서는 '렌트카' 관련 키워드가 두드러졌으며, 페이스북에서는 인기 있는 지역을 찾는 사용자가 많았습니다."
         ]
    ),
    
    Page("키워드 - 검색량 분석", 
         """
         ### 제주도 검색어 분석
         """,
         graphs=[fig10, fig11],
         graph_descriptions=[
             "계절에 따라 약간의 차이는 있지만, 사려니숲길, 성산일출봉, 비자림, 우도는 일관되게 높은 검색량을 기록하고 있는 것을 확인할 수 있습니다.",
             "각 분류별로 인기 있는 장소도 확인할 수 있습니다.",
         ]
    ),        
    
    Page("신한카드 - 음식 소비행태 분석",
         """
         ### 음식 소비행태 분석
         # 
         #
         """,
         graphs=[fig12, fig13, fig14, fig15, fig16, fig17],
         graph_descriptions=[
             "안덕면, 애월읍, 조천읍에서 가장 큰 매출을 기록하고 있으며, 시간이 지남에 따라 서귀포 시내와 제주 시내의 매출이 상승하고 있습니다.",
             "안덕면, 조천읍, 애월읍에서 큰 변화를 보이고 있으며, 제주 시내의 변화율도 점차 증가하고 있습니다.",
             "제주도민에서는 돼지고기 관련 매출이 눈에 띄게 높은 것을 확인할 수 있습니다.",
             "외지인들은 다양한 식당에서의 소비가 확인되고 있습니다.",
             "지역별 현황을 확인할 수 있습니다.",
             "대부분의 분류에서 관광객의 소비는 2023년 4월부터 8월까지 급감했으나, 8월부터 11월까지는 상승세를 보이다가 그 이후 다시 하락하는 추세입니다."
         ]         
    ),
    Page("농협카드 - 일자별 소비현황 데이터 확인", 
         """
         ## 계절성, 추세, 정상성, 노이즈 분석
         """,
         graphs=[fig18, fig19, fig20, fig21],
         graph_descriptions=[
             "이 선 그래프는 seasonal_decompose를 통해 추출된 시계열 데이터의 계절성 구성요소를 보여줍니다. 정기적인 간격으로 반복되는 패턴이 뚜렷이 나타나 계절성이 명확히 확인됩니다.",
             "이동 평균을 활용한 그래프 분석 결과, 점차 상승하는 추세가 확인됩니다.",
             "정상성 분석 결과 이상은 없습니다.",
             "노이즈 분석의 결과에서도 큰 문제는 없습니다.",
         ]
         
    ),
    Page("농협카드 - 시계열 모델링", 
         """
         ## 시계열 모델을 활용한 제주도 매출현황 파악
         """,
         graphs=[fig22, fig23, components_fig],
         graph_descriptions=[
             "예측 평균 매출액은 비교적 안정된 패턴을 보이며, 그 크기는 시간이 지남에 따라 점차 감소하는 경향이 보입니다. 이는 예측 기간 동안 제주도의 매출액이 안정적이긴 하지만, 약간의 하락 추세를 보일 수 있음을 나타냅니다. 신뢰 구간은 상대적으로 넓어, 실제 매출액이 예측된 평균값 주변에서 상당한 범위 내에서 변동할 수 있음을 나타냅니다.",
             "전반적으로 매출 트렌드는 시간이 지남에 따라 안정적으로 증가하는 경향을 보입니다.",
             "상단 그래프('trend')는 시간이 지남에 따라 변화하는 매출의 전반적인 경향을 보여줍니다. 이 그래프를 통해 매출이 시간에 따라 어떻게 변화하는지를 확인할 수 있습니다. 중간 그래프('yearly')는 연간 계절성을 나타냅니다. 이는 한 해 동안의 특정 시기(예: 관광 성수기)에 매출이 어떻게 변화하는지를 보여줍니다. 하단 그래프('weekly')는 주간 계절성을 나타냅니다. 이는 일주일 중 특정 요일에 매출이 어떻게 달라지는지를 보여줍니다."  
         ]     
    ), 
    Page("분류별 추천 관광지", 
         """
         ## 마을 광광자원, 반려견 동반 관광지, 안전여행 스탬프
         """,
         graphs=[create_map(combined_df)]
    ),
    Page("향후 계획", 
         """
         ## 호텔 데이터를 이용한 군집분석, 식당 추천 시스템 추가 예정
         """
    ),
]

# 페이지 제목 추가
add_page_title()

# 왼쪽 사이드바에 페이지 목록 추가
selected_page = st.sidebar.radio("목차", [page.title for page in pages])

# 선택된 페이지로 이동
for page in pages:
    if page.title == selected_page:
        show_pages([page])


