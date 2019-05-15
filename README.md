# aggregator
Simple general purpose aggregator in Python that looks through URLs through a topic

# About
This is an aggregator written in Python that uses command line arguments. It looks through a text file of source URLs and picks out lines which contain a user-specified topic, writing them to an output file called {topic}summary.txt.

# Usage
1. Download aggregator.py
2. Create a text file of source urls
3. Open Terminal
4. Navigate to the directory containing aggregator.py and the sources text file
5. Enter `python aggregator.py sourcefile topic` (Example: `python aggregator.py sources.txt art`)
7. The file {topic}summary.txt is created in the working directory (Example: artsummary.txt)
