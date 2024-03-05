import unittest, json, os
from server import app, controller

class TestScoreboard(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.server = app.test_client(self)
        file_dir: str = os.path.dirname(os.path.realpath(__file__))
        self.RESULT_SAMPLE_PATH: str = f"{file_dir}/resources/sample-election-results"

    def load_and_post_result_file(self, num: str) -> dict:
        file_number: str = str(num).zfill(3)
        with open(f"{self.RESULT_SAMPLE_PATH}/result{file_number}.json", "r") as file:
            result = file.read()
        return self.server.post("/result", json=json.loads(result))

    def load_results(self, quantity: int) -> list[dict]:
        results = []
        for i in range(quantity):
            results.append(self.load_and_post_result_file(i + 1))
        return results
    
    def fetch_scoreboard(self) -> list[dict]:
        response = self.server.get("/scoreboard")
        return [] if response.data == b'{}\n' else json.loads(response.data.decode("utf-8"))

    def setUp(self) -> None:
        controller.reset()

    def test_first_5(self) -> None:
        self.load_results(5)
        scoreboard: list = self.fetch_scoreboard()
        self.assertNotEqual(len(scoreboard), 0)
        # assert LD == 1
        self.assertEqual(scoreboard["LD"], 1)
        # assert LAB = 4
        self.assertEqual(scoreboard["LAB"], 4)
		# assert winner = noone
        self.assertIsNone(scoreboard["winner"])

    def test_first_100(self) -> None:
        self.load_results(100)
        scoreboard: list = self.fetch_scoreboard()
        self.assertNotEqual(len(scoreboard), 0)
        # assert LD == 12
        self.assertEqual(scoreboard["LD"], 12)
		# assert LAB == 56
        self.assertEqual(scoreboard["LAB"], 56)
		# assert CON == 31
        self.assertEqual(scoreboard["CON"], 31)
		# assert winner = noone
        self.assertIsNone(scoreboard["winner"])

    def test_first_554(self) -> None:
        self.load_results(554)
        scoreboard: list = self.fetch_scoreboard()
        self.assertNotEqual(len(scoreboard), 0)
        # assert LD == 52
        self.assertEqual(scoreboard["LD"], 52)
		# assert LAB = 325
        self.assertEqual(scoreboard["LAB"], 325)
		# assert CON = 167
        self.assertEqual(scoreboard["CON"], 167)
		# assert winner = LAB
        self.assertEqual(scoreboard["winner"], "LAB")

    def test_all_results(self) -> None:
        self.load_results(650)
        scoreboard: list = self.fetch_scoreboard()
        self.assertNotEqual(len(scoreboard), 0)
        # assert LD == 62
        self.assertEqual(scoreboard["LD"], 62)
		# assert LAB == 349
        self.assertEqual(scoreboard["LAB"], 349)
		# assert CON == 210
        self.assertEqual(scoreboard["CON"], 210)
		# assert winner = LAB
        self.assertEqual(scoreboard["winner"], "LAB")
		# assert sum = 650
        seat_sum = sum([seat_count for party, seat_count in scoreboard.items() if party != "winner"])
        self.assertEqual(seat_sum, 650)

if __name__ == "__main__":
    unittest.main()