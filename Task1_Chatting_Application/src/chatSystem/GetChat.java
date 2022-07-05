package chatSystem;

import java.io.IOException;
import java.util.Scanner;
import java.util.concurrent.TimeoutException;

import com.rabbitmq.client.CancelCallback;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

import connection.ConfigurationDetails;

public class GetChat {

	// method to print the chat data in console
	public void printChatInConsole() {
		try {
			// make the middleware connection
			ConfigurationDetails configurationDetails = new ConfigurationDetails();
			ConnectionFactory factory = new ConnectionFactory();
		    Connection connection = factory.newConnection(configurationDetails.getAMQP_URL());
		    Channel channel = connection.createChannel();
		    
//		    DeliverCallback deliverCallback = (consumerTag, message) -> {
//		      System.out.println(consumerTag);
//		      System.out.println(new String(message.getBody(), "UTF-8"));
//		    };

		    CancelCallback cancelCallback = consumerTag -> {
		      System.out.println(consumerTag);
		    };
		    
		    System.out.println("Welcome to Chatting Application");

		    // get data from the middleware and print it in console
		    // declaring autoack to false means, the acknowledgement is not sent and the message will be shown again
		    channel.basicConsume("chat", false, ((consumerTag, message) -> {
		    	//System.out.println("Username: "+factory.getUsername());
		       // System.out.println(consumerTag + " : " + factory.getUsername());
		        System.out.println(new String(message.getBody()));
		      }), consumerTag -> {
		        System.out.println(consumerTag);
		      });
		      
		}catch (IOException | TimeoutException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	  }

}
