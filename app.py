import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 0. 页面基础配置 ---
st.set_page_config(
    page_title="Dreamy Ledger Fixed",
    page_icon="🍬",
    layout="wide",
)

# --- 1. 核心样式层：强制覆盖暗黑模式，实现梦幻输入框 ---
def inject_custom_css():
    st.markdown("""
        <style>
        /* 1. 全局强制浅色背景 */
        .stApp {
            background-color: #FFFFFF;
        }

        /* 2. 核心修复：输入框标签 (Label) 颜色 */
        /* 强制所有输入框头顶的文字变成深蓝黑，不再隐身 */
        .stMarkdown p, .stMarkdown label, .stSelectbox label, .stNumberInput label, .stDateInput label, .stTextInput label {
            color: #2c3e50 !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }

        /* 3. 核心修复：输入框本体 (Input Box) */
        /* 针对 Streamlit 的所有输入组件进行深度定制 */
        
        /* 文本框、数字框、日期框、选择框的外壳 */
        div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="base-input"] {
            background-color: #ffffff !important; /* 强制白底 */
            border: 2px solid #e0c3fc !important; /* 梦幻紫边框 */
            border-radius: 15px !important;       /* 大圆角 */
            color: #2c3e50 !important;            /* 输入的字变成深色 */
            box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
        }

        /* 修复输入框内的文字颜色 (防止白字) */
        input, .stSelectbox div[data-baseweb="select"] div {
            color: #2c3e50 !important; 
            -webkit-text-fill-color: #2c3e50 !important;
            caret-color: #d57eeb !important; /* 光标颜色也变成紫色 */
        }
        
        /* 修复日期选择器的具体样式 */
        div[data-baseweb="calendar"] {
            background-color: white !important;
        }

        /* 4. 按钮美化：马卡龙渐变 */
        .stButton > button {
            background-image: linear-gradient(to right, #a18cd1 0%, #fbc2eb 100%);
            color: white !important;
            border: none;
            border-radius: 20px;
            font-weight: bold;
            height: 50px; /* 让按钮厚实一点 */
            width: 100%;
        }
        .stButton > button:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }

        /* 5. 标题与卡片样式 */
        .gradient-text {
            background: linear-gradient(45deg, #ff9a9e 0%, #ff6b6b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 3rem;
        }
        
        /* 隐藏 Streamlit 默认元素 */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* 图表容器 */
        .chart-container {
            border: 1px solid #f0f0f0;
            border-radius: 20px;
            padding: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.03);
        }
        
        /* 马卡龙卡片样式 */
        .macaron-card {
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            background-color: #ffffff; /* 卡片白底 */
        }
        
        /* 卡片文字颜色 */
        .card-title { color: #666666 !important; font-weight: 700; font-size: 0.9rem; margin-bottom: 5px; }
        .card-value { color: #2c3e50 !important; font-weight: 800; font-size: 2.2rem; }
        
        /* 具体的渐变边框装饰 */
        .style-pink { border-left: 6px solid #ff9a9e; background: linear-gradient(to right, #fff0f0, #ffffff); }
        .style-blue { border-left: 6px solid #a18cd1; background: linear-gradient(to right, #f3f0ff, #ffffff); }
        .style-purple { border-left: 6px solid #84fab0; background: linear-gradient(to right, #f0fff4, #ffffff); }

        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- 2. 配色方案 ---
MACARON_PALETTE = ['#FFB7B2', '#B5EAD7', '#C7CEEA', '#E2F0CB', '#FFDAC1', '#FF9AA2']

# --- 3. 数据逻辑 (保持不变) ---
DATA_FILE = 'ledger.csv'

def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["日期", "类别", "金额", "备注", "类型"])
        df.to_csv(DATA_FILE, index=False)
        return df
    df = pd.read_csv(DATA_FILE)
    df['日期'] = pd.to_datetime(df['日期'])
    return df

def save_transaction(date, category, amount, note, trans_type):
    df = load_data()
    new_data = pd.DataFrame({
        "日期": [pd.to_datetime(date)],
        "类别": [category],
        "金额": [amount],
        "备注": [note],
        "类型": [trans_type]
    })
    df = pd.concat([new_data, df], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- 4. 核心 UI 组件 ---

# A. 标题区
st.markdown('<div class="gradient-text" style="text-align: center; margin-bottom: 10px;">Macaron Ledger</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #888; margin-bottom: 40px;">清晰 · 柔和 · 记账</div>', unsafe_allow_html=True)

# B. 记账交互区
with st.container():
    # 这里的Expander背景我们不做特殊处理，让它融入白色，通过输入框的边框来提神
    with st.expander("➕ 点击展开：记一笔 (New Entry)", expanded=True): # 默认展开方便你看效果
        with st.form("accounting_form", clear_on_submit=True):
            st.markdown("#### 📝 新增记录")
            
            c1, c2, c3, c4 = st.columns([2, 2, 2, 3])
            with c1:
                # 这里的label颜色已经被CSS强制改为深蓝黑 #2c3e50
                amount = st.number_input("金额 (¥)", min_value=0.01, step=10.0)
            with c2:
                category = st.selectbox("类别", ["餐饮", "购物", "交通", "居住", "娱乐", "学习", "其他"])
            with c3:
                trans_type = st.selectbox("类型", ["支出", "收入"])
            with c4:
                date = st.date_input("日期", datetime.now())
            
            note = st.text_input("备注", placeholder="例如：周末和朋友聚餐...")
            
            st.write("") # 加一点间距
            submitted = st.form_submit_button("✨ 确认保存")
            
            if submitted:
                save_transaction(date, category, amount, note, trans_type)
                st.success("记录成功！")
                st.rerun()

# C. 数据处理
df = load_data()

if not df.empty:
    current_month = datetime.now().month
    current_year = datetime.now().year
    mask_month = (df['日期'].dt.month == current_month) & (df['日期'].dt.year == current_year) & (df['类型'] == '支出')
    month_df = df[mask_month]
    
    total_month = month_df['金额'].sum()
    budget = 5000
    remaining = budget - total_month
    
    # D. 指标卡
    st.markdown("### 📅 Monthly Overview")
    col1, col2, col3 = st.columns(3)
    
    def gradient_card(style_class, title, value, sub_text):
        return f"""
        <div class="macaron-card {style_class}">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
            <div style="color: #999; font-size: 0.8rem; margin-top:5px;">{sub_text}</div>
        </div>
        """
    
    with col1:
        st.markdown(gradient_card("style-pink", "本月支出", f"¥{total_month:,.0f}", "Total Expenses"), unsafe_allow_html=True)
    with col2:
        st.markdown(gradient_card("style-blue", "剩余预算", f"¥{remaining:,.0f}", "Remaining Budget"), unsafe_allow_html=True)
    with col3:
        percent = min(int((total_month / budget) * 100), 100)
        st.markdown(gradient_card("style-purple", "预算进度", f"{percent}%", "Budget Usage"), unsafe_allow_html=True)

    # E. 图表区
    st.markdown("### 🎨 Visual Analysis")
    chart_c1, chart_c2 = st.columns([3, 2])
    
    with chart_c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.caption("每日趋势")
        if not month_df.empty:
            daily_trend = month_df.groupby('日期')['金额'].sum().reset_index()
            fig_trend = px.area(daily_trend, x='日期', y='金额')
            fig_trend.update_traces(
                line_color='#a18cd1', 
                fillcolor='rgba(161, 140, 209, 0.3)'
            )
            fig_trend.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                margin=dict(l=0, r=0, t=10, b=0),
                height=280
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("暂无数据")
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.caption("支出占比")
        if not month_df.empty:
            cat_group = month_df.groupby('类别')['金额'].sum().reset_index()
            fig_pie = px.pie(
                cat_group, values='金额', names='类别', 
                color_discrete_sequence=MACARON_PALETTE,
                hole=0.6
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(l=0, r=0, t=10, b=0),
                height=280,
                annotations=[dict(text='支出', x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#555")]
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("暂无数据")
        st.markdown('</div>', unsafe_allow_html=True)

    # F. 列表
    st.markdown("### 📝 Recent Transactions")
    st.dataframe(
        df.sort_values("日期", ascending=False).head(5),
        use_container_width=True,
        hide_index=True,
        column_config={
            "日期": st.column_config.DateColumn(format="YYYY-MM-DD"),
            "金额": st.column_config.NumberColumn(format="¥%.2f"),
        }
    )

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👋 你的纯白账本已就绪，请点击上方 '➕' 开始记录。")