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
        public LoginServlet()
        {
                super();
        }

       public void drawHeader(HttpServletRequest req, PrintWriter out)
        {
			out.println("<html>");
			out.println("<head>");
						out.println("<title>UACats logged in</title>");
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

				out.println("<b>You have logged in UACATS</b></br>");
				out.println("<font size=4>");
				out.println("<b>University of Arizona Classified Ads Tracking System</b><br></font>");
				out.println("</font>");

                out.println("<hr");
                out.println("<br><br>");


                out.println("<form name=\"findall\" action=../../../examples/jsp/MerchandiseReportSummary.jsp>");
                	out.println("<input type=submit name=\"findallsubmit\" value=\"Show All Merchandise\">");
 				out.println("</form>");

                out.println("<br>");


                out.println("<form name=\"advancedfind\" action=FindMerchandiseServlet method=get>");
                	out.println("<input type=submit name=\"Adsearch\" value=\"Advanced Search\">");
 				out.println("</form>");

                out.println("<br>");

                out.println("<form name=\"addMerchandise\" action=AddMerchandiseServlet method=get>");
					out.println("<input type=submit name=\"Adsearch\" value=\"Add Merchandise\">");
				out.println("</form>");

                out.println("<br>");

                out.println("<form name=\"logout\" action=index.html>");
                	out.println("<input type=submit name=\"logoutUACATS\" value=\"Logout\">");
 				out.println("</form>");

        }




 		private void drawFailOptions(HttpServletRequest req, PrintWriter out)
        {
				out.println("<center>");
				out.println("<font size=5 face=\"Arial,Helvetica\">");

				out.println("<b>Sorry, only registered users can log into UACATS</b></br>");
				out.println("<font size=4>");
				out.println("<b>University of Arizona Classified Ads Tracking System</b><br></font>");
				out.println("</font>");

				out.println("</center>");

                out.println("<hr");
                out.println("<br><br>");


                out.println("<form name=\"logout\" action=index.html>");
				out.println("<center>");
				out.println("<input type=submit name=\"home\" value=\"Return to home\">");
				out.println("</center>");
 				out.println("</form>");

                out.println("<br>");
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
				int id=0;
				String[] paramValues = request.getParameterValues("loginID");
				try{
					id = Integer.parseInt(paramValues[0]);
				}catch(NumberFormatException nfe){
				}

				//Get the password....
				int pw=0;
				paramValues = request.getParameterValues("loginPW");
				try{
					pw = Integer.parseInt(paramValues[0]);
				}catch(NumberFormatException nfe){
				}

				//Add this stuff to the session...
				HttpSession session = request.getSession();
				session.setAttribute("loginID" , ""+id);
				session.setAttribute("loginPW" , ""+pw);

				//Now query the database to see if this user exists......
				try{
					Statement s = conn.createStatement();
					System.out.println("Select UserID from CatUser where UserID =" + id + " and Password = "+pw);
					ResultSet rs = s.executeQuery("Select UserID from CatUser where UserID =" + id + " and Password = "+pw);
					int count = 0;
					while(rs.next())count++;

					if(count == 0){
						System.out.println("CatUser does not exist");
						return false;
					}
				}catch(SQLException sqle){
					sqle.printStackTrace();
					return false;
				}

				return true;
			}
			else{
				//If the parameter is empty the session must have the info..
				HttpSession session = request.getSession();

				String id = (String)session.getAttribute("loginID");
				String pw = (String)session.getAttribute("loginPW");

				if(id != null && pw != null){
					try{
						//Now query the database to see if this user exists......
						try{
							Statement s = conn.createStatement();
							System.out.println("Select UserID from CatUser where UserID =" + Integer.parseInt(id) + " and Password = "+Integer.parseInt(pw));
							ResultSet rs = s.executeQuery("Select UserID from CatUser where UserID =" + Integer.parseInt(id) + " and Password = "+Integer.parseInt(pw));
							int count = 0;
							while(rs.next())count++;

							if(count == 0){
								System.out.println("CatUser does not exist");
								return false;
							}
							else{
								return true;
							}
						}catch(SQLException sqle){
							sqle.printStackTrace();
							return false;
						}
					}
					catch(Exception e){
						e.printStackTrace();
						return false;
					}
				}
				else{
					return false;
				}
			}
		}
}


