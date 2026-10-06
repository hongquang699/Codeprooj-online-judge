from backend.judge.models import Problem

class ProblemValidator:
    @staticmethod
    def validate(problem_identifier, user=None):
        if not problem_identifier:
            return False, "Vui lòng chọn bài tập.", None

        problem = None
        if str(problem_identifier).isdigit():
            problem = Problem.objects.filter(id=int(problem_identifier)).first()
        if not problem:
            problem = Problem.objects.filter(code__iexact=str(problem_identifier)).first()

        if not problem:
            return False, f"Bài tập '{problem_identifier}' không tồn tại.", None

        # Check permission if private
        if not problem.is_public:
            if not user or not user.is_staff:
                return False, "Bạn không có quyền nộp bài cho bài tập này.", None

        return True, "", problem
