package edu.upenn.cis.cis550.phase3;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

/**
 * Dumps an Oracle database schema to an XML file
 * 
 * @author val
 *
 */
public class DumpYourTable_ToTAXML {
	Connection conn;
	Statement stat;
	PrintWriter xmlOutput;
	
	static final String hostName = "tripster.ctaslvxazj3v.us-east-1.rds.amazonaws.com";
	static final String user = "root";
	static final String password = "raymondozu";
	static final String database = "ORCL";


	public DumpYourTable_ToTAXML() throws ClassNotFoundException, SQLException, IOException {
		Class.forName("oracle.jdbc.OracleDriver");
		conn = DriverManager.getConnection("jdbc:oracle:thin:@//" + hostName
				+ "/" + database, user, password);
		
		stat = conn.createStatement();
		
		xmlOutput = new PrintWriter(new BufferedWriter(new FileWriter("export.xml")));
		
		xmlOutput.println("<database>");
	}
	
	public void close() {
		try {
			stat.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		xmlOutput.println("</database>");
		xmlOutput.close();
		try {
			conn.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * In Oracle, get the list of tables
	 * 
	 * @return
	 * @throws SQLException 
	 */
	public List<String> getTables() throws SQLException {
		ResultSet rs = stat.executeQuery("SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER='" + 
				user.toUpperCase() + "'");
		
		List<String> ret = new ArrayList<String>();
		while (rs.next()) {
			ret.add(rs.getString(1));
		}
		return ret;
	}
	
	public void writeContents(final String tableName) throws SQLException {
		System.out.println("Dumping contents of " + tableName + "...");
		ResultSet rs = stat.executeQuery("SELECT * FROM " + tableName);
		
		xmlOutput.println("<" + tableName + ">");
		StringBuffer line;
		while (rs.next()) {
			line = new StringBuffer("<tuple>");
			for (int i = 0; i < rs.getMetaData().getColumnCount(); i++) {
				String col = rs.getMetaData().getColumnName(i + 1);
				
				// If we want to dump the types too...
//				line.append("<" + col + " type=\"" + 
//						rs.getMetaData().getColumnTypeName(i+1) + "\">");
				
				line.append("<" + col + ">");
				
				String val = rs.getString(i+1);
				line.append(val.trim());
				
				line.append("</" + col + ">");
			}
			line.append("</tuple>");
			xmlOutput.println(line.toString());
		}
		xmlOutput.println("</" + tableName + ">");
	}

	/**
	 * @param args
	 * @throws SQLException 
	 * @throws ClassNotFoundException 
	 * @throws IOException 
	 */
	public static void main(String[] args) throws ClassNotFoundException, SQLException, IOException {
		DumpYourTable_ToTAXML dump = new DumpYourTable_ToTAXML();
		
		List<String> tablesInSchema = dump.getTables();
		
		for (String table: tablesInSchema) {
			dump.writeContents(table);
		}
		dump.close();
	}

}
