package com.example.hce

import android.os.AsyncTask
import android.util.Log
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class UpdateKeyTask(val eid: String) : AsyncTask<Void, Void, String>() {

    override fun doInBackground(vararg params: Void?): String? {
        val url = "http://192.168.166.190:8080/api/employees/get_key" // Replace with your API URL
        val jsonObject = JSONObject()
        jsonObject.put("eid", eid)

        try {
            val response = URL(url).openConnection() as HttpURLConnection
            response.setRequestProperty("Content-Type", "application/json; charset=utf-8")
            response.requestMethod = "POST"
            response.doOutput = true

            val outputStream = response.outputStream
            outputStream.write(jsonObject.toString().toByteArray())
            outputStream.flush()
            outputStream.close()

            val inputStream = response.inputStream
            val buffer = ByteArray(1024)
            val builder = StringBuilder()

            while (true) {
                val bytesRead = inputStream.read(buffer)
                if (bytesRead == -1) break
                builder.append(String(buffer, 0, bytesRead))
            }

            inputStream.close()
            return builder.toString()
        } catch (e: Exception) {
            Log.e("UpdateKeyTask", "Error updating key: $e")
        }
        return null
    }

    override fun onPostExecute(result: String?) {
        super.onPostExecute(result)
        if (result != null) {
            try {
                val jsonObject = JSONObject(result)
                val key = jsonObject.getString("key")
                // Update UI or handle successful update here
            } catch (e: Exception) {
                Log.e("UpdateKeyTask", "Error parsing response: $e")
            }
        } else {
            // Handle update failure here
        }
    }
}

