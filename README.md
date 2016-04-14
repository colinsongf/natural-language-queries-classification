# natural-language-queries-classification
The objective of this repository is to classify natural language queries into some clusters. These clusters are formed by combing throught their equivalent SPARQL queries and using an unsupervised mechanism

The repository is divided into two major phases:
- Phase I - where we use Kmeans to classify SPARQL queries into 4 clusters
- Phase II - where we treat the ( NL Query , ClusterID) set as (data, class) and use supervised machine learning to classify unknown questions into either of these classes

We use Scikit-learn to achieve both of the above classification

##Usage

Run the following commands on your system (assuming you have pip installed already). They're meant to work with **debian** based linux. Please select your distro's package manager as and when required - 

    $ sudo apt-get install python-dev
    $ sudo apt-get install build-essential python-numpy python-scipy python-matplotlib python-pandas python-sympy python-nose
    $ sudo pip install -U scikit-learn
    $ git clone https://github.com/geraltofrivia/natural-language-queries-classification.git
  
  Change directory to the folder and run ``python clustering_sparql.py``
  The script will do all that's necessary and dump a list of 
  [ NL Query, SPARQL, Number of Answers, Featureset Array, Cluster ID]
  [ NL Query, SPARQL, Number of Answers, Featureset Array, Cluster ID]
  [ NL Query, SPARQL, Number of Answers, Featureset Array, Cluster ID]...
  
  To see this array, one by one run ``python pickle_reader.py`` and hit *ENTER* after every entry
  

