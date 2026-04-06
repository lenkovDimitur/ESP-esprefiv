package com.example.uikit

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.uikit.compose.UIKitScreen
import com.example.uikit.compose.UIKitTheme

/**
 * Main launcher activity — renders all UI kit components using Jetpack Compose.
 * Just run the app to see every component from the design photo.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            UIKitTheme {
                UIKitScreen()
            }
        }
    }
}
