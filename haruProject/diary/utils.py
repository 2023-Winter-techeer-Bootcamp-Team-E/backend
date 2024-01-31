import boto3
from collections import Counter
import requests
from celery.app import task

from .tasks import generate_sticker_image, remove_background
from celery import group
from celery import signature


def extract_top_keywords(diary_text):
    import time
    from datetime import time as datetime_time
    start_time = time.time()

    comprehend_client = boto3.client('comprehend', region_name='ap-northeast-2')

    cleaned_text = preprocess_diary_text(diary_text)
    response = comprehend_client.detect_key_phrases(
        Text=cleaned_text,
        LanguageCode='ko'
    )

    keywords = [phrase['Text'] for phrase in response['KeyPhrases']]
    stopwords = get_korean_stopwords()
    filtered_keywords = [keyword for keyword in keywords if keyword not in stopwords]
    keyword_counts = Counter(filtered_keywords)
    top_keywords = keyword_counts.most_common(2)

    end_time = time.time()

    execution_time = end_time - start_time
    print(execution_time)

    return [keyword[0] for keyword in top_keywords]


def preprocess_diary_text(diary_text):
    cleaned_text = ''.join(char for char in diary_text if char.isalnum() or char.isspace())
    return cleaned_text


def get_korean_stopwords():
    stopwords = [

        "민준", "서준", "도윤", "예준", "시우", "하준", "지호", "주원", "지후", "준우",
        "준서", "도현", "건우", "현우", "우진", "지훈", "선우", "유준", "서진", "연우",
        "은우", "민재", "현준", "시윤", "정우", "이준", "윤우", "승우", "지우", "지환",
        "승현", "유찬", "준혁", "수호", "승민", "시후", "진우", "민성", "수현", "준영",
        "지원", "이안", "재윤", "시현", "한결", "태윤", "지안", "동현", "윤호", "시원",
        "은찬", "시온", "민우", "재원", "민규", "지한", "서우", "은호", "재민", "민찬",
        "우주", "우빈", "하율", "준호", "율", "지율", "하진", "성민", "승준", "성현",
        "재현", "현서", "민호", "태민", "준", "지민", "예성", "지성", "윤재", "태현",
        "민혁", "로운", "하람", "하민", "규민", "성준", "윤성", "정민", "태양", "이현",
        "은성", "예찬", "준수", "도훈", "준희", "다온", "민석", "주안", "건", "도하", "송혜교", "전지현", "김태리", "김지원", "김하늘", "김혜수", "김유정",
        "이나영", "한지민", "박보영",
        "신민아", "한효주", "이성경", "전혜빈", "서현진", "이영애", "문근영", "박신혜", "김고은", "공효진",
        "김소현", "이성경", "김지원", "전혜진", "김희선", "유인나", "유리", "한예슬", "김향기", "조여정",
        "김민희", "이솜", "김소연", "이지아", "임수정", "강소라", "한가인", "이유리", "문채원", "김현주",
        "신세경", "남지현", "박민영", "신혜선", "김지혜", "배두나", "손예진", "김아중", "한지혜", "임윤아",
        "박해수", "임수향", "강예원", "김지영", "이성경", "신하균", "조정석", "이병헌", "하정우", "손석구",
        "손예진", "강동원", "이정재", "공유", "현빈", "이병헌", "김래원", "이민호", "차승원", "김남길",
        "정우성", "이선균", "김수현", "조인성", "송강호", "현빈", "조승우", "조진웅", "하정우", "곽도원",
        "유아인", "마동석", "강하늘", "황정민", "박서준", "박보검", "손현주", "김유정", "남주혁", "윤계상", "한가은", "이하늬", "한소희", "김지안", "오나라", "박신혜",
        "손예진", "김태리", "이지은", "이하늬",
        "조보아", "임주은", "이승연", "전소민", "김다미", "박나래", "김성령", "진세연", "강부자", "윤승아",
        "김세정", "강지영", "임지연", "윤승아", "이가은", "김슬기", "송현아", "전효성", "김애란", "문규리",
        "고아라", "신민아", "김혜자", "문채원", "이성경", "김태희", "김새론", "류현경", "신은경", "이새론",
        "진세연", "한지은", "김해숙", "배수지", "나연", "플로라", "오연서", "설지현", "예린", "아이린",
        "서현", "장나라", "정채연", "하선영", "조유리", "김소희", "배윤정", "강미나", "박민하", "노아",
        "김보라", "박지윤", "조이", "김유진", "이민정", "이민영", "최수영", "하슬라", "하슬라", "황선화",
        "송지효", "신봉선", "강은비", "채수빈", "설현", "박세리", "유승호", "김민재", "송중기", "이준기", "가", "가까스로", "가령", "각", "각각", "각자", "각종",
        "갖고말하자면", "같다", "같이", "개의치않고", "거니와",
        "거바", "거의", "것", "것과 같이", "것들", "게다가", "게우다", "겨우", "견지에서", "결과에 이르다", "결국", "결론을 낼 수 있다",
        "겸사겸사", "고려하면", "고로", "곧", "공동으로", "과", "과연", "관계가 있다", "관계없이", "관련이 있다", "관하여", "관한", "관해서는",
        "구", "구체적으로", "구토하다", "그", "그들", "그때", "그래", "그래도", "그래서", "그러나", "그러니", "그러니까", "그러므로",
        "그러한즉", "그런 까닭에", "그런데", "그런즉", "그럼", "그럼에도 불구하고", "그렇게 함으로써", "그렇지", "그렇지 않다면", "그렇지 않으면",
        "그렇지만", "그렇지않으면", "그리고", "그리하여", "그만이다", "그에 따르는", "그위에", "그저", "그중에서", "그치지 않다", "근거로",
        "근거하여", "기대여", "기점으로", "기준으로", "기타", "까닭으로", "까악", "까지", "까지 미치다", "까지도", "꽈당", "끙끙", "끼익",
        "나", "나머지는", "남들", "남짓", "너", "너희", "너희들", "네", "넷", "년", "논하지 않다", "놀라다", "누가 알겠는가", "누구", "다른",
        "다른 방면으로", "다만", "다섯", "다소", "다수", "다시 말하자자면", "다시말하면", "다음", "다음에", "다음으로", "단지", "답다", "당신",
        "당장", "대로 하다", "대하면", "대하여", "대해 말하자면", "대해서", "댕그", "더구나", "더군다나", "더라도", "더불어", "더욱더", "더욱이는",
        "도달하다", "도착하다", "동시에", "동안", "된바에야", "된이상", "두번째로", "둘", "둥둥", "뒤따라", "뒤이어", "든간에", "들", "등",
        "등등", "딩동", "따라", "따라서", "따위", "따지지 않다", "딱", "때", "때가 되어", "때문에", "또", "또한", "뚝뚝", "라 해도", "령",
        "로", "로 인하여", "로부터", "로써", "륙", "를", "마음대로", "마저", "마저도", "마치", "막론하고", "만 못하다", "만약", "만약에", "만은 아니다",
        "만이 아니다", "만일", "만큼", "말하자면", "말할것도 없고", "매", "매번", "메쓰겁다", "몇", "모", "모두", "무렵", "가량", "가지", "각", "간", "갖은",
        "개", "개국", "개년", "개소", "개월", "걔", "거", "거기", "일찍",
        "거리", "건", "것", "겨를", "격", "겸", "고", "군", "군데", "권", "그", "그거", "그것", "그곳",
        "그까짓", "그네", "그녀", "그놈", "그대", "그래", "그래도", "그서", "그러나", "그러니", "그러니까",
        "그러다가", "그러면", "그러면서", "그러므로", "그러자", "그런", "그런데", "그럼", "그렇지만", "그루",
        "그리고", "그리하여", "그분", "그이", "그쪽", "근", "근데", "글쎄", "글쎄요", "기", "김", "나",
        "나름", "나위", "남짓", "내", "냥", "너", "너희", "네", "네놈", "녀석", "년", "년대", "년도", "놈",
        "누구", "니", "다른", "다만", "단", "달", "달러", "당신", "대", "대로", "더구나", "더욱이", "데", "도",
        "동", "되", "두", "두세", "두어", "둥", "듯", "듯이", "등", "등등", "등지", "따라서", "따름", "따위",
        "딴", "때문", "또", "또는", "또한", "리", "마당", "마련", "마리", "만", "만큼", "말", "매", "맨", "명",
        "몇", "몇몇", "모", "모금", "모든", "무렵", "무슨", "무엇", "뭐", "뭣", "미터", "및", "바", "바람", "바퀴",
        "박", "발", "발짝", "번", "벌", "법", "별", "본", "부", "분", "뻔", "뿐", "살", "새", "서너", "석", "설",
        "섬", "세", "세기", "셈", "쇤네", "수", "순", "스무", "승", "시", "시간", "식", "씨", "아", "아냐", "아니",
        "아니야", "아무", "아무개", "아무런", "아아", "아이", "아이고", "아이구", "야", "약", "양", "얘", "어", "어느",
        "어디", "어머", "언제", "에이", "엔", "여기", "여느", "여러", "여러분", "여보", "여보세요", "여지", "역시", "예",
        "옛", "오", "오랜", "오히려", "온", "온갖", "올", "왜냐하면", "왠", "외", "요", "우리", "원", "월", "웬", "위",
        "음", "응", "이", "이거", "이것", "이곳", "이놈", "이래", "이런", "이런저런", "이른바", "이리하여", "이쪽", "일",
        "일대", "임마", "자", "자기", "자네", "장", "저", "저것", "저기", "저놈", "저런", "저쪽", "저편", "저희", "적",
        "전", "점", "제", "조", "주", "주년", "주일", "줄", "중", "즈음", "즉", "지", "지경", "지난", "집", "짝", "쪽",
        "쯤", "차", "참", "채", "척", "첫", "체", "초", "총", "측", "치", "큰", "킬로미터", "타", "터", "턱", "톤",
        "통", "투", "판", "퍼센트", "편", "평", "푼", "하기야", "하긴", "하물며", "하지만", "한", "한두", "한편", "허허",
        "헌", "현", "호", "혹은", "회", "흥", "아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희",
        "따라", "의해", "을", "를", "에", "의", "가", "으로", "로", "에게",
        "뿐이다", "의거하여", "근거하여", "입각하여", "기준으로", "예하면", "예를 들면",
        "예를 들자면", "저", "소인", "소생", "저희", "지말고", "하지마", "하지마라",
        "다른", "물론", "또한", "그리고", "비길수", "없다", "해서는", "안된다", "뿐만 아니라",
        "만이", "아니다", "만은", "아니면", "만 못하다", "하는 편이", "낫다", "불문하고",
        "향하여", "향해서", "향하다", "쪽으로", "틈타", "이용하여", "타다", "오르다", "제외하고",
        "이 외에", "이 밖에", "하여야", "비로소", "한다면", "몰라도", "외에도", "이곳", "여기",
        "부터", "기점으로", "따라서", "할 생각이다", "하려고하다", "이리하여", "그리하여", "그렇게",
        "함으로써", "하지만", "일때", "할때", "앞에서", "중에서", "보는데서", "으로써", "로써",
        "까지", "해야한다", "일것이다", "반드시", "할줄알다", "할수있다", "할수있어", "임에",
        "틀림없다", "한다면", "등", "등등", "제", "겨우", "단지", "다만", "할뿐", "딩동",
        "댕그", "대해서", "대하여", "대하면", "훨씬", "얼마나", "얼마만큼", "얼마큼", "남짓",
        "여", "얼마간", "약간", "다소", "좀", "조금", "다수", "몇", "얼마", "지만", "하물며",
        "또한", "그렇지만", "하지만", "이외에도", "대해", "말하자면", "뿐이다", "다음에", "반대로",
        "반대로", "말하자면", "이와", "반대로", "바꾸어서", "말하면", "바꾸어서", "한다면", "만약",
        "그렇지않으면", "까악", "툭", "딱", "삐걱거리다", "보드득", "비걱거리다", "꽈당", "응당",
        "해야한다", "에", "가서", "각", "각각", "여러분", "각종", "각자", "제각기", "하도록하다",
        "와", "과", "그러므로", "그래서", "고로", "한", "까닭에", "하기", "때문에", "거니와",
        "이지만", "대하여", "관하여", "관한", "과연", "실로", "아니나다를가", "생각한대로",
        "진짜로", "한적이있다", "하곤하였다", "하", "하하", "허허", "아하", "거바", "와", "오",
        "왜", "어째서", "무엇때문에", "어찌", "하겠는가", "무슨", "어디", "어느곳", "더군다나",
        "하물며", "더욱이는", "어느때", "언제", "야", "이봐", "어이", "여보시오", "흐흐", "흥",
        "휴", "헉헉", "헐떡헐떡", "영차", "여차", "어기여차", "끙끙", "아야", "앗", "아야",
        "콸콸", "조유리 직캠", "게다가", "더구나", "하물며", "와르르", "팍", "퍽", "펄렁", "동안", "이래", "하고있었다",
        "이었다", "에서", "로부터", "까지", "예하면", "했어요", "해요", "함께", "같이", "더불어",
        "마저", "마저도", "양자", "모두", "습니다", "가까스로", "하려고하다", "즈음하여", "다른",
        "다른", "방면으로", "해봐요", "습니까", "했어요", "말할것도", "없고", "무릎쓰고", "개의치않고",
        "하는것만", "못하다", "하는것이", "낫다", "매", "매번", "들", "모", "어느것", "어느", "로써",
        "갖고말하자면", "어디", "어느쪽", "어느것", "어느해", "어느", "년도", "라", "해도", "언젠가",
        "어떤것", "어느것", "저기", "저쪽", "저것", "그때", "그럼", "그때", "저것만큼", "그저", "이르기까지",
        "할", "줄", "안다", "할", "힘이", "있다", "너", "너희", "당신", "어찌", "설마", "차라리", "할지언정",
        "할지라도", "할망정", "할지언정", "구토하다", "게우다", "토하다", "메쓰겁다", "옆사람", "퉤", "쳇",
        "의거하여", "근거하여", "의해", "따라", "힘입어", "그", "다음", "버금", "두번째로", "기타", "첫번째로",
        "나머지는", "그중에서", "견지에서", "형식으로", "쓰여", "입장에서", "위해서", "당연히", "일반적으로",
        "일단", "한", "일", "일반적으로", "일단", "한켠으로는", "오자마자", "이렇게되면", "이와같다면", "전부", "한마디", "한항목", "근거로",
        "하기에", "아울러", "하지", "않도록", "않기", "위해서", "이르기까지", "이", "되다", "로", "인하여",
        "까닭으로", "이유만으로", "이로", "인하여", "그래서", "이", "때문에", "그러므로", "그런", "까닭에",
        "알", "수", "있다", "결론을", "낼", "수", "있다", "으로", "인하여", "있다", "어떤것", "관계가", "있다",
        "관련이", "있다", "연관되다", "어떤것들", "에", "대해", "이리하여", "그리하여", "여부", "하기보다는",
        "하느니", "하면", "할수록", "운운", "이러이러하다", "하구나", "하도다", "다시말하면", "다음으로", "에",
        "있다", "에", "달려", "있다", "우리", "우리들", "오히려", "하기는한데", "어떻게", "어떻해", "어찌됏어",
        "어때", "어째서", "본대로", "자", "이", "이쪽", "여기", "이것", "이번", "이렇게말하자면", "이런", "이러한",
        "이와", "같은", "요만큼", "요만한", "것", "얼마", "안", "되는", "것", "이만큼", "이", "정도의", "이렇게",
        "많은", "것", "이와", "같다", "이", "때", "이렇", "구나", "것과", "같이", "끼익", "삐걱", "따위", "와",
        "같은", "사람들", "부류의", "사람들", "왜냐하면", "중의하나", "오직", "오로지", "에", "한하다", "하기만", "하면", "도착하다", "까지", "미치다", "도달하다",
        "정도에", "이르다",
        "할", "지경이다", "결과에", "이르다", "관해서는", "여러분", "하고", "있다", "한", "후", "혼자", "자기", "자기집",
        "자신", "우에", "종합한것과같이", "총적으로", "보면", "총적으로", "말하면", "총적으로", "대로", "하다", "으로서", "참",
        "그만이다", "할", "따름이다", "쿵", "탕탕", "쾅쾅", "둥둥", "봐", "봐라", "아이야", "아니", "와아", "응", "아이",
        "참나", "년", "월", "일", "령", "영", "일", "이", "삼", "사", "오", "육", "륙", "칠", "팔", "구",
        "이천육", "이천칠", "이천팔", "이천구", "하나", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉", "령",
        "영", "이", "있", "하", "것", "들", "그", "되", "수", "이", "보", "않", "없", "나", "사람",
        "주", "아니", "등", "같", "우리", "때", "년", "가", "한", "지", "대하", "오", "말", "일", "그렇",
        "위하", "때문", "그것", "두", "말하", "알", "그러나", "받", "못하", "일", "그러", "또", "문제", "더",
        "사회", "많", "그리고", "좋", "크", "따르", "중", "나오", "가지", "씨", "시키", "만들", "지금", "생각하",
        "그러", "속", "하나", "집", "살", "모르", "적", "월", "데", "자신", "안", "어떤", "내", "내", "경우",
        "명", "생각", "시간", "그녀", "다시", "이런", "앞", "보이", "번", "나", "다른", "어떻", "여자", "개", "전",
        "들", "사실", "이렇", "점", "싶", "말", "정도", "좀", "원", "잘", "통하", "놓", "새로운", "그러나", "그리고", "그런데", "그래서", "따라서", "하지만",
        "또", "또는",
        "그러므로", "및", "또한", "그러면", "즉", "그럼", "그러니까", "그렇지만",
        "오히려", "역시", "그리하여", "다만", "혹은", "그래도", "한편", "이른바",
        "더구나", "왜냐하면", "근데", "그러자", "더욱이", "하긴", "하기야", "그",
        "러면서", "하물며", "그러니", "그러다가", "단", "이리하여", "그", "이", "한", "두", "다른", "그런", "이런", "어떤", "모든", "어느",
        "몇", "여러", "무슨", "세", "전", "저", "각", "첫", "새", "아무",
        "약", "네", "아무런", "총", "제", "온", "옛", "오랜", "단", "올",
        "온갖", "별", "현", "한두", "맨", "양", "몇몇", "수", "딴", "서너",
        "저런", "두어", "모", "주", "석", "스무", "여느", "이런저런", "본",
        "동", "웬", "헌", "순", "왠", "요", "두세", "지난", "근", "타",
        "그까짓", "매", "고", "갖은", "일대", "것", "수", "등", "년", "때문", "일", "중", "월", "씨", "데",
        "번", "명", "원", "개", "거", "가지", "뿐", "듯", "간", "쪽",
        "분", "시", "채", "만", "대", "년대", "줄", "놈", "적", "터",
        "만큼", "바", "측", "내", "편", "차", "자", "세", "대로", "점",
        "달러", "살", "초", "식", "외", "셈", "듯이", "지", "회", "장",
        "호", "개월", "말", "따위", "리", "마리", "위", "녀석", "평",
        "무렵", "나름", "마련", "권", "척", "양", "법", "이", "바람",
        "쯤", "건", "판", "지경", "도", "달", "군", "조", "주일", "뻔",
        "시간", "부", "이래", "등등", "주", "개국", "푼", "군데", "체",
        "거리", "년도", "따름", "주년", "격", "등지", "통", "겸", "설",
        "참", "둥", "퍼센트", "남짓", "미터", "기", "나위", "즈음", "년", "월", "일", "시간", "분", "초", "요일",
        "달력", "시간대", "저녁", "아침", "밤", "오전", "오후",
        "기간", "주", "월말", "월초", "계절", "윤년", "년", "월", "일", "시간", "분", "초", "요일",
        "달력", "시간대", "저녁", "아침", "밤", "오전", "오후",
        "기간", "주", "월말", "월초", "계절", "윤년",
        "시간 차이", "시간 측정", "기간 계산", "기간 비교", "달력 이벤트",
        "연도별", "월별", "일별", "주간", "분기", "시즌",
        "날짜 관련 용어",
        "내일", "일주일", "한달", "내일 모레", "글피",
        "오늘", "어제", "내일 모레", "내일 내일", "그제",
        "오늘은", "내일은",
        "몇일 후", "몇주 후", "몇달 후", "몇년 후", "몇일 전",
        "몇주 전", "몇달 전", "몇년 전", "지난주", "이번주",
        "다음주", "지난달", "이번달", "다음달", "작년",
        "내년", "새해", "설날", "추석", "연말",
        "종강", "졸업", "휴일", "월", "화", "수", "목", "금", "토", "일"
                                                        "휴일 여행", "워크샵", "업무일정", "프로젝트 마감", "데드라인",
        "출장", "휴가 신청", "휴가 계획", "워라벨", "연차",
        "오후반차", "오전반차", "반차", "초과근무", "야근",
        "주말근무", "휴가일수", "반휴", "일한 시간", "퇴근",
        "출근", "휴가 종류", "근태 관리", "근무일정", "출퇴근 시간",
        "가동일", "휴무일", "휴일 근무", "주기적 휴가", "국경일",
        "공휴일", "방학", "휴가 신청서", "일정 계획", "기간별 일정",
        "시간 차이", "시간 측정", "기간 계산", "기간 비교", "달력 이벤트",
        "연도별", "월별", "일별", "주간", "분기", "시즌",
        "날짜 형식", "날짜 변환", "날짜 입력", "날짜 출력", "윤년 판단",
        "포맷", "타임존", "UTC", "GMT", "DST", "타임 스탬프",
        "현재 날짜", "현재 시간", "지난 날짜", "미래 날짜", "날짜 조작",
        "날짜 비교", "날짜 검증", "날짜 차이", "날짜 더하기", "날짜 빼기",
        "날짜 포맷팅", "날짜 파싱", "날짜 표현", "날짜 표기", "날짜 표현식",
        "날짜 시스템", "날짜 함수", "날짜 라이브러리", "날짜 모듈", "날짜 관련 패키지",
        "ISO 날짜", "RFC 3339", "날짜 데이터", "날짜 저장", "날짜 처리",
        "달력 표시", "일정 관리", "시간 관리", "이벤트 일정", "날짜 주석",
        "일정 표시", "마감일", "기간 지정", "일정 변경", "일정 알림",
        "반복 일정", "일정 정렬", "날짜 정렬", "날짜 분류", "일정 플래너",
        "시간표", "일정 계획", "기간 예약", "날짜 예약", "일정 등록",
        "마감 기한", "일정 통합", "날짜 통합", "일정 확인", "일정 편집",
        "달력 편집", "시간 편집", "날짜 편집", "일정 관리 도구", "날짜 정보",
        "일정 앱", "일정 서비스", "날짜 알리미", "달력 앱", "달력 도구",
        "마당", "바퀴", "여지", "치", "벌", "그루", "박", "투", "승",
        "김", "가량", "큰술", "엔", "모금", "발짝", "석", "겨를", "전",
        "개소", "동", "톤", "개년", "한", "짝", "킬로미터", "나", "그", "우리", "이", "그것", "그녀", "내", "자기", "무엇",
        "이것", "누구", "저", "여기", "어디", "너", "뭐", "당신", "거기",
        "이곳", "그곳", "제", "아무", "네", "자네", "언제", "여러분", "이거",
        "너희", "니", "저희", "아무개", "이놈", "그놈", "저기", "그분", "그대",
        "그거", "모", "저쪽", "뭣", "저것", "그이", "이쪽", "그쪽", "지", "친구", "친구들",
        "엄마랑",  "엄마", "아빠랑", "아빠", "가족들", "가족", "할머니", "할아버지",
        "사촌동생", "사촌", "동생", "이미지", "월요일인 오늘", "화요일인 오늘", "수요일인 오늘",
        "목요일인 오늘", "금요일인 오늘", "토요일인 오늘", "일요일인 오늘", "주말이라", "주말", "주말에",
        "얘", "걔", "저편", "저놈", "네놈", "그네", "쇤네", "아니", "이", '지우', '민준', '서윤', '서준', '서연', '민준', '도윤', '지우', '서준', '예준',
        '서현', '서연', '시우', '하윤', '도윤', '하준', '하은', '민서', '하윤', '지후',
        '윤서', '연우', '준우', '채원', '서현', '준서', '지민', '지안', '하은', '선우',
        '지안', '하은', '예준', '건우', '지윤', '지민', '지안', '예은', '서진', '서아',
        '지후', '은우', '예린', '윤서', '지유', '현준', '하린', '채원', '이준', '수아',
        '지환', '윤아', '은호', '현서', '하린', '민우', '예원', '시아', '시은', '수연',
        '다인', '아윤', '서우', '예진', '민지', '주아', '지온', '가은', '아린', '시아',
        '시후', '서영', '하율', '나은', '주아', '민혁', '예지', '승아', '채아', '소은',
        '나연', '사랑', '지은', '시현', '예빈', '은채', '세아', '다윤', '소연', '지현',
        '주하', '지수', '승아', '채린', '혜원', '소민', '하영', '다온', '아영', '민아',
        '서희', '세은', '나현', '아현', '가윤', '지연', '민채', '김지우', '김서윤', '김민준', '김서준', '김서연', '김도윤', '김하윤', '김하은',
        '김도윤', '김하준', '김민서', '김하윤', '김연우', '김서현', '김주원', '김지호',
        '김하윤', '김지후', '김연우', '김서진', '김지유', '김채원', '김준서', '김준우',
        '김도현', '김지윤', '김수아', '김은우', '김선우', '김현우', '김지아', '김건우',
        '김우진', '김시윤', '김수현', '김하율', '김서우', '김은서', '김지훈', '김다은',
        '김수빈', '김예은', '김소율', '김시현', '김서아', '김지안', '김은찬', '김태윤',
        '김은호', '김우주', '김하율', '김정우', '김승현', '김지한', '김동현', '김은찬',
        '김로운', '김태민', '김예성', '김태현', '김윤재', '김주안', '김건', '김주호', '김서은', '이지우', '이서윤', '이민준', '이서준', '이서연', '이도윤', '이하윤',
        '이하은', "하다", "있다", "되다", "가다", "오다", "말하다", "보다", "알다",
        "쓰다", "들다", "갖다", "나가다", "들어가다", "앉다", "일어나다", "자다",
        "사랑하다", "먹다", "마시다", "생각하다", "들리다", "보이다", "좋아하다", "싫어하다",
        "받다", "주다", "웃다", "울다", "놀다", "일하다", "공부하다", "만나다",
        "기다리다", "약속하다", "찾다", "차다", "키우다", "닦다", "씻다", "입다",
        "걷다", "달리다", "뛰다", "쏘다", "쓰러지다", "일어나다", "타다", "내리다",
        "지나가다", "걸다", "끼다", "붙이다", "빼다", "돌리다", "닫다", "열다",
        "가리다", "보호하다", "지키다", "방어하다", "이기다", "지다", "지르다", "울리다",
        "안내하다", "알려주다", "도와주다", "이끌다", "따르다", "설명하다", "알려주다", "물어보다",
        "대화하다", "의논하다", "추천하다", "제안하다", "발표하다", "논의하다", "좋아지다", "나빠지다",
        "바뀌다", "만들다", "크다", "작다", "느리다", "빠르다", "높다", "낮다",
        "덥다", "춥다", "화나다", "슬프다", "놀랍다", "지루하다", "재미있다", "즐겁다",
        "힘들다", "쉽다", "많다", "적다", "맛있다", "맛없다", "아프다", "건강하다",
        "이상하다", "정상이다", "멋지다", "심심하다", "두렵다", "설레다", "부끄럽다", "자랑스럽다",
        "기쁘다", "슬프다", "화나다", "무섭다", "부럽다", "화나다", "차갑다", "뜨겁다",
        '이도윤', '이하준', '이민서', '이하윤', '이연우', '이서현', '이주원', '이지호',
        '이하윤', '이지후', '이연우', '이서진', '이지유', '이채원', '이준서', '이준우',
        '이도현', '이지윤', '이수아', '이은우', '이선우', '이현우', '이지아', '이건우',
        '이우진', '이시윤', '이수현', '이하율', '이서우', '이은서', '이지훈', '이다은',
        '이수빈', '이예은', '이소율', '이시현', '이서아', '이지안', '이은찬', '이태윤',
        '이은호', '이우주', '이하율', '이정우', '이승현', '이지한', '이동현', '이은찬',
        '이로운', '이태민', '이예성', '이태현', '이윤재', '이주안', '이건', '이주호', '이서은', '박지우', '박서윤', '박민준', '박서준', '박서연', '박도윤', '박하윤',
        '박하은', "오늘", "내일",
        '박도윤', '박하준', '박민서', '박하윤', '박연우', '박서현', '박주원', '박지호',
        '박하윤', '박지후', '박연우', '박서진', '박지유', '박채원', '박준서', '박준우',
        '박도현', '박지윤', '박수아', '박은우', '박선우', '박현우', '박지아', '박건우',
        '박우진', '박시윤', '박수현', '박하율', '박서우', '박은서', '박지훈', '박다은',
        '박수빈', '박예은', '박소율', '박시현', '박서아', '박지안', '박은찬', '박태윤',
        '박은호', '박우주', '박하율', '박정우', '박승현', '박지한', '박동현', '박은찬',
        '박로운', '박태민', '박예성', '박태현', '박윤재', '박주안', '박건', '박주호', '박서은', '촤지우', '촤서윤', '촤민준', '촤서준', '촤서연', '촤도윤', '촤하윤',
        '촤하은', "예정", "게",
        '촤도윤', '촤하준', '촤민서', '촤하윤', '촤연우', '촤서현', '촤주원', '촤지호',
        '촤하윤', '촤지후', '촤연우', '촤서진', '촤지유', '촤채원', '촤준서', '촤준우',
        '촤도현', '촤지윤', '촤수아', '촤은우', '촤선우', '촤현우', '촤지아', '촤건우',
        '촤우진', '촤시윤', '촤수현', '촤하율', '촤서우', '촤은서', '촤지훈', '촤다은',
        '촤수빈', '촤예은', '촤소율', '촤시현', '촤서아', '촤지안', '촤은찬', '촤태윤',
        '촤은호', '촤우주', '촤하율', '촤정우', '촤승현', '촤지한', '촤동현', '촤은찬',
        '촤로운', '촤태민', '촤예성', '촤태현', '촤윤재', '촤주안', '촤건', '촤주호', '촤서은', "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시",
        "대전광역시",
        "울산광역시", "세종특별자치시", "경기도", "강원도", "충청북도", "충청남도",
        "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도", "서울", "부산", "대구", "인천", "광주", "대전",
        "울산", "수원", "인천", "성남", "부천", "안양",
        "청주", "천안", "전주", "포항", "창원", "광명",
        "김해", "화성", "성남", "용인", "고양", "안산", "춘천", "원주", "강릉", "동해", "태백", "속초",
        "삼척", "홍천", "횡성", "영월", "평창", "정선", "청주", "충주", "제천", "보은", "옥천", "영동",
        "증평", "진천", "괴산", "음성", "천안", "공주", "보령", "아산", "서산", "논산",
        "계룡", "당진", "금산", "부여", "전주", "익산", "군산", "정읍", "김제", "남원",
        "완주", "진안", "무주", "장수", "임실", "목포", "여수", "순천", "나주", "광양", "담양",
        "곡성", "구례", "고흥", "보성", "화순", "포항", "경주", "김천", "안동", "구미", "영주",
        "영천", "상주", "문경", "경산", "군위", "창원", "진주", "통영", "사천", "김해", "밀양",
        "거제", "양산", "의령", "함안", "창녕", "서귀포시", "남제주군", "북제주군", "오조리", "영흥도", "매화도", "간월도", "이안도", "간월도",
        "성북도", "간도", "도두리", "광도", "거진도", "궁포도",
        "구도", "다대도", "덕곶도", "덕진도", "덕진도", "덕포도",
        "도개도", "독곶도", "동구도", "동도", "동봉도", "동성도",
        "동안도", "동황도", "두류도", "마도", "목포도", "문도",
        "바닷가도", "백석도", "버드나무도", "불하도", "비야도", "빙화도",
        "삼봉도", "생화도", "서강도", "선화도", "섬진도", "성화도",
        "수로도", "숭의도", "승도", "신도", "신화도", "실지도",
        "아미도", "아모도", "야놀자도", "애월도", "여수도", "영화도",
        "오룡도", "요동도", "용고도", "용진도", "용화도", "월래도",
        "위리도", "육지도", "율포도", "읍내도", "읍신도", "의령도",
        "이매도", "인공도", "인덕도", "인생도", "자도", "자린도",
        "자성도", "장고도", "장도", "장화도", "제기도", "제주도",
        "조남도", "조선도", "조약도", "조정도", "조화도", "주문도",
        "죽도", "중앙도", "중포도", "지도", "진도", "진하도",
        "척도", "천산도", "천황도", "청소도", "초당도", "초리도",
        "칠성도", "탄도", "탄도", "토암도", "팔선도", "평화도",
        "풍도", "한도", "해마도", "해미도", "해신도", "행안도",
        "향동도", "향포도", "협재도", "호가도", "화관도", "화천도",
        "효도", "강화도", "옹진도", "대모산도", "자월도", "송도", "연안부두도",
        "연평도", "소연평도", "만리포도", "도라도", "문촌도", "삼도",
        "백령도", "마안도", "봉평도", "달도", "원도", "다도",
        "영종도", "용유도", "무의도", "석모도", "소무의도", "실미도",
        "대이작도", "용오름", "예봉도", "안강도", "죽도", "화도",
        "도래지", "교동도", "말미도", "장봉도", "파도도", "봉포도",
        "당진도", "갑선도", "북도", "화순도", "새서리", "고래도", "완도", "진도", "여수", "강화도", "해남", "무안",
        "신안", "장흥", "진도", "고흥", "보성", "장흥",
        "남해", "화순", "순천", "목포", "신안", "해남",
        "나주", "곡성", "광양", "영광", "장성", "담양", "곶자왈도", "돌고도", "동도", "매도", "매화도", "명도",
        "백석도", "보리도", "사어도", "사령도", "서도", "송악도",
        "신도", "실화도", "야도", "양도", "어청도", "연화도",
        "외도", "운의도", "원도", "원해도", "월포도", "이어도",
        "이오도", "이추도", "임도", "장도", "장봉도", "장안도",
        "적도", "전도", "절도", "제먼도", "조도", "죽도",
        "지도", "차도", "창도", "청도", "칠도", "타도",
        "탄도", "태도", "평택도", "표도", "학동도", "학의도",
        "한도", "해미도", "해안도", "현도", "홍도", "화도",
        "화순도", "횡도", "거문도", "고사리도", "고작도", "고창", "금포도", "나도",
        "낙도", "노도", "담도", "대전도", "덕도", "도리도",
        "동외도", "둘내도", "땅끝도", "란도", "러도", "마도",
        "매화도", "면도", "목포", "무봉도", "미음도", "민도",
        "백령도", "백석도", "별도", "보도", "보리도", "보성",
        "봉도", "봉동도", "봉화도", "부도", "불완도", "비다리도",
        "산도", "새포도", "선의도", "섬진도", "성산도", "성의도",
        "세도", "소두도", "소이도", "솔미도", "수도", "숙도",
        "승도", "시도", "신안", "실미도", "심도", "아대도",
        "안마도", "양도", "양마도", "양촌도", "여경도", "연화도",
        "영광", "영순도", "영월도", "영해도", "영흥도", "외도",
        "용화도", "우선도", "우숙도", "월선도", "유건도", "유민도",
        "이도", "이로도", "이매도", "인근도", "임진도", "자야도",
        "자린도", "자방도", "자세도", "작도", "장도", "장터도",
        "장흥", "적도", "전도", "정도", "조도", "종도",
        "주전도", "지도", "진도", "창도", "창선도", "창포도",
        "청산도", "청도", "초도", "초도", "추도", "추자도",
        "추자도", "축도", "춘도", "치도", "칠도", "태도",
        "포도", "포도", "포도도", "푸라도", "하도", "한도",
        "해도", "해마도", "해양도", "향포도", "향화도", "허도",
        "호도", "호미도", "홍도", "화순", "화이도", "효도", "수원시", "성남시", "용인시", "안양시", "부천시", "화성시",
        "안산시", "평택시", "의정부시", "시흥시", "파주시", "김포시",
        "광명시", "광주시", "이천시", "양주시", "오산시", "구리시",
        "남양주시", "의왕시", "하남시", "용인시", "안성시", "양평군",
        "여주시", "가평군", "연천군", "포천시", "수원", "성남", "용인", "안양", "부천", "화성",
        "안산", "평택", "의정부", "시흥", "파주", "김포",
        "광명", "광주", "이천", "양주", "오산", "구리",
        "남양주", "의왕", "하남", "용인", "안성", "양평",
        "여주", "가평", "연천", "포천", "최근", "일본"

]
    return stopwords




def generate_sticker_image_wrapper(keyword):
    # 키워드를 리스트로 감싸서 apply_async에 전달
    result = generate_sticker_image.apply_async(args=[keyword])
    return keyword, result



def remove_background_wrapper(result):
    keyword, task_result = result
    image_data = requests.get(task_result.get()).content
    output_data = remove_background.apply_async(args=[image_data]).get()
    return keyword, output_data


def generate_sticker_images(keywords):
    sticker_image_urls = {}

    # generate_sticker_image 함수를 순차적으로 호출하여 이미지 생성
    for keyword in keywords:
        generated_image_url = generate_sticker_image(keyword)
        response = requests.get(generated_image_url)
        image_data = response.content

        # remove_background 함수를 호출하여 배경 제거
        processed_image_data = remove_background(image_data)

        sticker_image_urls[keyword] = processed_image_data

    return sticker_image_urls

