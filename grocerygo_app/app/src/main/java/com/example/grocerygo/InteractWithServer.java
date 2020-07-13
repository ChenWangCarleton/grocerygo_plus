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
import java.util.Arrays;

public class InteractWithServer {

    private static final int SERVERPORT = 65432;
    private static final String SERVER_IP = "10.0.2.2";
    public InteractWithServer(){

    }
    public void read_from_socket(Socket socket){
        try {
            DataInputStream din = new DataInputStream(socket.getInputStream());
            boolean has_protocol_length = false;
            int protocol_length= -1;
            int content_length = -1;
            int length_left = -1;
            int buffer_size = 256;
            byte[] buffer = new byte[buffer_size];
            String protocol = "";
            String dataString = "";
            boolean protocol_received = false;
            while(!protocol_received){
                int bytesRead = din.read(buffer);
                System.out.println("byte read");
                System.out.println(bytesRead);
                if (!has_protocol_length){
                    protocol_length = buffer[0] & 0xFF;
                    length_left = protocol_length;
                    has_protocol_length = true;
                    if (bytesRead == -1) {
                        dataString += new String(buffer, 1, length_left + 1);
                    }else{
                        dataString += new String(buffer, 1, bytesRead-1);
                        length_left = length_left - bytesRead + 1;
                        System.out.println("here length deducted");
                    }
                }else {
                    if (bytesRead == -1) {
                        dataString += new String(buffer, 0, length_left);
                    }else{
                        dataString += new String(buffer, 0, bytesRead);
                        length_left -= bytesRead;
                    }
                }
                if (dataString.length() >= protocol_length){
                    protocol_received = true;
                    protocol = dataString.substring(0,protocol_length);

                    //System.out.println(dataString.substring(protocol_length,protocol_length+613));
                }

                System.out.println("protocol_length");
                System.out.println(protocol_length);
                System.out.println(dataString.length());
                System.out.println(length_left);

            }
            System.out.println("Protocol: "+ protocol);
            System.out.println(protocol.length());

            din.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public void get_all(){
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
            read_from_socket(socket);
            /*byte[] receive = new byte[4096];
            din.read(receive);
            System.out.println(new String(receive, "UTF-8"));*/

            dOut.close();
            din.close();
            socket.close();
        }catch (IOException e1) {
            e1.printStackTrace();
        }
    }
}
