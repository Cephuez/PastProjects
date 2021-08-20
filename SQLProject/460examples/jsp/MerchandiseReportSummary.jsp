<%@ page language="java" contentType="text/html" %>
<%@ page import="java.sql.*" %>

<html>

		<head><title>UACATS Finding Result</title></head>
		<body link=#f0f0ff alink vlink=#f0f0ff>
		<p>
		<center>
		<font size=5 face=Arial, Helvetica >
		<b>UACATS</b><br>
		<font size=4>
		University of Arizona Classified Ads System<br>
		</font>
		</font>
		<hr>
		<br>

		<b>Merchandise Found in UACATS</b>

<br>


<%
	Class.forName ("oracle.jdbc.OracleDriver");// register drivers
	System.out.println("Attempting to connect 22222");
	Connection conn = DriverManager.getConnection("jdbc:oracle:thin:@aloe.cs.arizona.edu:1521:oracle","yourusername","yourpassword");

	Statement s = conn.createStatement();
	String query = "SELECT * from MERCHANDISE, BOOK , INDIVIDUAL , CatUser WHERE " +
			"CatUser.UserID = INDIVIDUAL.UserID AND CatUser.UserID = MERCHANDISE.UserID "+
			"AND MERCHANDISE.UserID = BOOK.UserID AND MERCHANDISE.MID = BOOK.MID AND INDIVIDUAL.UserID = BOOK.UserID ";
	System.out.println(query);
	ResultSet rs = s.executeQuery(query);
	System.out.println("Executed the query");
	int count =0;
	while(rs.next()){
		System.out.println("In ze query results");
		String booktitle=rs.getString("BookTitle");
		String author=rs.getString("BookAuthor");
		String howold=rs.getString("HowOldMonth");
		String price=rs.getString("AskingPrice");
		String description=rs.getString("Description");

		String ownerfirstname=rs.getString("FirstName");
		String ownerlastname=rs.getString("LastName");
		String owneremail=rs.getString("Email");
		String ownerphone=rs.getString("PhoneNum");

		out.println("<br>");
		out.println("<hr>");
		out.println("<p><b>Book Title:</b>  " + booktitle+"</p>");
		out.println("<p><b>Book Author:</b> " + author+"</p>");
		out.println("<p><b>How old:</b>  " + howold+"  months</p>");
		out.println("<p><b>Asking Price:</b>  $" + price+"</p>");
		out.println("<p><b>Description:</b>  " + description+"</p>");
		out.println("<br>");
		out.println("<p><b> Owner's Name:</b>  " + ownerfirstname + "  " + ownerlastname+"</p>");
		out.println("<p><b> Owner's Email:</b>  " +owneremail+"</p>");
		out.println("<p><b> Owner's Phone Number:</b>  " + ownerphone + "</p>");
		out.println("<hr>");
		out.println("<br><br>");
	}
		
						
	out.println("<table>");
	out.println("<tr>");
	out.println("<td>");
	out.println("<form name=\"mainmenu\" action=../LoginServlet method=get>");
	out.println("<input type=submit name=\"MainMenu\" value=\"Main Menu\">");
	out.println("</form>");
	out.println("</td>");
	out.println("</tr>");


	out.println("<td>");
	out.println("<form name=\"logout\" action=../LogoutServlet method=get>");
	out.println("<input type=submit name=\"logoutUACATS\" value=\"Logout\">");
	out.println("</form>");
	out.println("</td>");

	out.println("</table>");

%>
		</center>
		</p>
		</body>
		</html>

</html>
