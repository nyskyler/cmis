import wx
import wx.lib.buttons as buttons
import pickle
import datetime

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


app = wx.App()
frame_main = wx.Frame(None, 0, "MAIN", wx.Point(100,100), wx.Size(1200, 800), wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX)
frame_main.SetBackgroundColour(wx.Colour(255,255,255,0))

fm_panelvert1 = wx.Panel(frame_main)
fm_btn1 = buttons.GenButton(fm_panelvert1, label="경기 결과 등록")
fm_btn2 = buttons.GenButton(fm_panelvert1, label="전체 순위")
fm_btn3 = buttons.GenButton(fm_panelvert1, label="개인 전적 보기")
fm_btn4 = buttons.GenButton(fm_panelvert1, label="기록 수정 및 삭제")
fm_btn5 = buttons.GenButton(fm_panelvert1, label="프로그램 종료")
fm_font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
fm_btns = [fm_btn1, fm_btn2, fm_btn3, fm_btn4, fm_btn5]

for btn in fm_btns:
    btn.SetBezelWidth(9)
    btn.SetFont(fm_font)
    btn.SetBackgroundColour(wx.Colour(117,150,86,0))
    btn.SetForegroundColour(wx.WHITE)

fm_sub_box1 = wx.BoxSizer(wx.VERTICAL)

for btn in fm_btns:
    fm_sub_box1.Add(btn, border=160 if btn == fm_btn1 else 50, flag=wx.UP | wx.EXPAND)

fm_panelvert1.SetSizer(fm_sub_box1)

fm_panelvert2 = wx.Panel(frame_main)
fm_static = wx.StaticText(fm_panelvert2, label="4다솔 체스정보시스템")
fm_static.SetFont(wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD))
fm_static.SetForegroundColour(wx.Colour(0,0,0,0))

main_image = wx.Image("./kids.png")
resized_main_image = main_image.Scale(600,489)

main_bitmap = wx.Bitmap(resized_main_image)
static_main_bitmap = wx.StaticBitmap(fm_panelvert2, bitmap=main_bitmap)
static_main_bitmap.SetPosition((50,155))

fm_box = wx.BoxSizer(wx.HORIZONTAL)
frame_main.SetSizer(fm_box)
fm_box.Add(fm_panelvert1, proportion = 4, border = 10, flag = wx.LEFT)
fm_box.Add(fm_panelvert2, proportion = 6, border = 10, flag = wx.LEFT)

"""
frame_two = wx.Frame(None, 0, "두 번째 화면", wx.Point(100,100), wx.Size(600,400), wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
frame_two.SetBackgroundColour(wx.Colour(0,255,0,0))

frame_three = wx.Frame(None, 0, "세 번째 화면", wx.Point(100,100), wx.Size(600,400), wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
frame_three.SetBackgroundColour(wx.Colour(0,0,255,0))
"""
frame_main.Show(True)

#wx.CallLater(3000, show_message)
app.MainLoop()

"""
def main():
    app = wx.App()
    frame = wx.Frame(None)

    size = wx.Size(600,400)
    frame.SetSize(size)
    pos = wx.Point(100,100)
    frame.SetPosition(pos)
    color = wx.Colour(0,0,255,0)
    frame.SetBackgroundColour(color)
    frame.SetTitle("메인화면")
    frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)

    frame.Show(True)
    app.MainLoop()




if __name__ == '__main__':
    main()
"""