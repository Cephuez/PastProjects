//package UACATS.servlets;

import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
//import UACATS.servlets.*;
//import UACATS.utils.*;
import java.sql.*;
import java.util.ArrayList;

public class FindMerchandiseServlet extends HttpServlet
{

	String priceMin;
	String priceMax;
	String howOld;
	String title;
	String author;
	boolean checkTitle;
	boolean checkAuthor;

	ArrayList query_result = new ArrayList();
	String noResult = "There is no qualified book for your search. Please alter the search condition and try again.";
	boolean failed;

	public FindMerchandiseServlet()
	{
		super();
	}



	public void drawHeader(HttpServletRequest req, PrintWriter out)
	{
		out.println("<html>");
		out.println("<head><title>FindMerchandise</title></head>");

		out.println("<body>");
		out.println("<p>");
		out.println("<center>");
		out.println("<font size=5 face=\"Arial,Helvetica\">");
		out.println("<b>UACATS---Find Merchandise</b><br></font>");

		out.println("</center>");

		out.println("<hr>");
		out.println("<br><br>");
	}





	public void drawFooter(HttpServletRequest req, PrintWriter out)
	{

		out.println("<center>");

		out.println("<p>");
		out.println("<form name=\"Summary\" action=LoginServlet method=get>");
		out.println("<input type=submit name=\"MainMenu\" value=\"Main Menu\">");
		out.println("</form>");
		out.println("</p>");

		out.println("<p>");
		out.println("<form name=\"logout\" action=index.html>");
		out.println("<input type=submit name=\"logoutUACATS\" value=\"Logout\">");
		out.println("</form>");
		out.println("</p>");

		out.println("<br><br>");
		out.println("</center>");
		out.println("</p>");
		out.println("</body>");
		out.println("</html>");
	}




	public void drawSelectMenu(HttpServletRequest req, PrintWriter out)
	{

		HttpSession session = req.getSession();
		String category = (String)session.getAttribute("Category");
		String pricemin = (String)session.getAttribute("PriceMIN");
		String pricemax = (String)session.getAttribute("PriceMAX");
		String howold = (String)session.getAttribute("HowOld");
		String booktitle = (String)session.getAttribute("BookTitle");
		String checkbooktitle = (String)session.getAttribute("CheckBookTitle");
		String checkbookauthor = (String)session.getAttribute("CheckBookAuthor");
		String bookauthor = (String)session.getAttribute("BookAuthor");

		out.println("<h2 align=\"center\">Choose Category</h2>");


		out.println("<form name=\"chcagegory\" action=FindMerchandiseServlet method=get>");

		out.println("<p align=\"center\">");

		out.println("<select size=\"1\" name=\"Category\">");
  		out.println("<option value=\"null\">Choose category:\n</option>");
  		if(category.equals("book"))
  		{
  				out.println("<option selected=\"yes\" value=\"book\">book\n</option></select>");
		}
  		else
  				out.println("<option value=\"book\">book\n</option></select>");

		out.println("</p>");

		out.println("<h2 align=\"center\">Price Range</h2>");

		out.println("<p align=\"center\">");
    	out.println("<select size=\"1\" name=\"PriceMIN\"> ");
		out.println("<option value=\"null\">$0\n</option>");

		if(pricemin.equals("pricemin10"))
		{
				  out.println("<option selected=\"yes\" value=\"pricemin10\">$10\n</option></select> to");
		}
		else
		 		  out.println("<option value=\"pricemin10\">$10\n</option></select> to");

		out.println("<select size=\"1\" name=\"PriceMAX\" >");
		out.println("<option value=\"null\">No Limit\n</option>");

		if(pricemax.equals("pricemax1k"))
				  out.println("<option selected=\"yes\" value=\"pricemax1k\">$1000\n</option></select>");
		else
		  		  out.println("<option value=\"pricemax1k\">$1000\n</option></select>");

		out.println("</p>");

		out.println("<h2 align=\"center\">HowOld</h2>");

		out.println("<p align=\"center\">");
		out.println("<select size=\"1\" name=\"HowOld\">");
		out.println("<option value=\"null\">No limit</option>");

		if(howold.equals("6month"))
		   		  out.println("<option selected=\"yes\" value=\"6month\">less than 6 months</option></select><br>");
		else
				  out.println("<option value=\"6month\">less than 6 months</option></select><br>");

		out.println("</p>");

		out.println("<p align=\"center\">");

		if(checkbooktitle.equals("checked"))
		{
		     		out.println("<input type=\"checkbox\" checked=\"yes\" name=\"CheckBookTitle\" value=\"checked\">Book Title");
		     		out.println("<input type=text size=30 name=\"BookTitle\" value=\""+booktitle+"\">");
		}
		else
		{
					out.println("<input type=\"checkbox\" name=\"CheckBookTitle\" value=\"checked\">Book Title");
					out.println("<input type=text size=30 name=\"BookTitle\">");
		}
		out.println("</p>");

		out.println("<p align=\"center\">");

		if(checkbookauthor.equals("authorchecked"))
		{
		     		out.println("<input type=\"checkbox\" checked=\"yes\" name=\"CheckBookAuthor\" value=\"authorchecked\">Book Author");
		     		out.println("<input type=text size=30 name=\"BookAuthor\" value=\""+bookauthor+"\">");
	    }
		else
		{
					out.println("<input type=\"checkbox\" name=\"CheckBookAuthor\" value=\"authorchecked\">Book Author");
					out.println("<input type=text size=30 name=\"BookAuthor\" >");

	    }
		out.println("</p>");

		out.println("<p align=\"center\">");
		out.println("<input type=submit name=\"findmerchandise\" value=\"Find\" >");
		out.println("</p>");

		out.println("</form>");


	}

