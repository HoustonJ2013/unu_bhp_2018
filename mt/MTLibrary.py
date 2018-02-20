

## Feature selection based on PFD map
## From downstream to upstream. Please check the map for the corresponding location

#df2
separator_2nd_stage_train1_features = ["21-PT-10605.PV_Prod_Sep_2nd_Stg (PSIG)",
                        "21-LY-10616.OUT_Prod_Sep_2nd_Stg_Fluid_To_Exch (%)",
                        "21-LT-10618.PV_Prod_Sep_2nd_Stg_Interface (%)",
                        "30-FT-19107-01.PV_2nd_Stg_Hydrocyclone_Inlet (BPD)",
                        "21-LIC-10620.CV_2nd_Stg_Hydrocyclone_Wtr_Out (%)",
                        "21-LIC-10620.SP_2nd_Stg_Hydrocyclone_Wtr_Out (%)",
                        "21-LT-10620.PV_Prod_Sep_2nd_Stg_Interface (%)",
                        "21-LY-10620.OUT_2nd_Stg_Hydrocyclone_Wtr_Out (%)"
                         ]
#df2
prod_separator_train_1_features = ["21-PT-10505.PV_Production_Separator (PSIG)",
                            "21-FQI-10518-01.NetRate.PV (BPD)",
                            "21-LIC-40516.SP_Test_Allocation_Sep_Interface (%)",
                            "21-LT-40516.PV_Test_Allocation_Sep_Interface (%)",
                            "21-LY-40516.OUT (%)",
                            "21-LIC-10516.SP_Prod_Sep_Oil_Out_To_2nd_Stg_Sep (%)",
                            "21-LT-10516.PV_Prod_Sep_Oil_Interface_Level (%)",
                            "21-LY-10516.OUT_Prod_Sep_Oil_Out_To_2nd_Stg_Sep (%)"
                           ]

#df2
test_separator_features =  ["21-PT-40505.PV_Test_Allocation_Separator (PSIG)",
                            "21-FT-40518-03_Density_(Coriolis) (g/cc)",
                            "21-FT-40518-03_Gross_Volume_Flow_Rate_(Coriolis) (bbl/d)",
                            "21-LIC-40516.SP_Test_Allocation_Sep_Interface (%)",
                            "21-LT-40516.PV_Test_Allocation_Sep_Interface (%)",
                            "21-LY-40516.OUT (%)"
                            ]

#df2
flotation_cell_features =  ["30-PT-69512.PV (psig)",
                            "30-LIC-69518.CV_Flotation_Cell_Prod_Wtr_To_Ovbrd (%)",
                            "30-LT-69518.PV_Flotation_Cell (%)",
                            "30-LY-69518.OUT_Flotation_Cell_Prod_Wtr_To_Ovbrd (%)",
                            "30-FT-69521-01.PV_Flotation_Cell_Prod_Wtr_To_Ovbrd (BPD)"
                            ]

#df1 20-FAA-1020
heatexchanger_p2_features = ["20-ZT-10204.PV_To/From_Subsea_Flowline (%)",
                            "20-TT-10205.PV_Subsea_Flowline_Test_Sep (Deg.F)",
                            "20-PT-10007-01.PV_Flowline_From_Drill_Center_C (PSIG)"
                            ]
#df1 20-FAA-1010
heatexchanger_p1_features = ["20-ZT-10104.PV_To/From_Subsea_Flowline (%)",
                            "20-PT-10008-01.PV_Flowline_From_Drill_Center_C (PSIG)",
                            "20-TT-10105.PV_Subsea_Flowline_To_Train_1 (Deg.F)"
                            ]

#receives flow from P5.
#nb: control valves DBB-21-36, DBB-21-37 have no record.
#df1
heatexchanger_p5_features = ["2024 20-ZT-20204.PV_Train_2_Subsea_Flowline_Receiver (%)",
                             "20-PT-20007-01.PV_Flowline_From_Drill_Centers_B&G (PSIG)",
                             "20-TT-20205.PV_Train_2_Subsea_Flowline_Receiver (Deg.F)",
                             "20-HX-20003.Status_Flowline_From_Drill_Centers_B&G ( )"
                            ]
#
heatexchanger_p6_features = ["20-ZT-20104.PV_Train_2_Subsea_Flowline_Launcher (%)",
                            "20-PT-20008-01.PV_Flowline_From_Drill_Centers_B&G (PSIG)",
                            "20-TT-20105.PV_Train_2_Subsea_Flowline_Launcher (Deg.F)"
                            ]

#df1
downhole_H_p2_features = ["05-PT-34101-04_H1_Manifold_Pressure (Psi)",
                          "05-TT-34101-04_H1_Manifold_Temperature (DegF)"

                      ]

