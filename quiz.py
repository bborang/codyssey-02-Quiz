class Quiz:
    def __init__(self, question, choices, answer):
        """
        question: str (퀴즈 문제 내용)
        choices: list (4지선다 선택지 텍스트 리스트)
        answer: int (1~4 사이의 정답 번호)
        """
        self.question = question
        self.choices = choices
        self.answer = answer

    def to_dict(self):
        """JSON 데이터 저장을 위해 객체를 딕셔너리로 변환하는 메서드"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 다시 Quiz 객체로 복원하는 클래스 메서드"""
        return cls(data["question"], data["choices"], data["answer"])


def get_default_docker_quizzes():
    """초기 데이터가 없을 때 사용할 1주차 Docker 주제의 기본 퀴즈 5개를 반환합니다."""
    return [
        Quiz(
            question="Docker 컨테이너를 최초로 생성하고 실행하는 명령어는?",
            choices=["docker start", "docker run", "docker exec", "docker build"],
            answer=2
        ),
        Quiz(
            question="이미지 생성을 위해 작성하는 자동화 레시피 파일의 이름은?",
            choices=["docker-compose.yml", "Dockerfile", "Dockerconfig", "Makefile"],
            answer=2
        ),
        Quiz(
            question="현재 내 컴퓨터에 실행 중인 컨테이너 목록을 확인하는 명령어는?",
            choices=["docker ps", "docker ls", "docker images", "docker info"],
            answer=1
        ),
        Quiz(
            question="실행 중인 컨테이너 내부에 접속하여 터미널을 열기 위해 사용하는 명령어는?",
            choices=["docker attach", "docker ssh", "docker exec", "docker enter"],
            answer=3
        ),
        Quiz(
            question="컨테이너를 삭제해도 데이터가 날아가지 않게 저장소(공간)를 연결하는 개념은?",
            choices=["Port Mapping", "Docker Network", "Docker Hub", "Volume (바인드 마운트)"],
            answer=4
        )
    ]
