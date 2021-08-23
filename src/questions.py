from exceptions import InvalidStateException, ResponseTimeoutException
import utils
import config


class Question:
    def __init__(self, qdef):
        self.qdef = qdef
        self.start_time = 0
        self.answer_timeout = config.ANSWER_TIMEOUT

    def get_id(self):
        return self.qdef["id"]

    def get_defn(self):
        return self.qdef["question"]

    def get_options(self):
        return self.qdef["options"]

    def get_answer(self):
        return self.qdef["answer"]

    def set_start_time(self):
        self.start_time = utils.get_timestamp_utc()

    def has_started(self):
        return self.start_time is not None

    def time_since_started(self):
        if self.start_time < 1:
            return 0

        return utils.get_time_delta_utc(self.start_time)

    def validate_can_accpet_answer(self):
        if not self.has_started():
            raise InvalidStateException()

        if self.time_since_started() > self.answer_timeout:
            raise ResponseTimeoutException()

    def is_correct_answer(self, answer):
        return self.get_answer() == answer


set1 = [
    {
        "id": "aab6384d-e392-4508-8a2f-21b1bdd5b551",
        "question": "The Blackstreet lyric “I like the way you work it” is from what iconic song?",
        "options": [
            "No Diggity", "Yes Diggity", "Maybe a Lil Diggity"
        ],
        "answer":0
    },
    {
        "id": "8375a054-9817-4cac-9aa9-c09c0e78c202",
        "question": "The American episodic TV show that’s produced the most episodes is in what genre?",
        "options": ["Animated", "Game show", "Soap opera"],
        "answer":2
    },
    {
        "id": "cd3049e4-1362-4340-b520-eab9a50ae003",
        "question": "What does Edward prepare for the Christmas party in “Edward Scissorhands”?",
        "options": ["Cronuts", "Ice sculpture", "Santa costume"],
        "answer": 1
    },
    {
        "id": "bc9ea85a-6176-4197-a818-db6b490add64",
        "question": "Which of these teams is tied for the most Super Bowl losses?",
        "options": ["Buffalo Bills", "Minnesota Vikings", "New England Patriots"],
        "answer": 2
    },
    {
        "id": "a797a2db2-5aac-4d81-8a7e-dcf2432197b5",
        "question": "Which chess piece moves in what looks like an L-shape?",
        "options": ["Knight", "Rook", "Bishop"],
        "answer": 0
    },
    {
        "id": "976f8e43-df5f-4513-8548-17d51f9544d6",
        "question": "In which league do more than half the players score left-handed?",
        "options": ["NHL", "MLB", "NBA"],
        "answer": 0
    },
    {
        "id": "7ab38cbd-ed00-41a4-8043-d5b204b889f7",
        "question": "By annual sales, what is America's most popular condiment?",
        "options": ["Ketchup", "Mayonnaise", "Mustard"],
        "answer": 1
    },
    {
        "id": "3e1f9249-9bed-44d4-971f-0484a00e5d98",
        "question": "All four top-billed stars of what other film appeared in “Love Actually”?",
        "options": ["Sense and Sensibility", "Bridget Jones’s Diary", "Notting Hill"],
        "answer": 0
    },
    {
        "id": "b0cbb29b-6642-46ed-b18a-bd6c9a979d29",
        "question": "In The Modern Library’s 100 Best Novels, what author got two selections in the top 10?",
        "options": ["James Joyce", "William Faulkner", "F. Scott Fitzgerald"],
        "answer": 0
    },
    {
        "id": "18522237-307f-4a2d-8012-a97545a671ea",
        "question": "Who is the only American NBA player currently in the top 5 in total fantasy points this season?",
        "options": ["Julius Randle", "Damian Lillard", "Russell Westbrook"],
        "answer": 0
    },
    {
        "id": "1ec309e2-26ef-487b-ba30-d2749295565b",
        "question": "Who famously conquered a large portion of Asia?",
        "options": ["Charlemagne", "Columbus", "Genghis Khan"],
        "answer": 2
    },
    {
        "id": "41c9bc28-6f30-4ddb-ae95-7a0cb11a742c",
        "question": "Who is credited with inventing the printing press?",
        "options": ["Harper Collins", "Simon Schuster", "Johannes Gutenberg"],
        "answer": 2
    },
]


def get_next_question_set():
    qs = []
    for raw_q in set1:
        q = Question(raw_q)
        qs.append(q)
    return qs
