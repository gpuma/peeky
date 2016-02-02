package mrcv.peekyclient;

import android.os.AsyncTask;
import android.util.Log;

import java.net.Socket;

/**
 * Created by Gustavo on 02/02/2016.
 */
public class SocketTask extends AsyncTask<Void, Void, Void> {

    @Override
    protected Void doInBackground(Void... params) {
        String localIP = "192.168.0.11";
        String publicIP = "131.181.158.31";
        try
        {
            Log.d("SOCK", "Socket is being created!!");
            Socket s = new Socket(localIP, 6666);
            Log.d("SOCK", "Socket was created!!");
            //DataOutputStream dos = new DataOutputStream(s.getOutputStream());

        }
        catch (Exception e)
        {
            Log.d("SOCK", e.getMessage());
        }
        return null;
    }
}
