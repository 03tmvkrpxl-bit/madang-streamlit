import streamlit as st
import duckdb
import pandas as pd

# --------------------
# DB 연결 (캐싱)
# --------------------
@st.cache_resource
def get_connection():
    return duckdb.connect("madang.db")

conn = get_connection()

# --------------------
# UI 구성
# --------------------
st.title(" Madang  DB 검색")
st.markdown("### 검색")

# 테이블 선택
tables = ["Customer", "Book", "Orders"]
table = st.selectbox("테이블 선택", tables)

# WHERE 조건 입력
condition = st.text_input("WHERE 조건 (예: custid = 1 OR price > 10000)", "")

# SQL 만들기
query = f"SELECT * FROM {table}"
if condition.strip():
    query += f" WHERE {condition}"

st.code(query, language="sql")

# 실행 버튼
if st.button("검색 실행"):
    try:
        df = conn.execute(query).df()
        if df.empty:
            st.warning(" 결과가 없습니다.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f" SQL 오류: {e}")
