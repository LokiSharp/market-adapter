import time
from typing import List, TYPE_CHECKING, Type
from modules.long_port_market_adapter import LongPortMarketAdapter

if TYPE_CHECKING:
    from longport.openapi import SecurityQuote, SecurityStaticInfo


class TestPerformance:
    """性能相关的功能测试"""

    def test_batch_query_performance(self, live_adapter: LongPortMarketAdapter):
        """测试批量查询性能"""
        symbols_single = [
            # 美股 (8支)
            "AAPL.US",  # 苹果
            "MSFT.US",  # 微软
            "GOOG.US",  # Alphabet
            "AMZN.US",  # 亚马逊
            "META.US",  # Meta
            "NFLX.US",  # Netflix
            "INTC.US",  # 英特尔
            "AMD.US",  # AMD
            # 港股 (6支)
            "9988.HK",  # 阿里巴巴
            "0700.HK",  # 腾讯
            "1299.HK",  # 友邦保险
            "3690.HK",  # 美团
            "0388.HK",  # 香港交易所
            "2318.HK",  # 中国平安
            # A股 (6支)
            "600519.SH",  # 贵州茅台
            "601398.SH",  # 工商银行
            "000333.SZ",  # 美的集团
            "600036.SH",  # 招商银行
            "601888.SH",  # 中国中免
            "300059.SZ",  # 东方财富
        ]

        symbols_batch = [
            # 美股 (8支)
            "TSLA.US",  # 特斯拉
            "NVDA.US",  # 英伟达
            "JPM.US",  # 摩根大通
            "V.US",  # Visa
            "PG.US",  # 宝洁
            "DIS.US",  # 迪士尼
            "KO.US",  # 可口可乐
            "PFE.US",  # 辉瑞制药
            # 港股 (6支)
            "0941.HK",  # 中国移动
            "1398.HK",  # 工商银行
            "0005.HK",  # 汇丰控股
            "0883.HK",  # 中国海洋石油
            "1177.HK",  # 中国生物制药
            "0027.HK",  # 银河娱乐
            # A股 (6支)
            "601318.SH",  # 中国平安
            "000858.SZ",  # 五粮液
            "002594.SZ",  # 比亚迪
            "600276.SH",  # 恒瑞医药
            "601166.SH",  # 兴业银行
            "000001.SZ",  # 平安银行
        ]

        # 先进行预热调用
        _ = live_adapter.fetch_quote("AAPL.US")
        _ = live_adapter.fetch_quote_batch(["TSLA.US"])

        print("开始测试股票的查询性能...")

        # 测量单个查询总时间
        start_single = time.time()
        single_results: List[SecurityQuote | None] = []
        for symbol in symbols_single:
            result = live_adapter.fetch_quote(symbol)
            single_results.append(result)
        end_single = time.time()
        single_query_time = end_single - start_single

        # 测量批量查询时间
        start_batch = time.time()
        batch_results = live_adapter.fetch_quote_batch(symbols_batch)
        end_batch = time.time()
        batch_query_time = end_batch - start_batch

        # 打印性能比较信息
        print(f"单个查询总时间: {single_query_time:.4f}秒")
        print(f"批量查询时间: {batch_query_time:.4f}秒")
        print(f"性能提升: {(single_query_time / batch_query_time):.2f}倍")
        print(f"单个平均时间: {single_query_time / len(symbols_single):.4f}秒/股票")
        print(f"批量平均时间: {batch_query_time / len(symbols_batch):.4f}秒/股票")

        # 确保所有结果都有效
        assert len(single_results) == len(symbols_single)
        assert len(batch_results) == len(symbols_batch)

        # 批量查询应该明显快于单个查询
        assert batch_query_time < single_query_time, (
            f"批量查询({batch_query_time:.4f}秒)应该比单个查询({single_query_time:.4f}秒)快"
        )

    def test_static_info_batch_performance(self, live_adapter: LongPortMarketAdapter):
        """测试静态信息批量查询性能"""
        symbols_single = [
            # 美股 (6支)
            "AAPL.US",  # 苹果
            "MSFT.US",  # 微软
            "GOOG.US",  # Alphabet
            "AMZN.US",  # 亚马逊
            "META.US",  # Meta
            "NFLX.US",  # Netflix
            # 港股 (4支)
            "9988.HK",  # 阿里巴巴
            "0700.HK",  # 腾讯
            "1299.HK",  # 友邦保险
            "3690.HK",  # 美团
            # A股 (4支)
            "600519.SH",  # 贵州茅台
            "601398.SH",  # 工商银行
            "000333.SZ",  # 美的集团
            "600036.SH",  # 招商银行
        ]

        symbols_batch = [
            # 美股 (6支)
            "TSLA.US",  # 特斯拉
            "NVDA.US",  # 英伟达
            "JPM.US",  # 摩根大通
            "V.US",  # Visa
            "PG.US",  # 宝洁
            "DIS.US",  # 迪士尼
            # 港股 (4支)
            "0941.HK",  # 中国移动
            "1398.HK",  # 工商银行
            "0005.HK",  # 汇丰控股
            "0883.HK",  # 中国海洋石油
            # A股 (4支)
            "601318.SH",  # 中国平安
            "000858.SZ",  # 五粮液
            "002594.SZ",  # 比亚迪
            "600276.SH",  # 恒瑞医药
        ]

        # 先进行预热调用
        _ = live_adapter.fetch_static_info("AAPL.US")
        _ = live_adapter.fetch_static_info_batch(["TSLA.US"])

        print("开始测试静态信息的查询性能...")

        # 测量单个查询总时间
        start_single = time.time()
        single_results: list[SecurityStaticInfo | None] = []
        for symbol in symbols_single:
            result = live_adapter.fetch_static_info(symbol)
            single_results.append(result)
        end_single = time.time()
        single_query_time = end_single - start_single

        # 测量批量查询时间
        start_batch = time.time()
        batch_results = live_adapter.fetch_static_info_batch(symbols_batch)
        end_batch = time.time()
        batch_query_time = end_batch - start_batch

        # 打印性能比较信息
        print(f"单个查询总时间: {single_query_time:.4f}秒")
        print(f"批量查询时间: {batch_query_time:.4f}秒")
        print(f"性能提升: {(single_query_time / batch_query_time):.2f}倍")
        print(f"单个平均时间: {single_query_time / len(symbols_single):.4f}秒/股票")
        print(f"批量平均时间: {batch_query_time / len(symbols_batch):.4f}秒/股票")

        # 确保所有结果都有效
        assert len(single_results) == len(symbols_single)
        assert len(batch_results) == len(symbols_batch)

        # 批量查询应该明显快于单个查询
        assert batch_query_time < single_query_time, (
            f"批量查询({batch_query_time:.4f}秒)应该比单个查询({single_query_time:.4f}秒)快"
        )

    def test_history_candlesticks_performance(
        self, live_adapter: LongPortMarketAdapter
    ):
        """测试历史K线查询性能 - 不同时间范围"""
        from longport.openapi import Period, AdjustType, TradeSessions
        from datetime import date, timedelta

        symbol = "AAPL.US"
        period = Period.Day
        adjust_type = AdjustType.NoAdjust
        trade_sessions = TradeSessions.Intraday

        today = date.today()

        # 定义不同的时间范围
        time_ranges = [
            ("1个月", today - timedelta(days=30), today),
            ("3个月", today - timedelta(days=90), today),
            ("6个月", today - timedelta(days=180), today),
            ("1年", today - timedelta(days=365), today),
        ]

        print(f"开始测试 {symbol} 历史K线查询性能...")

        query_times: list[float] = []
        data_counts: list[int] = []

        for range_name, start_date, end_date in time_ranges:
            # 预热
            _ = live_adapter.fetch_history_candlesticks_by_date(
                symbol, period, adjust_type, start_date, end_date, trade_sessions
            )

            # 测量查询时间
            start_time = time.time()
            result = live_adapter.fetch_history_candlesticks_by_date(
                symbol, period, adjust_type, start_date, end_date, trade_sessions
            )
            end_time = time.time()

            query_time = end_time - start_time
            data_count = len(result) if result else 0

            query_times.append(query_time)
            data_counts.append(data_count)

            print(f"  {range_name}: {query_time:.4f}秒, 数据量: {data_count}条")

        # 验证查询时间随数据量增长的合理性
        # 通常来说，更长时间范围的查询时间应该不会显著增加（因为服务器端优化）
        max_time = max(query_times)
        min_time = min(query_times)

        print(f"最快查询: {min_time:.4f}秒")
        print(f"最慢查询: {max_time:.4f}秒")
        print(f"时间差异倍数: {(max_time / min_time):.2f}倍")

        # 验证所有查询都在合理时间内完成（比如10秒以内）
        assert max_time < 10.0, f"最慢查询时间({max_time:.4f}秒)超过10秒限制"

        # 验证查询成功
        assert all(count > 0 for count in data_counts), "所有时间范围都应该有数据返回"

    def test_different_period_candlesticks_performance(
        self, live_adapter: LongPortMarketAdapter
    ):
        """测试不同K线周期性能差异"""
        from longport.openapi import Period, AdjustType, TradeSessions
        from datetime import date, timedelta

        symbol = "AAPL.US"
        adjust_type = AdjustType.NoAdjust
        trade_sessions = TradeSessions.Intraday

        # 使用相同的时间范围（最近30天）
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        # 测试不同的K线周期
        periods: list[tuple[str, Type[Period]]] = [
            ("分钟线", Period.Min_1),
            ("5分钟线", Period.Min_5),
            ("15分钟线", Period.Min_15),
            ("30分钟线", Period.Min_30),
            ("60分钟线", Period.Min_60),
            ("日线", Period.Day),
        ]

        print(f"开始测试 {symbol} 不同K线周期性能差异...")

        for period_name, period in periods:
            # 预热
            _ = live_adapter.fetch_history_candlesticks_by_date(
                symbol, period, adjust_type, start_date, end_date, trade_sessions
            )

            # 测量查询时间
            start_time = time.time()
            result = live_adapter.fetch_history_candlesticks_by_date(
                symbol, period, adjust_type, start_date, end_date, trade_sessions
            )
            end_time = time.time()

            query_time = end_time - start_time
            data_count = len(result) if result else 0

            print(f"  {period_name}: {query_time:.4f}秒, 数据量: {data_count}条")

            # 验证查询成功且在合理时间内
            assert query_time < 5.0, (
                f"{period_name}查询时间({query_time:.4f}秒)超过5秒限制"
            )

            # 分钟级别的数据量应该比日线多
            if period_name == "分钟线":
                assert data_count > 100, f"分钟线数据量({data_count})似乎过少"
            elif period_name == "日线":
                assert data_count < 50, f"日线数据量({data_count})似乎过多"

    def test_realtime_data_latency(self, live_adapter: LongPortMarketAdapter):
        """测试实时数据查询延迟"""
        # 选择几个活跃的股票进行测试
        symbols = [
            "AAPL.US",  # 美股 - 苹果
            "TSLA.US",  # 美股 - 特斯拉
            "0700.HK",  # 港股 - 腾讯
            "9988.HK",  # 港股 - 阿里巴巴
            "600519.SH",  # A股 - 贵州茅台
            "000858.SZ",  # A股 - 五粮液
        ]

        print("开始测试实时数据查询延迟...")

        # 测试各种实时数据接口的响应时间
        methods_to_test = [
            ("实时报价", "fetch_quote"),
            ("五档深度", "fetch_depth"),
            ("成交记录", "fetch_trades"),
        ]

        for method_name, method_attr in methods_to_test:
            print(f"\n测试 {method_name} 延迟:")
            latencies: list[float] = []

            for symbol in symbols:
                # 预热调用
                method = getattr(live_adapter, method_attr)
                if method_attr == "fetch_trades":
                    _ = method(symbol, 5)  # 获取5条成交记录用于预热
                else:
                    _ = method(symbol)

                # 多次测量取平均值
                symbol_latencies: list[float] = []
                for _ in range(3):  # 每个股票测试3次
                    start_time = time.time()
                    if method_attr == "fetch_trades":
                        result = method(symbol, 10)  # 获取10条成交记录
                    else:
                        result = method(symbol)
                    end_time = time.time()

                    latency = (end_time - start_time) * 1000  # 转换为毫秒
                    symbol_latencies.append(latency)

                    # 验证查询成功
                    assert result is not None, f"{method_name} 查询 {symbol} 失败"

                avg_latency = sum(symbol_latencies) / len(symbol_latencies)
                latencies.append(avg_latency)
                print(f"  {symbol}: {avg_latency:.2f}ms")

            # 计算总体统计
            overall_avg = sum(latencies) / len(latencies)
            max_latency = max(latencies)
            min_latency = min(latencies)

            print(f"  平均延迟: {overall_avg:.2f}ms")
            print(f"  最大延迟: {max_latency:.2f}ms")
            print(f"  最小延迟: {min_latency:.2f}ms")

            # 延迟验证 - 实时数据应该在1秒内返回
            assert max_latency < 1000, (
                f"{method_name} 最大延迟({max_latency:.2f}ms)超过1秒限制"
            )

            # 平均延迟应该在500ms以内
            assert overall_avg < 500, (
                f"{method_name} 平均延迟({overall_avg:.2f}ms)超过500ms限制"
            )

    def test_concurrent_query_performance(self, live_adapter: LongPortMarketAdapter):
        """测试并发查询性能"""
        import concurrent.futures

        symbols = [
            "AAPL.US",
            "MSFT.US",
            "GOOG.US",
            "AMZN.US",
            "0700.HK",
            "9988.HK",
            "1299.HK",
            "3690.HK",
            "600519.SH",
            "601398.SH",
            "000333.SZ",
            "600036.SH",
        ]

        print("开始测试并发查询性能...")

        def query_single_symbol(symbol: str) -> tuple[str, float, bool]:
            """查询单个股票，返回股票代码、耗时和是否成功"""
            start_time = time.time()
            try:
                result = live_adapter.fetch_quote(symbol)
                end_time = time.time()
                return symbol, (end_time - start_time) * 1000, result is not None
            except Exception as e:
                end_time = time.time()
                print(f"查询 {symbol} 出错: {e}")
                return symbol, (end_time - start_time) * 1000, False

        # 测试不同的并发级别
        concurrency_levels = [1, 2, 4, 6, 8]

        for max_workers in concurrency_levels:
            print(f"\n测试并发级别: {max_workers}")

            # 预热
            _ = live_adapter.fetch_quote("AAPL.US")

            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                futures = [
                    executor.submit(query_single_symbol, symbol) for symbol in symbols
                ]
                results = [
                    future.result()
                    for future in concurrent.futures.as_completed(futures)
                ]
            end_time = time.time()

            total_time = (end_time - start_time) * 1000  # 转换为毫秒
            successful_queries = sum(1 for _, _, success in results if success)
            failed_queries = len(results) - successful_queries

            avg_query_time = sum(query_time for _, query_time, _ in results) / len(
                results
            )

            print(f"  总耗时: {total_time:.2f}ms")
            print(f"  成功查询: {successful_queries}/{len(symbols)}")
            print(f"  失败查询: {failed_queries}")
            print(f"  平均单次查询时间: {avg_query_time:.2f}ms")
            print(f"  吞吐量: {(len(symbols) / (total_time / 1000)):.2f} queries/sec")

            # 验证大部分查询都成功
            success_rate = successful_queries / len(symbols)
            assert success_rate >= 0.8, f"成功率({success_rate:.2%})低于80%"

            # 验证总时间在合理范围内
            assert total_time < 10000, f"总查询时间({total_time:.2f}ms)超过10秒"

    def test_api_rate_limit_behavior(self, live_adapter: LongPortMarketAdapter):
        """测试API速率限制行为"""
        print("开始测试API速率限制行为...")

        symbol = "AAPL.US"
        request_count = 50  # 快速发送50个请求

        print(f"快速发送 {request_count} 个查询请求...")

        start_time = time.time()
        successful_requests = 0
        failed_requests = 0
        response_times: list[float] = []

        for i in range(request_count):
            request_start = time.time()
            try:
                result = live_adapter.fetch_quote(symbol)
                request_end = time.time()

                if result is not None:
                    successful_requests += 1
                else:
                    failed_requests += 1

                response_time = (request_end - request_start) * 1000
                response_times.append(response_time)

                if i % 10 == 0:  # 每10个请求打印一次进度
                    print(f"  已完成 {i + 1}/{request_count} 个请求")

            except Exception as e:
                request_end = time.time()
                failed_requests += 1
                response_time = (request_end - request_start) * 1000
                response_times.append(response_time)
                print(f"  请求 {i + 1} 失败: {e}")

        end_time = time.time()
        total_time = (end_time - start_time) * 1000

        # 统计结果
        avg_response_time = (
            sum(response_times) / len(response_times) if response_times else 0
        )
        max_response_time = max(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0

        print("\n速率限制测试结果:")
        print(f"  总耗时: {total_time:.2f}ms")
        print(f"  成功请求: {successful_requests}")
        print(f"  失败请求: {failed_requests}")
        print(f"  成功率: {(successful_requests / request_count):.2%}")
        print(f"  平均响应时间: {avg_response_time:.2f}ms")
        print(f"  最大响应时间: {max_response_time:.2f}ms")
        print(f"  最小响应时间: {min_response_time:.2f}ms")
        print(f"  实际QPS: {(request_count / (total_time / 1000)):.2f}")

        # 验证基本的服务可用性
        # 即使有速率限制，也应该有一定比例的请求成功
        success_rate = successful_requests / request_count
        assert success_rate >= 0.5, f"成功率({success_rate:.2%})过低，API可能有问题"

        # 如果有失败请求，通常是因为速率限制，响应时间应该相对较快
        if failed_requests > 0:
            print(f"  检测到 {failed_requests} 个失败请求，可能触发了速率限制")

    def test_data_freshness_check(self, live_adapter: LongPortMarketAdapter):
        """测试数据新鲜度检查"""
        from datetime import datetime, timezone
        import time as time_module

        print("开始测试数据新鲜度...")

        # 选择几个活跃市场的股票
        symbols = [
            "AAPL.US",  # 美股
            "0700.HK",  # 港股
            "600519.SH",  # A股
        ]

        # 使用本地时间和 UTC 时间进行对比
        current_time_utc = datetime.now(timezone.utc)
        current_time_local = datetime.now()
        current_timestamp = time_module.time()

        print(f"当前 UTC 时间: {current_time_utc}")
        print(f"当前本地时间: {current_time_local}")
        print(f"当前时间戳: {current_timestamp}")

        for symbol in symbols:
            print(f"\n检查 {symbol} 的数据新鲜度:")

            # 测试实时报价数据
            start_time = time.time()
            quote = live_adapter.fetch_quote(symbol)
            query_time = (time.time() - start_time) * 1000

            if quote and hasattr(quote, "timestamp"):
                data_time = quote.timestamp

                print(f"  原始数据时间: {data_time} (类型: {type(data_time)})")
                print(f"  数据时间是否有时区: {data_time.tzinfo is not None}")

                # 更谨慎的时间处理
                if isinstance(data_time, datetime): # type: ignore
                    if data_time.tzinfo is None:
                        # 如果是 naive datetime，尝试多种假设
                        print("  数据时间为 naive datetime，尝试不同时区假设:")

                        # 假设1: 数据时间是 UTC
                        data_time_utc = data_time.replace(tzinfo=timezone.utc)
                        time_diff_utc = (
                            current_time_utc - data_time_utc
                        ).total_seconds()
                        print(f"    假设为UTC: 时间差 {time_diff_utc:.2f}秒")

                        # 假设2: 数据时间是本地时间
                        time_diff_local = float("inf")  # 初始化为无穷大
                        if current_time_local.tzinfo is None:
                            time_diff_local = (
                                current_time_local - data_time
                            ).total_seconds()
                            print(f"    假设为本地时间: 时间差 {time_diff_local:.2f}秒")
                        else:
                            print("    本地时间有时区信息，跳过本地时间假设")

                        # 选择更合理的时间差（绝对值较小的）
                        if abs(time_diff_utc) < abs(time_diff_local):
                            time_diff = time_diff_utc
                            used_assumption = "UTC"
                            final_data_time = data_time_utc
                        else:
                            time_diff = time_diff_local
                            used_assumption = "本地时间"
                            final_data_time = data_time
                    else:
                        # 如果有时区信息，直接计算
                        time_diff = (current_time_utc - data_time).total_seconds()
                        used_assumption = "原有时区"
                        final_data_time = data_time
                else:
                    # 如果不是 datetime 对象，可能是时间戳
                    print(f"  数据时间不是 datetime 对象: {type(data_time)}")
                    continue

                print(f"  查询耗时: {query_time:.2f}ms")
                print(f"  使用假设: {used_assumption}")
                print(f"  最终数据时间: {final_data_time}")
                print(f"  当前时间: {current_time_utc}")
                print(f"  时间差: {time_diff:.2f}秒")

                # 更宽松的数据新鲜度验证
                abs_time_diff = abs(time_diff)

                # 根据不同市场调整时间容忍度
                if symbol.endswith(".US"):
                    # 美股：考虑交易时间
                    max_allowed_diff = 24 * 3600  # 24小时
                elif symbol.endswith(".HK"):
                    # 港股：考虑交易时间
                    max_allowed_diff = 12 * 3600  # 12小时
                elif symbol.endswith((".SH", ".SZ")):
                    # A股：考虑交易时间，周末数据可能较旧
                    max_allowed_diff = 7 * 24 * 3600  # 7天（包含周末）
                else:
                    max_allowed_diff = 24 * 3600  # 默认24小时

                # 验证数据时间在合理范围内
                assert abs_time_diff < max_allowed_diff, (
                    f"{symbol} 数据时间异常，时间差: {time_diff:.2f}秒，"
                    f"超过允许范围({max_allowed_diff}秒)"
                )

                # 验证查询响应时间合理
                assert query_time < 2000, f"{symbol} 查询耗时过长: {query_time:.2f}ms"

                # 打印数据新鲜度评估
                if abs_time_diff < 300:  # 5分钟内
                    freshness = "非常新鲜"
                elif abs_time_diff < 1800:  # 30分钟内
                    freshness = "新鲜"
                elif abs_time_diff < 3600:  # 1小时内
                    freshness = "较新鲜"
                elif abs_time_diff < 7200:  # 2小时内
                    freshness = "一般"
                else:
                    freshness = "较旧"

                print(f"  数据新鲜度: {freshness}")

            else:
                print(f"  {symbol} 无法获取有效的时间戳数据")
                # 至少验证能获取到数据
                assert quote is not None, f"无法获取 {symbol} 的报价数据"
