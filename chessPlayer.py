import pickle
import datetime
import tkinter
import tkinter.ttk

sadasol_kids = ['강승언', '곽민솔', '김기민', '김민성', '김보현', '김준우', '김태준', 
                '나두경', '나형준', '배지혁', '심채원', '심채은', '유지현', '이윤지', 
                '이은별', '이지윤', '이채현', '임채윤', '장예특', '진라온', '진하영',
                '최민하', '최은성', '황희락', '유승우']

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
        return list(zip(self.record['time'], self.record['player'], self.record['results'], self.record['points']))

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
def main():
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

class chessInfoHandler:
    def __init__(self):
        self.chessPlayers = []

    def add_player(self, name): # chessPlayer 리스트에 이름 추가
        player = chessPlayer(name)
        self.chessPlayers.append(player)

    def show_all_players(self):
        for i in self.chessPlayers:
            print(i.name)

    def getNameIndex(self, name):   # 이름의 인덱스 위치 확인
        for i in self.chessPlayers:
            if i.name == name:
                return self.chessPlayers.index(i)
        return -1
    
    def show_personal_info(self, idx):  # 개인 전적 확인
        return self.chessPlayers[idx].print_match_results();

def main():
    handler = chessInfoHandler()
    for i in sadasol_kids:
        handler.add_player(i)
    num = handler.getNameIndex("유승우")
    treelist = handler.show_personal_info(num)

    root = tkinter.Tk()
    root.title("체스대국정보시스템")
    root.geometry("1800x1000+100+100")
    root.resizable(False, False)

    treeview = tkinter.ttk.Treeview(root, columns=["time", "player", "result", "point"], displaycolumns=["time", "player", "result", "point"])
    treeview.pack()

    treeview.column("time", width=400, anchor="center")
    treeview.heading("time", text="a", anchor="center")

    treeview.column("player", width=400, anchor="center")
    treeview.heading("player", text="b", anchor="center")

    treeview.column("result", width=400, anchor="center")
    treeview.heading("result", text="c", anchor="center")

    treeview.column("point", width=400, anchor="center")
    treeview.heading("point", text="d", anchor="center")
    
    for i in range(len(treelist)):
        treeview.insert("", "end", text="", values=treelist[i], iid=i)

    root.mainloop()

if __name__ == '__main__':
    main()