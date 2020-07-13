package com.example.grocerygo;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class InteractWithServer {

    private static final int SERVERPORT = 65432;
    private static final String SERVER_IP = "10.0.2.2";
    public InteractWithServer(){

    }
    public String read_from_socket(Socket socket){
        try {
            DataInputStream din = new DataInputStream(socket.getInputStream());
            boolean has_protocol_length = false;
            int protocol_length= -1;
            int content_length = -1;
            int length_left = -1;
            int buffer_size = 1024;
            String content_length_regex = "\"content-length\": [0-9]+";
            byte[] buffer = new byte[buffer_size];
            String protocol = "";
            String content = "";
            String dataString = "";
            boolean all_received = false;
            while(!all_received){
                int bytesRead = din.read(buffer);
                System.out.println("byte read");
                System.out.println(bytesRead);
                if (!has_protocol_length){
                    protocol_length = buffer[0] & 0xFF;
                    length_left = protocol_length;
                    has_protocol_length = true;
                    if (bytesRead == -1) {
                        dataString += new String(buffer, 1, length_left+1 );
                    }else{
                        dataString += new String(buffer, 1, bytesRead-1);
                        length_left = length_left - bytesRead + 1;

                    }
                    System.out.println("here length deducted");
                }else {
                    if (bytesRead == -1) {
                        dataString += new String(buffer, 0, length_left+4);
                    }else{
                        dataString += new String(buffer, 0, bytesRead);
                        length_left -= bytesRead;
                    }
                }
                if (protocol.equals("")) {
                    if (dataString.length() >= protocol_length) {
                        protocol = dataString.substring(0, protocol_length);
                        content_length = getContentLengthMatch(protocol,content_length_regex);
                        if (content_length<0){
                            System.out.println("something went wrong when getting content length");
                            return "";
                        }
                        System.out.println("protocol got");
                        System.out.println(length_left);
                        length_left += content_length;


                        //System.out.println(dataString.substring(protocol_length,protocol_length+613));
                    }
                }
                if (length_left <=0 && bytesRead <0){
                    all_received = true;
                    System.out.println(dataString.length());
                    content = dataString.substring(protocol_length,protocol_length+content_length);
                }

                System.out.println("protocol_length");
                System.out.println(protocol_length);
                System.out.println(dataString.length());
                System.out.println(length_left);
                System.out.println(content_length);

            }
            System.out.println("Protocol: "+ protocol);
            System.out.println(protocol.length());
            System.out.println("Content: "+ content);
            System.out.println(content.length());
            int last_img = content.indexOf("https://product-images.metro.ca/images/h09/h59/9185743667230.jpg");
            System.out.println(last_img);
            System.out.println(content.substring(last_img));
            System.out.println(content.substring(10070));

            din.close();
            return content;
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }
    public int getContentLengthMatch(String text, String regex) {
        Matcher m = Pattern.compile("(?=(" + regex + "))").matcher(text);
        while(m.find()) {
            return Integer.valueOf(m.group(1).replace("\"content-length\": ",""));
        }
        return -1;
    }
    public String get_all(){
        try {
            Socket socket = new Socket(SERVER_IP, SERVERPORT);
            DataOutputStream dOut = new DataOutputStream(socket.getOutputStream());
            DataInputStream din = new DataInputStream(socket.getInputStream());

            String message = "1{\"byteorder\": \"little\", \"content-type\": \"text/json\", \"content-encoding\": \"utf-8\", \"content-length\": 39}{\"action\": \"server\", \"value\": \"status\"}";
            byte[] b = message.getBytes();
            int i = 103;
            b[0] = (byte)i;
            System.out.println(message.length());
            System.out.println(b.length);
            System.out.println(Arrays.toString(b));
            dOut.write(b);
            dOut.flush();
            System.out.println("data sent");
            String result = read_from_socket(socket);
            /*byte[] receive = new byte[4096];
            din.read(receive);
            System.out.println(new String(receive, "UTF-8"));*/

            dOut.close();
            din.close();
            socket.close();
            return result;
        }catch (IOException e1) {
            e1.printStackTrace();

            return "";
        }
    }
}
