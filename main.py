import sys
from utils import get_valid_input

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

def main():
    while True:
        try:
            display_menu()
            # utils.py에 만들어둔 예외 처리 함수를 사용하여 안전하게 1~5번 사이의 숫자만 입력 받기
            choice = get_valid_input("원하시는 메뉴 번호를 입력하세요: ", 1, 5)
            
            if choice == 1:
                print("\n🛠️ [기능 준비 중] 퀴즈 풀기 기능이 곧 추가됩니다!")
            elif choice == 2:
                print("\n🛠️ [기능 준비 중] 퀴즈 추가 기능이 곧 추가됩니다!")
            elif choice == 3:
                print("\n🛠️ [기능 준비 중] 퀴즈 목록 조회 기능이 곧 추가됩니다!")
            elif choice == 4:
                print("\n🛠️ [기능 준비 중] 최고 점수 확인 기능이 곧 추가됩니다!")
            elif choice == 5:
                print("\n👋 게임을 정상적으로 종료합니다. 안녕히 가세요!")
                break
                
        # Ctrl+C (KeyboardInterrupt) 또는 Ctrl+D (EOFError) 로 강제 종료 시 예외 처리
        except (KeyboardInterrupt, EOFError):
            print("\n\n 비정상적인 종료가 감지되었습니다. 게임을 안전하게 종료합니다.")
            sys.exit(0)

if __name__ == "__main__":
    main()
