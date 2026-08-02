import os
import json
import random
from utils import get_valid_input

def get_valid_string(prompt_text):
    """빈칸을 허용하지 않는 문자열 입력 유틸리티 (퀴즈 추가 시 사용)"""
    while True:
        text = input(prompt_text).strip()
        if not text:
            print("⚠️ 빈 칸을 입력할 수 없습니다. 다시 입력해주세요.")
            continue
        return text

class Quiz:
    def __init__(self, question, choices, answer, hint="힌트가 제공되지 않았습니다."):
        """
        question: str (퀴즈 문제 내용)
        choices: list (4지선다 선택지 텍스트 리스트)
        answer: int (1~4 사이의 정답 번호)
        hint: str (힌트 내용)
        """
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def to_dict(self):
        """JSON 데이터 저장을 위해 객체를 딕셔너리로 변환하는 메서드"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 다시 Quiz 객체로 복원하는 클래스 메서드 (기존 데이터 호환을 위해 get 사용)"""
        return cls(
            data["question"], 
            data["choices"], 
            data["answer"], 
            data.get("hint", "힌트가 없습니다.")
        )

def get_default_python_quizzes():
    """초기 데이터가 없을 때 사용할 파이썬 기초 및 객체지향(OOP) 기본 퀴즈 5개를 반환합니다."""
    return [
        Quiz(
            question="파이썬에서 객체를 생성하기 위한 '틀' 또는 '설계도'를 뜻하는 키워드는?",
            choices=["class", "function", "method", "instance"],
            answer=1,
            hint="건물을 지을 때 사용하는 청사진(설계도)을 영어로 생각해보세요."
        ),
        Quiz(
            question="클래스 내부의 메서드에서, 생성된 객체 자신(현재 인스턴스)을 가리키기 위해 첫 번째 매개변수에 관례적으로 붙이는 이름은?",
            choices=["this", "me", "self", "cls"],
            answer=3,
            hint="영어로 '나 자신'을 뜻하는 단어입니다."
        ),
        Quiz(
            question="설계도(클래스)를 바탕으로 실제 메모리에 생성되어 사용할 수 있게 된 실체를 무엇이라고 하나요?",
            choices=["모듈 (Module)", "인스턴스 (Instance / 객체)", "패키지 (Package)", "속성 (Attribute)"],
            answer=2,
            hint="클래스라는 틀에서 찍어낸 구체적인 실체(메모리에 올라간 상태)를 의미하는 단어입니다."
        ),
        Quiz(
            question="객체가 생성된 직후 자동으로 호출되어 초기값을 설정해주는 초기화 메서드의 이름은?",
            choices=["__init__", "__start__", "__main__", "__class__"],
            answer=1,
            hint="'초기화'를 뜻하는 initialization의 약자를 앞뒤 언더바 두 개(__)와 함께 씁니다."
        ),
        Quiz(
            question="외부의 파이썬 파일(모듈)에 있는 클래스나 함수를 현재 파일로 가져오기 위해 사용하는 키워드는?",
            choices=["include", "require", "export", "import"],
            answer=4,
            hint="'수입하다, 외부에서 들여오다'라는 뜻의 영단어입니다."
        )
    ]


