import numpy as np
import pandas as pd
from pandas import DataFrame, Series  

import pims
import trackpy as tp
import os
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import time
import sys

def process_pickle_quiver(file_path, general_directory, microns_per_pixel, timestep, frame_lookback):
    ''' carry out analysis on a single .pkl given the above arguments'''
    

    tr_full_filtered = pd.read_pickle(file_path)
    last_dash = file_path.rfind("/")
    pkl_dir = file_path[:last_dash]
    df1 = tr_full_filtered.copy()


    def disp_for_single_particle(df):
        def find_dx(data):
            return data - initial_position[0]
        def find_dy(data):
            return data - initial_position[1]
        def find_displacement(x):
            #print(x[11], x[12])
            #print(math.sqrt(x[11]**2 + x[12]**2))
            return math.sqrt(x[11]**2 + x[12]**2)  # TODO - how to refer to named column rather than 'magic numbers'
        df['displacement'] = np.nan
        initial_position = [df.values[0][0], df.values[0][1]]
        df['dx'] = list(map(find_dx, df['x']))
        df['dy'] = list(map(find_dy, df['y']))
        df['displacement'] = df.apply(find_displacement, axis=1)


    first_particle = df1['particle'].unique()[0]
    disp_df = df1[df1['particle'] == first_particle].copy()
    disp_for_single_particle(disp_df)

    for c, x in enumerate(df1['particle'].unique()[1:]):
        sys.stdout.write("\r Calculating Displacement for particles: {:.2%}".format(c/ len(df1['particle'].unique()[1:])))
        sys.stdout.flush()
        w_df = df1[df1['particle'] == x].copy()
        disp_for_single_particle(w_df)
        disp_df = disp_df.append(w_df)
    sys.stdout.write("\r Calculating Displacement for particles: {:.2%}".format(1/1))
    df1 = disp_df.copy()

    df1.index.name = None

    df1 = df1.reset_index()

    df1 = df1.drop('index', 1)

    df1.head()
    print("\n")
    particles = df1.particle.unique()
    for c, particle in enumerate(particles):
        sys.stdout.write("\r Calculating Velocity for particle: {:.2%}".format(c/len(particles)))
        sys.stdout.flush()
        p = df1[df1.particle == particle]


        for ind in p.index:
            try:
                last_disp = p.loc[ind - frame_lookback].displacement.item()
            except:
                last_disp = np.NaN
            curr_disp = p.loc[ind].displacement.item()
            d_disp =  curr_disp - last_disp
            curr_frame = p.loc[ind].frame.item()
            try:
                last_frame = p.loc[ind - frame_lookback].frame.item()
            except:
                last_frame = np.NaN
            dframe = curr_frame - last_frame
            vel = (d_disp * microns_per_pixel * 10**-6) /(timestep * dframe)

            df1.set_value(ind, 'velocity', vel )
    sys.stdout.write("\r Calculating Velocity for particle: {:.2%}".format(1/1))
    final_df = df1.copy()
    particles = final_df.particle.unique()

    final_df.head()


    print("\n")
    for c, particle in enumerate(particles):
        sys.stdout.write("\r Calculating Y Velocity for particle: {:.2%}".format(c/len(particles)))
        sys.stdout.flush()
        p = final_df[final_df.particle == particle]


        for ind in p.index[1:]:
            try:
                last_y = p.loc[ind - frame_lookback].y.item()
            except:
                last_y = np.NaN
            curr_y = p.loc[ind].y.item()
            dy =  curr_y - last_y
            curr_frame = p.loc[ind].frame.item()
            try:
                last_frame = p.loc[ind - frame_lookback].frame.item()
            except:
                last_frame = np.NaN
            dframe = curr_frame - last_frame
            y_vel = (dy * microns_per_pixel * 10**-6) /(timestep * dframe)

            final_df.set_value(ind, 'y_velocity', y_vel )
    sys.stdout.write("\r Calculating Y Velocity for particle: {:.2%}".format(1 / 1))
    print("\n")
    for c, particle in enumerate(particles):
        sys.stdout.write("\r Calculating X Velocity for particle: {:.2%}".format(c / len(particles)))
        sys.stdout.flush()
        p = final_df[final_df.particle == particle]

        for ind in p.index[1:]:
            try:
                last_x = p.loc[ind - frame_lookback].x.item()
            except:
                last_x = np.NaN
            curr_x = p.loc[ind].x.item()
            dx = curr_x - last_x
            curr_frame = p.loc[ind].frame.item()
            try:
                last_frame = p.loc[ind - frame_lookback].frame.item()
            except:
                last_frame = np.NaN
            dframe = curr_frame - last_frame
            x_vel = (dx * microns_per_pixel * 10 ** -6) / (timestep * dframe)

            final_df.set_value(ind, 'x_velocity', x_vel)

    sys.stdout.write("\r Calculating X Velocity for particle: {:.2%}".format(1/1))

    final_df['hyp_vel'] = np.hypot(final_df.x_velocity, final_df.y_velocity)

    df = final_df.copy()
    df.y_velocity = -df.y_velocity
    print("\n")
    print("Storing data...")
    with open(pkl_dir + "/frame_dimensions.txt") as f:
        lines = f.readlines()
        lines = lines[0].split()
        height, width = int(lines[0]), int(lines[1])

    bin_width = 50
        
    df['binx'] = (df['x']/bin_width).apply(np.floor)*bin_width

    df['biny'] = (df['y']/bin_width).apply(np.floor)*bin_width
    

    df.to_excel(general_directory + "/data_quiver.xlsx")

    print("Finished")
    return df
