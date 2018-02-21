import pandas as pd
import matplotlib.pylab as plt
from datetime import datetime
import matplotlib.dates as mdates
from scipy.fftpack import fft, ifft
from scipy import signal
import numpy as np
pd.set_option('display.max_columns', 51)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 32}
plt.rc('font', **font)

plt.rcParams.update({'font.size': 16})
datefmt = mdates.DateFormatter('%m%d/%H')

#datefmt = mdates.DateFormatter('%H:%M:%S')

## Features
separator_2nd_features = ["21-PT-10605.PV_Prod_Sep_2nd_Stg (PSIG)",
                          "21-LY-10616.OUT_Prod_Sep_2nd_Stg_Fluid_To_Exch (%)",
                          "21-LT-10618.PV_Prod_Sep_2nd_Stg_Interface (%)",
                          "30-FT-19107-01.PV_2nd_Stg_Hydrocyclone_Inlet (BPD)",
                          "21-LIC-10620.SP_2nd_Stg_Hydrocyclone_Wtr_Out (%)",
                          "21-LT-10620.PV_Prod_Sep_2nd_Stg_Interface (%)",
                          "21-LY-10620.OUT_2nd_Stg_Hydrocyclone_Wtr_Out (%)"
                          ]

separator_2nd_features_1 = [
                           "21-LT-10618.PV_Prod_Sep_2nd_Stg_Interface (%)",
                           "21-LT-10620.PV_Prod_Sep_2nd_Stg_Interface (%)",
                         ]

separator_2nd_features_2 = [
                            "30-FT-19107-01.PV_2nd_Stg_Hydrocyclone_Inlet (BPD)"
                         ]
separator_2nd_features_3 = [
                            "21-LY-10620.OUT_2nd_Stg_Hydrocyclone_Wtr_Out (%)",
                            "30-PDY-19104.OUT_2nd_Stg_Prod_Hydrocyclone_Out (%)"
                         ]


separator_1st_1_features = ["21-PT-10505.PV_Production_Separator (PSIG)",
                            "21-FQI-10518-01.NetRate.PV (BPD)",
                            "21-LIC-10516.SP_Prod_Sep_Oil_Out_To_2nd_Stg_Sep (%)",
                            "21-LIC-40516.SP_Test_Allocation_Sep_Interface (%)",
                            "21-LT-10516.PV_Prod_Sep_Oil_Interface_Level (%)"
                            ]
separator_1st_2_features = ["21-PT-40505.PV_Test_Allocation_Separator (PSIG)",
                            "21-FT-40518-03_Density_(Coriolis) (g/cc)",
                            "21-FT-40518-03_Gross_Volume_Flow_Rate_(Coriolis) (bbl/d)",
                            "21-LIC-40516.SP_Test_Allocation_Sep_Interface (%)",
                            "21-LT-40516.PV_Test_Allocation_Sep_Interface (%)",
                            "21-LY-40516.OUT (%)"
                            ]
heatexchanger_p2_features = ["20-ZT-10204.PV_To/From_Subsea_Flowline (%)",
                             "20-TT-10205.PV_Subsea_Flowline_Test_Sep (Deg.F)",
                             "20-PT-10007-01.PV_Flowline_From_Drill_Center_C (PSIG)"
                             ]
heatexchanger_p1_features = ["20-ZT-10104.PV_To/From_Subsea_Flowline (%)",
                             "20-PT-10008-01.PV_Flowline_From_Drill_Center_C (PSIG)",
                             "20-TT-10105.PV_Subsea_Flowline_To_Train_1 (Deg.F)"
                             ]
heatexchanger_p6_features = ["20-ZT-20104.PV_Train_2_Subsea_Flowline_Launcher (%)",
                             "20-PT-20008-01.PV_Flowline_From_Drill_Centers_B&G (PSIG)",
                             "20-TT-20105.PV_Train_2_Subsea_Flowline_Launcher (Deg.F)"
                             ]
downhole_H_p2_features = ["05-PT-34101-04_H1_Manifold_Pressure (Psi)",
                          "05-TT-34101-04_H1_Manifold_Temperature (DegF)"

                          ]
downhole_H_p1_features = ["05-PT-34101-01_H1_Manifold_Pressure (Psi)",
                          "05-TT-34101-01_H1_Manifold_Temperature (DegF)"
                          ]

downhole_H_p_features = ["05-PT-34101-04_H1_Manifold_Pressure (Psi)",
                         "05-TT-34101-04_H1_Manifold_Temperature (DegF)",
                         "05-PT-34101-01_H1_Manifold_Pressure (Psi)",
                         "05-TT-34101-01_H1_Manifold_Temperature (DegF)"
                         ]

downhole_C_p2_features = ["05-PT-29101-02_C1_Manifold_Pressure (Psi)",
                          "05-TT-29101-02_C1_Manifold_Temperature (DegF)"
                          ]
downhole_C_p1_features = ["05-PT-29101-03_C1_Manifold_Pressure (Psi)",
                          "05-TT-29101-03_C1_Manifold_Temperature (DegF)"
                          ]
