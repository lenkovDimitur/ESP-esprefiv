package com.example.uikit.compose

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val UIKitColorScheme = lightColorScheme(
    primary = Color(0xFF5B8DEF),
    onPrimary = Color.White,
    secondary = Color(0xFF7B6BA8),
    onSecondary = Color.White,
    tertiary = Color(0xFF5EBD9B),
    background = Color(0xFFF5F0EB),
    surface = Color.White,
    onBackground = Color(0xFF2D3436),
    onSurface = Color(0xFF2D3436),
)

@Composable
fun UIKitTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = UIKitColorScheme,
        content = content
    )
}
