//ShowPetsServlet.java

import java.io.*;             // For PrintWriter
import java.sql.*;            // You need to import the java.sql package to use JDBC

import javax.servlet.*;       // For ServletException and other things
import javax.servlet.http.*;  // For HttpServlet and other HttpServlet classes

/**
 * This class is used to generate a response to a query given in the
  servlet.  It will make a connection to the database,
   execute the query to find the pets,
   and will generate an HTML page with an table for the result.
 */
public class ShowPetsServlet extends HttpServlet {
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
      System.out.println("Exception in ShowPetsServlet: " + e);
    }
  }

  /**
   * Processes the HTTP Get request that is sent to this servlet.
   * This is where we want to put most of our code.  Within this
   * method we will create the query we want to execute and send it to
   * the Statement object created in init().  What we get back is a
   * ResultSet, which is essentially a java.sql object that represents
   * the table (relation) that results from the query.  We iterate
   * through this ResultSet and print out the names of the customers
   * in the given city.
   */
  public void doGet(HttpServletRequest request, HttpServletResponse response)
                                          throws ServletException, IOException {

    // Make the query to the database and get the results.
    try {
      String memberEmail = request.getParameter("memberEmail");
      ResultSet rset = stmt.executeQuery ("select EmailAddress, Name, Birthday, IsSterilized, Breed, DaysWalk, BiteWire from Pet ");

      // Build the HTML page we want to send as a response to a query given to
      // our servlet.
      response.setContentType("text/html");
      PrintWriter out = response.getWriter();

      out.println("<html>\n" +
                  "<head><title>Adopters</title></head>\n" +
                  "<body>\n" +
                  "<h1>Pets:</h1>" +
                  " <table> \n" +
                  "   <tr>\n" +
              		"<th>Email</th>" +
              		"<th>Name</th>" +
              		"<th>Birthday</th>" +
              		"<th>IsSterilized</th>" +
                  "<th>Breed</th>" +
                  "<th>DaysWalk</th>" +
                  "<th>BitesWires</th>" +
              	  "<th>Add Favorite</th></tr>");

      //Print table with info about the pets
      while (rset.next ()){
        String petEmail = rset.getString(1);
        String petName = rset.getString(2);
        String petBirthday = rset.getString(3);
        String petIsSterilized = rset.getString(4);
        String petBreed = rset.getString(5);
        String petDaysWalk = rset.getString(6);
        String petBitesWires = rset.getString(7);
        out.println (" <tr><td> " + petEmail + "</td><td>" + petName + "</td><td>" + petBirthday + "</td><td>");
        //Check if pet is sterlized
        if(petIsSterilized.equals("y")){
            out.println("Yes");
        }
        else{
          out.println("No");
        }
         out.println("</td><td>" + petBreed + "</td>");
        
        if(petBreed.equals("Dog")){
            out.println ("<td>" + petDaysWalk + "</td><td>N/A</td>");
        }
        else if(petBreed.equals("Rabbit")){
            out.println ("<td>N/A</td><td>" + petBitesWires + "</td>");
        }
        else{
            out.println ("<td>N/A</td><td>N/A</td>");
        }
        out.println ("<td><form action='AddFavoriteServlet' method='get'>" +
         "<input name='memberEmail' type='hidden' value='" + memberEmail + "'>" + 
         "<input name='petEmail' type='hidden' value='" + petEmail + "'>" +
         "<input name='petName' type='hidden' value='" + petName + "'>" +
         "<input name='petBirthday' type='hidden' value='" + petBirthday + "'>" +
         "<input type='submit' value='Favorite'></form></td>");
        out.println ("</tr>");
    }
      out.println("   </table>" +
                  "<a href='index.html'><input type='button' value='Quit'></a></body></html>");
    } catch (Exception e) {
      System.out.println("Exception in ShowPetsServlet: " + e);
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
      System.out.println("Exception in ShowPetsServlet: " + e);
    }

  }
}