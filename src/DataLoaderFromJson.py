import PAMI.extras.dbStats.TransactionalDatabase as stats
from PAMI.frequentPattern.basic import FPGrowth as alg
from scipy.stats import zscore
import pandas as pd

class DataLoaderFromJson:
    def __init__(self, imput_file_link):
        self.imput_file_link = imput_file_link
        
    def load_json(self):
        
    
    def preprocess_and_pattern_miming(self):
        # CSVファイルの読み込み
        df = pd.read_csv(self.imput_file_link)

        # 'weather'列の数値を文字列ラベルに変換
        weather_mapping = {
            1: 'sunny with clouds',
            4: 'clear',
            10: 'rainy'
        }
        df['weather'] = df['weather'].map(weather_mapping)

        # 数値列のみを抽出してz-scoreで正規化
        numeric_cols = df.select_dtypes(include='number').columns
        df[numeric_cols] = df[numeric_cols].apply(zscore)

        # 結果を確認
        print(df.head())

        obj = stats.TransactionalDatabase(self.imput_file_link,sep=',')

        # #execute the class
        obj.run()

        #Printing each of the database statistics
        print(f'Database size : {obj.getDatabaseSize()}')
        print(f'Total number of items : {obj.getTotalNumberOfItems()}')
        # print(f'Database sparsity : {obj.getSparsity()}')
        print(f'Minimum Transaction Size : {obj.getMinimumTransactionLength()}')
        print(f'Average Transaction Size : {obj.getAverageTransactionLength()}')
        print(f'Maximum Transaction Size : {obj.getMaximumTransactionLength()}')
        print(f'Standard Deviation Transaction Size : {obj.getStandardDeviationTransactionLength()}')
        print(f'Variance in Transaction Sizes : {obj.getVarianceTransactionLength()}')

        # pattern mining
        from mlxtend.preprocessing import TransactionEncoder
        from mlxtend.frequent_patterns import apriori

        # 前処理済みデータを想定
        # df['temperature'], df['weather'] がある

        # temperatureを離散化（例: 5段階に分ける場合）
        df['temp_bin'] = pd.qcut(df['temperature'], q=5, labels=False)

        # temperatureとweatherのペアをリスト化
        transactions = df[['temp_bin', 'weather']].astype(str).values.tolist()

        # TransactionEncoderでOne-hotエンコーディング
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

        # Aprioriで頻出パターン抽出
        frequent_patterns = apriori(df_encoded, min_support=5/len(df_encoded), use_colnames=True)
        frequent_patterns = frequent_patterns.sort_values(by='support', ascending=False)

        # itemsets が NaN でなく、かつ要素数が2以上のパターンのみ抽出
        frequent_patterns_filtered = frequent_patterns[
            frequent_patterns['itemsets'].apply(lambda x: len(x) > 1 and all('nan' not in item for item in x))
        ]

        # 結果表示
        print(frequent_patterns_filtered)

        
        # frequent_patterns_filtered の itemsets と support を辞書に変換
        # frozenset(['0', '晴れ']) 形式で格納されているので、文字列に変換してマッピング
        pattern_support_dict = {
            frozenset(itemset): support
            for itemset, support in zip(frequent_patterns_filtered['itemsets'], frequent_patterns_filtered['support'])
        }

        # 各行ごとに support を取得、存在しない場合は 0
        def get_support(row):
            key = frozenset([str(row['temp_bin']), str(row['weather'])])
            return pattern_support_dict.get(key, 0)

        # 新しい列 'support' を追加
        df['support'] = df.apply(get_support, axis=1)

        # 結果確認
        print(df.head())
    
        return df
    