package com.example.argus

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.example.argus.data.NotificationClient
import com.example.argus.ui.theme.ArgusTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val notificationClient = NotificationClient(
            host = resources.getString(R.string.api_host),
            port = resources.getInteger(R.integer.api_post)
        )

        setContent {
            ArgusTheme {
                ArgusApp(notificationClient = notificationClient)
            }
        }
    }
}