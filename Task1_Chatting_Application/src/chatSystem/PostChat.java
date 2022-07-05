package chatSystem;

import java.io.IOException;
import java.util.Scanner;
import java.util.concurrent.TimeoutException;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import connection.ConfigurationDetails;

public class PostChat {

	public static void main(String[] args) {
		
		
	    PostChat postChat = new PostChat();
	    postChat.postChat();
	  }
	
	public void postChat() {
		try {
			// make the middleware connection
			ConfigurationDetails configurationDetails = new ConfigurationDetails();
		    ConnectionFactory factory = new ConnectionFactory();
		    Connection connection = factory.newConnection(configurationDetails.getAMQP_URL());
		    Channel channel = connection.createChannel();
		    
		    Scanner sc = new Scanner(System.in);
		    
		    // fetching the current username that is connected
		    String username = "guest";
		    String providedName = connection.getClientProvidedName();
		    if(null != providedName) {
		    	String str = providedName.split("\\/\\/")[1];
		    	username = str.split(":")[0];
		    }
		   
		    // use of loop to ask user the message for chatting
		    int i = 1;
		    while (i != 0) {
		    	
			    //Basic publish
		    	String message = "";
			    System.out.println("Enter message for chatting:");
			    message = sc.nextLine();
			    
			    message = username+": "+message;
			    channel.basicPublish("room", "personalMessage.chat", null, message.getBytes()); 
			    
//			    System.out.println("do you want to add more?");
//			    i = sc.nextInt();
		    }
	
		    //Close the channel and connection
		    channel.close();
		    connection.close();
		}catch (IOException | TimeoutException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
