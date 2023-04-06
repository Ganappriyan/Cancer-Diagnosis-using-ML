Requirements for Mac M1, M2:

Python 3.8,
xcode-select --install

For running cancer_diagnosis django server:
pip install django

For running image_processor fastapi server:
brew install graphviz
pip install pydot
pip install graphviz

conda install -c apple tensorflow-deps
pip install tensorflow-macos==2.9
pip install tensorflow-metal==0.5.0
conda install -c conda-forge pandas jupyter
conda install -c conda-forge opencv
conda install -c conda-forge numpy
conda install -c conda-forge matplotlib
conda install -c conda-forge scipy
pip install fastapi
pip install uvicorn