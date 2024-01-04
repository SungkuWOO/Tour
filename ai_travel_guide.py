
import openai
import streamlit as st
from openai import OpenAI
import os

st.markdown("<h1 style='text-align: left;'><b>AI_여행가이드</b></h1>", unsafe_allow_html=True)
#st.title(" AI_여행가이드")
#st.markdown("❤ 여행 가슴 설레고 너무나 멋지지 않나요 ❤")
st.markdown("<h4 style='text-align: left;'><i><font color=brown>🗽🏰 앗싸, AI가 여행 스케줄까지 💒🗽</font></i></h4>", unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.image("C:/Users/PC2307/PycharmProjects/pythonProject1/ai_tour/data/tour.png", width=450)
#client = OpenAI(api_key=st.secrets["api_key"])
def request_chat_completion(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 전문 여행 가이드 입니다."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    return response
def print_streaming_response(response):
    message = ""
    placeholder = st.empty()
    for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            message += delta.content
            placeholder.markdown(message + "▌")
    placeholder.markdown(message)
def generate_prompt(여행지역, 여행형태, 여행일수, max_line, keywords):
    prompt = f"""
    나는 {여행지역}지역으로 여행을 떠나고 싶어요.
    멋진 곳을 한 곳을 추천해 주세요.
    여행형태는 {여행형태} 이고요, 여행일수는 {여행일수}일 동안 다녀올 예정입니다.
    {max_line}줄 이내로 먼저 간결하게 여행지 자랑을 해 주세요.
    키워드가 주어질 경우, {keywords}가 있으면  포함시켰으면 좋겠네요.
    세부일정이 꼭 필요합니다.
    "일자별 세부일정"을 잡아서 반드시 일자별로 다음 줄부터 꼭 이모지를 넣어서 보기좋게 작성해 주세요.
    마지막으로 정확한 여행경비도 알려주세요(왕복항공료도 포함해 주세요)   
    해외 여행지역의 경우 여행지역의 이미지에 대한 url을 나타내면 금상첨화(해당사항이 없으면 표시하지 말것)
    ---
    여행지역: {여행지역}
    여행형태: {여행형태}
    여행일수: {여행일수}
    키워드: {keywords}
    ---
    """.strip()
    return prompt

# CSS를 사용하여 라디오 버튼을 가로로 배치하기
st.markdown(
    """
    <style>
        div.row-widget.stRadio > div{flex-direction:row;}
    </style>
    """,
    unsafe_allow_html=True
)

# 사용자에게 입력받을 여행 정보
여행지_옵션 = ['동남아','서남아','동유럽','서유럽','북유럽','북미','남미','국내여행','지중해','아프리카','남태평양','남극','달나라']
여행지역 = st.radio('🚋 여행 희망지역을 선택하세요.', 여행지_옵션)

# st.columns를 사용해 가로로 체크박스 배치

여행형태=[]
여행형태_1 = st.radio('🚋 여행의 유형을 선택 하세요.', ('자유', '패키지', '신혼','효도'))

st.write(" ")
여행형태_2 = st.radio('🚋 누구랑 여행 가세요?', ('나홀로', '친구', '가족', '애인'))
여행형태.append(여행형태_1)
여행형태.append(여행형태_2)

from datetime import datetime, timedelta

# 여행 시작일과 종료일을 선택
#start_date = st.date_input('일행일정: 여행 출발일을 선택하세요.', datetime.today())
#end_date = st.date_input('여행 종료일을 선택하세요.', datetime.today())
# 컬럼 두 개 생성하여 나란히 배치
col1, col2 = st.columns(2)
with col1:
    # 첫 번째 컬럼에 여행 시작일 선택기 배치
    start_date = st.date_input('🔜여행 시작일', datetime.today() + timedelta(days=3))
with col2:
    # 두 번째 컬럼에 여행 종료일 선택기 배치
    end_date = st.date_input('🔚여행 종료일', start_date + timedelta(days=2))

# 시작일과 종료일 사이의 일수를 계산
if start_date <= end_date:
    # 여행 일수 계산
    여행일수 = (end_date - start_date).days
    st.write(f"✔ 선택하신 여행 기간은 총 {여행일수}일 입니다.")
else:
    st.error("종료일이 시작일 보다 빠르군요! 다시 선택해 주세요.")

auto_complete = st.toggle(label="예시확인버튼 🌐키워드 입력은 선택사항 입니다. 예: 특정국가, 유적지, 바다 등")
with st.form("form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        ex_keyword1 = "계곡"
        name1 = st.text_input(
            label="여행 키워드 1",
            value=ex_keyword1 if auto_complete else "",
            placeholder=ex_keyword1
        )
    with col2:
        ex_keyword2 = "호수"
        name2 = st.text_input(
            label="여행 키워드 2",
            value=ex_keyword2 if auto_complete else "",
            placeholder=ex_keyword2
        )

    with col3:
        ex_keyword3 = ""
        name3 = st.text_input(
            label="여행 키워드 3",
           # value=ex_keyword3 if auto_complete else "",
           # placeholder=ex_keyword3
        )
    keywords = []
    if name1 == name2:
        name2 = ''
    if name2 == name3:
        name3 = ''
    if name1 == name3:
        name3 = ''

    keywords.append(name1)
    keywords.append(name2)
    keywords.append(name3)
    if keywords == '' or keywords == " ":
        st.write("1개 이상 키워드 입력을 추천 합니다!!")

    submitted = st.form_submit_button("입력한 여행 키워드 확인(엔터)")
    if submitted:
        st.write('키워드: ' + ', '.join(keywords[:3]))
       #st.write('키워드:', keywords[0],',',keywords[1],',',keywords[2])
    #st.write("✳✳✳✳✳✳✳✳✳✳✳✳✳✳✳")

# 입력받은 데이터 확인
if st.button('👌여기를 꾹 눌러서 여행 계획서를 확인 하세요'):
    st.write('여행지역:', 여행지역)
    st.write('여행형태:' + ', '.join(여행형태[:2]))
    st.write('여행일수:', 여행일수, '일  ', '🟧🟨🟩🟦🟫🔷🔹🔸 아래를 확인해 보세요◽▪▫▫▫ ')


    prompt = generate_prompt(
        여행지역 = 여행지역,
        여행형태 = 여행형태,
        여행일수 = 여행일수,
        max_line = 3,
        keywords= keywords
    )
    response = request_chat_completion(prompt)
    print_streaming_response(response)
    st.write("🟧🟨🟩🟦🟫🟧🟨🟩🟦🟫")
    st.write("🧡💛💚여행계획서가 마음에 드셨나요?")