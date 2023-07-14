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

# 메인 화면

app = wx.App()
frame_main = wx.Frame(None, 0, "홈 화면", wx.Point(100,100), wx.Size(1200, 800), wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX)
frame_main.SetBackgroundColour(wx.Colour(255,255,255,0))

def OnClick_fm_btn1(event):
    frame_main.Hide()
    frame_input.Show()
    splitter.SplitVertically(fi_panel1, fi_panel2)
    total_size = splitter.GetClientSize()
    sash_position = total_size.GetWidth() // 2
    splitter.SetSashPosition(sash_position)

def OnClick_fm_btn2(event):
    frame_main.Hide()
    frame_rank.Show()

def OnClick_fm_btn3(event):
    frame_main.Hide()
    frame_record.Show()

def OnClick_fm_btn4(event):
    frame_main.Hide()
    frame_update.Show()

def OnClick_fm_btn5(event):
    frame_main.Close()
    app.ExitMainLoop()

fm_panelvert1 = wx.Panel(frame_main)
fm_btn1 = buttons.GenButton(fm_panelvert1, label="경기 결과 등록")
fm_btn2 = buttons.GenButton(fm_panelvert1, label="전체 순위")
fm_btn3 = buttons.GenButton(fm_panelvert1, label="개인 기록 보기")
fm_btn4 = buttons.GenButton(fm_panelvert1, label="기록 수정 및 삭제")
fm_btn5 = buttons.GenButton(fm_panelvert1, label="프로그램 종료")
fm_font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
fm_btns = [fm_btn1, fm_btn2, fm_btn3, fm_btn4, fm_btn5]
fm_btns_funcs = [OnClick_fm_btn1, OnClick_fm_btn2, OnClick_fm_btn3, OnClick_fm_btn4, OnClick_fm_btn5]
zipped_main = zip(fm_btns, fm_btns_funcs)

for item in zipped_main:
    item[0].Bind(wx.EVT_BUTTON, item[1])

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
fm_box.Add(fm_panelvert1, proportion = 2, border = 10, flag = wx.LEFT)
fm_box.Add(fm_panelvert2, proportion = 3, border = 10, flag = wx.LEFT)

# 경기 결과 등록

frame_input = wx.Frame(None, 1, "경기 결과 등록", wx.Point(100,100), wx.Size(1200, 800), wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX)
frame_input.SetBackgroundColour(wx.Colour(255,255,255,0))

splitter = wx.SplitterWindow(frame_input)

fi_panel1 = wx.Panel(splitter)
fi_panel1.SetBackgroundColour(wx.WHITE)

fi_panel2 = wx.Panel(splitter)
fi_panel2.SetBackgroundColour(wx.Colour(117,150,86,0))

fi_left_outer_sizer = wx.BoxSizer(wx.VERTICAL)
fi_right_outer_sizer = wx.BoxSizer(wx.VERTICAL)

fi_panel1.SetSizer(fi_left_outer_sizer)
fi_panel2.SetSizer(fi_right_outer_sizer)

fi_left_inner_sizer1 = wx.StaticBoxSizer(wx.HORIZONTAL, fi_panel1, "백 플레이어")
fi_right_inner_sizer1 = wx.StaticBoxSizer(wx.HORIZONTAL, fi_panel2, "흑 플레이어")

combo_left = wx.ComboBox(fi_panel1, choices=sadasol_kids)
combo_left.SetSizeHints(150, -1)
combo_right = wx.ComboBox(fi_panel2, choices=sadasol_kids)
combo_right.SetSizeHints(150, -1)

fi_left_inner_sizer2 = wx.StaticBoxSizer(wx.HORIZONTAL, fi_panel1, "백의 경기 결과")
fi_right_inner_sizer2 = wx.StaticBoxSizer(wx.HORIZONTAL, fi_panel2, "흑의 경기 결과")

left_win = wx.RadioButton(fi_panel1, label = "승", style = wx.RB_GROUP)
left_draw = wx.RadioButton(fi_panel1, label = "무")
left_lose = wx.RadioButton(fi_panel1, label = "패")
right_win = wx.RadioButton(fi_panel2, label = "승", style = wx.RB_GROUP)
right_draw = wx.RadioButton(fi_panel2, label = "무")
right_lose = wx.RadioButton(fi_panel2, label = "패")

for item in [left_win, left_draw, left_lose]:
    item.SetForegroundColour(wx.Colour(0,0,0,0))
    item.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL ))

for item in [right_win, right_draw, right_lose]:
    item.SetForegroundColour(wx.Colour(255,255,255,0))
    item.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL ))

fi_left_inner_sizer1.Add(combo_left, border=30, flag=wx.ALL)
fi_right_inner_sizer1.Add(combo_right, border=30, flag=wx.ALL)

fi_left_inner_sizer2.Add(left_win, border=30, flag=wx.ALL)
fi_left_inner_sizer2.Add(left_draw, border=30, flag=wx.ALL)
fi_left_inner_sizer2.Add(left_lose, border=30, flag=wx.ALL)
fi_right_inner_sizer2.Add(right_win, border=30, flag=wx.ALL)
fi_right_inner_sizer2.Add(right_draw, border=30, flag=wx.ALL)
fi_right_inner_sizer2.Add(right_lose, border=30, flag=wx.ALL)

fi_left_inner_sizer3 = wx.StaticBoxSizer(wx.VERTICAL, fi_panel1, "포인트 계산")
fi_right_inner_sizer3 = wx.StaticBoxSizer(wx.VERTICAL, fi_panel2, "포인트 계산")

fi_left_outer_sizer.Add(fi_left_inner_sizer1, border=25, flag=wx.ALL | wx.EXPAND)
fi_right_outer_sizer.Add(fi_right_inner_sizer1, border=25, flag=wx.ALL | wx.EXPAND)

fi_left_outer_sizer.Add(fi_left_inner_sizer2, border=25, flag=wx.ALL | wx.EXPAND)
fi_right_outer_sizer.Add(fi_right_inner_sizer2, border=25, flag=wx.ALL | wx.EXPAND)

fi_left_outer_sizer.Add(fi_left_inner_sizer3, border=25, flag=wx.ALL | wx.EXPAND)
fi_right_outer_sizer.Add(fi_right_inner_sizer3, border=25, flag=wx.ALL | wx.EXPAND)


# 전체 순위

frame_rank = wx.Frame(None, 2, "전체 순위", wx.Point(100,100), wx.Size(1200, 800), wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX)
frame_rank.SetBackgroundColour(wx.Colour(255,255,255,0))

# 개인 기록 보기

frame_record = wx.Frame(None, 3, "개인 기록 보기", wx.Point(100,100), wx.Size(1200, 800), wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX)
frame_record.SetBackgroundColour(wx.Colour(255,255,255,0))

# 기록 수정 및 삭제

frame_update = wx.Frame(None, 4, "기록 수정 및 삭제", wx.Point(100,100), wx.Size(1200, 800), wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX)
frame_update.SetBackgroundColour(wx.Colour(255,255,255,0))


frame_main.Show()

#wx.CallLater(3000, show_message)
app.MainLoop()
