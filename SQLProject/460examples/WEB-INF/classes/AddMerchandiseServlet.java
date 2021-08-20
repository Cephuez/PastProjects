//package UACATS.servlets;
import java.util.*;

import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
//import UACATS.utils.*;
import java.sql.*;

public class AddMerchandiseServlet extends HttpServlet
{

	public AddMerchandiseServlet()
	{
		super();
	}


	public void drawUpdateMessage(HttpServletRequest req, PrintWriter out)
	{
		out.println("<h2 align=\"center\">Add New Merchandise Success!</h2>");
		out.println("<br>");

 		out.println("<p><b>UserID:"+userId+"</b></p>");

		out.println("<p><b>MID:</b>  " + maxMID+"</p>");
		out.println("<p><b>Section:</b> " + section+"</p>");
		out.println("<p><b>AskingPrice:</b>  " + price + "</p>");
		out.println("<p><b>HowOldMonth:</b>  " + howOld+"</p>");
		out.println("<p><b> Description:</b>  " + description +"</p>");
		out.println("<p><b> Title:</b>  " + Title +"</p>");
		out.println("<p><b> Author:</b>  " + Author +"</p>");

		out.println("<br><br><br>");

		out.println("<form name=\"MainMenu\" action=LoginServlet>");
		out.println("<input type=submit name=\"MainMenu\" value=\"MainMenu\">");
		out.println("</form>");

		out.println("<br>");

		out.println("<form name=\"logout\" action=LogoutServlet method=get>");
		out.println("<input type=submit name=\"logoutUACATS\" value=\"Logout\">");
		out.println("</form>");

	}




	public void drawHeader(HttpServletRequest req, PrintWriter out)
	{
		out.println("<html>");
		out.println("<head>");
		out.println("<title>Add Merchandise</title>");
		out.println("</head>");

		out.println("<body>");
		out.println("<p>");
		out.println("<center>");
		out.println("<font size=5 face=\"Arial,Helvetica\">");
		out.println("<b>UACATS---Add Merchandise into UACATS</b><br></font>");

		out.println("<hr");
		out.println("<br><br>");
	}


	public void drawFooter(HttpServletRequest req, PrintWriter out)
	{
		out.println("</center>");
		out.println("</p>");
		out.println("</body>");
		out.println("</html>");
	}


	public void drawAddIndividualMenu(HttpServletRequest req, PrintWriter out)
	{
		if(errorCode ==1){
			out.println("<h2 align=\"center\">"+merchandiseAlredyExists+"!</h2>");
			out.println("<br>");
		}else if(errorCode == 2){
			out.println("<h2 align=\"center\">"+allOtherErrors+"!</h2>");
			out.println("<br>");
		}

		errorCode = 0;

		out.println("<form name=\"AddMerchandise\" action=AddMerchandiseServlet method=get>");
		out.println("<br><br>");
		out.println("<font size=3>");

		out.println("<p>");
		out.println("<b>AskingPrice:</b>");
		out.println("<input type=text name=\"AskingPrice\">");
		out.println("<br>");
		out.println("</p>");

		out.println("<p>");
		out.println("<b>HowOldMonth:</b>");
		out.println("<input type=text name=\"HowOldMonth\">");
		out.println("<br>");
		out.println("</p>");


		out.println("<p>");
		out.println("<b>Description:</b>");
		out.println("<input type=text name=\"Description\">");
		out.println("<br>");
		out.println("</p>");

		out.println("<p>");
		out.println("<b>Title:</b>");
		out.println("<input type=text name=\"Title\">");
		out.println("<br>");
		out.println("</p>");

		out.println("<p>");
		out.println("<b>Author:</b>");
		out.println("<input type=text name=\"Author\">");
		out.println("<br>");
		out.println("</p>");

		out.println("<table>");
		out.println("<tr>");
		out.println("<td>");

		out.println("<input type=submit name=\"Submit\" value=\"AddMe\">&nbsp&nbsp");

		out.println("</td");
		out.println("</tr>");
		out.println("</form>");
		out.println("<tr>");
		out.println("<td>");
		out.println("<form name=\"Cancel\" action=AddMerchandiseServlet method=get>");
		out.println("<input type=submit name=\"Cancel\" value=\"Cancel\">&nbsp&nbsp");
		out.println("</form>");
		out.println("</td>");
		out.println("</tr>");


		out.println("<tr>");
		out.println("<td>");

		out.println("<p>");
		out.println("<form name=\"Summary\" action=LoginServlet method=get>");
		out.println("<input type=submit name=\"MainMenu\" value=\"Main Menu\">");
		out.println("</form>");
		out.println("</p>");

		out.println("</tr>");
		out.println("</table>");


		out.println("<br><br><br>");

	}




