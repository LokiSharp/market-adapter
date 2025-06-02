from datetime import date
from typing import List, Optional, Type
from longport.openapi import (
    QuoteContext,
    Config,
    SecurityStaticInfo,
    SecurityQuote,
    SecurityDepth,
    SecurityBrokers,
    ParticipantInfo,
    Trade,
    IntradayLine,
    Candlestick,
    Period,
    AdjustType,
    MarketTradingSession,
    MarketTradingDays,
    CapitalFlowLine,
    CapitalDistributionResponse,
    SecurityCalcIndex,
    CalcIndex,
    TradeSessions,
    Market,
    MarketTemperature,
    HistoryMarketTemperatureResponse,
)
from config import LONGPORT_APP_KEY, LONGPORT_APP_SECRET, LONGPORT_ACCESS_TOKEN


class LongPortMarketAdapter:
    def __init__(self):
        self.ctx = QuoteContext(
            Config(
                app_key=LONGPORT_APP_KEY,
                app_secret=LONGPORT_APP_SECRET,
                access_token=LONGPORT_ACCESS_TOKEN,
            )
        )

    def fetch_static_info_batch(self, symbols: List[str]) -> List[SecurityStaticInfo]:
        """
        批量获取标的的静态信息

        :param symbols: 标的代码列表
        :return: 静态信息对象列表
        """
        static_info = self.ctx.static_info(symbols)
        return static_info

    def fetch_static_info(self, symbol: str) -> Optional[SecurityStaticInfo]:
        """
        获取单个标的的静态信息

        :param symbol: 标的代码
        :return: 静态信息对象或None
        """
        static_info = self.fetch_static_info_batch([symbol])
        return static_info[0] if static_info else None

    def fetch_quote_batch(self, symbols: List[str]) -> List[SecurityQuote]:
        """
        批量获取标的的实时行情

        :param symbols: 标的代码列表
        :return: 行情对象列表
        """
        quote = self.ctx.quote(symbols)
        return quote

    def fetch_quote(self, symbol: str) -> Optional[SecurityQuote]:
        """
        获取单个标的的实时行情

        :param symbol: 标的代码
        :return: 行情对象或None
        """
        quote = self.fetch_quote_batch([symbol])
        return quote[0] if quote else None

    def fetch_depth(self, symbol: str) -> SecurityDepth:
        """
        获取标的的盘口深度信息

        :param symbol: 标的代码
        :return: 盘口深度对象
        """
        depth = self.ctx.depth(symbol)
        return depth

    def fetch_brokers(self, symbol: str) -> SecurityBrokers:
        """
        获取标的的券商列表

        :param symbol: 标的代码
        :return: 券商代码列表
        """
        brokers = self.ctx.brokers(symbol)
        return brokers

    def fetch_participants(self) -> List[ParticipantInfo]:
        """
        获取参与者代码列表

        :return: 参与者代码列表
        """
        participants = self.ctx.participants()
        return participants

    def fetch_trades(self, symbol: str, count: int) -> List[Trade]:
        """
        获取标的的交易请求列表

        :param symbol: 标的代码
        :param count: 请求数量
        :return: 交易请求对象列表
        """
        trades = self.ctx.trades(symbol, count)
        return trades

    def fetch_intraday(self, symbol: str) -> List[IntradayLine]:
        """
        获取标的日内分时数据

        :param symbol: 标的代码
        :return: 分时数据列表
        """
        intraday = self.ctx.intraday(symbol)
        return intraday

    def fetch_trading_session(self) -> List[MarketTradingSession]:
        """
        获取交易时段信息

        :param market: 市场代码
        :return: 交易时段信息列表
        """
        sessions = self.ctx.trading_session()
        return sessions

    def fetch_trading_days(
        self, market: Type[Market], begin: date, end: date
    ) -> MarketTradingDays:
        """
        获取交易日历

        :param market: 市场代码
        :param begin: 开始日期
        :param end: 结束日期
        :return: 交易日历信息
        """
        trading_days = self.ctx.trading_days(market, begin, end)
        return trading_days

    def fetch_capital_flow(self, symbol: str) -> List[CapitalFlowLine]:
        """
        获取标的的资金流向数据

        :param symbol: 标的代码
        :return: 资金流向数据列表
        """
        capital_flow = self.ctx.capital_flow(symbol)
        return capital_flow

    def fetch_capital_distribution(self, symbol: str) -> CapitalDistributionResponse:
        """
        获取标的的资金分布数据

        :param symbol: 标的代码
        :return: 资金分布数据列表
        """
        capital_distribution = self.ctx.capital_distribution(symbol)
        return capital_distribution

    def fetch_calc_indexes(
        self, symbols: List[str], indexes: List[type[CalcIndex]]
    ) -> List[SecurityCalcIndex]:
        """
        获取计算指数

        :param symbols: 标的代码列表
        :param indexes: 需要计算的指标类型列表
        :return: 计算指数对象列表
        """
        calc_indexes = self.ctx.calc_indexes(symbols, indexes)
        return calc_indexes

    def fetch_candlesticks(
        self,
        symbol: str,
        period: Type[Period],
        count: int,
        adjust_type: Type[AdjustType],
        trade_session: Type[TradeSessions],
    ) -> List[Candlestick]:
        """
        获取标的K线数据

        :param symbol: 标的代码
        :param period: K线周期
        :param count: 请求数量
        :param adjust_type: 复权类型
        :param trade_session: 可选的交易时段
        :return: K线数据列表
        """
        candles = self.ctx.candlesticks(
            symbol, period, count, adjust_type, trade_session
        )
        return candles

    def fetch_history_candlesticks_by_date(
        self,
        symbol: str,
        period: Type[Period],
        adjust_type: Type[AdjustType],
        start: Optional[date] = None,
        end: Optional[date] = None,
        trade_sessions: Type[TradeSessions] = TradeSessions.Intraday,
    ) -> List[Candlestick]:
        """
        获取标的K线数据

        :param symbol: 标的代码
        :param period: K线周期
        :param adjust_type: 复权类型
        :param start: 开始日期
        :param end: 结束日期
        :param trade_sessions: 可选的交易时段
        :return: K线数据列表
        """
        candles = self.ctx.history_candlesticks_by_date(
            symbol, period, adjust_type, start, end, trade_sessions
        )
        return candles

    def fetch_market_temperature(self, market: Type[Market]) -> MarketTemperature:
        """
        获取市场温度

        :param market: 市场代码

        :return: 市场温度值
        """
        temperature = self.ctx.market_temperature(market)
        return temperature

    def fetch_history_market_temperature(
        self, market: Type[Market], start: date, end: date
    ) -> HistoryMarketTemperatureResponse:
        """
        获取历史市场温度

        :param market: 市场代码
        :param start: 开始日期
        :param end: 结束日期
        :return: 历史市场温度值列表
        """
        history_temperature = self.ctx.history_market_temperature(market, start, end)
        return history_temperature
