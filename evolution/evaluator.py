class Evaluator:

    def evaluate(self, candidate):

        score = 100

        code = candidate["code"]

        if len(code) < 50:
            score -= 30

        if "TODO" in code:
            score -= 20

        if "pass" in code:
            score -= 20

        if "FIXME" in code:
            score -= 20

        return max(score, 0)