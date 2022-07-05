package middleware;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

import com.rabbitmq.client.BuiltinExchangeType;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import connection.ConfigurationDetails;

public class Binding {
	
	public void createBinding() {
		try {
			// make the middleware connection
			ConfigurationDetails configurationDetails = new ConfigurationDetails();
			ConnectionFactory connectionFactory = new ConnectionFactory();
		    Connection connection = connectionFactory.newConnection(configurationDetails.getAMQP_URL());
		    
		    try (Channel channel = connection.createChannel()) {
		      //creating a new bind for personalMessage
		      channel.queueBind("chat", "room", "personalMessage.*");
		    }
		    connection.close();
		} catch (IOException | TimeoutException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
