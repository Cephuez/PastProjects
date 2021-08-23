import java.io.*;
import java.util.ArrayList;
import java.sql.*;
import java.util.Scanner;
import java.util.*;  

class JDBCDemo {
	private static final String connect_string = "jdbc:oracle:thin:@aloe.cs.arizona.edu:1521:oracle";
	private static Connection m_conn;

	private static int messageID = 1;
	private static int reportedID = 1;

	public static void main(String[] args) {
		String user_name = "cephuez";
		String password = "a6466";
		Statement s = null;
		PreparedStatement pstmt = null;
		System.out.println("Begin JDBCDemo\n");

		try {
			// Registers drivers
			Class.forName("oracle.jdbc.OracleDriver");
			// get a connection
			m_conn = DriverManager.getConnection(connect_string, user_name, password);
			if (m_conn == null)
				throw new Exception("getConnection failed");
			// create a statement, resultset
			s = m_conn.createStatement();
			ResultSet rs = null;
			int loop = 1;

			System.out.println("Beginning!");
			try {
				if (s == null)
					throw new Exception("createStatement failed");

				
				// Create the tables
				/*
				CreateTables(s);
				
				// Values inserting into my tables
				InsertValuesMembers(s, pstmt);
				InsertValuesPet(s, pstmt);
				InsertValuesFavorite(s, pstmt);
				InsertValuesChatMessage(s, pstmt);
				InsertValuesReportMembers(s, pstmt);*/
				

				Scanner myObj = new Scanner(System.in);
				while (loop == 1) {
					PrintCommands();
					String command = myObj.nextLine(); // Read user input
					if (command.equals("1")) {
						CreateMember(s, pstmt, rs);
					} else if (command.equals("2")) {
						ShowChat(s, pstmt, rs);
					} else if (command.equals("3")) {
						FindFavoritePets(s, pstmt, rs);
					} else if (command.equals("4")) {
						ListPopularPets(s, pstmt, rs);
					} else if (command.equals("5")) {
						ReportMember(s, pstmt, rs);
					} else if (command.equals("6")) {
						ListReports(s, pstmt, rs);
					} else if (command.equals("7")) {
						//System.out.println("Shutting Down");
						loop = 0;
						//DropTables(s);
					}
				}

			} catch (Exception e) {
			} finally {
				try {
					if (rs != null)
						rs.close();
				} catch (Exception e) {
				}
				;
				try {
					if (s != null)
						s.close();
				} catch (Exception e) {
				}
				;
				try {
					if (pstmt != null)
						pstmt.close();
				} catch (Exception e) {
				}
				;
				try {
					if (m_conn != null)
						m_conn.close();
				} catch (Exception e) {
				}
				;
			}
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(1);
		}
		// Drop Tables
		System.out.println("JDBCDemo Successfully Completed");
	}

