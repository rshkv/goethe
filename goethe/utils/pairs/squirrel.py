from collections import deque
import random
import itertools as it


class Squirrel(object):
    def __init__(self, max_level=3):
        self.max_level = max_level

    def word_prob(self, word):
        return 1

    def dep_prob(self, dep_name):
        return 1

    def inv_level_prob(self, level):
        return 1 / level

    def word2vec_window_prob(self, level):
        return (self.max_level - level + 1) / self.max_level

    def keep(self, word, level):
        level_prob = self.word2vec_window_prob(level)
        # word_prob = self.word_prob(word)
        # dep_prob = self.dep_prob(word.dep_)
        return random.random() < level_prob

    def word_context(self, word):
        candidates = deque()
        seen = [word]

        def add_to_queue(word, level):
            for w in it.chain(word.children, [word.head]):
                if w not in seen:
                    seen.add(w)
                    candidates.append((level, w))

        add_to_queue(word, 1)
        while candidates:
            level, candidate = candidates.popleft()
            if self.keep(candidate, level):
                print('keep')
                yield candidate
            if level < self.max_level:
                add_to_queue(candidate, level + 1)

    def pairs(self, doc):
        for word in doc:
            for ctx in self.word_context(word):
                print(ctx)
                yield (word.text, ctx.text)