class QuizGame:
    STATE_FILE = "state.json"

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        """state.json 파일에서 데이터를 불러옵니다."""
        if not os.path.exists(self.STATE_FILE):
            print("\n📂 저장된 데이터가 없습니다. 기본 파이썬 기초 퀴즈 데이터를 불러옵니다.")
            self.quizzes = get_default_python_quizzes()
            self.best_score = 0
            return
            
        try:
            with open(self.STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            print(f"\n📂 저장된 데이터를 성공적으로 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
            
        except (json.JSONDecodeError, Exception):
            print("\n⚠️ 데이터 파일이 손상되었습니다. 기본 데이터를 불러옵니다.")
            self.quizzes = get_default_python_quizzes()
            self.best_score = 0

    def save_data(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장합니다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        try:
            with open(self.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n⚠️ 데이터 저장 중 오류가 발생했습니다: {e}")

    def play_quiz(self):
        """퀴즈 출제 및 채점 로직"""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다! 2번 메뉴를 통해 퀴즈를 추가해주세요.")
            return

        max_q = len(self.quizzes)
        print(f"\n총 {max_q}개의 퀴즈가 준비되어 있습니다.")
        num_to_play = get_valid_input(f"몇 문제를 푸시겠습니까? (1-{max_q}): ", 1, max_q)

        print(f"\n📝 퀴즈를 시작합니다! (선택한 {num_to_play}문제 출제)")
        score = 0
        
        # 보너스 과제 1 & 2: 지정된 개수만큼 랜덤으로 문제 뽑기
        play_list = random.sample(self.quizzes, num_to_play)
        
        for i, quiz in enumerate(play_list, 1):
            print("\n----------------------------------------")
            print(f"[문제 {i}]")
            print(quiz.question, "\n")
            
            for idx, choice_text in enumerate(quiz.choices, 1):
                print(f"  {idx}. {choice_text}")
            print()
            
            while True:
                # 0번을 힌트 기능으로 사용 (0~4 범위 허용)
                user_answer = get_valid_input("정답 번호 입력 (0 누르면 힌트 보기): ", 0, 4)
                
                if user_answer == 0:
                    if score >= 1:
                        score -= 1
                        print(f"\n💡 [힌트] {quiz.hint}")
                        print(f"📉 힌트 사용으로 1점이 차감되었습니다. (현재 점수: {score}점)\n")
                    else:
                        print("\n⚠️ 힌트를 보려면 최소 1점 이상의 점수(맞춘 문제 수)가 필요합니다!\n")
                else:
                    # 정답 체크 로직
                    if user_answer == quiz.answer:
                        print("✅ 정답입니다!")
                        score += 1
                    else:
                        print(f"❌ 오답입니다! (정답은 {quiz.answer}번)")
                    
                    # 퀴즈 하나를 풀었으므로 while 루프 탈출
                    break
                
        print("\n========================================")
        print(f"🏆 결과: {num_to_play}문제 중 {score}문제 정답!")
        print("========================================")
        
        if score > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = score
            self.save_data()

    def add_quiz(self):
        """새로운 퀴즈 추가 기능"""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = get_valid_string("문제를 입력하세요: ")
        
        choices = []
        for i in range(1, 5):
            choice_text = get_valid_string(f"선택지 {i}: ")
            choices.append(choice_text)
            
        answer = get_valid_input("정답 번호 (1-4): ", 1, 4)
        
        hint = input("힌트를 입력하세요 (엔터 시 생략): ").strip()
        if not hint:
            hint = "힌트가 제공되지 않았습니다."
        
        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")
        self.save_data()

    def list_quizzes(self):
        """등록된 퀴즈 목록 출력 기능"""
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")
        print("----------------------------------------")

    def show_best_score(self):
        """최고 점수 출력 기능"""
        print(f"\n🏆 현재 최고 점수: {self.best_score}점")

    def delete_quiz(self):
        """등록된 퀴즈 삭제 기능 (보너스 과제)"""
        if not self.quizzes:
            print("\n⚠️ 삭제할 퀴즈가 없습니다.")
            return
            
        print("\n🗑️ 삭제할 퀴즈를 선택해주세요.")
        # 삭제할 퀴즈 번호를 보기 쉽게 전체 리스트 출력
        self.list_quizzes()
        
        max_q = len(self.quizzes)
        # 0을 입력하면 취소하는 편의 기능 추가
        delete_idx = get_valid_input(f"삭제할 퀴즈 번호 입력 (1-{max_q}, 취소는 0): ", 0, max_q)
        
        if delete_idx == 0:
            print("삭제가 취소되었습니다.")
            return
            
        # 선택한 번호(1-indexed)를 0-indexed로 변환하여 리스트에서 삭제
        deleted_quiz = self.quizzes.pop(delete_idx - 1)
        print(f"\n✅ 퀴즈가 성공적으로 삭제되었습니다: {deleted_quiz.question}")
        self.save_data()