	public static void ListReports(Statement s, PreparedStatement pstmt, ResultSet rs) {
		boolean counts = false;
		Scanner answer = new Scanner(System.in);
		String email = "";
		System.out.println("Type the user's email to see all of their reports");
		email = answer.nextLine();

		try {

			rs = s.executeQuery("SELECT ID, Reason, Content " + 
					"FROM ReportMembers " + 
					"WHERE Accused = '" + email + "' " +
					"ORDER BY ID ASC");

			while (rs.next()) {
				System.out.println("ID: " + rs.getString(1) + " Reason: " + rs.getString(2) + "\n\t" + "Content: "
						+ rs.getString(3) + "\n");
				counts = true;
			}
			if(!	counts)
				System.out.println("There are no reports for this user");
			
			System.out.println("Returning to the menu...\n");
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}

	public static void ListPopularPets(Statement s, PreparedStatement pstmt, ResultSet rs) {
		System.out.println("The names of pets and their owners are: ");
		try {
			rs = s.executeQuery("SELECT Pet.Name, Member.Name " + "FROM Pet, Member "
					+ "WHERE Pet.EmailAddress = Member.EmailAddress " + "ORDER BY Pet.Name ASC");
			while (rs.next()) {
				System.out.println(rs.getString(1) + " " + rs.getString(2));
			}
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}

	}

	public static void ReportMember(Statement s, PreparedStatement pstmt, ResultSet rs) {
		/*
		 * String accuserEmail = "dave@gmail.com"; String accusedEmail =
		 * "cephuez@gmail.com"; String reason = "Scamming"; String content =
		 * "I don't know man";
		 */
		String accuserEmail = "";
		String accusedEmail = "";
		String reason = "";
		String content = "";
		String reply = "";

		Scanner answer = new Scanner(System.in);
		System.out.println("You are going to report this user!");
		System.out.println("Please write your email address");
		accuserEmail = answer.nextLine();
		
		while(true) {
			System.out.println("Type your reported member's email");
			accusedEmail = answer.nextLine();
			if(!accusedEmail.equals(accuserEmail)) {
				break;
			}
			System.out.println("You cannot report yourself");
			while(true) {
				System.out.println("Do you wish to continue (Y or N)?");
				reply = answer.nextLine();
				if(reply.equals("Y"))
					break;
				if(reply.equals("N")) {
					System.out.println("Returning to the menu...");
					return;
				}
				System.out.println("Wrong input.");
			}
		}
		
		while(1 == 1) {
			System.out.println("What is the reason for reporting this user? ('Scamming', 'Foul Language')");
			reason = answer.nextLine();
			
			if(!(reason.equals("Scamming") == true || reason.equals("Foul Language") == true)) {
				System.out.println("The reason you typed is not one of the options");
			}else {
				break;
			}
			
			while(1 == 1) {
				System.out.println("Do you want to retry? (Y or N)");
				reply = answer.nextLine();
				if(reply.equals("Y"))
					break;
				if(reply.equals("N")) {
					System.out.println("Returning to the menu...\n");
					return;
				}
				System.out.println("Your input was incorrect");
			}
		}
		
		
		
		while(1 == 1) {
			System.out.println("What appears to be the problem with this user?: ");
			content = answer.nextLine();
			if(content.length() < 201)
				break;
			while(1 == 1) {
				System.out.println("Your reply is longer than 200 characters. Do you want to retry (Y or N)?");
				reply = answer.nextLine();
				if(reply.equals("Y"))
					break;
				if(reply.equals("N")) {
					System.out.println("Returning to the menu...\n");
					return;
				}
				System.out.println("Your input is incorrect.");				
			}
		}

		if(CheckEmails(s, rs, accuserEmail) == 0 || CheckEmails(s, rs, accusedEmail) == 0) {
			System.out.println("Your email or the reported user's email is incorrect");
			System.out.println("Returning to the menu...\n");
			return; 
		}
			
		try {
			int newReportID = 0;
			rs = s.executeQuery("SELECT ID "
					+ "FROM ReportMembers "
					+ "ORDER BY ID DESC");
			if(rs.next()) {
				newReportID = Integer.valueOf(rs.getString(1)) + 1;
			}
			
			pstmt = m_conn.prepareStatement("INSERT INTO ReportMembers VALUES(?,?,?,?,?)");
			pstmt.setInt(1, newReportID);
			reportedID += 1;
			pstmt.setString(2, accuserEmail);
			pstmt.setString(3, accusedEmail);
			pstmt.setString(4, reason);
			pstmt.setString(5, content);
			pstmt.executeUpdate();
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}

		System.out.println("Thank you for submitting your report. We will evaluate your response!");
		System.out.println("Returning to the menu...");
	}
	
	public static int CheckEmails(Statement s, ResultSet rs, String email) {
		try {
			rs = s.executeQuery("SELECT emailaddress FROM Member");
			while(rs.next()) {
				if(rs.getString(1).equals(email))
					return 1;
			}
		}catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
		return 0;
	}

	public static void FindFavoritePets(Statement s, PreparedStatement pstmt, ResultSet rs) {
		Scanner answer = new Scanner(System.in);
		String email = "";
		System.out.println("You are going to find the favorite pets of a member!");
		System.out.println("Please enter the member's email address:");

		email = answer.nextLine();
		ListFavoritePets(s, rs, email);
		System.out.println("Returning to the menu...");
	}

	public static void ListFavoritePets(Statement s, ResultSet rs, String email) {
		ArrayList<String> emails = new ArrayList<String>();
		ArrayList<String> birthday = new ArrayList<String>();
		ArrayList<String> isSterilized = new ArrayList<String>();
		ArrayList<String> breed = new ArrayList<String>();
		ArrayList<String> name = new ArrayList<String>();
		ArrayList<String> specialInfo = new ArrayList<String>();
		try {
			// System.out.println("-----> 1");
			rs = s.executeQuery(
					"SELECT Favorite.EmailAddressPet, Favorite.Birthday, Pet.IsSterilized, Pet.Breed, Pet.DaysWalk, Pet.BiteWire "
							+ "FROM Member, Favorite, Pet " + "WHERE Member.EmailAddress = '" + email + "' "
							+ "AND Member.EmailAddress = Favorite.EmailAddressMember "
							+ "AND Favorite.EmailAddressPet = Pet.EmailAddress");
			while (rs.next()) {
				emails.add(rs.getString(1));
				birthday.add(rs.getString(2));
				if (rs.getString(3).equals("y"))
					isSterilized.add("sterilized");
				else
					isSterilized.add("unsterilized");
				breed.add(rs.getString(4));

				if (rs.getString(5) == null && rs.getString(6) == null)
					specialInfo.add("");
				else if (rs.getString(6) == null) {
					specialInfo.add(rs.getString(5) + " days for a walk");
				} else {
					if (rs.getString(6).equals("y"))
						specialInfo.add("bite wires");
					else
						specialInfo.add("not bite wires");

				}
			}

			for (int i = 0; i < emails.size(); i++) {
				rs = s.executeQuery("SELECT Member.name " + "FROM Member " + "WHERE Member.EmailAddress = '"
						+ emails.get(i) + "' ");
				while (rs.next()) {
					name.add(rs.getString(1));
				}
			}

			if (emails.size() == 0) {
				System.out.println("There is no favorite pet of that member!");
				return;
			}

			for (int i = 0; i < name.size(); i++) {
				String birthdayFormat = birthday.get(i).substring(5, 10) + "-" + birthday.get(i).substring(0,4);
				System.out.println("\t" + name.get(i) + " " + birthdayFormat + " " + isSterilized.get(i) + " "
						+ breed.get(i) + " " + specialInfo.get(i));
			}
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}

	public static void CreateMember(Statement s, PreparedStatement pstmt, ResultSet rs) {
		String name = "";
		String email = "";
		String reply = "";
		String location = "";
		String birthday = "";
		String introduction = "";
		int emailUsed = 1;
		Scanner answer = new Scanner(System.in);
		System.out.println("You are going to create a sender!");

		while (1 == 1) {
			System.out.print("Enter name: ");
			name = answer.nextLine();
			if (name.length() < 21) {
				break;
			}
			while (1 == 1) {
				System.out.println("Name longer than 20 characters. Do you wish to retry (Y or N)?");
				reply = answer.nextLine();
				if (reply.equals("N")) {
					System.out.println("Returning to the menu...\n");
					return;
				}
				if (reply.equals("Y"))
					break;
				System.out.println("Incorrect input.");

			}

		}

		while (1 == 1) {
			System.out.print("Enter email address: ");
			email = answer.nextLine();
			if (email.length() < 20)
				break;
			while (1 == 1) {
				System.out.println("Email longer than 20 characters. Do you wish to retry (Y or N)?");
				reply = answer.nextLine();
				if (reply.equals("N")) {
					System.out.println("Returning to the menu...\n");
					return;
				}if (reply.equals("Y"))
					break;
				System.out.println("Incorrect input.");
			}
		}

		introduction = CreateSelfIntroduction(answer);
		if (introduction == null) {
			System.out.println("Returning to the menu...\n");
			return;
		}

		System.out.println("Self-introduction created!");

		System.out.print("Enter location: ");
		location = answer.nextLine();
		int retry = 1;
		int charInt = 0;
		int birthdayWrong = 0;
		while (retry == 1 || retry == 3) {
			retry = 1;
			System.out.print("Enter birthday (as MMDDYY, e.g., 042221): ");
			birthday = answer.nextLine();
			if (birthday.length() != 6) {
				retry = 1;
			} else {
				retry = 0;
				// Check here one last time.
				
				for (int i = 0; i < birthday.length(); i++) {
					charInt = birthday.charAt(i);
					if (!(48 <= birthday.charAt(i) && birthday.charAt(i) <= 57)) {
						retry = 1;
					}
				}
				if(retry == 0) {
					retry = CheckDate(birthday);
					if(retry == 2) {
						System.out.println("Going back to the menu...");
						return;
					}
				}
			}
			if (retry == 1) {
				while (1 == 1) {
					System.out.println("Wrong format for birthday. Do you wish to continue (Y or N)?");
					reply = answer.nextLine();
					if (reply.equals("N")) {
						System.out.println("Returning to the menu...\n");
						return;
					}if (reply.equals("Y")) {
						break;
					}
					System.out.println("Incorrect Input.");
				}
			}
		}

		emailUsed = CheckMemberStatus(s, rs, email);
		if (emailUsed == 1) {
			System.out.println("This sendor already exists!");
			System.out.println("Returning to the menu...\n");
			return;
		}

		System.out.println("XD");
		CreateSender(s, pstmt, name, email, location, introduction, birthday);

	}

	public static int CheckDate(String birthday) {
		Scanner answer = new Scanner(System.in);
		String reply = "";
		String day = birthday.substring(2,4);
		String month = birthday.substring(0,2);
		String year = birthday.substring(4,6);
		int yearInt = Integer.valueOf(year);
		if(0 <= yearInt && yearInt <= 21) {
			year = "20" + year;
		}else {
			year = "19" + year;
		}
		
		String birthDate = year + "-" + month + "-" + day;
		
		Calendar cal = Calendar.getInstance();
		cal.setLenient(false);
		try {
			cal.setTime(java.sql.Date.valueOf(birthDate));
			//cal.getTime();
		}catch (Exception e) {
			  while(true) {
				  System.out.println("The date is invalid. The month or day is not correct");
				  System.out.println("Do you wish to retry birthday? (Y or N)?");
				  reply = answer.nextLine();
				  if(reply.equals("Y")) {
					  return 3;
				  }else if(reply.equals("N")) {
					  return 2;
				  }
				  System.out.println("Input is invalid");
			  }
		}
		return 0;
	}
	public static int CheckMemberStatus(Statement s, ResultSet rs, String email) {
		try {
			rs = s.executeQuery("SELECT emailaddress FROM Member");
			while (rs.next()) {
				if (email.equals(rs.getString(1))) {
					return 1;
				}
			}
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
		return 0;
	}

	public static void ShowChat(Statement s, PreparedStatement pstmt, ResultSet rs) {
		Scanner input = new Scanner(System.in);
		String reply = "";
		String emailAddress = "";
		System.out.println("You are going to look at one member's chat message!");
		System.out.println("Please enter the email address:");
		emailAddress = input.nextLine();
		FindRootMessages(s, pstmt, rs, emailAddress);
	}

	public static void FindRootMessages(Statement s, PreparedStatement pstmt, ResultSet rs, String emailAddress) {
		// MessageContent, ParentID, Names
		int index = 0;
		String reply = "";
		String content = "";
		String parentName = "";
		String childName = "";
		String id = "";
		String parentID = "";
		String email = "";
		String parentEmail = emailAddress;
		Scanner answer = new Scanner(System.in);
		ResultSet rs2 = null;
		ArrayList<String> idList = new ArrayList<String>();
		ArrayList<String> messageList = new ArrayList<String>();
		String senderName = "";
		ArrayList<String> receiverList = new ArrayList<String>();

		try {
			// PArent ID, MessageContent, SenderName
			rs = s.executeQuery("SELECT ChatMessage.MessageContent, ChatMessage.ID, Member.Name "
					+ "FROM ChatMessage, Member "
					+ "WHERE ChatMessage.ParentID IS NULL "
					+ "AND ChatMessage.FromEmailAddress = '"+ emailAddress + "' "
					+ "AND ChatMessage.FromEmailAddress = Member.EmailAddress ");
			
			while(rs.next()) {
				idList.add(rs.getString(2));
				messageList.add(rs.getString(1));
				senderName = rs.getString(3);
			}
			
			if(idList.size() == 0) {
				System.out.println("No root message exists!");
				System.out.println("Returning to the menu...\n");
				return;
			}
			
			rs = s.executeQuery("SELECT Member.Name " 
					+ "FROM ChatMessage, Member "
					+ "WHERE ChatMessage.ParentID IS NULL " 
					+ "AND ChatMessage.FromEmailAddress = '"+ emailAddress + "' " 
					+ "AND ChatMessage.ToEmailAddress = Member.EmailAddress");
			
			while(rs.next()) {
				receiverList.add(rs.getString(1));
			}
			
			System.out.println("The root messages are: ");
			for (int i = 0; i < idList.size(); i++) {
				System.out.println(
						"\t" + messageList.get(i) + " " + idList.get(i) + " " + senderName + " " + receiverList.get(i));
			}
			
			while(true) {
				System.out.println("Please enter the ID of the root message:");
				id = answer.nextLine(); 
				
				if(idList.contains(id)) {
					break;
				}
				System.out.println("Does not contain ID. Retry again");
			}
			
			System.out.println("The replies to message " + id + " and message " + id + " are:");

			
			index = idList.indexOf(id);
			
			System.out.println(
					"\t" + messageList.get(index) + " " + idList.get(index) + " " + senderName + " " + receiverList.get(index));
			while(true) {
				rs = s.executeQuery("SELECT DISTINCT MessageContent, ID, FromEmailAddress, ToEmailAddress "
						+ "FROM ChatMessage, Member "
						+ "WHERE ChatMessage.ParentID = '"+ id + "' ");
				if(!rs.next())
					break;
				
				content = rs.getString(1);
				id = rs.getString(2);
				parentName = rs.getString(3);
				childName = rs.getString(4);
				
				rs = s.executeQuery("SELECT DISTINCT Name "
						+ "FROM Member "
						+ "WHERE Member.EmailAddress = '" + parentName + "'");
				if(!rs.next())
					break;
				parentName = rs.getString(1);
				
				rs = s.executeQuery("SELECT DISTINCT Name "
						+ "FROM Member "
						+ "WHERE Member.EmailAddress = '" + childName + "'");
				if(!rs.next())
					break;
				childName = rs.getString(1);
				System.out.println("\t  "  + " " + content + " " + id + " " + parentName + " " + childName);
			}
			while(true) {
				System.out.println("Do you want to reply to a message? (Y or N):");
				reply = answer.nextLine();
				if(reply.equals("Y")) {
					int emailCheck = 0;
					while(emailCheck == 0) {
						System.out.println("Please enter your email address in order to reply:");
						email = answer.nextLine();
						emailCheck = CheckMemberStatus(s, rs, email);
						if(emailCheck == 0) {
							while(true) {
								System.out.println("Member does not exit. Do you wish to retry?(Y or N)");
								reply = answer.nextLine();
								if(reply.equals("Y")) {
									break;
								}else if(reply.equals("N")) {
									System.out.println("Going back to menu...\n");
									return;
								}
								System.out.println("Wrong input.");
							}
						}
					}
					while(true) {
						System.out.println("Plese enter the ID of the message that you want to reply:");
						reply = answer.nextLine();
						if(reply.equals(id)) {
							if(parentName == "") {
								parentName = parentEmail;
							}
							WriteInput(s, pstmt, rs, id, parentName, email);
							return;
						}
						while(true) {
							System.out.println("Wrong ID typed: ");
							System.out.println("Do you wish to retry? (Y or N): ");
							reply = answer.nextLine();
							if(reply.equals("Y"))
								break;
							else if(reply.equals("N")) {
								System.out.println("Returning back to menu...\n");
								return; 
							}
							System.out.println("Wrong Input typed.");
						}
					}
				}else if(reply.equals("N")) {
					System.out.println("Returning to the menu...\n");
					return;
				}
				System.out.println("Wrong input.");
			}

		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}

	public static void WriteInput(Statement s, PreparedStatement pstmt, ResultSet rs, String id, String parentName, String email) {
		Scanner answer = new Scanner(System.in);
		String reply = "";
		String comment = "";
		int newText = 0;
		while(true) {
			if(newText == 1) {
				System.out.println("Continue your reply:");
			}else {
				System.out.println("Please enter your reply:");
			}
			comment += answer.nextLine() + " ";
			while(true) {
				System.out.println("Are you finished with your reply? (Y or N)?");
				reply = answer.nextLine();
				if(reply.equals("Y")) {
					// enter info
					EnterNewReply(s, pstmt, rs, id, comment, parentName, email);
					System.out.println("A new reply is added!");
					System.out.println("Returning back to the menu ...\n");
					return;
				}else if(reply.equals("N")) {
					newText = 1;
					break;
				}
				System.out.println("Wrong input.");
			}
			
		}
		
	}
	
	public static void EnterNewReply(Statement s, PreparedStatement pstmt, ResultSet rs, String id, String messageContent,
				String parentName, String sender) {
		int newMessageID = 0;
		try {
			if(!parentName.contains("@")) {
				rs = s.executeQuery("SELECT DISTINCT EmailAddress "
						+ "FROM Member "
						+ "WHERE Name = '" + parentName + "'");
				if(rs.next())
					parentName = rs.getString(1);
			}
			
			rs = s.executeQuery("SELECT ID "
					+ "FROM ChatMessage "
					+ "ORDER BY ID DESC");

			if(rs.next()){
				newMessageID = Integer.valueOf(rs.getString(1)) + 1;
			}
			long millis=System.currentTimeMillis();  
			pstmt = m_conn.prepareStatement("INSERT INTO ChatMessage VALUES(?,?,?,?,?,?)");
			pstmt.setInt(1, newMessageID);
			pstmt.setInt(2, Integer.valueOf(id));
			pstmt.setString(3, messageContent);
			pstmt.setDate(4, new java.sql.Date(millis));
			pstmt.setString(5, sender);
			pstmt.setString(6, parentName);
			pstmt.executeUpdate();
			messageID += 1;
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}
	
	/*
	 * Okay coding after this. Don't need to look after this line
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 
	 * --Random Spacing XD
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 
	 * 
	 */

	public static String CreateSelfIntroduction(Scanner answer) {
		String introduction = "";
		String reply = "";
		int askAgain = 0;
		while (1 == 1) {
			reply = "";
			askAgain = 0;
			introduction = "";
			while (!reply.equals("N")) {
				System.out.println("Have self-introduction (Y or N)");
				reply = answer.nextLine();
				if (reply.equals("Y")) {
					System.out.println("Enter self-introduction:");
					introduction = answer.nextLine();
					while (1 == 1) {
						if (askAgain == 1) {
							System.out.println("Continue self-introduction:");
							introduction += "\n" + answer.nextLine();
						}
						System.out.println("Are you finshed with the self-introduction (Y or N)?");
						reply = answer.nextLine();
						if (reply.equals("N")) {
							askAgain = 1;
						} else if (reply.equals("Y")) {
							break;
						} else {
							while (1 == 1) {
								System.out.println(
										"Incorrect input for continuing self-introduction. Do you wish to continue? (Y or N)?");
								reply = answer.nextLine();
								if (reply.equals("N")) {
									return null;
								}
								if (reply.equals("Y"))
									break;
								System.out.println("Incorrect Input.");
								askAgain = 0;
							}
						}
					}
					if (reply.equals("Y")) {
						break;
					}
				} else if (!reply.equals("N")) {
					while (1 == 1) {
						System.out.println(
								"Incorrect input for creating a self-introduction. Do you wish to continue? (Y or N)?");
						reply = answer.nextLine();
						if (reply.equals("N"))
							return null;
						if (reply.equals("Y"))
							break;
						System.out.println("Incorrect Input.");
					}
				}
			}
			if (introduction.length() < 51) {
				break;
			}
			while (1 == 1) {
				System.out.println("Self Introduction longer than 50 characters. Do you wish to retry? (Y or N)?");
				reply = answer.nextLine();
				if (reply.equals("N"))
					return null;
				if (reply.equals("Y")) {
					break;
				}
				System.out.println("Incorrect Input.");
			}
		}
		return introduction;
	}

	public static void CreateSender(Statement s, PreparedStatement pstmt, String name, String email, String location,
			String introduction, String birthday) {
		try {
			String day = birthday.substring(2,4);
			String month = birthday.substring(0,2);
			String year = birthday.substring(4,6);
			int yearInt = Integer.valueOf(year);
			if(0 <= yearInt && yearInt <= 21) {
				year = "20" + year;
			}else {
				year = "19" + year;
			}
			
			String birthDate = year + "-" + month + "-" + day;

			System.out.println("Birthday: " + birthDate);
			pstmt = m_conn.prepareStatement("INSERT INTO Member VALUES(?,?,?,?,?,?,?,?)");
			pstmt.setString(1, email);
			pstmt.setString(2, name);
			pstmt.setString(3, introduction);
			pstmt.setString(4, location);
			pstmt.setDate(5, java.sql.Date.valueOf(birthDate));
			pstmt.setString(6, "n");
			pstmt.setString(7, "y");
			pstmt.setString(8, "");
			pstmt.executeUpdate();
			System.out.println("A new sender is added!");
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}

	public static void PrintCommands() {
		System.out.println("1) Create a member as a sender");
		System.out.println("2) Show chat of a user and reply to one message");
		System.out.println("3) Show a member's favorite pets");
		System.out.println(
				"4) List all pets' names and their owners' names in order of the popularity of the pet's name.");
		System.out.println("5) Report a user");
		System.out.println("6) List all reports for a user");
		System.out.println("7) Quit");
		System.out.println("Enter 1-6 or 7 to quit:");
	}

	public static void InsertValuesReportMembers(Statement s, PreparedStatement pstmt) {
		try {			
			pstmt = m_conn.prepareStatement("INSERT INTO ReportMembers VALUES(?,?,?,?,?)");
			pstmt.setInt(1, reportedID);
			pstmt.setString(2, "cephuez@gmail.com");
			pstmt.setString(3, "dave@gmail.com");
			pstmt.setString(4, "Scamming");
			pstmt.setString(5, "He is posting false pictures of his pets");
			pstmt.executeUpdate();
			
			reportedID += 1;
			pstmt.setInt(1, reportedID);
			pstmt.setString(2, "kate@gmail.com");
			pstmt.setString(3, "chapo@gmail.com");
			pstmt.setString(4, "Foul Language");
			pstmt.setString(5, "He is using the f word too many times!");
			pstmt.executeUpdate();
			
			reportedID += 1;
			pstmt.setInt(1, reportedID);
			pstmt.setString(2, "dave@gmail.com");
			pstmt.setString(3, "chapo@gmail.com");
			pstmt.setString(4, "Foul Language");
			pstmt.setString(5, "He has been harassing me with bad words all along!");
			
			reportedID += 1;
			pstmt.setInt(1, reportedID);
			pstmt.setString(2, "rick@gmail.com");
			pstmt.setString(3, "dave@gmail.com");
			pstmt.setString(4, "Foul Language");
			pstmt.setString(5, "In addition to him scamming people, he is also saying bad words to everyone");
			
			reportedID += 1;
			pstmt.executeUpdate();
			
			m_conn.commit();
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}
	
	public static void InsertValuesMembers(Statement s, PreparedStatement pstmt) {

		try {
			// Adopters
			pstmt = m_conn.prepareStatement("INSERT INTO Member VALUES(?,?,?,?,?,?,?,?)");
			pstmt.setString(1, "cephuez@gmail.com");
			pstmt.setString(2, "Saul");
			pstmt.setString(3, "I'm a new member in this place!");
			pstmt.setString(4, "Tucson");
			pstmt.setDate(5, java.sql.Date.valueOf("1998-10-11"));
			pstmt.setString(6, "y");
			pstmt.setString(7, "n");
			pstmt.setString(8, "It was very easy!");
			pstmt.executeUpdate();

			pstmt = m_conn.prepareStatement("INSERT INTO Member VALUES(?,?,?,?,?,?,?,?)");
			pstmt.setString(1, "kate@gmail.com");
			pstmt.setString(2, "Kate");
			pstmt.setString(3, "I like cats");
			pstmt.setString(4, "Yuma");
			pstmt.setDate(5, java.sql.Date.valueOf("2000-03-29"));
			pstmt.setString(6, "y");
			pstmt.setString(7, "n");
			pstmt.setString(8, "It was good stuff");
			pstmt.executeUpdate();

			// Senders
			pstmt.setString(1, "dave@gmail.com");
			pstmt.setString(2, "Dave");
			pstmt.setString(3, "I got pets to give out!");
			pstmt.setString(4, "Tucson");
			pstmt.setDate(5, java.sql.Date.valueOf("2000-05-02"));
			pstmt.setString(6, "n");
			pstmt.setString(7, "y");
			pstmt.setString(8, "I haven't gotten any pets from here.");
			pstmt.executeUpdate();

			pstmt.setString(1, "chavo@gmail.com");
			pstmt.setString(2, "Chavo");
			pstmt.setString(3, "I got one pet to give!");
			pstmt.setString(4, "Tucson");
			pstmt.setDate(5, java.sql.Date.valueOf("2005-11-12"));
			pstmt.setString(6, "n");
			pstmt.setString(7, "y");
			pstmt.setString(8, "I don't adopt pets.");
			pstmt.executeUpdate();

			pstmt.setString(1, "chapo@gmail.com");
			pstmt.setString(2, "Chapo");
			pstmt.setString(3, "Doggy to give!");
			pstmt.setString(4, "Tucson");
			pstmt.setDate(5, java.sql.Date.valueOf("2002-04-20"));
			pstmt.setString(6, "n");
			pstmt.setString(7, "y");
			pstmt.setString(8, "Giving a free pet.");
			pstmt.executeUpdate();

			pstmt.setString(1, "rick@gmail.com");
			pstmt.setString(2, "Rick");
			pstmt.setString(3, "No entry");
			pstmt.setString(4, "Phoenix");
			pstmt.setDate(5, java.sql.Date.valueOf("2000-06-19"));
			pstmt.setString(6, "n");
			pstmt.setString(7, "y");
			pstmt.setString(8, "I don't want to give free pets.");
			pstmt.executeUpdate();

			pstmt.setString(1, "leo@gmail.com");
			pstmt.setString(2, "Leo");
			pstmt.setString(3, "Hello guys!");
			pstmt.setString(4, "Scottsdale");
			pstmt.setDate(5, java.sql.Date.valueOf("2001-08-01"));
			pstmt.setString(6, "n");
			pstmt.setString(7, "y");
			pstmt.setString(8, "I don't take pets. I give pets");
			pstmt.executeUpdate();

			pstmt.setString(1, "jessica@gmail.com");
			pstmt.setString(2, "Jessica");
			pstmt.setString(3, "First time on this site!");
			pstmt.setString(4, "Flagstaff");
			pstmt.setDate(5, java.sql.Date.valueOf("2002-03-30"));
			pstmt.setString(6, "n");
			pstmt.setString(7, "y");
			pstmt.setString(8, "I would like to give a pet.");
			pstmt.executeUpdate();

			m_conn.commit();
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}

	public static void InsertValuesPet(Statement s, PreparedStatement pstmt) {
		try {
			pstmt = m_conn
					.prepareStatement("INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed, DaysWalk) "
							+ "VALUES(?,?,?,?,?,?)");

			pstmt.setString(1, "chapo@gmail.com");
			pstmt.setString(2, "Angel");
			pstmt.setDate(3, java.sql.Date.valueOf("2019-05-15"));
			pstmt.setString(4, "n");
			pstmt.setString(5, "Dog");
			pstmt.setInt(6, 5);
			pstmt.executeUpdate();

			pstmt.setString(1, "rick@gmail.com");
			pstmt.setString(2, "Angel");
			pstmt.setDate(3, java.sql.Date.valueOf("2021-02-25"));
			pstmt.setString(4, "y");
			pstmt.setString(5, "Dog");
			pstmt.setInt(6, 3);
			pstmt.executeUpdate();

			pstmt.setString(1, "leo@gmail.com");
			pstmt.setString(2, "Angel");
			pstmt.setDate(3, java.sql.Date.valueOf("2021-01-01"));
			pstmt.setString(4, "n");
			pstmt.setString(5, "Dog");
			pstmt.setInt(6, 2);
			pstmt.executeUpdate();

			pstmt = m_conn.prepareStatement(
					"INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed) " + "VALUES(?,?,?,?,?)");

			pstmt.setString(1, "dave@gmail.com");
			pstmt.setString(2, "Katty");
			pstmt.setDate(3, java.sql.Date.valueOf("2020-02-05"));
			pstmt.setString(4, "n");
			pstmt.setString(5, "Cat");
			pstmt.executeUpdate();

			pstmt.setString(1, "jessica@gmail.com");
			pstmt.setString(2, "Katty");
			pstmt.setDate(3, java.sql.Date.valueOf("2021-03-21"));
			pstmt.setString(4, "y");
			pstmt.setString(5, "Cat");
			pstmt.executeUpdate();

			pstmt = m_conn
					.prepareStatement("INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed, Bitewire) "
							+ "VALUES(?,?,?,?,?,?)");

			pstmt.setString(1, "chavo@gmail.com");
			pstmt.setString(2, "Rabby");
			pstmt.setDate(3, java.sql.Date.valueOf("2020-01-11"));
			pstmt.setString(4, "y");
			pstmt.setString(5, "Rabbit");
			pstmt.setString(6, "y");

			pstmt.executeUpdate();

			m_conn.commit();
		} catch (SQLException e) {
			// do something appropriate with the exception, * asdasdat least*:
			e.printStackTrace();
		}
	}

	public static void InsertValuesFavorite(Statement s, PreparedStatement pstmt) {
		try {
			pstmt = m_conn.prepareStatement("INSERT INTO Favorite"
					+ "(EmailAddressMember, EmailAddressPet, PetName, Birthday) " + "VALUES(?,?,?,?)");
			pstmt.setString(1, "cephuez@gmail.com");
			pstmt.setString(2, "dave@gmail.com");
			pstmt.setString(3, "Katty");
			pstmt.setDate(4, java.sql.Date.valueOf("2020-02-05"));
			pstmt.executeUpdate();

			pstmt.setString(1, "cephuez@gmail.com");
			pstmt.setString(2, "chavo@gmail.com");
			pstmt.setString(3, "Rabby");
			pstmt.setDate(4, java.sql.Date.valueOf("2020-01-11"));
			pstmt.executeUpdate();

			m_conn.commit();
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}

	public static void InsertValuesChatMessage(Statement s, PreparedStatement pstmt) {
		try {
			long millis=System.currentTimeMillis(); 
			
			pstmt = m_conn.prepareStatement("INSERT INTO ChatMessage"
					+ "(ID, MessageContent, PostingTime, FromEmailAddress, ToEmailAddress) "
					+ "VALUES(?,?,?,?,?)");
			pstmt.setInt(1, messageID);	// 1
			pstmt.setString(2, "Hello, man. Do you want a pet?");
			pstmt.setDate(3, new java.sql.Date(millis));
			pstmt.setString(4, "cephuez@gmail.com");
			pstmt.setString(5, "rick@gmail.com");
			pstmt.executeUpdate();

			messageID += 1;
			
			pstmt = m_conn.prepareStatement("INSERT INTO ChatMessage"
					+ "(ID, MessageContent, PostingTime, FromEmailAddress, ToEmailAddress) "
					+ "VALUES(?,?,?,?,?)");
			pstmt.setInt(1, messageID);	// 2
			pstmt.setString(2, "Hello, man. Do you want a pet?");
			pstmt.setDate(3, new java.sql.Date(millis));
			pstmt.setString(4, "dave@gmail.com");
			pstmt.setString(5, "cephuez@gmail.com");
			pstmt.executeUpdate();

			messageID += 1;

			pstmt = m_conn.prepareStatement("INSERT INTO ChatMessage"
					+ "(ID, ParentID, MessageContent, PostingTime, FromEmailAddress, ToEmailAddress) "
					+ "VALUES(?,?,?,?,?,?)");
			
			pstmt.setInt(1, messageID); // 3
			pstmt.setInt(2, 2);
			pstmt.setString(3, "No, I'm good. I'm looking for something else");
			pstmt.setDate(4, new java.sql.Date(millis));
			pstmt.setString(5, "cephuez@gmail.com");
			pstmt.setString(6, "dave@gmail.com");
			pstmt.executeUpdate();
			
			messageID += 1;
			
			pstmt.setInt(1, messageID);	// 4
			pstmt.setInt(2, 3);
			pstmt.setString(3, "Let me know if you change your mind :3.");
			pstmt.setDate(4, new java.sql.Date(millis));
			pstmt.setString(5, "dave@gmail.com");
			pstmt.setString(6, "cephuez@gmail.com");
			pstmt.executeUpdate();

			messageID += 1;

			pstmt = m_conn.prepareStatement("INSERT INTO ChatMessage"
					+ "(ID, MessageContent, PostingTime, FromEmailAddress, ToEmailAddress) "
					+ "VALUES(?,?,?,?,?)");
			
			pstmt.setInt(1, messageID); // 5
			//pstmt.setInt(2, null);
			pstmt.setString(2, "Do you like cats or something??");
			pstmt.setDate(3, new java.sql.Date(millis));
			pstmt.setString(4, "dave@gmail.com");
			pstmt.setString(5, "kate@gmail.com");
			pstmt.executeUpdate();

			messageID += 1;

			pstmt = m_conn.prepareStatement("INSERT INTO ChatMessage"
					+ "(ID, ParentID, MessageContent, PostingTime, FromEmailAddress, ToEmailAddress) "
					+ "VALUES(?,?,?,?,?,?)");
			
			pstmt.setInt(1, messageID); // 6
			pstmt.setInt(2, 5);
			pstmt.setString(3, "Alala?");
			pstmt.setDate(4, new java.sql.Date(millis));
			pstmt.setString(5, "kate@gmail.com");
			pstmt.setString(6, "dave@gmail.com");
			pstmt.executeUpdate();

			messageID += 1;

			m_conn.commit();
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}

	public static void DropTables(Statement s) {
		try {
			s.executeUpdate("DROP TABLE ReportMembers");
			s.executeUpdate("DROP TABLE ChatMessage");
			s.executeUpdate("DROP TABLE Favorite");
			s.executeUpdate("DROP TABLE Pet");
			s.executeUpdate("DROP TABLE Member");
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}

	public static void CreateTables(Statement s) {
		System.out.println("Creating tables for Pet Adoption\n");
		try {
			
			s.executeUpdate("CREATE TABLE Member (\n" + "	EmailAddress  		varchar2(20) primary key,\n"
					+ "	Name	    		varchar2(20) not null,\n" + "	SelfIntroduction 	varchar2(50),\n"
					+ "	Location			varchar2(50) not null,\n" + "	Birthday			date not null,\n"
					+ "	IsAdopter			varchar2(1) check(IsAdopter in ('y', 'n')) not null,\n"
					+ "	IsSender			varchar2(1) check(IsSender in ('y', 'n')) not null,\n"
					+ "	AdoptingExperience 	varchar2(50))");
			
			s.executeUpdate(
					"CREATE TABLE Pet (\n" + "	EmailAddress  	varchar2(20) 	references Member(EmailAddress),\n"
							+ "	Name			varchar2(10),\n" + "	Birthday		date,\n"
							+ "	IsSterilized	varchar2(1)		check(IsSterilized in ('y', 'n')),\n"
							+ "	Breed			varchar2(7) 	check(Breed in ('Cat', 'Dog', 'Rabbit')) not null,\n"
							+ "	DaysWalk		number(3) 		check (DaysWalk > 0),\n"
							+ "	BiteWire		varchar2(1) 	check(BiteWire in ('y', 'n')),\n"
							+ "	constraint PK_Pet 				primary key(EmailAddress, Name, Birthday))");
			s.executeUpdate("CREATE TABLE Favorite (\n" + "	EmailAddressMember	varchar2(20),\n"
					+ "	EmailAddressPet		varchar2(20),\n" + "	PetName				varchar2(10),\n"
					+ "	Birthday			date,\n"
					+ "	constraint PK_Favorite 	primary key(EmailAddressMember, EmailAddressPet, PetName, Birthday),\n"
					+ "	constraint FK1_Favorite foreign key(EmailAddressMember) references Member(EmailAddress),\n"
					+ "	constraint FK2_Favorite	foreign key(EmailAddressPet, PetName, Birthday) references Pet(EmailAddress, Name, Birthday)\n"
					+ ")");
			s.executeUpdate("CREATE TABLE ChatMessage (\n" + "	ID 					Number(10) primary key,\n"
					+ "	ParentID			Number(10),\n" + "	MessageContent		varchar2(50) not null,\n"
					+ "	PostingTime			date,\n" + "	FromEmailAddress	varchar2(20) not null,\n"
					+ "	ToEmailAddress		varchar2(20) not null,\n"
					+ "	constraint FK1_Chat	foreign key(FromEmailAddress) 	references Member(EmailAddress),\n"
					+ "	constraint FK2_Chat	foreign key(ToEmailAddress) 	references Member(EmailAddress)\n" + ")");
					
			
			s.executeUpdate("CREATE TABLE ReportMembers (" + "	ID		Number(10) PRIMARY KEY, \n"
					+ "	Accuser		varchar2(20) NOT NULL,\n" + "	Accused		varchar2(20) NOT NULL,\n"
					+ "	Reason		varchar2(13) CHECK (Reason in ('Scamming', 'Foul Language')),\n"
					+ "	Content		varchar2(200) NOT NULL,\n"
					+ "	FOREIGN KEY(Accuser) REFERENCES Member(EmailAddress),\n"
					+ "	FOREIGN KEY(Accused) REFERENCES Member(EmailAddress))");
		} catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
	}
}