	public void drawMerchandiseList(HttpServletRequest req, PrintWriter out)
	{

		if(failed){
			out.println("<h2 align=\"center\">" + noResult + "</h2>");
			out.println("<br>");
		}else{

			out.println("<h2 align=\"center\">Merchandise Found in UACATS Listed below:</h2>");
			out.println("<br>");
			out.println("<hr>");

			for(int i=0; i < query_result.size(); i++){
				MerchandiseInfo info = (MerchandiseInfo)query_result.get(i);

				out.println("<p><b>Book Title:</b>  " + info.booktitle+"</p>");
				out.println("<p><b>Book Author:</b> " + info.author+"</p>");
				out.println("<p><b>How old:</b>  " + info.howold+"  months</p>");
				out.println("<p><b>Asking Price:</b>  $" + info.price+"</p>");
				out.println("<p><b>Description:</b>  " + info.description+"</p>");
				out.println("<br>");
				out.println("<p><b> Owner's Name:</b>  " + info.ownerfirstname + "  " + info.ownerlastname+"</p>");
				out.println("<p><b> Owner's Email:</b>  " +info.owneremail+"</p>");
				out.println("<p><b> Owner's Phone Number:</b>  " + info.ownerphone + "</p>");
				out.println("<hr>");
				out.println("<br><br>");
			}
		}

	}


