package edu.upenn.cis.cis550.phase3;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;
import javax.xml.stream.events.XMLEvent;

public class LoadTAXML_toYourTable {
	BufferedReader xmlInput;
	XMLInputFactory factory = XMLInputFactory.newInstance();
	
	enum Level {NONE, ROOT, TABLE, TUPLE, ATTRIB};
	Level currentLevel = Level.NONE;
	
	PrintWriter currentTable;
	StringBuffer currentTuple;
	String currentAttribute;
	String currentValue;
	int column;
	
	public LoadTAXML_toYourTable() throws ClassNotFoundException, SQLException, IOException {
		xmlInput = new BufferedReader(new FileReader("import.xml"));
	}
	
	public void close() {
		try {
			xmlInput.close();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}
	
	/**
	 * Simple STAX event handler that maintains our context level in the XML file,
	 *  and writes comma-delimited output.  There's enough state information that
	 *  one could alternatively write the attribute names.
	 *  
	 * @param reader
	 * @param eventType
	 * @return
	 * @throws IOException
	 */
	boolean handleEvent(XMLStreamReader reader, int eventType) throws IOException {
		switch (eventType) {
		case XMLEvent.START_ELEMENT:
			currentLevel = Level.values()[currentLevel.ordinal() + 1];
			if (currentLevel == Level.TABLE) {
				currentTable = new PrintWriter(new BufferedWriter(
						new FileWriter(reader.getLocalName() + ".csv")));
				System.out.println("Reading table " + reader.getLocalName());
			} else if (currentLevel == Level.TUPLE) {
				column = 0;
				currentTuple = new StringBuffer();
			} else if (currentLevel == Level.ATTRIB)
				currentAttribute = reader.getLocalName();
			break;
		case XMLEvent.END_ELEMENT:
			currentLevel = Level.values()[currentLevel.ordinal() - 1];
			if (currentLevel == Level.TABLE) {
				currentTable.println(currentTuple);
				return true;
			} else if (currentLevel == Level.ROOT) {
				currentTable.close();
				System.out.println("Read and exported table " + currentTable);
				return true;
			} else if (currentLevel == Level.TUPLE) {
				currentTuple.append(((column++ == 0) ? "" : ",") + currentValue);
			}

			break;
		case XMLEvent.CHARACTERS:
			currentValue = reader.getText();
			break;
		default:
			break;
		}
		return false;
	}
	
	public void parseAndLoad() throws XMLStreamException, IOException {
        XMLStreamReader xmlr = factory.createXMLStreamReader(xmlInput);

        // when XMLStreamReader is created, 
        // it is positioned at START_DOCUMENT event.
        int eventType = xmlr.getEventType();
        handleEvent(xmlr, eventType);

        // check if there are more events 
        // in the input stream
        while(xmlr.hasNext()) {
            eventType = xmlr.next();
            handleEvent(xmlr, eventType);
        }

	}

	/**
	 * @param args
	 * @throws IOException 
	 * @throws SQLException 
	 * @throws ClassNotFoundException 
	 * @throws XMLStreamException 
	 */
	public static void main(String[] args) throws ClassNotFoundException, SQLException, IOException, XMLStreamException {
		LoadTAXML_toYourTable load = new LoadTAXML_toYourTable();
		
		load.parseAndLoad();
		
		load.close();
	}

}
