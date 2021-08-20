//ShowAdopterServlet.java

import java.io.*;             // For PrintWriter
import java.sql.*;            // You need to import the java.sql package to use JDBC

import javax.servlet.*;       // For ServletException and other things
import javax.servlet.http.*;  // For HttpServlet and other HttpServlet classes

/**
 * This class is used to generate a response to a query given in the
   JDBCServletDemo servlet.  It will make a connection to the database,
   execute the query to find the customers that live in the given city,
   and will generate an HTML page with an HTML list for the result.
 */
public class ShowAdopterServlet extends HttpServlet {
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
      System.out.println("Exception in ShowAdopterServlet: " + e);
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
      ResultSet rset = stmt.executeQuery ("select EmailAddress, Name, SelfIntroduction, AdoptingExperience " +
                                          "  from Member " +
                                          "  where IsAdopter = 'y'");

      // Build the HTML page we want to send as a response to a query given to
      // our servlet.
      response.setContentType("text/html");
      PrintWriter out = response.getWriter();

      out.println("<html>\n" +
                  "<head><title>Adopters</title></head>\n" +
                  "<body>\n" +
                  "<h1>Adopters:</h1>" +
                  " <table> \n" +
                  "   <tr>\n" +
		"<th>Email</th>" +
		"<th>Name</th>" +
		"<th>Self-Introduction</th>" +
		"<th>Adoption experience</th>" +
	"</tr>");

      while (rset.next ()){
        out.println (" <tr><td> " + rset.getString(1) + "</td><td>" + rset.getString(2) + "</td><td>" + rset.getString(3) + "</td><td>" + rset.getString(4) + "</td></tr>");
    }
      out.println("   </table>" +
                  "<a href='index.html'><input type='button' value='Quit'></a></body></html>");
    } catch (Exception e) {
      System.out.println("Exception in ShowAdopterServlet: " + e);
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
      System.out.println("Exception in ShowAdopterServlet: " + e);
    }

  }
}