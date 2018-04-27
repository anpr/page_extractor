package algorithmia.web.AnalyzeURL;
import com.algorithmia.*;
import com.algorithmia.algo.*;
import com.algorithmia.data.*;
import com.google.gson.*;
import java.util.*;
import java.io.*;
import java.net.SocketTimeoutException;
import java.nio.charset.Charset;

import org.jsoup.*;
import org.jsoup.Connection.Response;
import org.jsoup.nodes.*;
import org.jsoup.parser.*;
import org.jsoup.select.*;

public class AnalyzeURL {

    private final int MAX_SIZE = 1024 * 1024 * 8;

    public Map<String,Object> apply(String url) throws IOException, AlgorithmException {
        return apply(url, "");
    }

    public Map<String,Object> apply(String url,String searchTerm) throws IOException, AlgorithmException {
        // Clean up URL
        if( url == null || url.trim().equals("") ) {
            throw new AlgorithmException("Html2Text: input url cannot be empty");
        }
        try {
            // Filter out PDFs etc
            if( url.matches(".*\\.pdf$") || url.matches(".*\\.doc$") || url.matches(".*\\.docx$") || url.matches(".*\\.pptx$") ) {
                throw new AlgorithmException("url must be an html document, not a .doc, .docx, .pdf, or .pptx");//Algorithmia.call("/util/ExtractText", url, String.class);
            }
            // Add missing protocol if necessary
            if( ! url.matches("\\w+://.+") ) {
                url = "http://" + url;
            }

            String content = null;

            Charset cset = Charset.forName("UTF-8");
            // Fetch content
            Connection con = Jsoup.connect(url)
                    .userAgent("Mozilla")
                    .referrer("http://www.google.com")
                    .ignoreContentType(true)
                    //.ignoreHttpErrors(true)
                    .followRedirects(true)
                    //.charset(cset)
                    .timeout(10 * 1000) // milliseconds
                    .parser(Parser.xmlParser());

            //System.out.println("url: " + url);
            Response response = con.execute();



            // TODO: Check status code
            int statusCode = response.statusCode();

            //System.out.println("statusCode: " + statusCode);

            Document doc = con.get();

            doc.outputSettings().charset("UTF-8");

            Element head = doc.head();
            String title = url;
            try {
                title = head.select("title").text();
                // TODO: This is a hack
                if(title.endsWith(" - GeekWire")) {
                    title = title.replaceAll(" - GeekWire", "");
                }
            } catch(Exception e) {}

            String metaDesc = null;
            try {
                Elements metalinks = doc.select("meta[name=description]");
                metaDesc = metalinks.attr("content");
            } catch(Exception e) {}

            //get main thumbnail (primarily for GeekWire)
            //<meta property="og:image" content="http://cdn.geekwire.com/wp-content/uploads/2015/06/DSC06217.jpg" />
            String thumbnailURL = null;
            try {
                Elements metalinks = doc.select("meta[property=og:image]");
                thumbnailURL = metalinks.attr("content");
            } catch(Exception e) {}

            String date = getDate(doc);

            boolean hasString = doc.toString().contains(searchTerm);
            Element body = doc.body();
            if(body == null) {
                content = doc.text();
            } else {
                // Remove script tags in the body
                for(Element e : body.select("script")) {
                    e.remove();
                }
                // Remove style tags in the body
                for(Element e : body.select("style")) {
                    e.remove();
                }
                // Remove pre tags in the body
                for(Element e : body.select("pre")) {
                    e.remove();
                }
                // Remove code tags in the body
                for(Element e : body.select("code")) {
                    e.remove();
                }
                // Remove code aside in the body
                for(Element e : body.select("aside")) {
                    e.remove();
                }
                for(;;) {
                    Elements paragraphs = body.select("p");
                    if(paragraphs.size()>0) {
                        paragraphs.get(0).html(paragraphs.get(0).text());
                        paragraphs.get(0).tagName("algo-p");
                    } else {
                        break;
                    }
                }
                Elements algoParagraphs = body.select("algo-p");
                if(0.1 * body.text().length() < algoParagraphs.text().length()) {
                    content = algoParagraphs.text();
                } else {
                    content = body.text();
                }
                //content = doc.toString();
            }
            if (content.length() > MAX_SIZE) {
                content = content.substring(0, MAX_SIZE);
            }

            Map<String,Object> out = new HashMap<>();
            out.put("text", content.replace("?", " "));

            if (metaDesc == null) {
                String summary = Algorithmia.algo("algo://nlp/Summarizer").pipe(content).toString();
                out.put("summary",summary);
            } else {
                out.put("summary",metaDesc);
            }
            if (date != null) {
                out.put("date", date);
            }
            out.put("marker", hasString);
            out.put("title", title);
            if(thumbnailURL != null) {
                out.put("thumbnail", thumbnailURL);
            }
            out.put("url", url);
            out.put("statusCode", statusCode);

            return out;
        } catch (SocketTimeoutException e){
            throw new AlgorithmException("The website timed out!", e);
        } catch(IOException e) {
            throw new AlgorithmException("The requested URL did not return HTTP status code 200.");
        }
    }

    public String getDate(Document doc) {
        Element head = doc.head();
        String date = null;
        try {
            Elements test = head.select("meta[itemprop=datePublished]");
            date = test.attr("content");
            //println("date after first attempt: " + date);
        } catch(Exception e) {

        }

        if (date == null || date.equals("")) {
            try {
                Elements metalinks = doc.select("meta[property=article:published_time]");
                date = metalinks.attr("content");
                //println("date on second attempt: " + date);
            } catch(Exception e) {

            }
        }

        if (date == null || date.equals("")) {
            try {
                //Elements metalinks = doc.select("meta[property=og:pubdate]");
                Elements metalinks = doc.select("meta[name=pubdate]");
                date = metalinks.attr("content");
                //println("date on third attempt: " + date);
            } catch(Exception e) {

            }
        }

        if (date == null || date.equals("")) {
            try {
                //Elements metalinks = doc.select("meta[property=og:pubdate]");
                Elements metalinks = doc.select("meta[name=timestamp]");
                date = metalinks.attr("content");
                //println("date on fourth attempt: " + date);
            } catch(Exception e) {

            }
        }

        if (date == null || date.equals("")) {
            try {
                //Elements metalinks = doc.select("meta[property=og:pubdate]");
                Elements metalinks = doc.select("time[class=timestamp_article]");
                date = metalinks.attr("datetime");
                //println("date on fifth attempt: " + date);
            } catch(Exception e) {

            }
        }

        return date;
    }

}
