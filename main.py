import sys
from utils import get_valid_input
from quiz import QuizGame

def display_menu():
    print("\n========================================")
    print("         도커 퀴즈 게임     ")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 퀴즈 삭제")
    print("5. 최고 점수 확인")
    print("6. 종료")
    print("========================================")

def main():
    # QuizGame 인스턴스를 생성하면 __init__에서 자동으로 load_data()가 실행됨
    game = QuizGame()
    
    while True:
        try:
            display_menu()
            choice = get_valid_input("원하시는 메뉴 번호를 입력하세요: ", 1, 6)
            
            if choice == 1:
                game.play_quiz()
            elif choice == 2:
                game.add_quiz()
            elif choice == 3:
                game.list_quizzes()
            elif choice == 4:
                game.delete_quiz()
            elif choice == 5:
                game.show_best_score()
            elif choice == 6:
                print("\n 게임을 정상적으로 종료합니다.")
                game.save_data()
                break
                
        # Ctrl+C (KeyboardInterrupt) 또는 Ctrl+D (EOFError) 로 강제 종료 시 예외 처리
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 비정상적인 종료가 감지되었습니다. 데이터를 안전하게 저장하고 종료합니다.")
            game.save_data()
            sys.exit(0)

if __name__ == "__main__":
    main()
