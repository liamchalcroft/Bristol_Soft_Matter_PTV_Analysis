Hopefully the comments in the two Jupyter notebooks should explain what's going on. 
The documentation at https://soft-matter.github.io/trackpy/v0.3.2/ should also be useful.

Process_Images.ipynb is a Jupyter Notebook which takes in a folder of images of gel vials and allows you to select a vial to analyse, and stores the calculated trajectories in a .pkl file. This .pkl is then loaded by Process_Data.ipynb and this notebook is used to calculate characteristics of the gel, which are then saved in a .xlsx, with accompanying graphs.

process_pickle.py contains the code written to carry out the calculations, it doesn't need interacting with directly, it just needs to stay in the same folder as the two Jupyter notebooks mentioned above. If you want to change the way calculations are carried out, or add more, change the sole function defined in process_pickle.py

To run the Jupyter notebooks, several dependencies will be required. It's easiest to just install Anaconda - a prepackaged Python distribution with many scientific packages included, as well as Jupyter. If the import cells throw errors after installing Anaconda, you'll need to look at installing those packages separately.

If you have any questions please contact me at fs13019@my.bristol.ac.uk
