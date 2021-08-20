// SimpleServlet.java


import javax.servlet.*;       // For ServletException and other things
import javax.servlet.http.*;  // For HttpServlet and other HttpServlet classes
import java.io.*;             // For PrintWriter

public class SimpleServlet extends HttpServlet{

   public void doGet (HttpServletRequest request,
			HttpServletResponse response) throws
			ServletException, IOException{
	 PrintWriter out;
	 String title = "Simple Servlet Output";
     response.setContentType("text/html");
     out = response.getWriter();
     out.println("<HTML><HEAD>");
     out.println("<TITLE>" + title + "</TITLE></HEAD>");
     out.println("<BODY><P>This is output from SimpleServlet.");
     out.println("</BODY></HTML>");
     out.close();
     }
} // end of servlet
