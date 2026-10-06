from django.utils import timezone
from backend.judge.models import Contest

class ContestValidator:
    @staticmethod
    def validate(contest_identifier, user=None):
        if not contest_identifier:
            return True, "", None # Not a contest submission

        contest = None
        if str(contest_identifier).isdigit():
            contest = Contest.objects.filter(id=int(contest_identifier)).first()
        if not contest:
            contest = Contest.objects.filter(key__iexact=str(contest_identifier)).first()

        if not contest:
            return False, f"Kỳ thi '{contest_identifier}' không tồn tại.", None

        now = timezone.now()
        if contest.start_time and now < contest.start_time:
            return False, "Kỳ thi chưa bắt đầu.", None

        if contest.end_time and now > contest.end_time:
            # Past contest: can be allowed as practice
            pass

        return True, "", contest
