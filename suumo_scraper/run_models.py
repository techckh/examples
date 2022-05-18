import uuid
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import Ridge, HuberRegressor, LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics
from sklearn.model_selection import train_test_split

from scipy.stats import skew, norm, probplot

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping

from utils import one_hot_encode_categorical_cols
from utils import has_null, null_count, plot_simple, plot_values_distribution
from utils import get_mean, get_mode, get_col_names, get_col_dtype


def create_model(info, input_len):
    info['model'] = '1024_mae'
    model = Sequential()
    model.add(Dense(1024, input_dim=input_len, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1))
    #model.add(tf.keras.layers.Lambda(lambda x: (x * 0.4) + 12.02))
    # Compile model
    #model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='mae', metrics=['msle'])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='mae')
    #model.compile(optimizer='adam', loss='mse')
    #model.compile(optimizer='adam', loss='mae')
    #model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae', 'mape'])
    return model


def remove_outliers(info, df):
    info['outliers'] = 'iso'

    clf = IsolationForest(max_samples=100, random_state=42)
    clf.fit(df)
    y_noano = clf.predict(df)
    y_noano = pd.DataFrame(y_noano, columns=['Top'])
    #y_noano[y_noano['Top'] == 1].index.values
    df = df.iloc[y_noano[y_noano['Top'] == 1].index.values]
    print("Number of Outliers:", y_noano[y_noano['Top'] == -1].shape[0])
    print("Number of rows without outliers:", df.shape[0])
    return df


def get_null_cols(df):
    out = list()
    for col in df.columns:
        if df[col].isnull().values.any():
            out.append(col)
    return out


def clean_simple(info, df):
    info['clean'] = 'clean_simple'

    full = df.copy()

    """
    'name', '販売価格', '専有面積', '所在地', 'バルコニー', '沿線・駅', '間取り', '築年月', 'id',
    'ward', 'area', 'subway', 'station', 'walking', 'built_year',
    'built_month'
    """
    # remove columns
    cols_to_remove = ['id', 'name', '所在地', '沿線・駅', '築年月', 'built_month']
    full.drop(cols_to_remove, axis=1, inplace=True)
    full.columns = ['price', 'size', 'balcony', 'config', 'ward', 'area', 'subway', 'station', 'walking', 'built_year']

    return full


def encode_cat_cols(info, full):
    info['encode'] = '1'
    cat_cols = list(full.select_dtypes(include=['object']).columns)
    encoder, full = one_hot_encode_categorical_cols(full, cat_cols)
    return encoder, full


def scale_num_cols(info, df, scaler_type='standard', scaler=None):
    cat_cols = list(df.select_dtypes(include=['object']).columns)
    num_cols = list(df.select_dtypes(include=['number']).columns)
    add_back = list()
    if 'price' in num_cols:
        add_back.append('price')
        num_cols.remove('price')
    if not scaler:
        if scaler_type == 'minmax':
            scaler = MinMaxScaler()
            info['scaler'] = 'minmax'
        else:
            scaler = StandardScaler()
            info['scaler'] = 'standard'
        df_scaled = pd.DataFrame(scaler.fit_transform(df[num_cols]), columns=num_cols)
    else:
        df_scaled = pd.DataFrame(scaler.transform(df[num_cols]), columns=num_cols)
    if add_back:
        cat_cols = cat_cols + add_back
    result = pd.merge(df[cat_cols], df_scaled, left_index=True, right_index=True)
    return scaler, result


def fit_validate_model(info, model, X_train, y_train, trial=False):
    info['fit_val'] = 'val_split_10'

    if trial:
        epoch_count = 3
    else:
        epoch_count = 1000

    # val_loss, val_msle
    monitor = 'val_loss'
    early_stop = EarlyStopping(monitor=monitor,
                               mode='min',
                               verbose=1,
                               patience=20)
    history = model.fit(x=X_train,
                        y=y_train,
                        validation_split=0.1,
                        batch_size=128,
                        epochs=epoch_count,
                        callbacks=[early_stop])
    return history


def save_pipeline_info(info, submission=None):
    rnd_str = str(uuid.uuid4())
    info['id'] = rnd_str
    with open('output/%s_%s.json' % (info['clean'], rnd_str), 'w', encoding='utf8') as f:
        f.write(json.dumps(info, indent=2))
    submission.to_csv('output/%s_%s.csv' % (info['clean'], rnd_str), index=False)


def pipeline_simple(options):
    trial = options['trial']
    scaler_type = options['scaler_type']

    df = pd.read_pickle('20220516_filtered.pkl')

    info = dict()
    df = clean_simple(info, df)
    print(df.shape)

    cat_cols = list(df.select_dtypes(include=['object']).columns)
    num_cols = list(df.select_dtypes(include=['number']).columns)
    assert (len(cat_cols) + len(num_cols)) == len(df.columns), 'error columns count'
    print(len(cat_cols))
    print(len(num_cols))
    print(len(df.columns))

    #ids = df_test['id'].values

    scaler, df = scale_num_cols(info, df, scaler_type=scaler_type)
    print(df.shape)

    encoder, df = encode_cat_cols(info, df)
    print(df.shape)

    df = remove_outliers(info, df)

    assert df.isnull().values.any() == False, 'df still has null values'
    assert 'price' in df.columns, 'missing price column'

    X = df.drop(['price'], axis=1).values
    y = df['price'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print(X_train.shape)
    print(X_test.shape)

    model = create_model(info, X_train.shape[1])
    history = fit_validate_model(info, model, X_train, y_train, trial=trial)
    epoch_count = len(history.epoch)
    info['epoch_count'] = epoch_count

    model = create_model(info, X_train.shape[1])
    history = model.fit(x=X_train,
                        y=y_train,
                        batch_size=128,
                        epochs=epoch_count)

    eval = model.evaluate(X_train, y_train)
    print(eval)

    y_test_pred = model.predict(X_test)
    print(y_test_pred.shape)
    print('stats on predicting testing set:')
    print('Mean Absolute Error: {:.2f}'.format(metrics.mean_absolute_error(y_test, y_test_pred)))
    print('Mean Squared Error: {:.2f}'.format(metrics.mean_squared_error(y_test, y_test_pred)))
    print('Root Mean Squared Error: {:.2f}'.format(np.sqrt(metrics.mean_squared_error(y_test, y_test_pred))))
    print('Variance score is: {:.2f}'.format(metrics.explained_variance_score(y_test, y_test_pred)))
    print('\n\n')

    y_pred = model.predict(X_train)
    print('stats on predicting training set:')
    print('Mean Absolute Error: {:.2f}'.format(metrics.mean_absolute_error(y_train, y_pred)))
    print('Mean Squared Error: {:.2f}'.format(metrics.mean_squared_error(y_train, y_pred)))
    print('Root Mean Squared Error: {:.2f}'.format(np.sqrt(metrics.mean_squared_error(y_train, y_pred))))
    print('Variance score is: {:.2f}'.format(metrics.explained_variance_score(y_train, y_pred)))
    info['var_score'] = '{:.5f}'.format(metrics.explained_variance_score(y_train, y_pred))

    """
    rnd_str = str(uuid.uuid4())
    info['id'] = rnd_str    
    with open('output/%s_%s.json' % (info['clean'], rnd_str), 'w', encoding='utf8') as f:
        f.write(json.dumps(info, indent=2))
    """
    print(info)


if __name__ == '__main__':

    trial = True
    #scaler_types = ['minmax', 'standard']
    scaler_types = ['standard']

    for scaler_type in scaler_types:
        options = dict()

        options['scaler_type'] = scaler_type
        options['trial'] = trial
        pipeline_simple(options)
