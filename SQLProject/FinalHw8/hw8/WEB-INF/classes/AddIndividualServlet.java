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
	String email = "";
	String name = "";
	String selfIntroduction = "";
	String location = "";
	String dobmonth = "";
	String dobday = "";
	String dobyear = "";
	String adopter = "";
	String sender = "";
	String birthday = "";
	String adoptingExperience = "";
	
	String petName = "";
	String petBirthday = "";
	String isSterilized = "";
	String breed = "";
	String daysWalk = "";
	String biteWire = "";
	
	int status = 0;
	int usedEmail = 0;
	int inputCheck[] = new int[3];
	boolean finalUpdateMessage;
	boolean moreAdoptingInfo;
	boolean moreSenderInfo;
	boolean enteredInfo;
	boolean extraPetInfo;
	boolean inProcess;
	boolean morePetInfo = false;
	boolean submitAnswer = false;
	
	PreparedStatement pstmt = null;
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
		
		String email = req.getParameter("email");
		String name = req.getParameter("name");
		String selfIntroduction = req.getParameter("selfIntroduction");
		String location = req.getParameter("location");
		String dobday = req.getParameter("DoBday");
		String dobmonth = req.getParameter("DoBmonth");
		String dobyear = req.getParameter("DoByear");
		String adopter = req.getParameter("adopter");
		String sender = req.getParameter("sender");
		String adoptingExperience = req.getParameter("adoptingExperience");

		String blank_str = "";
		if(email.equals(blank_str))
		    email = "none";

		out.println("<h2 align=\"center\">Add New User Success!</h2>");
		out.println("<br>");

		out.println("<p><b>Email:</b>  " + email+"</p>");
		out.println("<p><b>Name:</b>  " + name+"</p>");
		out.println("<p><b>Self-Introduction:</b> " + selfIntroduction+"</p>");
		out.println("<p><b>Location:</b> " + location+"</p>");
		out.println("<p><b>Date of Birth:</b>  " + dobmonth + "/" + dobday + "/" +dobyear + "</p>");
		out.println("<p><b>Adopter:</b>  " + adopter +"</p>");
		out.println("<p><b>Sender:</b>  " + sender +"</p>");
		out.println("<p><b>Adopting Experience:</b> " + adoptingExperience+"</p>");
		

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
		//out.println("<title>PetAdoptRegister</title>");
		out.println("<title>PetAdoptRegister</title>");
		out.println("</head>");

		out.println("<body>");
		out.println("<p>");
		out.println("<center>");
		out.println("<font size=5 face=\"Arial,Helvetica\">");
		//out.println("<b>Register as a member for PetAdopt</b><br></font>");
		out.println("<b>Register as qps,fmdw</b><br></font>");

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

	public void requestAdopterInfo(HttpServletRequest req, PrintWriter out) {
		InsertDates inputDates = new InsertDates();		
		out.println("<font size=3>");
		out.println("<p>");
		out.println("<b>Adopting Experience:</b>");
		out.println("<textarea id=\"adoptingExperience\" name = \"adoptingExperience\" row=\"4\" cols=\"25\" maxlength = \"50\"> </textarea>");
		out.println("<br>");
		out.println("</p>");
		
		//out.println("<input type=submit name=\"SubmitPost\" value=\"SubmitPost\">&nbsp&nbsp");
	}
	
	public void requestSenderInfo(HttpServletRequest req, PrintWriter out) {
		InsertDates inputDates = new InsertDates();		
		out.println("<font size=3>");
		out.println("<p>");
		out.println("<b>Pet Name:</b>");
		out.println("<textarea id=\"petName\" name = \"petName\" row=\"4\" cols=\"25\" maxlength = \"10\"> </textarea>");			
		out.println("<br>");
		out.println("</p>");

		out.println("<h4 align=\"center\">Month");
		out.println("<p align=\"center\">");
		out.println("<select size=\"12\" name=\"DoBmonthPet\">");
		out.println("<option selected value=\"01\">January</option>");
		inputDates.PlaceMonths(out);
		out.println("</select>");
		out.println("</p>");

		out.println("<h4 align=\"center\">Day");
		out.println("<p align=\"center\">");
		out.println("<select size=\"1\" name=\"DoBdayPet\">");
		out.println("<option selected value=\"01\">01</option>");
		inputDates.PlaceDays(out);
		out.println("</select>");
		out.println("</p>");
		
		out.println("<h4 align=\"center\">Year");
		out.println("<p align=\"center\">");
		out.println("<select size=\"1\" name=\"DoByearPet\">");
		out.println("<option selected value=\"1922\">1922</option>");
		inputDates.PlaceYears(out);
		out.println("</select>");
		out.println("</p>");
		
		out.println("<font size=3>");
		out.println("<p>Is it Sterilized?</p>");
		out.println("<input type=\"radio\" id=\"senderYesPet\" name=\"senderPetSte\" value=\"Yes\" checked>");
		out.println("<label for=\"Yes\">Yes</label><br>");
		out.println("<input type=\"radio\" id=\"senderNoPet\" name=\"senderPetSte\" value=\"No\">");
		out.println("<label for=\"No\">No</label><br>");
		out.println("<br>");
		
		out.println("<font size=3>");
		out.println("<p>Is it Sterilized?</p>");
		out.println("<input type=\"radio\" id=\"Cat\" name=\"senderPet\" value=\"Cat\" checked>");
		out.println("<label for=\"Cat\">Cat</label><br>");
		out.println("<input type=\"radio\" id=\"Dog\" name=\"senderPet\" value=\"Dog\">");
		out.println("<label for=\"Dog\">Dog</label><br>");
		out.println("<input type=\"radio\" id=\"Rabbit\" name=\"senderPet\" value=\"Rabbit\">");
		out.println("<label for=\"Rabbit\">Rabbit</label><br>");
		out.println("<br>");
		
		//out.println("<input type=submit name=\"SubmitPost\" value=\"SubmitPost\">&nbsp&nbsp");
	}
	
	public void requestExtraPetInfo(HttpServletRequest req, PrintWriter out) {
		if(breed.equals("Dog")) {
			out.println("<font size=3>");
			out.println("<p>");
			out.println("<b>Days Walk(Put valid number):</b>");
			out.println("<textarea id=\"petName\" name = \"petName\" row=\"1\" cols=\"3\" maxlength = \"3\"> </textarea>");			
			out.println("<br>");
			out.println("</p>");
		}else {
			out.println("<font size=3>");
			out.println("<p>Will rabbit bite wires?</p>");
			out.println("<input type=\"radio\" id=\"biteYes\" name=\"bite\" value=\"Yes\" checked>");
			out.println("<label for=\"Yes\">Yes</label><br>");
			out.println("<input type=\"radio\" id=\"biteNo\" name=\"bite\" value=\"No\">");
			out.println("<label for=\"No\">No</label><br>");
			out.println("<br>");
		}
	}
	
	public void drawAddIndividualMenu(HttpServletRequest req, PrintWriter out)
	{
		InsertDates inputDates = new InsertDates();
		out.println("<form name=\"AddIndividual\" action=AddIndividualServlet method=get>");
		out.println("<br><br>");
		
		out.println("<font size=3>");
		out.println("<p>");
		if(inputCheck[0] == 1) {
			out.println("<b>Email(Left Blank):</b>");
		}else if(usedEmail == 1){
			out.println("<b>Email(Email in Used):</b>");
		}else {
			out.println("<b>Email:</b>");
		}
		out.println("<input type=text name=\"email\" maxlength = \"20\">");
		out.println("<br>");
		out.println("</p>");
		
		
		out.println("<font size=3>");
		out.println("<p>");
		if(inputCheck[1] == 1) {
			out.println("<b>Name(Left Blank):</b>");
		}else {
			out.println("<b>Name:</b>");
		}
		out.println("<input type=text name=\"name\" maxlength = \"20\">");
		out.println("<br>");
		out.println("</p>");
		
		out.println("<font size=3>");
		out.println("<p>");
		out.println("<b>Self Introduction:</b>");
		out.println("<textarea id=\"selfIntroduction\" name = \"selfIntroduction\" row=\"4\" cols=\"25\" maxlength = \"50\"> </textarea>");
		out.println("<br>");
		out.println("</p>");

		out.println("<font size=3>");
		out.println("<p>");
		if(inputCheck[2] == 1) {
			out.println("<b>Location(Left Blank):</b>");
		}else {
			out.println("<b>Location:</b>");
		}
		out.println("<input type=text name=\"location\" maxlength = \"50\">");
		out.println("<br>");
		out.println("</p>");
		
		out.println("<h4 align=\"center\">Month");
		out.println("<p align=\"center\">");
		out.println("<select size=\"12\" name=\"DoBmonth\">");
		out.println("<option selected value=\"01\">January</option>");
		inputDates.PlaceMonths(out);
		out.println("</select>");
		out.println("</p>");

		out.println("<h4 align=\"center\">Day");
		out.println("<p align=\"center\">");
		out.println("<select size=\"1\" name=\"DoBday\">");
		out.println("<option selected value=\"01\">01</option>");
		inputDates.PlaceDays(out);
		out.println("</select>");
		out.println("</p>");
		
		out.println("<h4 align=\"center\">Year");
		out.println("<p align=\"center\">");
		out.println("<select size=\"1\" name=\"DoByear\">");
		out.println("<option selected value=\"1922\">1922</option>");
		inputDates.PlaceYears(out);
		out.println("</select>");
		out.println("</p>");
		
		out.println("<font size=3>");
		out.println("<p>Are you an adopter?</p>");
		out.println("<input type=\"radio\" id=\"adopterYes\" name=\"adopter\" value=\"Yes\" checked>");
		out.println("<label for=\"Yes\">Yes</label><br>");
		out.println("<input type=\"radio\" id=\"adopterNo\" name=\"adopter\" value=\"No\">");
		out.println("<label for=\"No\">No</label><br>");
		out.println("<br>");

		out.println("<font size=3>");
		out.println("<p>Are you a sender?</p>");
		out.println("<input type=\"radio\" id=\"senderYes\" name=\"sender\" value=\"Yes\" checked>");
		out.println("<label for=\"Yes\">Yes</label><br>");
		out.println("<input type=\"radio\" id=\"senderNo\" name=\"sender\" value=\"No\">");
		out.println("<label for=\"No\">No</label><br>");
		out.println("<br>");
		
		if(moreAdoptingInfo) {
			requestAdopterInfo(req, out);
		}
		
		if(moreSenderInfo) {
			requestSenderInfo(req, out);
		}
		
		if(morePetInfo) {
			requestExtraPetInfo(req, out);	
		}

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
	
	public void SubmitAllResponses(HttpServletRequest req, Connection conn) {
		SubmitMember(conn);
		SubmitSender(req, conn);
		//if(sender.equals("Yes"))
		//SubmitSender(req, conn);
	}
	
	private void SubmitMember(Connection conn) {
		adoptingExperience = "No experience XD";
		try{
			pstmt = conn.prepareStatement("INSERT INTO Member VALUES(?,?,?,?,?,?,?,?)");
			pstmt.setString(1, email);
			pstmt.setString(2, name);
			pstmt.setString(3, selfIntroduction);
			pstmt.setString(4, location);
			pstmt.setDate(5, java.sql.Date.valueOf(birthday));
			pstmt.setString(6, adopter.substring(0,1).toLowerCase());
			pstmt.setString(7, sender.substring(0,1).toLowerCase());
			pstmt.setString(8, adoptingExperience);
			pstmt.executeUpdate();
			finalUpdateMessage = true;
			
		}catch(SQLException sqle){
			sqle.printStackTrace();
			System.out.println("No..here...over here....");
			errorCode = 2;
		}
	}
	
	private void SubmitSender(HttpServletRequest req, Connection conn) {
		petName = "Poggers";
		petBirthday = "2010-10-11";
		isSterilized = "Yes";
		breed = "Dog";
		daysWalk = "350";
		biteWire = "Yes";
		try{
			//pstmt = conn.prepareStatement("INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed) "
			//		+ "VALUES(?,?,?,?,?)");

			if(breed.equals("Cat")) {
				pstmt = conn.prepareStatement("INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed) "
						+ "VALUES(?,?,?,?,?)");
				pstmt.setString(1, email);
				pstmt.setString(2, petName);
				pstmt.setDate(3, java.sql.Date.valueOf(petBirthday));
				pstmt.setString(4, isSterilized.substring(0,1).toLowerCase());
				pstmt.setString(5, breed);
				pstmt.executeUpdate();
			}else if(breed.equals("Dog")) {
				pstmt = conn.prepareStatement("INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed, DaysWalk) "
						+ "VALUES(?,?,?,?,?,?)");
				pstmt.setString(1, email);
				pstmt.setString(2, petName);
				pstmt.setDate(3, java.sql.Date.valueOf(petBirthday));
				pstmt.setString(4, isSterilized.substring(0,1).toLowerCase());
				pstmt.setString(5, breed);
				pstmt.setInt(6, Integer.valueOf(daysWalk));
				pstmt.executeUpdate();
			}else {
				pstmt = conn.prepareStatement("INSERT INTO Pet(EmailAddress, Name, Birthday, IsSterilized, Breed, Bitewire) "
						+ "VALUES(?,?,?,?,?,?)");
				pstmt.setString(1, email);
				pstmt.setString(2, petName);
				pstmt.setDate(3, java.sql.Date.valueOf(petBirthday));
				pstmt.setString(4, isSterilized.substring(0,1).toLowerCase());
				pstmt.setString(5, breed);
				pstmt.setString(6, biteWire.substring(0,1).toLowerCase());
				pstmt.executeUpdate();
			}
			finalUpdateMessage = true;
			
		}catch(SQLException sqle){
			sqle.printStackTrace();
			System.out.println("No..here...over here....");
		}
	}

	public void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException
	{
		inputCheck[0] = 0;
		inputCheck[1] = 0;
		inputCheck[2] = 0;
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

		if(req.getParameter("Submit") == null || !enterInfo(req , conn)){		
			drawAddIndividualMenu(req, out);
		}else {
			drawAddIndividualMenu(req, out);
			//drawUpdateMessage(req, out);
		}
		
		morePetInfo = breed.equals("Dog") || breed.equals("Rabbit");
		
		submitAnswer = adopter.equals("No") && sender.equals("No");
		//submitAnswer = breed.equals("Cat");
		if(submitAnswer) {
			SubmitAllResponses(req, conn);
			drawUpdateMessage(req, out);
		}
		/*
		 * if(!enteredInfo && req.getParameter("Submit") == null || !enterInfo(req , conn)){		
			drawAddIndividualMenu(req, out);
		}
		else if(moreAdoptingInfo) {
			SubmitAllResponses(req, conn);
			drawUpdateMessage(req, out);
			//requestAdopterInfo(req, out);
		}else if(req.getParameter("SubmitPost") != null) {              
			requestSenderInfo(req, out);
		}else if(extraPetInfo) {
			requestExtraPetInfo(req, out);
		}else if(finalUpdateMessage) {
			drawUpdateMessage(req, out);
		}else {
			drawAddIndividualMenu(req, out);
		}
		/*else if(CheckForFurtherInfo()){
			requestFurtherInfo(req, out);
		}else if(finalUpdateMessage) {
			drawUpdateMessage(req, out);
		}*/
		

		drawFooter(req,out);
		try{
			conn.close();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}

	// Will gather information to put into the program
	boolean enterInfo(HttpServletRequest request , Connection conn){
		int id = 0;
		moreAdoptingInfo = false;
		moreSenderInfo = false;
		//Get the firstname
		String[] paramValues = request.getParameterValues("email");
		email = paramValues[0];
		if(email.equals("")) {
			inputCheck[0] = 1;
		}else {
			inputCheck[0] = 0;
		}

		//Get the lastname
		paramValues = request.getParameterValues("name");
		name = paramValues[0];
		if(name.equals("")) {
			inputCheck[1] = 1;
		}else {
			inputCheck[1] = 0;
		}
		
		paramValues = request.getParameterValues("selfIntroduction");
		selfIntroduction = paramValues[0];
		if(selfIntroduction.equals("")) {
			selfIntroduction = " ";
		}
		
		paramValues = request.getParameterValues("location");
		location = paramValues[0];
		if(location.equals("")) {
			inputCheck[2] = 1;
		}else {
			inputCheck[2] = 0;
		}

		paramValues = request.getParameterValues("DoBday");
		dobday = paramValues[0];

		paramValues = request.getParameterValues("DoBmonth");
		dobmonth = paramValues[0];

		paramValues = request.getParameterValues("DoByear");
		dobyear = paramValues[0];

		paramValues = request.getParameterValues("adopter");
		adopter = paramValues[0];
		
		paramValues = request.getParameterValues("sender");
		sender = paramValues[0];
		if(CheckEmptyInputs()) {
			status = 1;
			return true;
		}
		
		status = CheckResponse(conn);
		if(status == 2) {
			return true;
		}
		
		
		moreAdoptingInfo = adopter.equals("Yes");
		moreSenderInfo = sender.equals("Yes");
		birthday = getBirthday(dobyear, dobmonth, dobday);
		
		inProcess = true;
		enteredInfo = true;

		return true;
	}
	
	private boolean CheckForFurtherInfo() {
		return adopter.equals("Yes") || sender.equals("Yes");
	}
	private int CheckResponse(Connection conn) {
		CheckEmptyInputs();
		int num = CheckEmails(conn);
		return num;
	}
	
	private boolean CheckEmptyInputs() {
		return inputCheck[0] == 1 || inputCheck[1] == 1 || inputCheck[2] == 1;
	}
	
	private int CheckEmails(Connection conn) {
		try {
			Statement s = conn.createStatement();
			ResultSet rs = s.executeQuery("SELECT emailAddress FROM Member WHERE emailAddress = '" + email +"' ");
			if(rs.next()) {
				usedEmail = 1;
				return 2;
			}else {
				usedEmail = 0;
			}
		}catch (SQLException e) {
			// do something appropriate with the exception, *at least*:
			e.printStackTrace();
		}
		return 0;
	}
	
	private String getBirthday(String year, String month, String day) {
		String birthDate = year + "-" + month + "-" + day;
		return birthDate;
	}
}














