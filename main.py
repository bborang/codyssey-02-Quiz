import sys
from utils import get_valid_input
from quiz import get_default_docker_quizzes, Quiz

def display_menu():
    print("\n========================================")
    print("        나만의 도커 퀴즈 게임    ")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
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
    # 현재는 기본 제공 퀴즈 5개만 로드해서 변수에 담아둡니다 (나중에 파일로 관리 예정)
    quizzes = get_default_docker_quizzes()
    best_score = 0
    
    while True:
        try:
            display_menu()
            choice = get_valid_input("원하시는 메뉴 번호를 입력하세요: ", 1, 5)
            
            if choice == 1:
                # 퀴즈 풀기 실행 후 반환된 점수가 현재 최고 점수보다 높으면 갱신
                current_score = play_quiz(quizzes)
                if current_score > best_score:
                    print("🎉 새로운 최고 점수입니다!")
                    best_score = current_score
                    
            elif choice == 2:
                add_quiz(quizzes)
            elif choice == 3:
                list_quizzes(quizzes)
            elif choice == 4:
                show_best_score(best_score)
            elif choice == 5:
                print("\n 게임을 정상적으로 종료합니다.")
                break
                
        # Ctrl+C (KeyboardInterrupt) 또는 Ctrl+D (EOFError) 로 강제 종료 시 예외 처리
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 비정상적인 종료가 감지되었습니다. 게임을 안전하게 종료합니다.")
            sys.exit(0)

if __name__ == "__main__":
    main()