#df1
downhole_H_p1_features = ["05-PT-34101-01_H1_Manifold_Pressure (Psi)",
                          "05-TT-34101-01_H1_Manifold_Temperature (DegF)"
                      ]


#df1
downhole_C_p2_features = ["05-PT-29101-02_C1_Manifold_Pressure (Psi)",
                          "05-TT-29101-02_C1_Manifold_Temperature (DegF)"
                      ]

#df1
downhole_C_p1_features = ["05-PT-29101-03_C1_Manifold_Pressure (Psi)",
                          "05-TT-29101-03_C1_Manifold_Temperature (DegF)"
                      ]

#df1
downhole_B_p6_features = ["05-PT-28201-01_B2_Manifold_Pressure (Psi)",
                          "05-TT-28201-01_B2_Manifold_Temperature (DegF)"
                      ]

#df1
downhole_G_p6_features = ["05-PT-33101-03_G1_Manifold_Pressure (Psi)",
                          "05-TT-33101-03_G1_Manifold_Temperature (DegF)"
                      ]

#df2
#21-FQI-10518-01.NetRate.PV (BPD) : flowrate from production separator
#21-FT-40518-03_Gross_Volume_Flow_Rate_(Coriolis) (bbl/d) : flowrate from test separator
#30-FT-19107-01.PV_2nd_Stg_Hydrocyclone_Inlet (BPD) : flow from 2nd stage separator to hydrocyclone
#30-FT-69521-01.PV_Flotation_Cell_Prod_Wtr_To_Ovbrd (BPD) : from flotation cell to overboard
flow_features       =  ["21-FQI-10518-01.NetRate.PV (BPD)",
                        "21-FT-40518-03_Gross_Volume_Flow_Rate_(Coriolis) (bbl/d)",
                        "30-FT-19107-01.PV_2nd_Stg_Hydrocyclone_Inlet (BPD)",
                        "30-FT-19108.PV ( )",
                        "30-FT-29108.PV (BPD)",
                        "30-FT-69521-01.PV_Flotation_Cell_Prod_Wtr_To_Ovbrd (BPD)"
                        ]


## Super important Feature to analyze and identify excursion event.
## Level indicator 21-LT-10618.PV_Prod_Sep_2nd_Stg_Interface (%) doesn't drop as much as
## Level indicator 21-LT-10620.PV_Prod_Sep_2nd_Stg_Interface (%). The mismatch between those two indicator
## 30-PDY-19104.OUT_2nd_Stg_Prod_Hydrocyclone_Out (%) : The oil ouput at Hydrocyclone drops correspondingly to those events
#

#instruments of interest
#28201-03
#29101-02
#29101-03  spikes above 2200 psi
#33101-02
#33101-03
#34101-01  spikes above 2100 psi
#34101-04  spikes above 2100 psi  nb: most of 'normal' is @ 1000 psi and @ 1800 psi.
#28201-01  average typically @ 160 deg F, spikes below 140 deg F. drops in temp correlated to drops in flowrate?
#28201-03  average typically @ 140 deg F, spikes below 120 deg F. drops in temp correlated to drops in flowrate?
#29101-02  average typically @ 115 deg F, spikes below 100 deg F. drops in temp correlated to drops in flowrate?
#29101-03  average typically @ 115 deg F, spikes below 100 deg F. drops in temp correlated to drops in flowrate?
#33101-02  average typically @ 155 deg F, spikes below 100 deg F. drops in temp correlated to drops in flowrate?
#33101-03  average psi 900-1100 psi, spikes when above 1200 or below 850
#34101-01  normal range 1600-1800 psi, spikes when above 2000 or below 1300 tho weird period in dec 2016  w extended operation @ 1000 psi
#34101-04  normal range 1000 psi, spikes when above 1300, period in Dec 2017 to Jan 2018 when norm is at 1700 psi with lot of variation
#
#df1
features_w_cutoffs = [  ["05-PT-29101-03_C1_Manifold_Pressure (Psi)", 2200],
                        ["05-PT-34101-01_H1_Manifold_Pressure (Psi)", 2100],
                        ["05-TT-28201-01_B2_Manifold_Temperature (DegF)", 140]
                        ["05-TT-28201-03_B2_Manifold_Temperature (DegF)", 120]
                        ["05-TT-29101-02_C1_Manifold_Temperature (DegF)", 100],
                        ["05-TT-29101-03_C1_Manifold_Temperature (DegF)", 100],
                        ["05-TT-33101-02_G1_Manifold_Temperature (DegF)", 100]
                      ]
