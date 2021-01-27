from itertools import combinations

class PeopleCombination:
    """
    Usage: 
        email = EmailMeta(...)
        PeopleCombination(email)
    """

    def __init__(self, email):
        people = [email.sender] + email.recipients + email.cc
        people = filter(lambda p: p is not None, people)
        people = set(addr.email for addr in people if addr.email)
        self.people = sorted(people)

    def __repr__(self):
        return str(self.people)


    @property
    def combo(self):
        for combination in combinations(self.people, 2):
            yield combination
