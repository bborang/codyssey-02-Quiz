import sys
import os
import json
from utils import get_valid_input
from quiz import get_default_docker_quizzes, Quiz

STATE_FILE = "state.json"

def load_data():
    """state.json 파일에서 데이터를 불러옵니다."""
    if not os.path.exists(STATE_FILE):
        print("\n📂 저장된 데이터가 없습니다. 기본 도커 퀴즈 데이터를 불러옵니다.")
        return get_default_docker_quizzes(), 0
        
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
        best_score = data.get("best_score", 0)
        print(f"\n📂 저장된 데이터를 성공적으로 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {best_score}점)")
        return quizzes, best_score
        
    except (json.JSONDecodeError, Exception):
        print("\n⚠️ 데이터 파일이 손상되었습니다. 기본 데이터를 불러옵니다.")
        return get_default_docker_quizzes(), 0

def save_data(quizzes, best_score):
    """현재 퀴즈 목록과 최고 점수를 state.json에 저장합니다."""
    data = {
        "quizzes": [q.to_dict() for q in quizzes],
        "best_score": best_score
    }
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"\n⚠️ 데이터 저장 중 오류가 발생했습니다: {e}")

def display_menu():
    print("\n========================================")
    print("        나만의 도커 퀴즈 게임    ")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 최고 점수 확인")
    print("5. 종료")
    print("========================================")

def play_quiz(quizzes):
    """퀴즈 출제 및 채점 로직"""
    if not quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다! 2번 메뉴를 통해 퀴즈를 추가해주세요.")
        return 0

    print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)")
    score = 0
    
    for i, quiz in enumerate(quizzes, 1):
        print("\n----------------------------------------")
        print(f"[문제 {i}]")
        print(quiz.question, "\n")
        
        for idx, choice_text in enumerate(quiz.choices, 1):
            print(f"  {idx}. {choice_text}")
        print()
        
        # utils.py의 함수를 재사용하여 1~4번 내에서만 정답을 입력받도록 방어
        user_answer = get_valid_input("정답 번호 입력: ", 1, 4)
        
        if user_answer == quiz.answer:
            print("✅ 정답입니다!")
            score += 1
        else:
            print(f"❌ 오답입니다! (정답은 {quiz.answer}번)")
            
    print("\n========================================")
    print(f"🏆 결과: {len(quizzes)}문제 중 {score}문제 정답!")
    print("========================================")
    return score

def get_valid_string(prompt_text):
    """빈칸을 허용하지 않는 문자열 입력 유틸리티"""
    while True:
        text = input(prompt_text).strip()
        if not text:
            print("빈 칸을 입력할 수 없습니다. 다시 입력해주세요.")
            continue
        return text

def add_quiz(quizzes):
    """새로운 퀴즈 추가 기능"""
    print("\n📌 새로운 퀴즈를 추가합니다.")
    question = get_valid_string("문제를 입력하세요: ")
    
    choices = []
    for i in range(1, 5):
        choice_text = get_valid_string(f"선택지 {i}: ")
        choices.append(choice_text)
        
    # 예외 처리가 완비된 utils.py의 함수 사용
    answer = get_valid_input("정답 번호 (1-4): ", 1, 4)
    
    new_quiz = Quiz(question, choices, answer)
    quizzes.append(new_quiz)
    print("\n 퀴즈가 성공적으로 추가되었습니다!")

def list_quizzes(quizzes):
    """등록된 퀴즈 목록 출력 기능"""
    print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("----------------------------------------")
    for i, quiz in enumerate(quizzes, 1):
        print(f"[{i}] {quiz.question}")
    print("----------------------------------------")

def show_best_score(best_score):
    """최고 점수 출력 기능"""
    print(f"\n🏆 현재 최고 점수: {best_score}점")

def main():
    # state.json에서 데이터를 불러옵니다.
    quizzes, best_score = load_data()
    
    while True:
        try:
            display_menu()
            choice = get_valid_input("원하시는 메뉴 번호를 입력하세요: ", 1, 5)
            
            if choice == 1:
                # 퀴즈 풀기 실행 후 반환된 점수가 현재 최고 점수보다 높으면 갱신 및 자동 저장
                current_score = play_quiz(quizzes)
                if current_score > best_score:
                    print("🎉 새로운 최고 점수입니다!")
                    best_score = current_score
                    save_data(quizzes, best_score)
                    
            elif choice == 2:
                add_quiz(quizzes)
                save_data(quizzes, best_score)  # 추가된 퀴즈 자동 저장
                
            elif choice == 3:
                list_quizzes(quizzes)
                
            elif choice == 4:
                show_best_score(best_score)
                
            elif choice == 5:
                print("\n👋 게임을 정상적으로 종료합니다. 안녕히 가세요!")
                save_data(quizzes, best_score)
                break
                
        # Ctrl+C (KeyboardInterrupt) 또는 Ctrl+D (EOFError) 로 강제 종료 시 예외 처리
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 비정상적인 종료가 감지되었습니다. 데이터를 안전하게 저장하고 종료합니다.")
            save_data(quizzes, best_score)
            sys.exit(0)

if __name__ == "__main__":
    main()
