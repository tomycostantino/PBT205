
This program was coded in Python 3.10


I have used PyCharm as my IDE, so it is the preferred option to use it when running the code.

However, it can also be run from the command terminal by accessing the file directly and running the 'main.py' file.
The command line for my case on Mac goes as follows:
    cd pycharmprojects/pbt205/contacttracing
    python main.py

The message broker is hosted on the RabbitMQ AMPQ server so the queue is basically running on the internet using a
Amazon server located in Sydney.

Many instances can be created and when trackers read the information from the queue they will update their database.

The system still requires a lot of improvement on GUI and backend code to make it more functional.

There is more functionalities to add for the final system when finished.
