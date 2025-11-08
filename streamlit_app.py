import streamlit as st
import random
import re

st.set_page_config(page_title="문자와 식 문제 생성기", layout="centered")

st.title("📘 중1-1학기 문자와 식 문제 생성기")
st.write("문제 유형을 고르고 문제 수를 정한 뒤 '문제 생성'을 누르세요. 정답을 입력하고 '채점'으로 정답을 확인할 수 있습니다.")

def int_from_str(s):
    m = re.search(r"-?\d+", str(s))
    return int(m.group()) if m else None

def gen_value_problem():
    a = random.randint(-5, 10)
    b = random.randint(-10, 10)
    x = random.randint(-5, 10)
    expr = f"{a}x"
    if b > 0:
        expr += f" + {b}"
    elif b < 0:
        expr += f" - {abs(b)}"
    # 깔끔한 표현: 1x -> x, -1x -> -x
    expr = expr.replace(" 1x", " x").replace("-1x", "-x")
    question = f"{expr}에서 x = {x}일 때 식의 값은?"
    answer = a * x + b
    return question, answer

def gen_simplify_problem():
    # 생성: 여러 항을 합쳐 계수만 묻기 (예: 2x + 3x - x = ?x)
    terms = []
    total = 0
    n_terms = random.randint(2,4)
    for _ in range(n_terms):
        coeff = random.randint(-5, 8)
        # 피항이 0이면 건너뛰기
        if coeff == 0:
            coeff = random.choice([1, -1])
        terms.append(coeff)
        total += coeff
    # 표현 만들기
    expr_parts = []
    for c in terms:
        if c == 1:
            expr_parts.append("x")
        elif c == -1:
            expr_parts.append("-x")
        elif c > 0:
            expr_parts.append(f"{c}x")
        else:
            expr_parts.append(f"({c})x" if c < -9 else f"{c}x")
    expr = " + ".join(expr_parts).replace("+ -", "- ")
    question = f"{expr}을(를) 간단히 하시오. (결과를 예: 4x 혹은 4 로 입력 가능)"
    answer = total  # 의미: total x
    return question, answer

def gen_solve_problem():
    # ax + b = c 형태, 해가 정수인 문제 생성
    a = random.choice([i for i in range(-9,10) if i not in (0,)])
    x = random.randint(-8, 8)
    b = random.randint(-10, 10)
    c = a * x + b
    # 표현 정리
    left = f"{a}x"
    if b > 0:
        left += f" + {b}"
    elif b < 0:
        left += f" - {abs(b)}"
    left = left.replace(" 1x", " x").replace("-1x", "-x")
    question = f"{left} = {c} 를 풀어라. (x = ?)"
    answer = x
    return question, answer

GEN_FUNCS = {
    "값 구하기 (대입)": gen_value_problem,
    "식 간단히 하기 (동류항 정리)": gen_simplify_problem,
    "일차방정식 풀기 (기본)": gen_solve_problem,
}

with st.sidebar:
    st.header("설정")
    kind = st.selectbox("문제 유형", list(GEN_FUNCS.keys()))
    count = st.slider("문제 수", min_value=1, max_value=10, value=5)
    if st.button("문제 생성"):
        problems = []
        for _ in range(count):
            q, a = GEN_FUNCS[kind]()
            problems.append({"q": q, "a": a, "user": ""})
        st.session_state["problems"] = problems

if "problems" not in st.session_state:
    # 초기 문제 자동 생성
    problems = []
    for _ in range(5):
        q, a = gen_value_problem()
        problems.append({"q": q, "a": a, "user": ""})
    st.session_state["problems"] = problems

st.subheader("문제")
for i, p in enumerate(st.session_state["problems"], start=1):
    st.markdown(f"**{i}. {p['q']}**")
    key = f"ans_{i}"
    user_in = st.text_input("정답 입력", value=p.get("user", ""), key=key)
    p["user"] = user_in

if st.button("채점"):
    correct = 0
    results = []
    for p in st.session_state["problems"]:
        user = p.get("user", "")
        user_int = int_from_str(user)
        # 정답 비교: simplify 문제는 계수 정답(정수), 다른 유형도 정수
        expected = p["a"]
        ok = (user_int is not None) and (user_int == expected)
        results.append((p["q"], expected, user, ok))
        if ok:
            correct += 1
    st.success(f"채점 완료 — 정답 {correct} / {len(results)}")
    st.markdown("정답 상세:")
    for idx, (q, exp, usr, ok) in enumerate(results, start=1):
        status = "✅" if ok else "❌"
        st.write(f"{idx}. {q}  → 정답: {exp}  입력: {usr}  {status}")

st.write("")
st.caption("문제 유형과 개수를 바꾼 뒤 '문제 생성'을 눌러 다른 문제를 만들어 보세요.")
