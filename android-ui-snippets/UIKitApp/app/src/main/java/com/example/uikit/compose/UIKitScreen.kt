package com.example.uikit.compose

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.Dp
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
private val Divider = Color(0xFFDFE6E9)

// ── Main Composable ────────────────────────────────────────────

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true, widthDp = 420, heightDp = 2200, name = "UI Kit Full Preview")
@Composable
fun UIKitScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(BgCream)
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // ━━━━━━━━━━ BUTTONS ━━━━━━━━━━
        SectionTitle("Buttons")
        SectionLabel("Filled Gradient")

        GradientButton("GET STARTED", listOf(BluePrimary, BlueLight), icon = Icons.Default.RocketLaunch)
        GradientButton("LOGIN", listOf(OrangePrimary, OrangeLight), horizontalPadding = 36.dp)
        GradientButton("SIGN UP", listOf(PurplePrimary, PurpleLight), horizontalPadding = 32.dp)

        Button(onClick = {}, shape = RoundedCornerShape(25.dp),
            colors = ButtonDefaults.buttonColors(containerColor = GreenPrimary),
            contentPadding = PaddingValues(horizontal = 24.dp, vertical = 14.dp)) {
            Icon(Icons.Default.ShoppingCart, null, Modifier.size(20.dp))
            Spacer(Modifier.width(8.dp))
            Text("CONTINUE", fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(onClick = {}, shape = RoundedCornerShape(23.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PurplePrimary),
                contentPadding = PaddingValues(start = 20.dp, end = 14.dp, top = 12.dp, bottom = 12.dp)) {
                Text("Explore", fontSize = 14.sp); Spacer(Modifier.width(2.dp))
                Icon(Icons.Default.ChevronRight, null, Modifier.size(20.dp))
            }
            Button(onClick = {}, shape = RoundedCornerShape(23.dp),
                colors = ButtonDefaults.buttonColors(containerColor = GreenPrimary),
                contentPadding = PaddingValues(horizontal = 20.dp, vertical = 12.dp)) {
                Text("Explore  >", fontSize = 14.sp)
            }
            Button(onClick = {}, shape = RoundedCornerShape(23.dp),
                colors = ButtonDefaults.buttonColors(containerColor = OrangePrimary),
                contentPadding = PaddingValues(horizontal = 20.dp, vertical = 12.dp)) {
                Text("Shop Now", fontSize = 14.sp)
            }
        }

        Spacer(Modifier.height(4.dp))
        SectionLabel("Outlined")

        OutlinedButton(onClick = {}, shape = RoundedCornerShape(25.dp),
            border = BorderStroke(1.5.dp, GreenPrimary),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 14.dp)) {
            Text("G", color = GreenPrimary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
            Spacer(Modifier.width(10.dp))
            Text("GET STARTED", color = TextDark, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(onClick = {}, shape = RoundedCornerShape(25.dp),
                border = BorderStroke(1.5.dp, BluePrimary),
                contentPadding = PaddingValues(horizontal = 36.dp, vertical = 14.dp)) {
                Text("LOGIN", color = BluePrimary, fontWeight = FontWeight.Medium, fontSize = 14.sp)
            }
            OutlinedButton(onClick = {}, shape = RoundedCornerShape(25.dp),
                border = BorderStroke(1.5.dp, OrangePrimary),
                contentPadding = PaddingValues(horizontal = 32.dp, vertical = 14.dp)) {
                Text("SIGN UP", color = OrangePrimary, fontWeight = FontWeight.Medium, fontSize = 14.sp)
            }
        }

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(onClick = {}, shape = RoundedCornerShape(25.dp),
                border = BorderStroke(1.5.dp, TextDark),
                contentPadding = PaddingValues(horizontal = 18.dp, vertical = 14.dp)) {
                Icon(Icons.Default.PlayArrow, null, Modifier.size(20.dp), tint = TextDark)
                Spacer(Modifier.width(4.dp))
                Text("CONTINUE", color = TextDark, fontWeight = FontWeight.Medium, fontSize = 14.sp)
            }
            OutlinedButton(onClick = {}, shape = RoundedCornerShape(25.dp),
                border = BorderStroke(1.5.dp, TextDark),
                contentPadding = PaddingValues(horizontal = 18.dp, vertical = 14.dp)) {
                Icon(Icons.Default.ArrowForward, null, Modifier.size(20.dp), tint = TextDark)
                Spacer(Modifier.width(4.dp))
                Text("CONTINUE", color = TextDark, fontWeight = FontWeight.Medium, fontSize = 14.sp)
            }
        }

        Spacer(Modifier.height(4.dp))
        SectionLabel("Small / Utility")
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(onClick = {}, shape = RoundedCornerShape(20.dp),
                colors = ButtonDefaults.buttonColors(containerColor = BluePale, contentColor = BluePrimary),
                contentPadding = PaddingValues(horizontal = 28.dp, vertical = 10.dp)) {
                Text("GET", fontWeight = FontWeight.Medium, fontSize = 13.sp)
            }
            Button(onClick = {}, shape = RoundedCornerShape(20.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Coral),
                contentPadding = PaddingValues(horizontal = 24.dp, vertical = 10.dp)) {
                Text("CLOSE", fontWeight = FontWeight.Medium, fontSize = 13.sp)
            }
        }

        // ━━━━━━━━━━ ICON BUTTONS ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Icon Buttons")
        SectionLabel("Filled")
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            FilledCircleIcon(Icons.Default.Add, BluePrimary)
            FilledCircleIcon(Icons.Default.Search, PurplePrimary)
            FilledCircleIcon(Icons.Default.Person, OrangePrimary)
            FilledCircleIcon(Icons.Default.Add, GreenPrimary)
            BadgedBox(badge = { Badge(containerColor = RedBadge) { Text("1", fontSize = 10.sp) } }) {
                FilledCircleIcon(Icons.Default.Notifications, PurplePrimary)
            }
            FilledCircleIcon(Icons.Default.Close, RedBadge)
        }
        SectionLabel("Outlined")
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedCircleIcon(Icons.Default.Search, PurplePrimary)
            OutlinedCircleIcon(Icons.Default.Person, OrangePrimary)
            OutlinedCircleIcon(Icons.Default.Settings, TextMedium)
        }

        // ━━━━━━━━━━ SEGMENTED TABS ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Segmented Tabs")
        SegmentedTabs(
            items = listOf("DAILY", "WEEKLY", "MONTHLY"),
            selectedColor = PurplePrimary, unselectedColor = PurpleLight.copy(alpha = 0.3f),
            selectedTextColor = Color.White, unselectedTextColor = TextMedium
        )
        SegmentedTabsBordered(
            items = listOf("DAILY", "WEEKLY", "MONTHLY"),
            color = BluePrimary
        )

        // ━━━━━━━━━━ BADGES ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Badges")
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
            BadgePill("NEW", GreenPrimary)
            BadgePill("SALE", OrangePrimary)
            BadgedBox(badge = { Badge(containerColor = RedBadge) { Text("3") } }) {
                Icon(Icons.Default.Notifications, null, Modifier.size(28.dp), tint = PurplePrimary)
            }
            BadgePill("ONLINE", GreenPrimary)
            BadgePill("STATUS", OrangePrimary)
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            BadgePillOutlined("NEW", BluePrimary)
            BadgePill("SALE", OrangePrimary)
            BadgePill("···", BluePrimary)
        }

        // ━━━━━━━━━━ PRODUCT CARDS ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Product Cards")
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            ProductCard(Modifier.weight(1f))
            FeaturedCard(Modifier.weight(1f))
        }

        // ━━━━━━━━━━ PROGRESS ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Progress & Sliders")
        var sliderVal by remember { mutableStateOf(50f) }
        val animProg by animateFloatAsState(sliderVal / 100f, label = "p")

        @Suppress("DEPRECATION")
        LinearProgressIndicator(progress = 0.65f, modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
            color = GreenPrimary, backgroundColor = GreenLight)
        @Suppress("DEPRECATION")
        LinearProgressIndicator(progress = 0.45f, modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
            color = BluePrimary, backgroundColor = BlueLight)
        Slider(value = sliderVal, onValueChange = { sliderVal = it }, valueRange = 0f..100f,
            colors = SliderDefaults.colors(thumbColor = BluePrimary, activeTrackColor = BluePrimary, inactiveTrackColor = BlueLight))
        @Suppress("DEPRECATION")
        LinearProgressIndicator(progress = 0.85f, modifier = Modifier.fillMaxWidth().height(12.dp).clip(RoundedCornerShape(6.dp)),
            color = Color(0xFF4A6FA5), backgroundColor = Divider)

        Box(Modifier.fillMaxWidth().padding(top = 8.dp), contentAlignment = Alignment.Center) {
            @Suppress("DEPRECATION")
            CircularProgressIndicator(progress = animProg, modifier = Modifier.size(100.dp), strokeWidth = 8.dp,
                color = BluePrimary)
            Text("${(animProg * 100).toInt()}%", fontSize = 20.sp, fontWeight = FontWeight.Medium, color = TextDark)
        }

        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.Center) {
            listOf(GreenPrimary, BluePrimary, PurplePrimary).forEach {
                CircularProgressIndicator(Modifier.size(32.dp).padding(4.dp), strokeWidth = 3.dp, color = it)
                Spacer(Modifier.width(8.dp))
            }
        }

        // ━━━━━━━━━━ TOGGLES ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Checkboxes & Toggles")
        var cb1 by remember { mutableStateOf(true) }
        var cb2 by remember { mutableStateOf(false) }
        var sw1 by remember { mutableStateOf(true) }
        var sw2 by remember { mutableStateOf(false) }
        var sw3 by remember { mutableStateOf(true) }

        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(cb1, { cb1 = it }, colors = CheckboxDefaults.colors(checkedColor = BluePrimary))
            Text("Checkbox", Modifier.padding(start = 4.dp)); Spacer(Modifier.width(16.dp))
            RadioButton(cb1, { cb1 = !cb1 }, colors = RadioButtonDefaults.colors(selectedColor = BluePrimary))
        }
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(cb2, { cb2 = it }); Text("Radio", Modifier.padding(start = 4.dp))
            Spacer(Modifier.width(16.dp)); RadioButton(cb2, { cb2 = !cb2 })
        }
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(true, {}, colors = CheckboxDefaults.colors(checkedColor = GreenPrimary))
            Text("Toggle", Modifier.padding(start = 4.dp)); Spacer(Modifier.width(16.dp))
            Switch(sw1, { sw1 = it }, colors = SwitchDefaults.colors(checkedTrackColor = BluePrimary))
        }
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Switch(sw1, { sw1 = it }, colors = SwitchDefaults.colors(checkedTrackColor = BluePrimary))
            Switch(sw2, { sw2 = it })
            Switch(sw3, { sw3 = it }, colors = SwitchDefaults.colors(checkedTrackColor = GreenPrimary))
        }

        // ━━━━━━━━━━ CHAT BUBBLES ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Chat Bubbles")
        // Typing indicator
        Row { Box(Modifier.background(Divider, RoundedCornerShape(16.dp)).padding(horizontal = 16.dp, vertical = 12.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) { repeat(3) { Box(Modifier.size(8.dp).background(TextMedium, CircleShape)) } }
        }}
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
            Text("Hello! How are you?", color = Color.White, fontSize = 14.sp,
                modifier = Modifier.background(GreenPrimary, RoundedCornerShape(16.dp, 16.dp, 4.dp, 16.dp)).padding(12.dp))
        }
        Row { Text("I'm doing great, thanks!", color = TextDark, fontSize = 14.sp,
            modifier = Modifier.background(Divider, RoundedCornerShape(4.dp, 16.dp, 16.dp, 16.dp)).padding(12.dp)) }

        // ━━━━━━━━━━ GRID CARDS ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Grid Cards")
        val grid = listOf(
            listOf(Triple(Icons.Default.GridView, BlueLight, "Grid"), Triple(Icons.Default.ChevronRight, BluePrimary, "Next"), Triple(Icons.Default.Layers, PurplePrimary, "Layers")),
            listOf(Triple(Icons.Default.Image, BlueLight, "Image"), Triple(Icons.Default.ShoppingCart, OrangePrimary, "Cart"), Triple(Icons.Default.Settings, PurplePrimary, "Settings")),
            listOf(Triple(Icons.Default.ArrowForward, BluePrimary, "Forward"), Triple(Icons.Default.Star, GreenPrimary, "Star"), Triple(Icons.Default.MoreHoriz, OrangePrimary, "More"))
        )
        grid.forEach { row ->
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                row.forEach { (icon, color, desc) ->
                    Card(Modifier.weight(1f).height(80.dp), shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = color),
                        elevation = CardDefaults.cardElevation(2.dp)) {
                        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Icon(icon, desc, Modifier.size(32.dp), tint = Color.White)
                        }
                    }
                }
            }
        }

        // ━━━━━━━━━━ BOTTOM NAV ━━━━━━━━━━
        Spacer(Modifier.height(8.dp))
        SectionTitle("Bottom Navigation")
        var navIdx by remember { mutableStateOf(0) }
        val navItems = listOf("Home" to Icons.Default.Home, "Discover" to Icons.Default.Explore,
            "Cart" to Icons.Default.ShoppingCart, "Profile" to Icons.Default.Person)
        Card(shape = RoundedCornerShape(16.dp), elevation = CardDefaults.cardElevation(4.dp)) {
            NavigationBar(containerColor = Color.White) {
                navItems.forEachIndexed { i, (label, icon) ->
                    NavigationBarItem(
                        icon = {
                            if (label == "Cart") BadgedBox(badge = { Badge(containerColor = RedBadge) { Text("1") } }) { Icon(icon, label) }
                            else Icon(icon, label)
                        },
                        label = { Text(label, fontSize = 11.sp) },
                        selected = navIdx == i, onClick = { navIdx = i },
                        colors = NavigationBarItemDefaults.colors(selectedIconColor = BluePrimary, selectedTextColor = BluePrimary, indicatorColor = BlueLight.copy(0.3f))
                    )
                }
            }
        }

        Spacer(Modifier.height(32.dp))
    }
}

