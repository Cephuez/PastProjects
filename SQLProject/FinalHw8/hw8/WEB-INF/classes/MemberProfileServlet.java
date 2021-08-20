//ShowPetsServlet.java

import java.io.*;             // For PrintWriter
import java.sql.*;            // You need to import the java.sql package to use JDBC
import java.util.Calendar;

import javax.servlet.*;       // For ServletException and other things
import javax.servlet.http.*;  // For HttpServlet and other HttpServlet classes

public class MemberProfileServlet extends HttpServlet {
  private Connection conn;
  private Statement stmt;

  /**
   * The init() method is called when the servlet is first created and
   * is NOT called again for each user request.  So, it is used for
   * one-time initializations. For example, since we could use the same
   * database Connection and Statement for each call to this servlet,
   * initialize the database Connection and Statement here.
   *
   * @throws ServletException a general exception a servlet can throw when it
   *                          encounters difficulty
   */
  public void init() throws ServletException {
    try {
      // Load the Oracle JDBC driver
      Class.forName("oracle.jdbc.OracleDriver");  // load drivers

      // Connect to the database
      conn =
        DriverManager.getConnection (
	     "jdbc:oracle:thin:@aloe.cs.arizona.edu:1521:oracle",
             OracleConnect.user_name,
             OracleConnect.password);

      // Create a Statement
      stmt = conn.createStatement();
    } catch (Exception e) {
      System.out.println("Exception in MemberProfileServlet: " + e);
    }
  }

  public void doGet(HttpServletRequest request, HttpServletResponse response)
                                          throws ServletException, IOException {

    // Make the query to the database and get the results.
    try {
      String memberEmail = request.getParameter("memberEmail");
      //ResultSet rset = stmt.executeQuery ("select EmailAddress, Name, Birthday, IsSterilized, Breed, DaysWalk, BiteWire from Pet ");
      ResultSet rset = stmt.executeQuery ("select EmailAddress, Name, SelfIntroduction, Location, Birthday, IsAdopter, IsSender, AdoptingExperience from Member where EmailAddress = '" + memberEmail + "'");
      // Build the HTML page we want to send as a response to a query given to
      // our servlet.
      response.setContentType("text/html");
      PrintWriter out = response.getWriter();
      rset.next(); //Get information about member. Since the member is logged in this will alwasy return something.

      System.out.println("Obtaining Information about user 2: ");
      String userName = rset.getString(2);
      System.out.println("Obtaining Information about user 3: ");
      String userIntro = rset.getString(3);
      System.out.println("Obtaining Information about user 4: ");
      String userLocation = rset.getString(4);
      System.out.println("Obtaining Information about user 5: ");
      String userBirthday = rset.getString(5);
      System.out.println("Obtaining Information about user 6: ");
      String isAdopter = rset.getString(6);
      System.out.println("Obtaining Information about user 7: ");
      String isSender = rset.getString(7);
      System.out.println("Obtaining Information about user 8: ");
      String userAdoptExp = rset.getString(8);
      System.out.println("Finished obtaining Information about user: ");

      out.println("<html>\n" +
                  "<head><title>Profile</title></head>\n" +
                  "<body>\n");
      out.println("<h2>User Information</h2>");
      out.println("<b>EmailAddress:</b> " + memberEmail + "<br>");
      out.println("<b>Name:</b> " + userName + "<br>");
      out.println("<b>Self Introduction:</b> " + userIntro + "<br>");
      out.println("<b>Location:</b> " + userLocation + "<br>");
      out.println("<b>Birthday:</b> " + userBirthday + "<br>");
      out.println("<b>Member Type:</b> ");
      if(isAdopter.equals("y")){
        out.println("Adopter");
      }
      else{
        out.println("Sender");
      }
      out.println("<br>");
      out.println("<b>Adopting Experience:</b> " + userAdoptExp + "<br>");

      if(isSender.equals("y")){
        //Show pets
        rset = stmt.executeQuery ("select Name, Birthday, Breed from Pet where EmailAddress ='" + memberEmail + "'");

        out.println("<hr><h2>Pets:</h2>" +
        " <table> \n" +
        "   <tr>\n" +
        "<th>Name</th>" +
        "<th>Age</th>" +
        "<th>Breed</th>" +
        "</tr>");

        //Print table with info about the pets
        while (rset.next ()){
          String petName = rset.getString(1);
          String petBirthday = rset.getString(2);
          String petBreed = rset.getString(3);
          int petAge = getAge(petBirthday);

          out.println (" <tr><td> " + petName + "</td><td>" + petAge + "</td><td>" + petBreed + "</td>");
          out.println ("</tr>");
        }
        out.println("   </table>");
      }

      rset = stmt.executeQuery("SELECT * FROM Favorite WHERE EmailAddressMember = '" + memberEmail + "'");
      out.println("<hr><h2>Favorite Pets</h2><b>Names:</b><ul>");

      if(rset.next()) {
         out.println("<li>" + rset.getString(3) + "</li>");
         while(rset.next()){
            out.println("<li>" + rset.getString(3) + "</li>");
         }
         out.println("</ul><br>");
      }




      out.println("<a href='index.html'><input type='button' value='Quit'></a></body></html>");
    } catch (Exception e) {
      System.out.println("Exception in MemberProfileServlet: " + e);
    }
  }

  private int getAge(String birthday){
    Calendar calendar = Calendar.getInstance();
    int birthYear = Integer.parseInt(birthday.substring(2,4));
    int birthMonth = Integer.parseInt(birthday.substring(5,7));
    int birthDay = Integer.parseInt(birthday.substring(8,10));
    if(birthYear < 30){
      birthYear += 2000;
    }
    else{
      birthYear += 1900;
    }
    int currentYear = calendar.get(Calendar.YEAR);
    int age = currentYear - birthYear;
    if(birthMonth > calendar.get(Calendar.MONTH)){
        age -= 1;
    }
    else if(birthMonth == calendar.get(Calendar.MONTH) && birthDay > calendar.get(Calendar.DAY_OF_MONTH)){
      age -= 1;
    }

    return age;
  }

  /**
   * Called when the servlet is being destroyed.  Here we can close
   * our Statement and Connection.
   */
  public void destroy() {
    // Disconnect from the database.
    try {
      stmt.close();
      conn.close();
    } catch (Exception e) {
      System.out.println("Exception in MemberProfileServlet: " + e);
    }

  }
}