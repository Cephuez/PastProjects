//AddFavoriteServlet.java

import java.io.*;             // For PrintWriter
import java.sql.*;            // You need to import the java.sql package to use JDBC
import java.util.Calendar;    //Needed for adding a date

import javax.servlet.*;       // For ServletException and other things
import javax.servlet.http.*;  // For HttpServlet and other HttpServlet classes

/**
 * This class is used add a favorite pet for a member.  It will make a connection to the database,
   execute the statment to insert a new row into the favorite table,
   and will generate an HTML page with an table for the result.
 */
public class AddFavoriteServlet extends HttpServlet {
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
      System.out.println("Exception in AddFavoriteServlet: " + e);
    }
  }

  /**
   * Processes the HTTP Get request that is sent to this servlet.
   * This is where we want to put most of our code.  Within this
   * method we will create the query we want to execute and send it to
   * the Statement object created in init().  What we get back is a
   * ResultSet, which is essentially a java.sql object that represents
   * the table (relation) that results from the query.
   */
  public void doGet(HttpServletRequest request, HttpServletResponse response)
                                          throws ServletException, IOException {


    //Get paremeters from form
    String memberEmail = request.getParameter("memberEmail");
    String petEmail = request.getParameter("petEmail");
    String petName = request.getParameter("petName");
    String petBirthday = request.getParameter("petBirthday");
    
    try {

      response.setContentType("text/html");
      PrintWriter out = response.getWriter();

      out.println("<html>\n" +
                  "<head><title>Adding Favorite</title></head>\n" +
                  "<body>\n");

      // Make the query to the database and get the results.
      ResultSet rset = stmt.executeQuery("SELECT * FROM Favorite WHERE EmailAddressMember = '" + memberEmail 
        + "' AND EmailAddressPet = '" + petEmail
        + "' AND PetName = '" + petName
        + "' AND Birthday = TO_DATE('" + petBirthday.substring(5,7) + petBirthday.substring(8,10) + petBirthday.substring(2,4) + "', 'MMDDYY')" );

      if(rset.next()) {
        //Member is already favorting this pet
         out.println("You already have this pet as a favorite <br><br>");
      }
      else {

        //Check to make sure the loged in member does not already have five favorite pets
        int favoriteCount = 0;
        rset = stmt.executeQuery("SELECT * FROM Favorite WHERE EmailAddressMember = '" + memberEmail + "'");
        while(rset.next()){
          favoriteCount += 1;
        }
        if(favoriteCount >= 5){
          out.println("You have too many favorite pets! <br><br>");
        }
        else{
          
          stmt.executeUpdate ("INSERT INTO Favorite(EmailAddressMember, EmailAddressPet, PetName, Birthday) " +
          "VALUES ('" + memberEmail + "', '" + petEmail +"', '" + petName + "', TO_DATE('" + petBirthday.substring(5,7) + petBirthday.substring(8,10) + petBirthday.substring(2,4) + "', 'MMDDYY'))");

        out.println("You added have this pet as a favorite <br><br>");
        }
      }


      out.println("  <form action='ShowPetsServlet' method='get'>" +
                  "<input type='hidden' name='memberEmail' value='" + memberEmail + "'>" +
                  "<input type='submit' name='showPets' value='Back'></form><br><br> " +
                  "<a href='index.html'><input type='button' value='Quit'></a></body></html>");
    } catch (Exception e) {
      System.out.println("Exception in AddFavoriteServlet: " + e);
    }
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
      System.out.println("Exception in AddFavoriteServlet: " + e);
    }

  }
}