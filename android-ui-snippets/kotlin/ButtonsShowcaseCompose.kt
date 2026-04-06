package com.example.uikit.compose

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// ── Color Palette ──────────────────────────────────────────────
private val BluePrimary = Color(0xFF5B8DEF)
private val BlueLight = Color(0xFFA8C4F0)
private val BluePale = Color(0xFFD4E4FA)
private val PurplePrimary = Color(0xFF7B6BA8)
private val PurpleLight = Color(0xFFB8A9D4)
private val OrangePrimary = Color(0xFFE8895C)
private val OrangeLight = Color(0xFFF2B899)
private val GreenPrimary = Color(0xFF5EBD9B)
private val GreenLight = Color(0xFFA4DBC8)
private val RedBadge = Color(0xFFEF5350)
private val Coral = Color(0xFFE07C7C)
private val BgCream = Color(0xFFF5F0EB)
private val TextDark = Color(0xFF2D3436)
private val TextMedium = Color(0xFF636E72)

// ── Main Screen ────────────────────────────────────────────────

@Preview(showBackground = true, widthDp = 400, heightDp = 900)
@Composable
fun ButtonsShowcaseScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(BgCream)
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // ── Filled Gradient Buttons ────────────────────────────
        SectionLabel("Filled Gradient")

        // GET STARTED - blue gradient + rocket icon
        GradientButton(
            text = "GET STARTED",
            colors = listOf(BluePrimary, BlueLight),
            icon = Icons.Default.RocketLaunch
        )

        // LOGIN - orange gradient
        GradientButton(
            text = "LOGIN",
            colors = listOf(OrangePrimary, OrangeLight),
            horizontalPadding = 36.dp
        )

        // SIGN UP - purple gradient
        GradientButton(
            text = "SIGN UP",
            colors = listOf(PurplePrimary, PurpleLight),
            horizontalPadding = 32.dp
        )

        // CONTINUE - solid green + cart icon
        Button(
            onClick = {},
            shape = RoundedCornerShape(25.dp),
            colors = ButtonDefaults.buttonColors(containerColor = GreenPrimary),
            contentPadding = PaddingValues(horizontal = 24.dp, vertical = 14.dp)
        ) {
            Icon(Icons.Default.ShoppingCart, null, Modifier.size(20.dp))
            Spacer(Modifier.width(8.dp))
            Text("CONTINUE", fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }

        // Explore > purple
        Button(
            onClick = {},
            shape = RoundedCornerShape(23.dp),
            colors = ButtonDefaults.buttonColors(containerColor = PurplePrimary),
            contentPadding = PaddingValues(start = 20.dp, end = 16.dp, top = 12.dp, bottom = 12.dp)
        ) {
            Text("Explore", fontSize = 14.sp)
            Spacer(Modifier.width(4.dp))
            Icon(Icons.Default.ChevronRight, null, Modifier.size(20.dp))
        }

        // Explore > green
        Button(
            onClick = {},
            shape = RoundedCornerShape(23.dp),
            colors = ButtonDefaults.buttonColors(containerColor = GreenPrimary),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 12.dp)
        ) {
            Text("Explore  >", fontSize = 14.sp)
        }

        // Shop Now - orange
        Button(
            onClick = {},
            shape = RoundedCornerShape(23.dp),
            colors = ButtonDefaults.buttonColors(containerColor = OrangePrimary),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 12.dp)
        ) {
            Text("Shop Now", fontSize = 14.sp)
        }

        Spacer(Modifier.height(12.dp))

        // ── Outlined Buttons ───────────────────────────────────
        SectionLabel("Outlined")

        // GET STARTED - green border + G icon
        OutlinedButton(
            onClick = {},
            shape = RoundedCornerShape(25.dp),
            border = BorderStroke(1.5.dp, GreenPrimary),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 14.dp)
        ) {
            Icon(Icons.Default.GTranslate, null, Modifier.size(20.dp), tint = GreenPrimary)
            Spacer(Modifier.width(8.dp))
            Text("GET STARTED", color = TextDark, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }

        // LOGIN - blue outlined
        OutlinedButton(
            onClick = {},
            shape = RoundedCornerShape(25.dp),
            border = BorderStroke(1.5.dp, BluePrimary),
            contentPadding = PaddingValues(horizontal = 36.dp, vertical = 14.dp)
        ) {
            Text("LOGIN", color = BluePrimary, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }

        // SIGN UP - orange outlined
        OutlinedButton(
            onClick = {},
            shape = RoundedCornerShape(25.dp),
            border = BorderStroke(1.5.dp, OrangePrimary),
            contentPadding = PaddingValues(horizontal = 32.dp, vertical = 14.dp)
        ) {
            Text("SIGN UP", color = OrangePrimary, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }

        // CONTINUE - dark outlined + play icon
        OutlinedButton(
            onClick = {},
            shape = RoundedCornerShape(25.dp),
            border = BorderStroke(1.5.dp, TextDark),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 14.dp)
        ) {
            Icon(Icons.Default.PlayArrow, null, Modifier.size(20.dp), tint = TextDark)
            Spacer(Modifier.width(4.dp))
            Text("CONTINUE", color = TextDark, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }

        // CONTINUE - dark outlined + arrow icon
        OutlinedButton(
            onClick = {},
            shape = RoundedCornerShape(25.dp),
            border = BorderStroke(1.5.dp, TextDark),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 14.dp)
        ) {
            Icon(Icons.AutoMirrored.Filled.ArrowForward, null, Modifier.size(20.dp), tint = TextDark)
            Spacer(Modifier.width(4.dp))
            Text("CONTINUE", color = TextDark, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }

        // Explore - green outlined + toggle
        var exploreEnabled by remember { mutableStateOf(true) }
        OutlinedButton(
            onClick = { exploreEnabled = !exploreEnabled },
            shape = RoundedCornerShape(23.dp),
            border = BorderStroke(1.5.dp, GreenPrimary),
            contentPadding = PaddingValues(start = 16.dp, end = 8.dp, top = 8.dp, bottom = 8.dp)
        ) {
            Text("Explore", color = GreenPrimary, fontSize = 14.sp, fontWeight = FontWeight.Medium)
            Spacer(Modifier.width(8.dp))
            Switch(
                checked = exploreEnabled,
                onCheckedChange = { exploreEnabled = it },
                modifier = Modifier.height(24.dp),
                colors = SwitchDefaults.colors(
                    checkedTrackColor = GreenLight,
                    checkedThumbColor = Color.White
                )
            )
        }

        Spacer(Modifier.height(12.dp))

        // ── Small / Utility Buttons ────────────────────────────
        SectionLabel("Small / Utility")

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            // GET - pale blue pill
            Button(
                onClick = {},
                shape = RoundedCornerShape(20.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = BluePale,
                    contentColor = BluePrimary
                ),
                contentPadding = PaddingValues(horizontal = 28.dp, vertical = 10.dp)
            ) {
                Text("GET", fontWeight = FontWeight.Medium, fontSize = 13.sp)
            }

            // CLOSE - coral pill
            Button(
                onClick = {},
                shape = RoundedCornerShape(20.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Coral),
                contentPadding = PaddingValues(horizontal = 24.dp, vertical = 10.dp)
            ) {
                Text("CLOSE", fontWeight = FontWeight.Medium, fontSize = 13.sp)
            }
        }

        Spacer(Modifier.height(12.dp))

        // ── Circular Icon Buttons ──────────────────────────────
        SectionLabel("Icon Buttons")

        // Row 1: Filled circles
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            FilledCircleIcon(Icons.Default.Add, BluePrimary)
            FilledCircleIcon(Icons.Default.Search, PurplePrimary)
            FilledCircleIcon(Icons.Default.Person, OrangePrimary)
            FilledCircleIcon(Icons.Default.Add, GreenPrimary)

            // Notification bell with badge
            BadgedBox(
                badge = {
                    Badge(containerColor = RedBadge) {
                        Text("1", fontSize = 10.sp, color = Color.White)
                    }
                }
            ) {
                FilledCircleIcon(Icons.Default.Notifications, PurplePrimary)
            }

            FilledCircleIcon(Icons.Default.Close, RedBadge)
        }

        Spacer(Modifier.height(8.dp))

        // Row 2: Outlined circles
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedCircleIcon(Icons.Default.Search, PurplePrimary)
            OutlinedCircleIcon(Icons.Default.Person, OrangePrimary)
            OutlinedCircleIcon(Icons.Default.Settings, TextMedium)
        }

        Spacer(Modifier.height(24.dp))
    }
}

