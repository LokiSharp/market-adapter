from modules.long_port_market_adapter import LongPortMarketAdapter


class TestBasicLiveFunctions:
    """基础功能的功能测试"""

    def test_fetch_static_info(self, live_adapter: LongPortMarketAdapter):
        """测试获取单个标的的静态信息"""
        result = live_adapter.fetch_static_info("AAPL.US")

        # 基础验证：确保返回结果正常
        assert result is not None
        assert result.symbol == "AAPL.US"

        # 验证几个核心字段存在且有值
        assert result.name_en and isinstance(result.name_en, str)
        assert result.exchange and isinstance(result.exchange, str)
        assert result.currency in ["CNY", "USD", "SGD", "HKD"]

        print(f"成功获取 {result.symbol} ({result.name_en}) 的静态信息")

    def test_fetch_static_info_batch(self, live_adapter: LongPortMarketAdapter):
        """测试批量获取标的的静态信息"""
        symbols = ["AAPL.US", "MSFT.US", "9988.HK", "600519.SH", "000001.SZ"]
        results = live_adapter.fetch_static_info_batch(symbols)

        # 基础验证：确保返回结果列表正常
        assert results is not None
        assert len(results) > 0

        # 验证每个结果对象都有基本字段
        for item in results:
            assert hasattr(item, "symbol")
            assert hasattr(item, "name_en")

        print(f"成功批量获取了 {len(results)} 个标的的静态信息")

    def test_fetch_quote(self, live_adapter: LongPortMarketAdapter):
        """测试获取单个标的的实时行情"""
        result = live_adapter.fetch_quote("AAPL.US")

        # 基础验证
        assert result is not None
        assert result.symbol == "AAPL.US"

        # 验证行情数据的核心字段
        assert hasattr(result, "last_done")  # 最新价
        assert hasattr(result, "open")  # 开盘价
        assert hasattr(result, "high")  # 最高价
        assert hasattr(result, "low")  # 最低价
        assert hasattr(result, "volume")  # 成交量

        print(f"成功获取 {result.symbol} 的实时行情，最新价: {result.last_done}")

    def test_fetch_quote_batch(self, live_adapter: LongPortMarketAdapter):
        """测试批量获取标的的实时行情"""
        symbols = ["AAPL.US", "MSFT.US", "TSLA.US"]
        results = live_adapter.fetch_quote_batch(symbols)

        # 基础验证
        assert results is not None
        assert len(results) == len(symbols)

        # 验证每个结果都有基本字段
        for result in results:
            assert hasattr(result, "symbol")
            assert hasattr(result, "last_done")
            assert hasattr(result, "volume")

        print(f"成功批量获取了 {len(results)} 个标的的实时行情")

    def test_fetch_depth(self, live_adapter: LongPortMarketAdapter):
        """测试获取标的的盘口深度信息"""
        result = live_adapter.fetch_depth("AAPL.US")

        # 基础验证
        assert result is not None

        # 验证盘口数据字段
        assert hasattr(result, "asks")  # 卖盘
        assert hasattr(result, "bids")  # 买盘

        # 验证买卖盘数据结构
        if result.asks:
            assert len(result.asks) > 0
            assert hasattr(result.asks[0], "price")
            assert hasattr(result.asks[0], "volume")

        if result.bids:
            assert len(result.bids) > 0
            assert hasattr(result.bids[0], "price")
            assert hasattr(result.bids[0], "volume")

        print(f"  买盘档数: {len(result.bids)}, 卖盘档数: {len(result.asks)}")

    def test_fetch_brokers(self, live_adapter: LongPortMarketAdapter):
        """测试获取标的的券商列表"""
        result = live_adapter.fetch_brokers("AAPL.US")

        # 基础验证
        assert result is not None

        # 验证券商数据字段
        assert hasattr(result, "ask_brokers")  # 卖方券商
        assert hasattr(result, "bid_brokers")  # 买方券商

        # 如果有券商信息，验证其结构
        if result.ask_brokers:
            for broker in result.ask_brokers:
                assert hasattr(broker, "broker_ids")
                assert hasattr(broker, "price")

        if result.bid_brokers:
            for broker in result.bid_brokers:
                assert hasattr(broker, "broker_ids")
                assert hasattr(broker, "price")

        print(
            f"买方券商档数: {len(result.bid_brokers)}, 卖方券商档数: {len(result.ask_brokers)}"  # noqa: E501
        )

    def test_fetch_participants(self, live_adapter: LongPortMarketAdapter):
        """测试获取参与者代码列表"""
        result = live_adapter.fetch_participants()

        # 基础验证
        assert result is not None
        assert isinstance(result, list)

        # 如果有参与者信息，验证其结构
        if len(result) > 0:
            participant = result[0]
            assert hasattr(participant, "broker_ids")  # 券商代码列表
            assert hasattr(participant, "name_cn")  # 中文名称
            assert hasattr(participant, "name_en")  # 英文名称
            assert hasattr(participant, "name_hk")  # 繁体中文名称

            print(f"成功获取 {len(result)} 个参与者信息")
            if len(result) > 0:
                print(f"  第一个参与者: {participant.name_en} ({participant.name_cn})")
        else:
            print("当前没有参与者信息")

    def test_fetch_trades(self, live_adapter: LongPortMarketAdapter):
        """测试获取标的的交易请求列表"""
        symbol = "AAPL.US"
        count = 10
        result = live_adapter.fetch_trades(symbol, count)

        # 基础验证
        assert result is not None
        assert isinstance(result, list)

        # 验证交易数据结构
        if len(result) > 0:
            trade = result[0]
            assert hasattr(trade, "price")  # 交易价格
            assert hasattr(trade, "volume")  # 交易量
            assert hasattr(trade, "timestamp")  # 交易时间
            assert hasattr(trade, "trade_type")  # 交易类型

            print(f"成功获取 {symbol} 的 {len(result)} 条交易记录")
            print(f"  最新交易: 价格={trade.price}, 数量={trade.volume}")
        else:
            print(f"当前 {symbol} 没有交易记录")

    def test_fetch_intraday(self, live_adapter: LongPortMarketAdapter):
        """测试获取标的日内分时数据"""
        symbol = "AAPL.US"
        result = live_adapter.fetch_intraday(symbol)

        # 基础验证
        assert result is not None
        assert isinstance(result, list)

        # 验证分时数据结构
        if len(result) > 0:
            intraday_point = result[0]
            assert hasattr(intraday_point, "price")  # 价格
            assert hasattr(intraday_point, "timestamp")  # 时间戳
            assert hasattr(intraday_point, "volume")  # 成交量
            assert hasattr(intraday_point, "turnover")  # 成交额

            print(f"成功获取 {symbol} 的 {len(result)} 个分时数据点")
            print(
                f"  最新数据: 价格={intraday_point.price}, 成交量={intraday_point.volume}"  # noqa: E501
            )
        else:
            print(f"当前 {symbol} 没有分时数据")

    def test_fetch_trading_session(self, live_adapter: LongPortMarketAdapter):
        """测试获取交易时段信息"""
        result = live_adapter.fetch_trading_session()

        # 基础验证
        assert result is not None
        assert isinstance(result, list)

        # 验证交易时段数据结构
        if len(result) > 0:
            session = result[0]
            assert hasattr(session, "market")  # 市场代码
            assert hasattr(session, "trade_sessions")  # 交易时段列表（注意是复数）

            # 验证交易时段的详细信息
            if session.trade_sessions and len(session.trade_sessions) > 0:
                trading_session_info = session.trade_sessions[0]
                assert hasattr(trading_session_info, "begin_time")  # 开始时间
                assert hasattr(trading_session_info, "end_time")  # 结束时间
                assert hasattr(trading_session_info, "trade_session")  # 交易时段类型

                print(f"成功获取 {len(result)} 个市场的交易时段信息")
                print(
                    f"  {session.market} 市场有 {len(session.trade_sessions)} 个交易时段"  # noqa: E501
                )
                print(
                    f"  第一个时段: {trading_session_info.begin_time} - {trading_session_info.end_time}"  # noqa: E501
                )
            else:
                print(f"成功获取 {len(result)} 个市场的交易时段信息")
                print(f"  {session.market} 市场当前无交易时段信息")
        else:
            print("当前没有交易时段信息")

    def test_fetch_trading_days(self, live_adapter: LongPortMarketAdapter):
        """测试获取交易日历"""
        from longport.openapi import Market
        from datetime import date, timedelta

        # 使用最近一个月的日期范围
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        result = live_adapter.fetch_trading_days(Market.US, start_date, end_date)

        # 基础验证
        assert result is not None

        # 验证交易日历结构
        assert hasattr(result, "trading_days")  # 交易日列表
        assert hasattr(result, "half_trading_days")  # 半日交易日列表

        print(f"成功获取美股市场 {start_date} 到 {end_date} 的交易日历")
        print(f"  交易日数量: {len(result.trading_days)}")
        print(f"  半日交易日数量: {len(result.half_trading_days)}")

    def test_fetch_capital_flow(self, live_adapter: LongPortMarketAdapter):
        """测试获取标的的资金流向数据"""
        symbol = "0700.HK"  # 使用港股测试，通常有资金流向数据
        result = live_adapter.fetch_capital_flow(symbol)

        # 基础验证
        assert result is not None
        assert isinstance(result, list)

        # 验证资金流向数据结构
        if len(result) > 0:
            capital_flow = result[0]
            assert hasattr(capital_flow, "inflow")  # 流入资金
            assert hasattr(capital_flow, "timestamp")  # 时间戳

            print(f"成功获取 {symbol} 的 {len(result)} 条资金流向数据")
            print(f"  最新流向: 流入={capital_flow.inflow}")
        else:
            print(f"当前 {symbol} 没有资金流向数据")

    def test_fetch_capital_distribution(self, live_adapter: LongPortMarketAdapter):
        """测试获取标的的资金分布数据"""
        symbol = "0700.HK"  # 使用港股测试
        result = live_adapter.fetch_capital_distribution(symbol)

        # 基础验证
        assert result is not None

        # 验证资金分布响应结构
        assert hasattr(result, "timestamp")  # 时间戳
        assert hasattr(result, "capital_in")  # 流入资金数据
        assert hasattr(result, "capital_out")  # 流出资金数据

        # 验证流入资金分布结构
        if result.capital_in:
            assert hasattr(result.capital_in, "large")  # 大单资金
            assert hasattr(result.capital_in, "medium")  # 中单资金
            assert hasattr(result.capital_in, "small")  # 小单资金

        # 验证流出资金分布结构
        if result.capital_out:
            assert hasattr(result.capital_out, "large")  # 大单资金
            assert hasattr(result.capital_out, "medium")  # 中单资金
            assert hasattr(result.capital_out, "small")  # 小单资金

        print(f"成功获取 {symbol} 的资金分布数据")
        print(f"  时间戳: {result.timestamp}")

        if result.capital_in:
            print(
                f"  流入资金 - 大单: {result.capital_in.large}, "
                f"中单: {result.capital_in.medium}, "
                f"小单: {result.capital_in.small}"
            )

        if result.capital_out:
            print(
                f"  流出资金 - 大单: {result.capital_out.large}, "
                f"中单: {result.capital_out.medium}, "
                f"小单: {result.capital_out.small}"
            )

    def test_fetch_calc_indexes(self, live_adapter: LongPortMarketAdapter):
        """测试获取计算指数"""
        from longport.openapi import CalcIndex

        symbols = ["AAPL.US", "MSFT.US"]
        # 选择几个常用的计算指标
        indexes: list[type[CalcIndex]] = [
            CalcIndex.LastDone,
            CalcIndex.ChangeRate,
            CalcIndex.Volume,
        ]

        result = live_adapter.fetch_calc_indexes(symbols, indexes)

        # 基础验证
        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

        # 验证计算指数数据结构
        for calc_index in result:
            assert hasattr(calc_index, "symbol")  # 标的代码
            assert hasattr(calc_index, "last_done")  # 最新价
            assert hasattr(calc_index, "change_rate")  # 涨跌幅
            assert hasattr(calc_index, "volume")  # 成交量

        print(f"成功获取 {len(symbols)} 个标的的计算指数")
        for calc_index in result:
            print(
                f"  {calc_index.symbol}: 最新价={calc_index.last_done}, 涨跌幅={calc_index.change_rate}"  # noqa: E501
            )

    def test_fetch_candlesticks(self, live_adapter: LongPortMarketAdapter):
        """测试获取标的K线数据"""
        from longport.openapi import Period, AdjustType, TradeSessions

        symbol = "AAPL.US"
        period = Period.Day  # 日线
        count = 10  # 获取10根K线
        adjust_type = AdjustType.NoAdjust  # 不复权
        trade_session = TradeSessions.Intraday  # 交易时段

        result = live_adapter.fetch_candlesticks(
            symbol, period, count, adjust_type, trade_session
        )

        # 基础验证
        assert result is not None
        assert isinstance(result, list)
        assert len(result) <= count  # 返回数量不应超过请求数量

        # 验证K线数据结构
        if len(result) > 0:
            candle = result[0]
            assert hasattr(candle, "close")  # 收盘价
            assert hasattr(candle, "open")  # 开盘价
            assert hasattr(candle, "high")  # 最高价
            assert hasattr(candle, "low")  # 最低价
            assert hasattr(candle, "volume")  # 成交量
            assert hasattr(candle, "timestamp")  # 时间戳

            print(f"成功获取 {symbol} 的 {len(result)} 根K线数据")
            print(
                f"  最新K线: 开={candle.open}, 高={candle.high}, 低={candle.low}, 收={candle.close}"  # noqa: E501
            )
        else:
            print(f"当前 {symbol} 没有K线数据")

    def test_fetch_history_candlesticks_by_date(
        self, live_adapter: LongPortMarketAdapter
    ):
        """测试按日期获取历史K线数据"""
        from longport.openapi import Period, AdjustType, TradeSessions
        from datetime import date, timedelta

        symbol = "AAPL.US"
        period = Period.Day  # 日线
        adjust_type = AdjustType.NoAdjust  # 不复权
        # 获取最近30天的数据
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        trade_sessions = TradeSessions.Intraday

        result = live_adapter.fetch_history_candlesticks_by_date(
            symbol, period, adjust_type, start_date, end_date, trade_sessions
        )

        # 基础验证
        assert result is not None
        assert isinstance(result, list)

        # 验证K线数据结构
        if len(result) > 0:
            candle = result[0]
            assert hasattr(candle, "close")  # 收盘价
            assert hasattr(candle, "open")  # 开盘价
            assert hasattr(candle, "high")  # 最高价
            assert hasattr(candle, "low")  # 最低价
            assert hasattr(candle, "volume")  # 成交量
            assert hasattr(candle, "timestamp")  # 时间戳

            print(
                f"成功获取 {symbol} 从 {start_date} 到 {end_date} 的 {len(result)} 根K线数据"  # noqa: E501
            )
            print(
                f"  最新K线: 开={candle.open}, 高={candle.high}, 低={candle.low}, 收={candle.close}"  # noqa: E501
            )
        else:
            print(f"指定日期范围内 {symbol} 没有K线数据")

    def test_fetch_market_temperature(self, live_adapter: LongPortMarketAdapter):
        """测试获取市场温度"""
        from longport.openapi import Market

        market = Market.US  # 美股市场
        result = live_adapter.fetch_market_temperature(market)

        # 基础验证
        assert result is not None

        # 验证市场温度数据结构
        assert hasattr(result, "temperature")  # 温度值
        assert hasattr(result, "timestamp")  # 时间戳

        # 温度值应该在合理范围内
        assert isinstance(result.temperature, (int, float))

        print(f"成功获取美股市场温度: {result.temperature}")
        print(f"  时间戳: {result.timestamp}")

    def test_fetch_history_market_temperature(
        self, live_adapter: LongPortMarketAdapter
    ):
        """测试获取历史市场温度"""
        from longport.openapi import Market
        from datetime import date, timedelta

        market = Market.US  # 美股市场
        # 获取最近7天的历史温度
        end_date = date.today()
        start_date = end_date - timedelta(days=7)

        result = live_adapter.fetch_history_market_temperature(
            market, start_date, end_date
        )

        # 基础验证
        assert result is not None

        # 验证历史市场温度响应结构
        assert hasattr(result, "granularity")  # 粒度
        assert hasattr(result, "records")  # 温度记录列表

        # 验证温度数据列表
        if result.records and len(result.records) > 0:
            temp_data = result.records[0]
            assert hasattr(temp_data, "temperature")  # 温度值
            assert hasattr(temp_data, "timestamp")  # 时间戳

            print(f"成功获取美股市场从 {start_date} 到 {end_date} 的历史温度数据")
            print(f"  粒度: {result.granularity}")
            print(f"  数据点数量: {len(result.records)}")
            print(f"  最新温度: {temp_data.temperature} (时间: {temp_data.timestamp})")
        else:
            print("指定日期范围内没有美股市场温度数据")
            print(f"  粒度: {result.granularity}")
