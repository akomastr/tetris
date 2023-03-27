#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import copy

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0
    HoldShape_class = 0
    icount = 0
    maxcount = 0

    # GetNextMove is main function.
    # input
    #    nextMove : nextMove structure which is empty.
    #    GameStatus : block/field/judge/debug information. 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : nextMove structure which includes next shape position and the other.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        
        # print GameStatus
        print("=================================================>")
#        pprint.pprint(GameStatus, width = 61, compact = True)

        maxcount = sum(GameStatus["field_info"]["backboard"][80:89])


        # get data from GameStatus
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        NextShapeDirectionRange = GameStatus["block_info"]["nextShape"]["direction_range"]
        HoldShapeDirectionRange = GameStatus["block_info"]["holdShape"]["direction_range"]
    
        # Indexを判断に使う
        CurrentShapeIndex = GameStatus["block_info"]["currentShape"]["index"]
        NextShapeIndex = GameStatus["block_info"]["nextShape"]["index"]
        HoldShapeIndex = GameStatus["block_info"]["holdShape"]["index"]

        # current shape info
        self.CurrentShape_class = GameStatus["block_info"]["currentShape"]["class"]
        self.NextShape_class = GameStatus["block_info"]["nextShape"]["class"]
        self.HoldShape_class = GameStatus["block_info"]["holdShape"]["class"]

        # current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # default board definition
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        self.ShapeNone_index = GameStatus["debug_info"]["shape_info"]["shapeNone"]["index"]

#        if HoldShapeIndex == None:
        if HoldShapeIndex == None:
#            if NextShapeIndex == 1:
            nextMove["strategy"]["use_hold_function"] = "y"

        # search best nextMove -->
        strategy = None
        LatestEvalValue = -100000
        # search with current block Shape
        for direction0 in CurrentShapeDirectionRange:   #このforループで、CurrentShapeDirectionRange（現在のshapeを何回回転できるかのリスト）を一個ずつ回すfor ループ。
            # search with x range
            x0Min, x0Max = self.getSearchXRange(self.CurrentShape_class, direction0)   #getSearchXRangeで、現在のshapeを[direction0]回 回転させたときに、左右に何個動かせるかの範囲を取得


            #for x0 in range(x0Min, x0Max): #ｘ座標原点から横方向の最大値まで、１マスずつ動かすfor ループ
            if CurrentShapeIndex != 1:
                print(maxcount)
                if maxcount < 1:
                    x0Max = x0Max - 1
                else:
                    print(maxcount)

#                if self.board_data_height < 10:
#            else:    
#                nextMove["strategy"]["use_hold_function"] = "y"
#                nextMove["strategy"]["direction"] = "0"
#                nextMove["strategy"]["x"] = "0"
#                nextMove["strategy"]["y_operation"] = "0"
#                nextMove["strategy"]["y_moveblocknum"] = "0"
#                print(nextMove)
#                return nextMove

            for x0 in range(x0Min, x0Max): #ｘ座標原点から横方向の最大値まで、１マスずつ動かすfor ループ
                # get board data, as if dropdown block
                board = self.getBoard(self.board_backboard, self.CurrentShape_class, direction0, x0) #現在の盤面に、現在のshapeを[direction0]回 回転し、[x0]マス動かす操作をしたときの盤面状態を返す

                # evaluate board
                EvalValue = self.calcEvaluationValueSample(board)  #上で導出した盤面状態をcalcEvaluationValueSample関数で評価
                # update best move
                if EvalValue > LatestEvalValue:  #一個前の評価値と比較
                    strategy = (direction0, x0, 1, 1)  #一個前の評価値と比較し、今の評価値が高ければ、strategyを更新
                    LatestEvalValue = EvalValue

                ##test
                for direction1 in NextShapeDirectionRange:
                    x1Min, x1Max = self.getSearchXRange(self.NextShape_class, direction1)
                    for x1 in range(x1Min, x1Max):
                        board2 = self.getBoard(board, self.NextShape_class, direction1, x1)
                        EvalValue = self.calcEvaluationValueSample(board2)
                        if EvalValue > LatestEvalValue:
                            strategy = (direction0, x0, 1, 1)
                            LatestEvalValue = EvalValue
        # search best nextMove <--

        if self.HoldShape_class != None:
            for direction2 in HoldShapeDirectionRange:   #このforループで、CurrentShapeDirectionRange（現在のshapeを何回回転できるかのリスト）を一個ずつ回すfor ループ。
                # search with x range
                x2Min, x2Max = self.getSearchXRange(self.HoldShape_class, direction2)   #getSearchXRangeで、現在のshapeを[direction0]回 回転させたときに、左右に何個動かせるかの範囲を取得
                #for x0 in range(x0Min, x0Max): #ｘ座標原点から横方向の最大値まで、１マスずつ動かすfor ループ

                if HoldShapeIndex != 1:
                    if maxcount < 1:
                        x2Max = x2Max - 1
                    else:
                        print(maxcount)

                for x2 in range(x2Min, x2Max): #ｘ座標原点から横方向の最大値まで、１マスずつ動かすfor ループ
                    # get board data, as if dropdown block
                    board = self.getBoard(self.board_backboard, self.HoldShape_class, direction2, x2) #現在の盤面に、現在のshapeを[direction0]回 回転し、[x0]マス動かす操作をしたときの盤面状態を返す

                    # evaluate board
                    EvalValue = self.calcEvaluationValueSample(board)  #上で導出した盤面状態をcalcEvaluationValueSample関数で評価
                    # update best move
                    if EvalValue > LatestEvalValue:  #一個前の評価値と比較
                        strategy = (direction2, x2, 1, 1)  #一個前の評価値と比較し、今の評価値が高ければ、strategyを更新
                        LatestEvalValue = EvalValue
                        nextMove["strategy"]["use_hold_function"] = "y"
