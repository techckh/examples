using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.Loader;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.ComponentModel;
using System.Collections;
using Binance.Client.Websocket;
using Binance.Client.Websocket.Client;
using Binance.Client.Websocket.Communicator;
using Binance.Client.Websocket.Subscriptions;
using Binance.Client.Websocket.Websockets;
using Serilog;
using Serilog.Events;
using System.Diagnostics;


namespace WpfAppWebSocket
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        MyInstrument myInstrument = new MyInstrument { Bid=0, Ask=0 };

        private static readonly ManualResetEvent ExitEvent = new ManualResetEvent(false);
        public string MsgText;

        public MainWindow()
        {
            AppDomain.CurrentDomain.ProcessExit += CurrentDomainOnProcessExit;
            AssemblyLoadContext.Default.Unloading += DefaultOnUnloading;
            Console.CancelKeyPress += ConsoleOnCancelKeyPress;

            InitializeComponent();

            this.DataContext = myInstrument;
            var progress = new Progress<Hashtable>();
            progress.ProgressChanged +=
                ((sender, data) => 
                {
                    myInstrument.Bid = Convert.ToDouble(data["Bid"]);
                    myInstrument.Ask = Convert.ToDouble(data["Ask"]);
                    this.OutStatusLog($"{data["text"]}");
                });

            Task slowTask = new Task(() => Initialize2(progress));
            slowTask.Start();

            this.OutStatusLog("started");
        }

        private void InitLogging()
        {
            var executingDir = System.IO.Path.GetDirectoryName(Assembly.GetEntryAssembly().Location);
            var logPath = System.IO.Path.Combine(executingDir, "logs", "verbose.log");

            Log.Logger = new LoggerConfiguration()
                .MinimumLevel.Verbose()
                .WriteTo.File(logPath, rollingInterval: RollingInterval.Day)
                .WriteTo.Console(LogEventLevel.Debug)
                .CreateLogger();
        }

        private void Initialize2(IProgress<Hashtable> progress)
        {
            InitLogging();

            var url = BinanceValues.ApiWebsocketUrl;
            var fUrl = BinanceValues.FuturesApiWebsocketUrl;
            using (var communicator = new BinanceWebsocketCommunicator(url))
            using (var fCommunicator = new BinanceWebsocketCommunicator(fUrl))
            {
                communicator.Name = "Binance-1";
                communicator.ReconnectTimeout = TimeSpan.FromMinutes(10);
                communicator.ReconnectionHappened.Subscribe(type => Log.Information($"Reconnection happened, type: {type}"));

                fCommunicator.Name = "Binance-f";
                fCommunicator.ReconnectTimeout = TimeSpan.FromMinutes(10);
                fCommunicator.ReconnectionHappened.Subscribe(type => Log.Information($"Reconnection happened, type: {type}"));

                using (var client = new BinanceWebsocketClient(communicator))
                using (var fClient = new BinanceWebsocketClient(fCommunicator))
                {
                    SubscribeToStreams(client, communicator, progress);
                    SubscribeToStreams(fClient, communicator, progress);

                    client.SetSubscriptions(
                        //new TradeSubscription("btcusdt"),
                        //new TradeSubscription("ethbtc"),
                        //new TradeSubscription("bnbusdt"),
                        //new AggregateTradeSubscription("bnbusdt"),
                        //new OrderBookPartialSubscription("btcusdt", 5),
                        //new OrderBookPartialSubscription("bnbusdt", 10),
                        //new OrderBookDiffSubscription("btcusdt"),
                        new BookTickerSubscription("btcusdt")
                        //new KlineSubscription("btcusdt", "1m"),
                        //new MiniTickerSubscription("btcusdt")
                    );
                    fClient.SetSubscriptions(new FundingSubscription("btcusdt"));
                    communicator.Start().Wait();
                    fCommunicator.Start().Wait();
                    ExitEvent.WaitOne();
                }
            }           
        }

        private void Initialize()
        {
            var url = BinanceValues.ApiWebsocketUrl;
            var fUrl = BinanceValues.FuturesApiWebsocketUrl;
            using (var communicator = new BinanceWebsocketCommunicator(url))
            using (var fCommunicator = new BinanceWebsocketCommunicator(fUrl))
            {
                communicator.Name = "Binance-1";
                communicator.ReconnectTimeout = TimeSpan.FromMinutes(10);
                communicator.ReconnectionHappened.Subscribe(type =>
                    Log.Information($"Reconnection happened, type: {type}"));

                fCommunicator.Name = "Binance-f";
                fCommunicator.ReconnectTimeout = TimeSpan.FromMinutes(10);
                fCommunicator.ReconnectionHappened.Subscribe(type =>
                    Log.Information($"Reconnection happened, type: {type}"));

                using (var client = new BinanceWebsocketClient(communicator))
                using (var fClient = new BinanceWebsocketClient(fCommunicator))
                {
                    //SubscribeToStreams(client, communicator);
                    //SubscribeToStreams(fClient, communicator);

                    client.SetSubscriptions(
                        new TradeSubscription("btcusdt"),
                        new TradeSubscription("ethbtc"),
                        new TradeSubscription("bnbusdt"),
                        new AggregateTradeSubscription("bnbusdt"),
                        new OrderBookPartialSubscription("btcusdt", 5),
                        new OrderBookPartialSubscription("bnbusdt", 10),
                        new OrderBookDiffSubscription("btcusdt"),
                        new BookTickerSubscription("btcusdt"),
                        new KlineSubscription("btcusdt", "1m"),
                        new MiniTickerSubscription("btcusdt")
                    );

                    fClient.SetSubscriptions(
                        new FundingSubscription("btcusdt"));
                    communicator.Start().Wait();
                    fCommunicator.Start().Wait();

                    ExitEvent.WaitOne();
                }
            }
        }        

        public class MyInstrument : INotifyPropertyChanged
        {
            public event PropertyChangedEventHandler PropertyChanged;

            private string _ticker;

            public string Ticker
            {
                get { return _ticker; }
                set { _ticker = value; }
            }

            private double _bid;
            public double Bid
            {
                get { return _bid; }

                set
                {
                    if (value != _bid)
                    {
                        _bid = value;
                        if (PropertyChanged != null)
                        {
                            PropertyChanged(this, new PropertyChangedEventArgs("Bid"));
                        }
                    }
                }
            }

            private double _ask;
            public double Ask
            {
                get { return _ask; }

                set
                {
                    if (value != _ask)
                    {
                        _ask = value;
                        if (PropertyChanged != null)
                        {
                            PropertyChanged(this, new PropertyChangedEventArgs("Ask"));
                        }
                    }
                }
            }
        }

        public void OutStatusLog(string str)
        {
            this.output.AppendText(str + "\n");
            this.output.ScrollToEnd();
        }

        private void SubscribeToStreams(BinanceWebsocketClient client, IBinanceCommunicator comm, IProgress<Hashtable> progress)
        {
            client.Streams.PongStream.Subscribe(x =>
                Log.Information($"Pong received ({x.Message})"));

            client.Streams.FundingStream.Subscribe(response =>
            {
                var funding = response.Data;
                Log.Information($"Funding: [{funding.Symbol}] rate:[{funding.FundingRate}] " +
                                $"mark price: {funding.MarkPrice} next funding: {funding.NextFundingTime} " +
                                $"index price {funding.IndexPrice}");
            });

            client.Streams.AggregateTradesStream.Subscribe(response =>
            {
                var trade = response.Data;
                Log.Information($"Trade aggreg [{trade.Symbol}] [{trade.Side}] " +
                                $"price: {trade.Price} size: {trade.Quantity}");
            });

            client.Streams.TradesStream.Subscribe(response =>
            {
                var trade = response.Data;
                Log.Information($"Trade normal [{trade.Symbol}] [{trade.Side}] " +
                                $"price: {trade.Price} size: {trade.Quantity}");
            });

            client.Streams.OrderBookPartialStream.Subscribe(response =>
            {
                var ob = response.Data;
                Log.Information($"Order book snapshot [{ob.Symbol}] " +
                                $"bid: {ob.Bids.FirstOrDefault()?.Price:F} " +
                                $"ask: {ob.Asks.FirstOrDefault()?.Price:F}");
                Task.Delay(500).Wait();
                //OrderBookPartialResponse.StreamFakeSnapshot(response.Data, comm);
            });

            client.Streams.OrderBookDiffStream.Subscribe(response =>
            {
                var ob = response.Data;
                /*
                progress.Report($"Order book diff [{ob.Symbol}] " +
                                $"bid: {ob.Bids.FirstOrDefault()?.Price:F} " +
                                $"ask: {ob.Asks.FirstOrDefault()?.Price:F}");
                */
            });

            client.Streams.BookTickerStream.Subscribe(response =>
            {
                var ob = response.Data;
                /*
                progress.Report($"Book ticker [{ob.Symbol}] " +
                                $"Best ask price: {ob.BestAskPrice} " +
                                $"Best ask qty: {ob.BestAskQty} " +
                                $"Best bid price: {ob.BestBidPrice} " +
                                $"Best bid qty: {ob.BestBidQty}");
                */
                var data = new Hashtable();
                data["Bid"] = ob.BestBidPrice;
                data["Ask"] = ob.BestAskPrice;
                data["text"] = $"Book ticker [{ob.Symbol}] " +
                               $"Best ask price: {ob.BestAskPrice} " +
                               $"Best ask qty: {ob.BestAskQty} " +
                               $"Best bid price: {ob.BestBidPrice} " +
                               $"Best bid qty: {ob.BestBidQty}";
                progress.Report(data);
            });

            client.Streams.KlineStream.Subscribe(response =>
            {
                var ob = response.Data;
                /*
                progress.Report($"Kline [{ob.Symbol}] " +
                                $"Kline start time: {ob.StartTime} " +
                                $"Kline close time: {ob.CloseTime} " +
                                $"Interval: {ob.Interval} " +
                                $"First trade ID: {ob.FirstTradeId} " +
                                $"Last trade ID: {ob.LastTradeId} " +
                                $"Open price: {ob.OpenPrice} " +
                                $"Close price: {ob.ClosePrice} " +
                                $"High price: {ob.HighPrice} " +
                                $"Low price: {ob.LowPrice} " +
                                $"Base asset volume: {ob.BaseAssetVolume} " +
                                $"Number of trades: {ob.NumberTrades} " +
                                $"Is this kline closed?: {ob.IsClose} " +
                                $"Quote asset volume: {ob.QuoteAssetVolume} " +
                                $"Taker buy base: {ob.TakerBuyBaseAssetVolume} " +
                                $"Taker buy quote: {ob.TakerBuyQuoteAssetVolume} " +
                                $"Ignore: {ob.Ignore} ");
                */
            });

            
            client.Streams.MiniTickerStream.Subscribe(response =>
            {
                var ob = response.Data;       
                /*
                progress.Report($"Mini-ticker [{ob.Symbol}] " +
                                $"Open price: {ob.OpenPrice} " +
                                $"Close price: {ob.ClosePrice} " +
                                $"High price: {ob.HighPrice} " +
                                $"Low price: {ob.LowPrice} " +
                                $"Base asset volume: {ob.BaseAssetVolume} " +
                                $"Quote asset volume: {ob.QuoteAssetVolume}");
                */
            });
        }

        private static void CurrentDomainOnProcessExit(object sender, EventArgs eventArgs)
        {
            Log.Warning("Exiting process");
            ExitEvent.Set();
        }

        private static void DefaultOnUnloading(AssemblyLoadContext assemblyLoadContext)
        {
            Log.Warning("Unloading process");
            ExitEvent.Set();
        }

        private static void ConsoleOnCancelKeyPress(object sender, ConsoleCancelEventArgs e)
        {
            Log.Warning("Canceling process");
            e.Cancel = true;
            ExitEvent.Set();
        }
    }
}