	public void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException
	{
		res.setContentType("text/html");
		PrintWriter out = res.getWriter();



		if(req.getParameter("findmerchandise") != null)
		{
			System.out.println("BOO BOO HOO HOO...I WANT MOMMY");

			HttpSession session = req.getSession();
			session.setAttribute("Category", req.getParameter("Category"));
			session.setAttribute("PriceMIN", req.getParameter("PriceMIN"));
			session.setAttribute("PriceMAX", req.getParameter("PriceMAX"));
			session.setAttribute("HowOld", req.getParameter("HowOld"));
			session.setAttribute("BookTitle", req.getParameter("BookTitle"));
			session.setAttribute("BookAuthor", req.getParameter("BookAuthor"));

			if(req.getParameter("CheckBookTitle")!=null)
			{
					session.setAttribute("CheckBookTitle",req.getParameter("CheckBookTitle"));
			 }
			 else
			 {
					String noCheck="null";
					session.setAttribute("CheckBookTitle",noCheck);
			 }

			 if(req.getParameter("CheckBookAuthor")!=null)
			 {
					session.setAttribute("CheckBookAuthor",req.getParameter("CheckBookAuthor"));
			  }
			  else
			  {
					String auCheck="null";
					session.setAttribute("CheckBookAuthor",auCheck);
			  }

	    }
	    else
	    {
			System.out.println("Horrible Horrible code....puta.....chabron...");
			HttpSession session = req.getSession();
			String clearinput="";
			session.setAttribute("Category", clearinput);
			session.setAttribute("PriceMIN", clearinput);
			session.setAttribute("PriceMAX",clearinput);
			session.setAttribute("HowOld", clearinput);
			session.setAttribute("BookTitle", clearinput);
			session.setAttribute("BookAuthor", clearinput);
			session.setAttribute("CheckBookTitle",clearinput);
			session.setAttribute("CheckBookAuthor",clearinput);
		}

		drawHeader(req,out);

		drawSelectMenu(req,out);

		if(req.getParameter("findmerchandise") != null){
			/***************************************************************************************************/
			priceMin = req.getParameter("PriceMIN");
			priceMax = req.getParameter("PriceMAX");
			howOld = req.getParameter("HowOld");
			title = req.getParameter("BookTitle");
			author = req.getParameter("BookAuthor");
			if(req.getParameter("CheckBookTitle")!=null)
			{
				checkTitle = true;
			}else{
				checkTitle = false;
			}

			if(req.getParameter("CheckBookAuthor")!=null)
			{
				checkAuthor = true;
			}else{
				checkAuthor = false;
			}

			String query = "SELECT * from MERCHANDISE, BOOK , INDIVIDUAL , CatUser , ADVERTISES WHERE " +
							"CatUser.UserID = INDIVIDUAL.UserID AND CatUser.UserID = MERCHANDISE.UserID "+
							"AND MERCHANDISE.UserID = BOOK.UserID AND MERCHANDISE.MID = BOOK.MID AND INDIVIDUAL.UserID = BOOK.UserID " +
							"AND ADVERTISES.UserID = MERCHANDISE.UserID and ADVERTISES.MID = MERCHANDISE.MID ";

			if(priceMin.equals("null")){
				query += "AND AskingPrice >= 0";
			}else if(priceMin.equals("pricemin10")){
				query += "AND AskingPrice >= 10 ";
			}

			if(priceMax.equals("null")){

			}else if(priceMax.equals("pricemax1k")){
				query += " AND AskingPrice <= 1000 ";
			}

			if(howOld.equals("6month")){
				query += " AND HowOldMonth <= 6 ";
			}

			if(checkTitle){
				query += " AND BookTitle = '" + title + "' ";
			}

			if(checkAuthor){
				query += " AND BookAuthor = '" + author + "' ";
			}

			Connection conn=null;
			try{
				System.out.println("Rignt before ze query");
				Class.forName ("oracle.jdbc.OracleDriver");// register drivers
				System.out.println("Attempting to connect 1111");
				conn = DriverManager.getConnection(OracleConnect.connect_string,OracleConnect.user_name,OracleConnect.password);

				Statement s = conn.createStatement();
				System.out.println(query);
				ResultSet rs = s.executeQuery(query);
				System.out.println("Executed the query");
				int count =0;
				failed = false;
				query_result.clear();
				while(rs.next()){
					System.out.println("In ze query results");
					count++;


					MerchandiseInfo item = new MerchandiseInfo();
					item.booktitle = rs.getString("BookTitle");
					item.author = rs.getString("BookAuthor");
					item.howold = rs.getString("HowOldMonth");
					item.price = rs.getString("AskingPrice");
					item.description = rs.getString("Description");

					item.ownerfirstname = rs.getString("FirstName");
					item.ownerlastname = rs.getString("LastName");
					item.owneremail = rs.getString("Email");
					item.ownerphone = rs.getString("PhoneNum");

					query_result.add(item);
				}

				if(count == 0){
					failed = true;
				}
			}catch(Exception e){
				System.out.println("BlAH....BLOODY EXCEPTION");
				e.printStackTrace();
			}
			drawMerchandiseList(req,out);
		}

		drawFooter(req,out);


	}

	class MerchandiseInfo{
		public String booktitle;
		public String author;
		public String howold;
		public String price;
		public String description;

		public String ownerfirstname;
		public String ownerlastname;
		public String owneremail;
		public String ownerphone;
	}

}