// ── Reusable Components ────────────────────────────────────────

@Composable private fun SectionTitle(text: String) {
    Text(text, fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark, modifier = Modifier.padding(top = 8.dp, bottom = 4.dp))
}

@Composable private fun SectionLabel(text: String) {
    Text(text, fontSize = 12.sp, fontWeight = FontWeight.Medium, color = TextMedium, letterSpacing = 1.sp, modifier = Modifier.padding(bottom = 4.dp))
}

@Composable private fun GradientButton(text: String, colors: List<Color>, icon: ImageVector? = null, horizontalPadding: Dp = 24.dp) {
    Button(onClick = {}, shape = RoundedCornerShape(25.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent), contentPadding = PaddingValues()) {
        Row(Modifier.background(Brush.horizontalGradient(colors), RoundedCornerShape(25.dp))
            .padding(horizontal = horizontalPadding, vertical = 14.dp), verticalAlignment = Alignment.CenterVertically) {
            if (icon != null) { Icon(icon, null, Modifier.size(20.dp), tint = Color.White); Spacer(Modifier.width(8.dp)) }
            Text(text, color = Color.White, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        }
    }
}

@Composable private fun FilledCircleIcon(icon: ImageVector, color: Color) {
    IconButton(onClick = {}, modifier = Modifier.size(48.dp).background(color, CircleShape)) {
        Icon(icon, null, Modifier.size(24.dp), tint = Color.White)
    }
}

@Composable private fun OutlinedCircleIcon(icon: ImageVector, color: Color) {
    IconButton(onClick = {}, modifier = Modifier.size(48.dp).border(1.5.dp, color, CircleShape)) {
        Icon(icon, null, Modifier.size(24.dp), tint = color)
    }
}

@Composable private fun BadgePill(text: String, color: Color) {
    Text(text, color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Medium,
        modifier = Modifier.background(color, RoundedCornerShape(12.dp)).padding(horizontal = 12.dp, vertical = 4.dp))
}

@Composable private fun BadgePillOutlined(text: String, color: Color) {
    Text(text, color = color, fontSize = 11.sp, fontWeight = FontWeight.Medium,
        modifier = Modifier.border(1.dp, color, RoundedCornerShape(12.dp)).padding(horizontal = 12.dp, vertical = 4.dp))
}

@Composable private fun SegmentedTabs(items: List<String>, selectedColor: Color, unselectedColor: Color, selectedTextColor: Color, unselectedTextColor: Color) {
    var sel by remember { mutableStateOf(0) }
    Row(Modifier.fillMaxWidth().height(44.dp).clip(RoundedCornerShape(22.dp)).background(unselectedColor)) {
        items.forEachIndexed { i, label ->
            Box(Modifier.weight(1f).fillMaxHeight().clip(RoundedCornerShape(22.dp))
                .background(if (i == sel) selectedColor else Color.Transparent).clickable { sel = i }, contentAlignment = Alignment.Center) {
                Text(label, color = if (i == sel) selectedTextColor else unselectedTextColor, fontSize = 12.sp, fontWeight = FontWeight.Medium)
            }
        }
    }
}

@Composable private fun SegmentedTabsBordered(items: List<String>, color: Color) {
    var sel by remember { mutableStateOf(0) }
    Row(Modifier.fillMaxWidth().height(44.dp).clip(RoundedCornerShape(22.dp)).border(1.5.dp, color, RoundedCornerShape(22.dp))) {
        items.forEachIndexed { i, label ->
            Box(Modifier.weight(1f).fillMaxHeight().background(if (i == sel) color else Color.Transparent).clickable { sel = i },
                contentAlignment = Alignment.Center) {
                Text(label, color = if (i == sel) Color.White else color, fontSize = 12.sp, fontWeight = FontWeight.Medium)
            }
        }
    }
}

@Composable private fun ProductCard(modifier: Modifier = Modifier) {
    Card(modifier, shape = RoundedCornerShape(16.dp), elevation = CardDefaults.cardElevation(4.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)) {
        Column {
            Text("PRODUCT", Modifier.fillMaxWidth().background(GreenLight).padding(8.dp), fontWeight = FontWeight.Bold, fontSize = 12.sp)
            Box(Modifier.fillMaxWidth().height(100.dp).background(GreenLight), contentAlignment = Alignment.Center) {
                Icon(Icons.Default.Image, null, Modifier.size(48.dp), tint = TextMedium)
            }
            Column(Modifier.padding(12.dp)) {
                Text("Title title", fontWeight = FontWeight.Medium, fontSize = 16.sp)
                Text("Image polotor", color = TextMedium, fontSize = 12.sp)
                Spacer(Modifier.height(8.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Price", color = TextMedium, fontSize = 12.sp, modifier = Modifier.weight(1f))
                    Text("$200", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }
            }
        }
    }
}

@Composable private fun FeaturedCard(modifier: Modifier = Modifier) {
    Card(modifier, shape = RoundedCornerShape(16.dp), elevation = CardDefaults.cardElevation(4.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White)) {
        Column {
            Column(Modifier.fillMaxWidth().background(PurpleLight).padding(12.dp)) {
                Text("FEATURED", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                Spacer(Modifier.height(4.dp))
                Box(Modifier.width(60.dp).height(2.dp).background(PurplePrimary))
                Spacer(Modifier.height(3.dp))
                Box(Modifier.width(40.dp).height(2.dp).background(PurplePrimary))
            }
            Box(Modifier.fillMaxWidth().height(120.dp).background(PurpleLight), contentAlignment = Alignment.Center) {
                Icon(Icons.Default.Image, null, Modifier.size(56.dp), tint = PurplePrimary)
            }
        }
    }
}
