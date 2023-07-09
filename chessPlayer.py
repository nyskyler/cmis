import pickle
import datetime

class chessPlayer:
    def __init__(self, name):
        try:
            with open('./players/' + name + '.p', 'rb') as f:
                temp = pickle.load(f)
                self.name = temp.name
                self.record = temp.record
                self.numOfMatches = len(temp.record['results'])
        except FileNotFoundError:
            self.name =  name
            self.record = {'time': [], 'player': [], 'results': [], 'points': []}
            self.numOfMatches = 0

    def enter_match_result(self, player, result, point):  # 경기 결과 입력
        dt_now = datetime.datetime.now()
        self.record['time'].append(dt_now.strftime('%Y-%m-%d %H:%M:%S'))
        self.record['player'].append(player)
        self.record['results'].append(result)
        self.record['points'].append(point)
        self.numOfMatches += 1
        with open('./players/' + self.name + '.p', 'wb') as f:
            pickle.dump(self, f)

    def print_match_results(self):  # 역대 경기 결과 출력
        desc_tuple = list(zip(self.record['time'], self.record['player'], self.record['results'], self.record['points']))
        print(desc_tuple)

    def calculate_average_score(self):  # 평균점수 계산
        return round(self.calculate_cumulative_points() / self.numOfMatches, 2)

    def calculate_winning_rate(self):   # 승률 계산
        numOfWonGames = self.record['results'].count('승')
        return round(numOfWonGames / self.numOfMatches * 100, 2)

    def calculate_cumulative_points(self):  # 누적 포인트 계산
        sum = 0 
        for p in self.record['points']:
            sum += p
        return sum

"""
myself = chessPlayer('유승우')
myself.enter_match_result('김민성', '승', 39)
myself.enter_match_result('김태준', '승', 39)
myself.enter_match_result('심채은', '무', 36)
myself.enter_match_result('배지혁', '승', 39)
print(myself.calculate_cumulative_points())
print(myself.calculate_average_score())
print(myself.calculate_winning_rate())
print(myself.print_match_results())
"""

