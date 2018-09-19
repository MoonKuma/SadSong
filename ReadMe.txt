## Use Python to tell whether a song is sad or not

# This is a test program for using python to do some simple data processing and analysing (also simple machine learning)

# The basic ideas is as follow:
# -- 1. Generate a data sample (music-sad/not_sad)
# -- 2. Use pyaudio to trans music files into digital files
# -- 3. Use scipy.fft to transform the time based data in step two into frequency based data
# -- 4. Sample the frequency based data and use sampled data to carry out svm and see how it works

# To successfully run this project, you need the following python libs:
# -- pyaudio (analysing .mp3 or .wav files)
# -- numpy (basic data computing)
# -- scipy (casting fast Fourier transform)
# -- sklearn (offering svm method)


# For more interesting machine learning related python examples, see : http://scikit-learn.org/stable/auto_examples/index.html