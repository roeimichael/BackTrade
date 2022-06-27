from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import math
import backtrader as bt

from strategy_skeleton import Strategy_skeleton


class Bollinger_three(Strategy_skeleton):

    def __init__(self, args):
        super(Bollinger_three, self).__init__(args)
        self.in_trade = 0
        self.size = 0
        self.adx = bt.indicators.AverageDirectionalMovementIndex()  # period=14
        self.boll3 = bt.indicators.BollingerBands(period=14, devfactor=3.0)
        self.boll2 = bt.indicators.BollingerBands(period=14, devfactor=2.0)

    def __str__(self):
         return self.__class__.__name__

    def next(self):
        self.log('Close, %.2f' % self.data[0])

        if self.order:
            return  # pending order execution

        if self.in_trade == 0:  # not in the market
            amount_to_invest = self.broker.cash
            if self.adx[0] <= 40:
                if self.data.low[0] < self.boll3.lines.bot:
                    self.size = math.floor(amount_to_invest / self.data.low)
                    # self.buy(size=self.size)# long
                    self.buy(size=self.size)
                    self.log('BUY CREATE (LONG), %.2f ' % self.data[0])
                    self.in_trade = 1
                if self.data.high[0] > self.boll3.lines.top:
                    self.size = math.floor(amount_to_invest / self.data.low)
                    # self.buy(size=self.size)# long
                    self.sell(size=self.size)
                    self.log('SELL CREATE (SHORT), %.2f ' % self.data[0])
                    self.in_trade = 2
        else:
            if self.in_trade == 1:
                if self.data.high[0] > self.boll3.lines.mid[0]:
                    self.close()
                    self.log('SELL CREATE (LONG), %.2f ' % self.data[0])
                    self.in_trade = 0
                    self.print_stats()
            else:  # trade = 2 short
                if self.data.low[0] < self.boll3.lines.mid[0]:
                    self.close()
                    self.log('BUY CREATE (SHORT), %.2f ' % self.data[0])
                    self.in_trade = 0
                    self.print_stats()

