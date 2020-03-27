Process_Images.ipynb is a Jupyter Notebook which takes in a folder of images of gel vials and allows you to select a vial to analyse, and stores the calculated trajectories in a .pkl file. This .pkl is then loaded by Process_Data.ipynb and this notebook is used to calculate characteristics of the gel, which are then saved in a .csv, with accompanying graphs.

process_pickle.py contains the code written to carry out the calculations, it doesn't need interacting with directly, it just needs to stay in the same folder as the two Jupyter notebooks mentioned above. If you want to change the way calculations are carried out, or add more, change the sole function defined in process_pickle.py

'Process Images w Trajectory Plots (for ML).ipynb' is a modified version of Process_Images with a cell to produce images of individual trajectories as needed for the CNN work detailed in the accompanying dissertation.

'Activity Maps.ipynb' produces the heatmap animations detailed in the dissertation, whilst 'Vector Plot (and tests for chi sq scaling).ipynb' produces the accompanying vector plots along with an extra cell with scaling performed by a chi-squared measure of 'heterogeneity' of tracer motion. All files should be kept in the same folder as process_pickle.py however this isnt necessary for the image analysis if a .csv file has already been produced.

To run the Jupyter notebooks, several dependencies will be required. It's easiest to just install Anaconda - a prepackaged Python distribution with many scientific packages included, as well as Jupyter. If the import cells throw errors after installing Anaconda, you'll need to look at installing those packages separately.

If you have any questions please contact me at liamchalcroft@gmail.com
