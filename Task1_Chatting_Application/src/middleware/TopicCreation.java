package middleware;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

import com.rabbitmq.client.BuiltinExchangeType;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import connection.ConfigurationDetails;

public class TopicCreation {
	
	public void createExchange() {
		try {
			// make the middleware connection
			ConfigurationDetails configurationDetails = new ConfigurationDetails();
			ConnectionFactory factory = new ConnectionFactory();
		    Connection connection;
			connection = factory.newConnection(configurationDetails.getAMQP_URL());
		    Channel channel = connection.createChannel();

		    //Create an exchange with the name room
		    channel.exchangeDeclare("room", BuiltinExchangeType.TOPIC, true);

		    channel.close();
		    connection.close();
		} catch (IOException | TimeoutException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
