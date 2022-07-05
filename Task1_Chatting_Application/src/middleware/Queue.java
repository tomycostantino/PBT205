package middleware;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import connection.ConfigurationDetails;

public class Queue {
	
	public void createQueue() {
		try {
			// make the middleware connection
			ConfigurationDetails configurationDetails = new ConfigurationDetails();
			ConnectionFactory factory = new ConnectionFactory();
		    Connection connection = factory.newConnection(configurationDetails.getAMQP_URL());
		    Channel channel = connection.createChannel();

		    // creating a new queue with name chat
		    channel.queueDeclare("chat", true, false, false, null);

		 
		    channel.close();
		    connection.close();
		}catch (IOException | TimeoutException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
