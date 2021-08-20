<%@ page language="java" contentType="text/html" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.io.*" %>


<HTML>
<BODY>
<head>
<title>Customer list</title>
</head>
<body bgcolor=\"#FDF5E6\">
<p>
The customers that live in

<% out.println(" " + request.getParameter("givenCity") + " are: ");%>
<ul>
   	    	    
<%
    // CustomerList.jsp
    try {
      	// Load the Oracle JDBC driver
	Class.forName("oracle.jdbc.OracleDriver");  // load drivers

      	// Connect to the database
      	// You should put your name and password for the 2nd and 3rd parameter.
      	Connection conn = DriverManager.getConnection (
		"jdbc:oracle:thin:@aloe.cs.arizona.edu:1521:oracle",
       		"yourusername",
       		"yourpassword"
                           	);
		String cityGiven = request.getParameter("givenCity");


      	// Create a Statement
      	Statement stmt = conn.createStatement();

      	ResultSet rset = stmt.executeQuery ("select distinct name " +
                                          "  from customer " +
                                          "  where city = '" + cityGiven +"'");

      	while (rset.next ()){
      	  	// Here use a different method of ResultSet.  getString gets
      	  	// the String value of the element that is in the current
      	  	// row of the result set and the given column.
		//  Note: the first column is column 1.
      		out.println (" <li> " + rset.getString (1) + "</li>");
      	}
	    stmt.close();
        conn.close();

    } catch (Exception e) {
      System.out.println("Exception in CustomerListServlet: " + e);
    }

%>

</ul>
</p>
</body>
</html>
