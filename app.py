import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent

@st.cache_resource
def get_connection():
    # 메모리 DB 생성
    conn = duckdb.connect(database=":memory:")

    # CSV -> 테이블 생성
    conn.execute("""
        CREATE TABLE Customer AS
        SELECT * FROM read_csv_auto(?, header=True)
    """, [str(BASE_DIR / "Customer_madang.csv")])

    conn.execute("""
        CREATE TABLE Book AS
        SELECT * FROM read_csv_auto(?, header=True)
    """, [str(BASE_DIR / "Book_madang.csv")])

    conn.execute("""
        CREATE TABLE Orders AS
        SELECT * FROM read_csv_auto(?, header=True)
    """, [str(BASE_DIR / "Orders_madang.csv")])

    return conn

conn = get_connection()

# =========================
# 검색 UI
# =========================
st.title("Madang DB 검색")
st.markdown("### 검색")

tables = ["Customer", "Book", "Orders"]
table = st.selectbox("테이블 선택", tables)

condition = st.text_input("WHERE 조건 (예: name = '박지성' OR price > 10000)", "")

query = f"SELECT * FROM {table}"
if condition.strip():
    query += f" WHERE {condition}"

st.code(query, language="sql")

if st.button("검색 실행"):
    try:
        df = conn.execute(query).df()
        if df.empty:
            st.warning("결과가 없습니다.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"SQL 오류: {e}")

# =========================
# 새 고객 추가 UI
# =========================
st.markdown("---")
st.markdown("### 새 고객 추가")

new_name = st.text_input("이름", key="new_name")
new_address = st.text_input("주소", key="new_address")
new_phone = st.text_input("전화번호", key="new_phone")

if st.button("고객 추가"):
    try:
        new_id = conn.execute(
            "SELECT COALESCE(MAX(custid) + 1, 1) FROM Customer"
        ).fetchone()[0]

        conn.execute(
            "INSERT INTO Customer VALUES (?, ?, ?, ?)",
            (new_id, new_name, new_address, new_phone)
        )

        st.success(f"고객 추가됨! (custid={new_id}, 이름={new_name})")
    except Exception as e:
        st.error(f"고객 추가 중 오류: {e}")
