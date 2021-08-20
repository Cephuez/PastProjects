//package UACATS.servlets;
import java.util.*;

import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
//import UACATS.servlets.*;
//import UACATS.utils.*;
import java.sql.*;

public class AddIndividualServlet extends HttpServlet
{
	String dobmonth;
	String dobday;
	String dobyear;

	String firstname;
	String lastname;
	String email;
	String phone;

	String pw1 , pw2;

	String userAlredyExists = "Error: User exists.";
	String allOtherErrors = "Error: Request could not be carried out.";
	String passwordsDontMatch = "The two passwords did not match. Please enter the same password twice. Please try again.";

	int errorCode;//if its 1 print error 'userAlreadyExists'; if its 2 print error 'allOtherErrors'; 3 if passwords didnt match...

	int userId;

	public AddIndividualServlet()
	{
		super();
	}


	public void drawUpdateMessage(HttpServletRequest req, PrintWriter out)
	{

		String firstname = req.getParameter("firstname");
		String lastname = req.getParameter("lastname");
		String dobmonth = req.getParameter("DoBmonth");
		String dobday = req.getParameter("DoBday");
		String dobyear = req.getParameter("DoByear");
		String email = req.getParameter("email");
		String phone = req.getParameter("phone");
		String pword = req.getParameter("pw");

		String blank_str = "";
		if(email.equals(blank_str))
		    email = "none";

		out.println("<h2 align=\"center\">Add New User Success!</h2>");
		out.println("<br>");

 		out.println("<p><b>UserID:"+userId+"</b></p>");

		out.println("<p><b>First Name:</b>  " + firstname+"</p>");
		out.println("<p><b>Last Name:</b> " + lastname+"</p>");
		out.println("<p><b>Date of Birth:</b>  " + dobmonth + "/" + dobday + "/" +dobyear + "</p>");
		out.println("<p><b>Email:</b>  " + email+"</p>");
		out.println("<p><b> Phone Number:</b>  " + phone +"</p>");

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
		out.println("<title>IndividualRegister</title>");
		out.println("</head>");

		out.println("<body>");
		out.println("<p>");
		out.println("<center>");
		out.println("<font size=5 face=\"Arial,Helvetica\">");
		out.println("<b>UACATS---Register for UACATS as Individual</b><br></font>");

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

	public void drawFailOption(HttpServletRequest req, PrintWriter out)
	{
		out.println("<h2 align=\"center\">Error: Request could not be carried out.</h2>");
		out.println("<form name=\"logoutbad\" action=index.html>");
		out.println("<center>");
		out.println("<input type=submit name=\"tohomebad\" value=\"Return to home\">&nbsp&nbsp");
		out.println("</center>");
		out.println("</form>");
	}



	public void drawAddIndividualMenu(HttpServletRequest req, PrintWriter out)
	{
		out.println("<form name=\"AddIndividual\" action=AddIndividualServlet method=get>");
		out.println("<br><br>");
		out.println("<font size=3>");
		out.println("<p>");
		out.println("<b>First Name:</b>");
		out.println("<input type=text name=\"firstname\">");
		out.println("<br>");
		out.println("</p>");

		out.println("<p>");
		out.println("<b>Last Name:</b>");
		out.println("<input type=text name=\"lastname\">");
		out.println("<br>");
		out.println("</p>");

		out.println("<h4 align=\"center\">Date of Birth");
		out.println("<p align=\"center\">");
		out.println("<select size=\"12\" name=\"DoBmonth\">");
		out.println("<option selected value=\"null\">Month</option>");
		out.println("<option value=\"JAN\">January</option>");
		out.println("<option value=\"FEB\">February</option>");
		out.println("<option value=\"MAR\">March</option>");
		out.println("<option value=\"APR\">April</option>");
		out.println("<option value=\"MAY\">May</option>");
		out.println("<option value=\"JUN\">June</option>");
		out.println("<option value=\"JUL\">July</option>");
		out.println("<option value=\"AUG\">August</option>");
		out.println("<option value=\"SEP\">September</option>");
		out.println("<option value=\"OCT\">October</option>");
		out.println("<option value=\"NOV\">November</option>");
		out.println("<option value=\"DEC\">December</option>");
		out.println("</select>");
		out.println("</p>");

		out.println("<p align=\"center\">");
		out.println("<select size=\"1\" name=\"DoBday\">");
		out.println("<option selected value=\"null\">Day</option>");
		out.println("<option value=\"01\">01</option>");
		out.println("<option value=\"02\">02</option>");
		out.println("<option value=\"03\">03</option>");
		out.println("<option value=\"04\">04</option>");
		out.println("<option value=\"05\">05</option>");
		out.println("<option value=\"06\">06</option>");
		out.println("<option value=\"07\">07</option>");
		out.println("<option value=\"08\">08</option>");
		out.println("<option value=\"09\">09</option>");
		out.println("<option value=\"10\">10</option>");
		out.println("<option value=\"11\">11</option>");
		out.println("<option value=\"12\">12</option>");
		out.println("<option value=\"13\">13</option>");
		out.println("<option value=\"14\">14</option>");
		out.println("<option value=\"15\">15</option>");
		out.println("<option value=\"16\">16</option>");
		out.println("<option value=\"17\">17</option>");
		out.println("<option value=\"18\">18</option>");
		out.println("<option value=\"19\">19</option>");
		out.println("<option value=\"20\">20</option>");
		out.println("<option value=\"21\">21</option>");
		out.println("<option value=\"22\">22</option>");
		out.println("<option value=\"23\">23</option>");
		out.println("<option value=\"24\">24</option>");
		out.println("<option value=\"25\">25</option>");
		out.println("<option value=\"26\">26</option>");
		out.println("<option value=\"27\">27</option>");
		out.println("<option value=\"28\">28</option>");
		out.println("<option value=\"29\">29</option>");
		out.println("<option value=\"30\">30</option>");
		out.println("<option value=\"31\">31</option>");
		out.println("</select>");
		out.println("</p>");

		out.println("<p align=\"center\"><b>Year:</b>");
		out.println("<input type=text name=\"DoByear\"<br><br><br>");
		out.println("</p>");

		out.println("<b> Email Address:</b>");
		out.println("<input type=text name=\"email\" size=20<br><br>");
		out.println("<b> Phone Number:</b>");
		out.println("<input type=text name=\"phone\"<br><br>");

		out.println("<p><br><b> Password:</b>");
		out.println("<input type=text name=\"pw\"><br><br>");

		out.println("<b> Confirm Password:</b>");
		out.println("<input type=text name=\"pwconfirm\"><br><br>");
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
		out.println("<form name=\"Cancel\" action=AddIndividualServlet method=get>");
		out.println("<input type=submit name=\"Cancel\" value=\"Cancel\">&nbsp&nbsp");
		out.println("</form>");
		out.println("</td>");
		out.println("</tr>");


		out.println("<tr>");
		out.println("<td>");

		out.println("<form name=\"logout\" action=index.html>");
		out.println("<input type=submit name=\"tohome\" value=\"Return to home\">&nbsp&nbsp");
		out.println("</form>");
		out.println("</tr>");
		out.println("</table>");


		out.println("<br><br><br>");

	}




	public void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException
	{
		System.out.println("\nIn AddIndividualServlet doGet");
		res.setContentType("text/html");
		PrintWriter out = res.getWriter();

		Connection conn=null;
		try{
			Class.forName ("oracle.jdbc.OracleDriver");// register drivers
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
		//Get the firstname
		String[] paramValues = request.getParameterValues("firstname");
		firstname = paramValues[0];

		//Get the lastname
		paramValues = request.getParameterValues("lastname");
		lastname = paramValues[0];

		paramValues = request.getParameterValues("DoBday");
		dobday = paramValues[0];

		paramValues = request.getParameterValues("DoBmonth");
		dobmonth = paramValues[0];

		paramValues = request.getParameterValues("DoByear");
		dobyear = paramValues[0];

		paramValues = request.getParameterValues("email");
		email = paramValues[0];

		paramValues = request.getParameterValues("phone");
		phone = paramValues[0];

		paramValues = request.getParameterValues("pw");
		pw1 = paramValues[0];

		paramValues = request.getParameterValues("pwconfirm");
		pw2 = paramValues[0];

		if(!pw1.equals(pw2)){
			System.out.println("Here....");
			errorCode = 3;
			return false;
		}

		//Now query the database to see if this user exists......
		try{
			Statement s = conn.createStatement();

			ResultSet rs = s.executeQuery("Select UserID from INDIVIDUAL where FirstName = '" + firstname
														+ "' and LastName = '"+lastname
														+ "' and DoB = '" + dobday +"-"+dobmonth +"-"+dobyear+"'");
			int count = 0;
			while(rs.next())count++;

			if(count > 0){
				errorCode = 1;
				return false;
			}
		}catch(SQLException sqle){
			sqle.printStackTrace();
			System.out.println("No..here...here....");
			errorCode = 2;
			return false;
		}

		//The user does not already exits in the DB. Insert the new user in the two tables...
		//For table Individual, get the largest id used so far....
		int id = -1;
		try{
			Statement s = conn.createStatement();

			ResultSet rs = s.executeQuery("Select UserID from INDIVIDUAL");
			while(rs.next()){
				int temp = rs.getInt(1);
				if(temp > id)
					id = temp;
			}

			System.out.println("Old id is "+id);

			//Insert info into table CatUser...
			s.executeUpdate("INSERT INTO CatUser VALUES("+(id+1)+" , "+phone+" , "+pw1+" , '"+email+"')");

			//Insert info into table INDIVIDUAL....
			s.executeUpdate("INSERT INTO INDIVIDUAL VALUES('"+firstname+"' , '"+lastname+"' , '"+dobday +"-"+dobmonth +"-"+dobyear+"' , "+(id+1)+")");


			userId = id+1;
		}catch(SQLException sqle){
			sqle.printStackTrace();
			System.out.println("No..here...over here....");
			errorCode = 2;
			return false;
		}

		//Add this info into the session...
		HttpSession session = request.getSession();
		session.setAttribute("loginID" , ""+userId);
		session.setAttribute("loginPW" , ""+pw1);

		return true;
	}
}
