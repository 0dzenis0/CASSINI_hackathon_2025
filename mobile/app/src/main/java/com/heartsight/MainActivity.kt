package com.heartsight

import android.os.*
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.location.*
import okhttp3.*
import org.json.JSONObject
import java.io.IOException

class MainActivity : AppCompatActivity() {
    private lateinit var fusedLocationClient: FusedLocationProviderClient
    private val client = OkHttpClient()
    private val backend = "https://YOUR_BACKEND_URL/api/vitals"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
        sendLoop()
    }

    private fun sendLoop() {
        val hr = (60..140).random()
        fusedLocationClient.lastLocation.addOnSuccessListener { loc ->
            val json = JSONObject().apply {
                put("user_id", "demo")
                put("timestamp", System.currentTimeMillis()/1000.0)
                put("heart_rate", hr)
                put("lat", loc.latitude)
                put("lon", loc.longitude)
            }
            val body = RequestBody.create(MediaType.parse("application/json"), json.toString())
            val req = Request.Builder().url(backend).post(body).build()
            client.newCall(req).enqueue(object: Callback {
                override fun onFailure(call: Call, e: IOException) {}
                override fun onResponse(call: Call, resp: Response) {
                    // TODO: parse risk and update UI
                }
            })
        }
        Handler(Looper.getMainLooper()).postDelayed({ sendLoop() }, 5000)
    }
}
