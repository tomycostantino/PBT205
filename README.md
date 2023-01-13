# Contact Tracing


## This system tracks interactions between individuals and record them in a database. This information can be used to quickly and efficiently trace the spread of a contagious disease.

To run the program, you will need to have Python 3.10 installed on your computer and PyCharm as your IDE. If you prefer to run the program from the command terminal, you can access the file directly and run the 'main.py' file. The code to be inputted in the command line is the following:
    #!/bin/bash
    
    # Clone the repository
    git clone https://github.com/tomycostantino/contact-tracing.git
    
    # Change into the ContactTracing directory
    cd contact-tracing/ContactTracing
    
    # Run the main.py file
    python3 main.py


The system uses a message broker hosted on the RabbitMQ AMPQ server, which allows for multiple instances of the program to access and update the same database. The RabbitMQ instance is running on a cloud-based server located in Sydney.
The contact tracing system randomly generates the location of an individual every 5 seconds,and sends it to thetracker to be stored in the database. This information can be used to simulate and trace the spread of a contagious disease.

Please note that the program is still in development and there are improvements that need to be made to the GUI and backend code. Additional functionalities will be added as the program nears completion. As an example, data analysis and Machine Learning techniques can be utilized to learn from the data to make decisions.

Overall, the contact tracing system is a valuable project that provides an opportunity to gain experience in software engineering and development by focusing on the integration of multiple components. This project will help users to understand how to combine different technologies and how to handle large amounts of data in a reliable and efficient way. 

