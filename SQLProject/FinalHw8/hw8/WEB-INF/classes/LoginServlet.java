//package UACATS.servlets;
import java.util.*;

import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
//import UACATS.servlets.*;
//import UACATS.utils.*;
import java.sql.*;

public class LoginServlet extends HttpServlet
{
	private boolean wrongEmail;
	private boolean correctEmail;
        public LoginServlet()
        {
                super();
        }

       public void drawHeader(HttpServletRequest req, PrintWriter out)
        {
			out.println("<html>");
			out.println("<head>");
						out.println("<title>Main Page</title>");
			out.println("</head>");

			out.println("<body>");
			out.println("<p>");
			out.println("<center>");

        }


        public void drawFooter(HttpServletRequest req, PrintWriter out)
        {
			out.println("</center>");
			out.println("</p>");
			out.println("</body>");
			out.println("</html>");
        }


        private void drawUACATSOptions(HttpServletRequest req, PrintWriter out)
        {
				out.println("<font size=5 face=\"Arial,Helvetica\">");

				out.println("<b>You have logged in PetAdopt</b></br>");
				out.println("</font>");

                out.println("<hr>");
                out.println("<br><br>");

                out.println("<form action='ShowAdopterServlet' method='get'>");
				out.println("<input type='submit' name='showAdopters' value='Show Adopters'></form>");
                
                out.println("<br>");

                HttpSession session = req.getSession();
				String id = String.valueOf(session.getAttribute("loginID"));

                out.println("<form action='ShowPetsServlet' method='get'><input type='hidden' name='memberEmail' value=");
                out.println("'" + id + "'>");
				out.println("<input type='submit' name='showPets' value='Show Pets'></form>");
                
                out.println("<br>");

                out.println("<form action='MemberProfileServlet' method='get'><input type='hidden' name='memberEmail' value=");
                out.println("'" + id + "'>");
				out.println("<input type='submit' name='showProfile' value='Show Profile'></form>");

                out.println("<br>");

                out.println("<form name=\"logout\" action=index.html>");
                	out.println("<input type=submit name=\"logoutUACATS\" value=\"Logout\">");
 				out.println("</form>");

        }




 		private void drawFailOptions(HttpServletRequest req, PrintWriter out)
        {
				out.println("<body>");
				out.println("<p>");

				out.println("<center>");
				out.println("<font size=5 face=\"Arial,Helvetica\" >");
				out.println("<b>Welcome to PetAdopt</b></br>");
				out.println("<hr>");

				out.println("</center>");

                out.println("<br><br>");
                out.println("<table>");


                out.println("<tr>");
				out.println("<td>");
				if(wrongEmail) {
					out.println("<form name=\"Email\" action=LoginServlet method=get>");
					out.println("<b>Email(Wrong Email)</b>");
				}else {
					out.println("<form name=\"Email\" action=LoginServlet method=get>");
					out.println("<b>Email</b>");
				}
 				out.println("<input type=text name=\"loginID\"><br><br>");
                out.println("<input type=submit name=\"login\" value=\"login\">&nbsp;&nbsp;");
                
                out.println("</form>");
                out.println("<form name=\"register\" action=AddIndividualServlet method=get>");
                out.println("<input type=submit name=\"register\" value=\"register\"><br>");
                out.println("</form>");
                out.println("</font>");
                out.println("</form> </td>");
                out.println("</tr>");
                out.println("</table>");
                out.println("</font></center></p></body>");
	    }


		public void drawLoginSuccess(HttpServletRequest req, PrintWriter out)
		{
				drawHeader(req,out);
				drawUACATSOptions(req,out);
			    drawFooter(req,out);
		}



		public void drawLoginFail(HttpServletRequest req, PrintWriter out)
		{
				drawHeader(req,out);
				drawFailOptions(req,out);
				drawFooter(req,out);
		}


        public void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException
        {

			Connection conn=null;
			try{
				Class.forName("oracle.jdbc.OracleDriver");  // load drivers
				System.out.println("Attempting to connect 000");
				conn = DriverManager.getConnection(OracleConnect.connect_string,OracleConnect.user_name,OracleConnect.password);
			}
			catch(Exception e){
				e.printStackTrace();
			}

			res.setContentType("text/html");
			PrintWriter out = res.getWriter();

			//if login success, call the following function
			if(loginSuccess(conn , req))
				drawLoginSuccess(req,out);
			//if fail, call the following function
			else
				drawLoginFail(req,out);

			try{
				conn.close();
			}
			catch(Exception e){
				e.printStackTrace();
			}
        }


        //Checks to see if the user exists.
        private boolean loginSuccess(Connection conn , HttpServletRequest request){

			if(request.getParameter("loginID") != null){
				//Get the id
				String id = request.getParameter("loginID");

				//Add this stuff to the session...
				HttpSession session = request.getSession();
				session.setAttribute("loginID" , id);

				//Now query the database to see if this user exists......
				
				try{
					Statement s = conn.createStatement();
					ResultSet rs = s.executeQuery("SELECT emailAddress "
							+ "FROM Member "
							+ "WHERE emailAddress = '" + request.getParameter("loginID") + "' ");
					int count = 0;
					if(rs.next()) {
						wrongEmail = true;
						return true;
					}
					
					wrongEmail = true;
					return false;
				}catch(SQLException sqle){
					sqle.printStackTrace();
					return false;
				}
				
			}
			
			else{
				
			}
			return false;
		}
}


