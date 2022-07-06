package chatSystem;

import java.util.Scanner;

import javax.management.Query;

import connection.ConfigurationDetails;
import middleware.Binding;
import middleware.Queue;
import middleware.TopicCreation;

public class RunChatSystem {
	
	public static void main(String[] args) {
	
		TopicCreation topicCreation = new TopicCreation();
		topicCreation.createExchange();
		
		Queue queue = new Queue();
		queue.createQueue();
		
		Binding binding = new Binding();
		binding.createBinding();
		
		GetChat getChat = new GetChat();
		getChat.printChatInConsole();
		
	}

}