// ── Reusable Components ────────────────────────────────────────

@Composable
private fun SectionLabel(text: String) {
    Text(
        text = text,
        fontSize = 13.sp,
        fontWeight = FontWeight.Medium,
        color = TextMedium,
        letterSpacing = 1.sp,
        modifier = Modifier.padding(bottom = 4.dp)
    )
}

@Composable
private fun GradientButton(
    text: String,
    colors: List<Color>,
    icon: ImageVector? = null,
    horizontalPadding: androidx.compose.ui.unit.Dp = 24.dp
) {
    Button(
        onClick = {},
        shape = RoundedCornerShape(25.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent),
        contentPadding = PaddingValues()
    ) {
        Row(
            modifier = Modifier
                .background(
                    Brush.horizontalGradient(colors),
                    RoundedCornerShape(25.dp)
                )
                .padding(horizontal = horizontalPadding, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            if (icon != null) {
                Icon(icon, null, Modifier.size(20.dp), tint = Color.White)
                Spacer(Modifier.width(8.dp))
            }
            Text(text, color = Color.White, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }
    }
}

@Composable
private fun FilledCircleIcon(icon: ImageVector, color: Color) {
    IconButton(
        onClick = {},
        modifier = Modifier
            .size(48.dp)
            .background(color, CircleShape)
    ) {
        Icon(icon, null, Modifier.size(24.dp), tint = Color.White)
    }
}

@Composable
private fun OutlinedCircleIcon(icon: ImageVector, color: Color) {
    IconButton(
        onClick = {},
        modifier = Modifier
            .size(48.dp)
            .border(1.5.dp, color, CircleShape)
    ) {
        Icon(icon, null, Modifier.size(24.dp), tint = color)
    }
}