downhole_C_p_features = ["05-PT-29101-02_C1_Manifold_Pressure (Psi)",
                         "05-TT-29101-02_C1_Manifold_Temperature (DegF)",
                         "05-PT-29101-03_C1_Manifold_Pressure (Psi)",
                         "05-TT-29101-03_C1_Manifold_Temperature (DegF)"
                         ]

downhole_B_p_features = ["05-PT-28201-01_B2_Manifold_Pressure (Psi)",
                         "05-TT-28201-01_B2_Manifold_Temperature (DegF)",
                         "05-PT-28201-03_B2_Manifold_Pressure (Psi)",
                         "05-TT-28201-03_B2_Manifold_Temperature (DegF)"
                         ]
downhole_G_p_features = ["05-PT-33101-03_G1_Manifold_Pressure (Psi)",
                         "05-TT-33101-03_G1_Manifold_Temperature (DegF)",
                         "05-PT-33101-02_G1_Manifold_Pressure (Psi)",
                         "05-TT-33101-02_G1_Manifold_Temperature (DegF)"
                         ]

downhole_presures =["05-PT-34101-04_H1_Manifold_Pressure (Psi)",
                    "05-PT-34101-01_H1_Manifold_Pressure (Psi)",
                    "05-PT-29101-02_C1_Manifold_Pressure (Psi)",
                    "05-PT-29101-03_C1_Manifold_Pressure (Psi)",
                    "05-PT-28201-01_B2_Manifold_Pressure (Psi)",
                    "05-PT-28201-03_B2_Manifold_Pressure (Psi)",
                    "05-PT-33101-03_G1_Manifold_Pressure (Psi)",
                    "05-PT-33101-02_G1_Manifold_Pressure (Psi)"
]



def downhole_40_removal(df,features):
    for feature in features:
        df.loc[df[feature] < 45, [feature]] = 0
    return df


def time_fft(datetime, y):
    '''
    input: array of datetime object
           y signal
    Output: frequency, ABS(signal)
    '''
    N = len(y)
    y_f = np.fft.fft2(y - np.mean(y))
    y_f = y_f[0:int(N / 2)]  ## Nyquist
    f_max = 1 / ((datetime[1] - datetime[0]).item() / 1e9) / 2
    f = np.linspace(0, f_max, len(y_f))
    return f, abs(y_f)


def lp_butter(y, Wn=0.2):
    n = len(y)
    b, a = signal.butter(4, Wn, 'low')
    output_signal = signal.filtfilt(b, a, y, axis=0)
    return output_signal


def normalize_for_plot(v):
    v_mean = np.mean(v)
    v = v - v_mean
    v_min, v_max = min(v), max(v)
    v = v / max([abs(v_min), abs(v_max)])
    return v


def plot_features(df, start_time, end_time, features, normalized=True, lp_filter=True, legend_on=True):
    '''
    plot the feautres for EDA in different time range
    Feature is suggested to normalize for feature comparison
    '''
    fig, ax = plt.subplots(figsize=(15, 6))
    time_range = (df["Time"] < end_time) & (df["Time"] > start_time)
    x = df.loc[time_range, ["Time"]].values
    level = 0
    for feature in features:
        y = df.loc[time_range, [feature]].values
        if y[0] is None:
            continue
        if lp_filter:
            y = lp_butter(y, 0.06)
        if normalized and np.mean(y) != 0:
            y = normalize_for_plot(y)
        ax.plot(x, y + level, label=feature)
        level = level - 2
    if normalized: ax.set_ylim([level, 2])
    ax.xaxis.set_major_formatter(datefmt)
    if legend_on:
        plt.legend(features, framealpha=0.2, fontsize=12)


def subplot_features(df, start_time, end_time, features1, features2, features3,
                     normalized=False, lp_filter=True):
    '''
    plot the feautres for EDA in different time range
    Feature is suggested to normalize for feature comparison
    '''
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(15, 14))
    time_range = (df["Time"] < end_time) & (df["Time"] > start_time)
    x = df.loc[time_range, ["Time"]].values
    for feature in features1:
        y = df.loc[time_range, [feature]].values
        if y[0] is None:
            continue
        if lp_filter:
            y = lp_butter(y, 0.06)
        if normalized:
            y = normalize_for_plot(y)
        ax1.plot(x, y, label=feature)
    ax1.xaxis.set_major_formatter(datefmt)
    ax1.legend(features1, framealpha=0.2)

    for feature in features2:
        y = df.loc[time_range, [feature]].values
        if y[0] is None:
            continue
        if lp_filter:
            y = lp_butter(y, 0.06)
        if normalized:
            y = normalize_for_plot(y)
        ax2.plot(x, y, label=feature)
    ax2.xaxis.set_major_formatter(datefmt)
    ax2.legend(features2, framealpha=0.2)

    for feature in features3:
        y = df.loc[time_range, [feature]].values
        if y[0] is None:
            continue
        if lp_filter:
            y = lp_butter(y, 0.06)
        if normalized:
            y = normalize_for_plot(y)
        ax3.plot(x, y, label=feature)
    ax3.xaxis.set_major_formatter(datefmt)
    ax3.legend(features3, framealpha=0.2)

