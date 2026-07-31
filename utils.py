def get_valid_input(prompt_text, min_val, max_val):
    """
    사용자로부터 메뉴 선택이나 정답 번호 입력을 안전하게 받는 공통 방어 함수입니다.
    
    [예외 처리 조건]
    1. 빈칸(Enter만 누름) 입력 시 튕기지 않고 재입력 요구
    2. 문자열(abc 등) 입력 시 ValueError를 잡아서 재입력 요구
    3. 지정된 범위(min_val ~ max_val)를 벗어난 숫자 입력 시 재입력 요구
    4. Ctrl+C (KeyboardInterrupt) 또는 EOF(입력 종료) 발생 시 에러 전파하여 메인 루프에서 안전 종료 처리
    """
    while True:
        try:
            # 좌우 공백을 제거하고 입력 받기
            user_input = input(prompt_text).strip()
            
            # 빈 입력(엔터) 방어
            if not user_input:
                print("아무것도 입력하지 않으셨습니다. 다시 입력해주세요.")
                continue
            
            # 문자열이 숫자로 변환될 수 있는지 확인 (소수점(4.5)이나 문자열(abc)이면 ValueError 발생)
            choice = int(user_input)
            
            # '004' 처럼 앞에 0이 붙거나 불필요한 기호가 포함된 비정상적인 입력 방어
            if str(choice) != user_input:
                print("⚠️ 0으로 시작하는 숫자나 비정상적인 형태는 입력할 수 없습니다.")
                continue
            
            # 지정된 범위 밖의 숫자 방어
            if choice < min_val or choice > max_val:
                print(f"⚠️ {min_val}부터 {max_val} 사이의 숫자만 입력해주세요.")
                continue
                
            return choice
            
        except ValueError:
            print("⚠️ 숫자(정수)가 아닙니다. 올바른 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            # Ctrl+C가 눌렸을 때 비정상 종료(Traceback 출력)되지 않도록 예외 던지기
            raise KeyboardInterrupt
        except EOFError:
            # Ctrl+D가 눌렸을 때 비정상 종료되지 않도록 예외 던지기
            raise EOFError
