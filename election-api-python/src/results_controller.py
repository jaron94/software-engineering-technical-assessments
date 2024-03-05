from results_service import ResultStore
from collections import Counter

class ResultsController:

    def __init__(self) -> None:
        self.store: ResultStore = ResultStore()
    
    def get_result(self, id: int) -> dict:
        return self.store.get_result(id)
    
    def new_result(self, result: dict) -> dict:
        self.store.new_result(result)
        return {}
    
    def reset(self) -> None:
        self.store.reset()
    
    def scoreboard(self) -> dict:
        winners = []
        for result in self.store.get_all():
            votes = []
            parties = []
            for party_res in result["partyResults"]:
                parties.append(party_res["party"])
                votes.append(party_res["votes"])
            winners.append(parties[votes.index(max(votes))])
        
        score = dict(Counter(winners))
        overall_winner = None
        for party, seat_count in score.items():
            if seat_count >= 325:
                overall_winner = party
                
        score.update({"winner": overall_winner})
        
        return score