	public void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException
	{
		System.out.println("\nIn AddMerchandiseServlet doGet");
		res.setContentType("text/html");
		PrintWriter out = res.getWriter();

		Connection conn=null;
		try{
			Class.forName ("oracle.jdbc.driver.OracleDriver");// register drivers
			System.out.println("Attempting to connect 111");
			conn = DriverManager.getConnection(OracleConnect.connect_string,OracleConnect.user_name,OracleConnect.password);
		}catch(Exception e){
			e.printStackTrace();
		}

		drawHeader(req,out);

		if(req.getParameter("Submit") == null || !enterInfo(req , conn))
		{
			drawAddIndividualMenu(req,out);
		}
		else
		{
			drawUpdateMessage(req,out);
		}

		drawFooter(req,out);
		try{
			conn.close();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}

	boolean enterInfo(HttpServletRequest request , Connection conn){
		System.out.println("\nIn AddIndividualServlet enterInfo");

		HttpSession session = request.getSession();
		userId = (String)session.getAttribute("loginID");
		if(userId == null){
			errorCode = 2;
			return false;
		}

		String[] paramValues = request.getParameterValues("AskingPrice");
		price = paramValues[0];

		paramValues = request.getParameterValues("HowOldMonth");
		howOld = paramValues[0];

		paramValues = request.getParameterValues("Description");
		description = paramValues[0];

		paramValues = request.getParameterValues("Title");
		Title = paramValues[0];

		paramValues = request.getParameterValues("Author");
		Author = paramValues[0];

		maxMID = 0;
		//Now query the database to get the largest MID in the merchandise table
		try{
			Statement s = conn.createStatement();

			ResultSet rs = s.executeQuery("Select MID from MERCHANDISE");

			while(rs.next()){
				int temp = rs.getInt("MID");
				if(temp > maxMID)
					maxMID = temp;
			}
			maxMID++;

		}catch(SQLException sqle){
			sqle.printStackTrace();
			System.out.println("No..here...here....");
			errorCode = 2;
			return false;
		}

		//The user does not already exits in the DB. Insert the new user.....
		int id = -1;
		try{
			Statement s = conn.createStatement();

			//Insert info into table MERCHANDISE...
			s.executeUpdate("INSERT INTO MERCHANDISE VALUES("+userId+" , "+maxMID+" , '"+section+"' , "+price+" , "+howOld+" , '"+description+ "')");

			s.executeUpdate("INSERT INTO BOOK VALUES("+userId+" , "+maxMID+" , '"+Title+"' , '"+Author+"')");

		}catch(SQLException sqle){
			sqle.printStackTrace();
			System.out.println("No..here...over here....");
			errorCode = 2;
			return false;
		}

		return true;
	}

	String userId;
	String section = "b";
	int maxMID;
	String price;
	String howOld;
	String description;

	String Title;
	String Author;


	String merchandiseAlredyExists = "Error: Merchandise exists.";
	String allOtherErrors = "Error: Request could not be carried out.";

	int errorCode;//if its 1 print error 'merchandiseAlreadyExists'; if its 2 print error 'allOtherErrors';


}