#                        if CurrentShapeIndex == 1:
#                            nextMove["strategy"]["use_hold_function"] = "n"



                    ###test
                    ###for direction1 in NextShapeDirectionRange:
                    ###  x1Min, x1Max = self.getSearchXRange(self.NextShape_class, direction1)
                    ###  for x1 in range(x1Min, x1Max):
                    ###        board2 = self.getBoard(board, self.NextShape_class, direction1, x1)
                    ###        EvalValue = self.calcEvaluationValueSample(board2)
                    ###        if EvalValue > LatestEvalValue:
                    ###            strategy = (direction0, x0, 1, 1)
                    ###            LatestEvalValue = EvalValue
            # search best nextMove <--


        print("===", datetime.now() - t1)
        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        print(self.board_data_width)
        print(nextMove)
        print("###### SAMPLE CODE ######")
        return nextMove

    def getSearchXRange(self, Shape_class, direction):
        #
        # get x range from shape direction.
        #
        minX, maxX, _, _ = Shape_class.getBoundingOffsets(direction) # get shape x offsets[minX,maxX] as relative value.
        xMin = -1 * minX
        xMax = self.board_data_width - maxX
        return xMin, xMax

    def getShapeCoordArray(self, Shape_class, direction, x, y):
        #
        # get coordinate array by given shape.
        #
        coordArray = Shape_class.getCoords(direction, x, y) # get array from shape direction, x, y.
        return coordArray

    def getBoard(self, board_backboard, Shape_class, direction, x):
        # 
        # get new board.
        #
        # copy backboard data to make new board.
        # if not, original backboard data will be updated later.
        board = copy.deepcopy(board_backboard)
        _board = self.dropDown(board, Shape_class, direction, x)
        return _board

    def dropDown(self, board, Shape_class, direction, x):
        # 
        # internal function of getBoard.
        # -- drop down the shape on the board.
        # 
        dy = self.board_data_height - 1
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        # update dy
        for _x, _y in coordArray:
            _yy = 0
            while _yy + _y < self.board_data_height and (_yy + _y < 0 or board[(_y + _yy) * self.board_data_width + _x] == self.ShapeNone_index):
                _yy += 1
            _yy -= 1
            if _yy < dy:
                dy = _yy
        # get new board
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board

    def dropDownWithDy(self, board, Shape_class, direction, x, dy):
        #
        # internal function of dropDown.
        #
        _board = board
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        for _x, _y in coordArray:
            _board[(_y + dy) * self.board_data_width + _x] = Shape_class.shape
        return _board

    def calcEvaluationValueSample(self, board):    #strategyに入れる次の手を評価する？大事な関数
        #
        # sample function of evaluate board.
        #
        width = self.board_data_width
        height = self.board_data_height

        # evaluation paramters
        ## lines to be removed
        fullLines = 0
        ## number of holes or blocks in the line.
        nHoles, nIsolatedBlocks = 0, 0
        ## absolute differencial value of MaxY
        absDy = 0  #たぶん高さの差の合計値をカウントする変数
        ## how blocks are accumlated
        BlockMaxY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width

        ### check board
        # each y line
        for y in range(height - 1, 0, -1): #内側のfor ループで横一列をサーチし、このforループで縦方向をサーチ
            hasHole = False
            hasBlock = False
            # each x line
            for x in range(width):      #横一列のブロック、穴の有無の判定を行う（サーチ）
                ## check if hole or block..
                if board[y * self.board_data_width + x] == self.ShapeNone_index:   #サーチした座標にShapeNone_index=0を見つけたら
                    # hole
                    hasHole = True #穴あり判定を行う
                    holeCandidates[x] += 1  # just candidates in each column..　その列における穴候補の空白の数（上にブロックがあれば穴と確定される）をインクリメント
                else:      #サーチした座標が0以外なら、
                    # block
                    hasBlock = True  #ブロックあり判定を行う
                    BlockMaxY[x] = height - y                # update blockMaxY ブロックを見つけた最も高い位置、を更新する。
                    if holeCandidates[x] > 0:   #ブロックがそこにある事が確定した時点で、その下の穴候補は穴と確定される。
                        holeConfirm[x] += holeCandidates[x]  # update number of holes in target column.. その列における穴の数を確定
                        holeCandidates[x] = 0                # reset  その行における穴の数候補変数をリセット
                    if holeConfirm[x] > 0:                   # 確定穴数が０以上なら（冗長なコードな気がするが）
                        nIsolatedBlocks += 1                 # update number of isolated blocks　　その列に、下にブロックがない孤立したブロックの数を１増やす

            if hasBlock == True and hasHole == False: #hasblockがTrueでhasholeがFalseなら、フルで埋まっている
                # filled with block
                fullLines += 1   #その場合はfullLinesを１インクリメント
            elif hasBlock == True and hasHole == True:   #hasblockもhasholeもTrueなら何もしない
                # do nothing
                pass
            elif hasBlock == False:     #hasblockがfalseなら何もないので何もしない
                # no block line (and ofcourse no hole)
                pass

        # nHoles
        for x in holeConfirm:
            nHoles += abs(x)

        ### absolute differencial value of MaxY
        BlockMaxDy = []
        for i in range(len(BlockMaxY) - 1):
            val = BlockMaxY[i] - BlockMaxY[i+1]
            BlockMaxDy += [val]
        for x in BlockMaxDy:
            absDy += abs(x)

        #### maxDy
        maxDy = max(BlockMaxY) - min(BlockMaxY)
        #### maxHeight
        maxHeight = max(BlockMaxY) - fullLines

        ## statistical data
        #### stdY
        #if len(BlockMaxY) <= 0:
        #    stdY = 0
        #else:
        #    stdY = math.sqrt(sum([y ** 2 for y in BlockMaxY]) / len(BlockMaxY) - (sum(BlockMaxY) / len(BlockMaxY)) ** 2)
        #### stdDY
        #if len(BlockMaxDy) <= 0:
        #    stdDY = 0
        #else:
        #    stdDY = math.sqrt(sum([y ** 2 for y in BlockMaxDy]) / len(BlockMaxDy) - (sum(BlockMaxDy) / len(BlockMaxDy)) ** 2)

        self.maxcount = maxHeight

        # calc Evaluation Value
        score = 0
        score = score + fullLines * 1.0           # try to delete line 
        score = score - nHoles * 20.0               # try not to make hole   これを10倍にしたらめっちゃスコア上がった
        score = score - nIsolatedBlocks * 1.0      # try not to make isolated block
        score = score - absDy * 2.0                # try to put block smoothly
        score = score - maxDy * 1.0                # maxDy
        #score = score - maxHeight * 1              # maxHeight
        #score = score - stdY * 1.0                 # statistical data
        #score = score - stdDY * 0.01               # statistical data

        # print(score, fullLines, nHoles, nIsolatedBlocks, maxHeight, stdY, stdDY, absDy,maxDy)
        #print(score, fullLines, nHoles, nIsolatedBlocks, maxHeight, absDy, maxDy, BlockMaxY)
        # print(score, fullLines, nHoles, nIsolatedBlocks, maxHeight, stdY, stdDY, absDy, BlockMaxY)

        return score


BLOCK_CONTROLLER = Block_Controller()
