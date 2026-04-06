package com.example.uikit.compose

import androidx.compose.animation.core.animateFloatAsState
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
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// ==================== COLOR PALETTE ====================

val BluePrimary = Color(0xFF5B8DEF)
val BlueLight = Color(0xFFA8C4F0)
val PurplePrimary = Color(0xFF7B6BA8)
val PurpleLight = Color(0xFFB8A9D4)
val OrangePrimary = Color(0xFFE8895C)
val OrangeLight = Color(0xFFF2B899)
val GreenPrimary = Color(0xFF5EBD9B)
val GreenLight = Color(0xFFA4DBC8)
val RedBadge = Color(0xFFEF5350)
val Coral = Color(0xFFE07C7C)
val BgCream = Color(0xFFF5F0EB)
val TextDark = Color(0xFF2D3436)
val TextMedium = Color(0xFF636E72)

// ==================== FULL SCREEN PREVIEW ====================

@Composable
fun UIKitScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(BgCream)
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text("Buttons", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        ButtonsSection()

        Spacer(Modifier.height(24.dp))
        Text("Icon Buttons", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        IconButtonsSection()

        Spacer(Modifier.height(24.dp))
        Text("Segmented Tabs", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        SegmentedTabsSection()

        Spacer(Modifier.height(24.dp))
        Text("Progress & Sliders", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        ProgressSection()

        Spacer(Modifier.height(24.dp))
        Text("Badges", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        BadgesSection()

        Spacer(Modifier.height(24.dp))
        Text("Product Cards", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        ProductCardsSection()

        Spacer(Modifier.height(24.dp))
        Text("Toggles & Controls", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        TogglesSection()

        Spacer(Modifier.height(24.dp))
        Text("Chat Bubbles", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        ChatBubblesSection()

        Spacer(Modifier.height(24.dp))
        Text("Grid Cards", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        GridCardsSection()

        Spacer(Modifier.height(24.dp))
        Text("Bottom Navigation", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = TextDark)
        Spacer(Modifier.height(8.dp))
        BottomNavSection()

        Spacer(Modifier.height(32.dp))
    }
}

// ==================== 1. BUTTONS ====================

@Composable
fun ButtonsSection() {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // GET STARTED - gradient filled
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            GradientButton(
                text = "GET STARTED",
                gradient = Brush.horizontalGradient(listOf(BluePrimary, BlueLight)),
                icon = Icons.Default.Rocket
            )
            OutlinedButton(
                onClick = {},
                shape = RoundedCornerShape(24.dp),
                border = ButtonDefaults.outlinedButtonBorder(true).copy(
                    brush = Brush.linearGradient(listOf(GreenPrimary, GreenPrimary))
                )
            ) {
                Icon(Icons.Default.Star, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(8.dp))
                Text("GET STARTED")
            }
        }

        // LOGIN buttons
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(
                onClick = {},
                shape = RoundedCornerShape(24.dp)
            ) { Text("LOGIN") }

            GradientButton(
                text = "LOGIN",
                gradient = Brush.horizontalGradient(listOf(OrangePrimary, OrangeLight))
            )
        }

        // SIGN UP buttons
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            GradientButton(
                text = "SIGN UP",
                gradient = Brush.horizontalGradient(listOf(PurplePrimary, PurpleLight))
            )
            OutlinedButton(
                onClick = {},
                shape = RoundedCornerShape(24.dp),
                colors = ButtonDefaults.outlinedButtonColors(contentColor = OrangePrimary)
            ) { Text("SIGN UP") }
        }

        // CONTINUE buttons
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            OutlinedButton(onClick = {}, shape = RoundedCornerShape(24.dp)) {
                Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(4.dp))
                Text("CONTINUE")
            }
            Button(
                onClick = {},
                shape = RoundedCornerShape(24.dp),
                colors = ButtonDefaults.buttonColors(containerColor = GreenPrimary)
            ) {
                Icon(Icons.Default.ShoppingCart, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(4.dp))
                Text("CONTINUE")
            }
        }

        // GET / CLOSE small buttons
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(
                onClick = {},
                shape = RoundedCornerShape(20.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = BlueLight,
                    contentColor = BluePrimary
                ),
                contentPadding = PaddingValues(horizontal = 24.dp, vertical = 8.dp)
            ) { Text("GET") }

            Button(
                onClick = {},
                shape = RoundedCornerShape(20.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Coral),
                contentPadding = PaddingValues(horizontal = 24.dp, vertical = 8.dp)
            ) { Text("CLOSE") }
        }
    }
}

@Composable
fun GradientButton(
    text: String,
    gradient: Brush,
    icon: ImageVector? = null,
    onClick: () -> Unit = {}
) {
    Button(
        onClick = onClick,
        shape = RoundedCornerShape(24.dp),
        colors = ButtonDefaults.buttonColors(containerColor = Color.Transparent),
        contentPadding = PaddingValues(),
    ) {
        Box(
            modifier = Modifier
                .background(gradient, RoundedCornerShape(24.dp))
                .padding(horizontal = 24.dp, vertical = 12.dp),
            contentAlignment = Alignment.Center
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                if (icon != null) {
                    Icon(icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(18.dp))
                    Spacer(Modifier.width(8.dp))
                }
                Text(text, color = Color.White, fontWeight = FontWeight.Medium)
            }
        }
    }
}

// ==================== 2. ICON BUTTONS ====================

@Composable
fun IconButtonsSection() {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // Filled circular icon buttons
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            CircleIconButton(Icons.Default.Add, BluePrimary)
            CircleIconButton(Icons.Default.Search, PurplePrimary)
            CircleIconButton(Icons.Default.Person, OrangePrimary)
        }
        // Outlined circular icon buttons
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            CircleIconButtonOutlined(Icons.Default.Search, PurplePrimary)
            CircleIconButtonOutlined(Icons.Default.Person, OrangePrimary)
            CircleIconButtonOutlined(Icons.Default.Settings, TextMedium)
        }
        // With notification badge
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            CircleIconButton(Icons.Default.Add, GreenPrimary)
            IconWithBadge(Icons.Default.Notifications, PurplePrimary, badgeCount = 1)
            CircleIconButton(Icons.Default.Close, RedBadge)
        }
    }
}

@Composable
fun CircleIconButton(icon: ImageVector, color: Color, onClick: () -> Unit = {}) {
    IconButton(
        onClick = onClick,
        modifier = Modifier
            .size(48.dp)
            .background(color, CircleShape)
    ) {
        Icon(icon, contentDescription = null, tint = Color.White, modifier = Modifier.size(24.dp))
    }
}

@Composable
fun CircleIconButtonOutlined(icon: ImageVector, color: Color, onClick: () -> Unit = {}) {
    IconButton(
        onClick = onClick,
        modifier = Modifier
            .size(48.dp)
            .border(1.5.dp, color, CircleShape)
    ) {
        Icon(icon, contentDescription = null, tint = color, modifier = Modifier.size(24.dp))
    }
}

@Composable
fun IconWithBadge(icon: ImageVector, color: Color, badgeCount: Int) {
    BadgedBox(
        badge = {
            Badge(containerColor = RedBadge) {
                Text("$badgeCount", color = Color.White, fontSize = 10.sp)
            }
        }
    ) {
        IconButton(
            onClick = {},
            modifier = Modifier
                .size(48.dp)
                .background(color, CircleShape)
        ) {
            Icon(icon, contentDescription = null, tint = Color.White)
        }
    }
}

// ==================== 3. SEGMENTED TABS ====================

@Composable
fun SegmentedTabsSection() {
    val tabs = listOf("DAILY", "WEEKLY", "MONTHLY")
    var selectedTab by remember { mutableIntStateOf(0) }

    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        // Purple variant
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(44.dp)
                .clip(RoundedCornerShape(22.dp))
                .background(PurpleLight)
        ) {
            tabs.forEachIndexed { index, label ->
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(22.dp))
                        .background(if (index == selectedTab) PurplePrimary else Color.Transparent)
                        .clickable { selectedTab = index },
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        label,
                        color = if (index == selectedTab) Color.White else TextMedium,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        }

        // Blue bordered variant
        var selectedTabBlue by remember { mutableIntStateOf(0) }
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(44.dp)
                .clip(RoundedCornerShape(22.dp))
                .border(1.5.dp, BluePrimary, RoundedCornerShape(22.dp))
        ) {
            tabs.forEachIndexed { index, label ->
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxHeight()
                        .background(if (index == selectedTabBlue) BluePrimary else Color.Transparent)
                        .clickable { selectedTabBlue = index },
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        label,
                        color = if (index == selectedTabBlue) Color.White else BluePrimary,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
            }
        }
    }
}

// ==================== 4. PROGRESS & SLIDERS ====================

@Composable
fun ProgressSection() {
    var sliderValue by remember { mutableFloatStateOf(50f) }
    val animatedProgress by animateFloatAsState(targetValue = sliderValue / 100f, label = "progress")

    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        // Green linear progress
        LinearProgressIndicator(
            progress = { 0.65f },
            modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
            color = GreenPrimary,
            trackColor = GreenLight,
        )

        // Blue linear progress
        LinearProgressIndicator(
            progress = { 0.45f },
            modifier = Modifier.fillMaxWidth().height(8.dp).clip(RoundedCornerShape(4.dp)),
            color = BluePrimary,
            trackColor = BlueLight,
        )

        // Slider
        Slider(
            value = sliderValue,
            onValueChange = { sliderValue = it },
            valueRange = 0f..100f,
            colors = SliderDefaults.colors(
                thumbColor = BluePrimary,
                activeTrackColor = BluePrimary,
                inactiveTrackColor = BlueLight
            )
        )

        // Full-width dark blue progress
        LinearProgressIndicator(
            progress = { 0.85f },
            modifier = Modifier.fillMaxWidth().height(12.dp).clip(RoundedCornerShape(6.dp)),
            color = Color(0xFF4A6FA5),
            trackColor = Color(0xFFDFE6E9),
        )

        // Circular progress with percentage
        Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(
                progress = { animatedProgress },
                modifier = Modifier.size(100.dp),
                strokeWidth = 8.dp,
                color = BluePrimary,
                trackColor = Color(0xFFDFE6E9),
            )
            Text(
                "${(animatedProgress * 100).toInt()}%",
                fontSize = 20.sp,
                fontWeight = FontWeight.Medium,
                color = TextDark
            )
        }

        // Small loading spinners
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            listOf(GreenPrimary, BluePrimary, PurplePrimary).forEach { color ->
                CircularProgressIndicator(
                    modifier = Modifier.size(32.dp).padding(4.dp),
                    strokeWidth = 3.dp,
                    color = color,
                )
                Spacer(Modifier.width(8.dp))
            }
        }
    }
}

// ==================== 5. BADGES ====================

@Composable
fun BadgesSection() {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
            BadgePill("NEW", GreenPrimary)
            BadgePill("SALE", OrangePrimary)
            IconWithBadge(Icons.Default.Notifications, PurplePrimary, badgeCount = 3)
            BadgePill("ONLINE", GreenPrimary)
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
            BadgePill("STATUS", OrangePrimary)
            IconWithBadge(Icons.Default.Notifications, BluePrimary, badgeCount = 3)
            BadgePill("ONLINE", GreenPrimary)
        }
    }
}

@Composable
fun BadgePill(text: String, color: Color) {
    Text(
        text = text,
        color = Color.White,
        fontSize = 11.sp,
        fontWeight = FontWeight.Medium,
        modifier = Modifier
            .background(color, RoundedCornerShape(12.dp))
            .padding(horizontal = 12.dp, vertical = 4.dp)
    )
}

// ==================== 6. PRODUCT CARDS ====================

@Composable
fun ProductCardsSection() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        // Product card
        Card(
            modifier = Modifier.weight(1f),
            shape = RoundedCornerShape(16.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White)
        ) {
            Column {
                Text(
                    "PRODUCT",
                    modifier = Modifier.fillMaxWidth().background(GreenLight).padding(8.dp),
                    fontWeight = FontWeight.Bold,
                    fontSize = 12.sp
                )
                Box(
                    modifier = Modifier.fillMaxWidth().height(100.dp).background(GreenLight),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.Image, contentDescription = null, modifier = Modifier.size(48.dp), tint = TextMedium)
                }
                Column(modifier = Modifier.padding(12.dp)) {
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

        // Featured card
        Card(
            modifier = Modifier.weight(1f),
            shape = RoundedCornerShape(16.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White)
        ) {
            Column {
                Column(modifier = Modifier.fillMaxWidth().background(PurpleLight).padding(12.dp)) {
                    Text("FEATURED", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                    Spacer(Modifier.height(4.dp))
                    Box(Modifier.width(60.dp).height(2.dp).background(PurplePrimary))
                    Spacer(Modifier.height(3.dp))
                    Box(Modifier.width(40.dp).height(2.dp).background(PurplePrimary))
                }
                Box(
                    modifier = Modifier.fillMaxWidth().height(120.dp).background(PurpleLight),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.Image, contentDescription = null, modifier = Modifier.size(56.dp), tint = PurplePrimary)
                }
            }
        }
    }
}

// ==================== 7. TOGGLES & CONTROLS ====================

@Composable
fun TogglesSection() {
    var checked1 by remember { mutableStateOf(true) }
    var checked2 by remember { mutableStateOf(false) }
    var switch1 by remember { mutableStateOf(true) }
    var switch2 by remember { mutableStateOf(false) }
    var switch3 by remember { mutableStateOf(true) }

    Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
        // Checkbox row
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = checked1, onCheckedChange = { checked1 = it },
                colors = CheckboxDefaults.colors(checkedColor = BluePrimary))
            Text("Checkbox", modifier = Modifier.padding(start = 8.dp))
            Spacer(Modifier.width(24.dp))
            RadioButton(selected = checked1, onClick = { checked1 = !checked1 },
                colors = RadioButtonDefaults.colors(selectedColor = BluePrimary))
        }

        // Radio row
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = checked2, onCheckedChange = { checked2 = it })
            Text("Radio", modifier = Modifier.padding(start = 8.dp))
            Spacer(Modifier.width(24.dp))
            RadioButton(selected = checked2, onClick = { checked2 = !checked2 })
        }

        // Toggle switch row
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(checked = true, onCheckedChange = {},
                colors = CheckboxDefaults.colors(checkedColor = GreenPrimary))
            Text("Toggle", modifier = Modifier.padding(start = 8.dp))
            Spacer(Modifier.width(24.dp))
            Switch(checked = switch1, onCheckedChange = { switch1 = it },
                colors = SwitchDefaults.colors(checkedTrackColor = BluePrimary))
        }

        // Row of switches
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Switch(checked = switch1, onCheckedChange = { switch1 = it },
                colors = SwitchDefaults.colors(checkedTrackColor = BluePrimary))
            Switch(checked = switch2, onCheckedChange = { switch2 = it })
            Switch(checked = switch3, onCheckedChange = { switch3 = it },
                colors = SwitchDefaults.colors(checkedTrackColor = GreenPrimary))
        }
    }
}

// ==================== 8. CHAT BUBBLES ====================

@Composable
fun ChatBubblesSection() {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // Typing indicator (received)
        Row(modifier = Modifier.fillMaxWidth()) {
            Box(
                modifier = Modifier
                    .background(Color(0xFFDFE6E9), RoundedCornerShape(16.dp, 16.dp, 16.dp, 4.dp))
                    .padding(horizontal = 16.dp, vertical = 12.dp)
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    repeat(3) {
                        Box(Modifier.size(8.dp).background(TextMedium, CircleShape))
                    }
                }
            }
        }

        // Sent message (right-aligned)
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
            Text(
                "Hello! How are you?",
                color = Color.White,
                fontSize = 14.sp,
                modifier = Modifier
                    .background(GreenPrimary, RoundedCornerShape(16.dp, 16.dp, 4.dp, 16.dp))
                    .padding(12.dp)
            )
        }

        // Received message (left-aligned)
        Row(modifier = Modifier.fillMaxWidth()) {
            Text(
                "I'm doing great, thanks!",
                color = TextDark,
                fontSize = 14.sp,
                modifier = Modifier
                    .background(Color(0xFFDFE6E9), RoundedCornerShape(4.dp, 16.dp, 16.dp, 16.dp))
                    .padding(12.dp)
            )
        }
    }
}

// ==================== 9. GRID CARDS ====================

@Composable
fun GridCardsSection() {
    val gridItems = listOf(
        listOf(
            Triple(Icons.Default.GridView, BlueLight, "Grid"),
            Triple(Icons.Default.ChevronRight, BluePrimary, "Next"),
            Triple(Icons.Default.Layers, PurplePrimary, "Layers"),
        ),
        listOf(
            Triple(Icons.Default.Image, BlueLight, "Image"),
            Triple(Icons.Default.ShoppingCart, OrangePrimary, "Cart"),
            Triple(Icons.Default.Settings, PurplePrimary, "Settings"),
        ),
        listOf(
            Triple(Icons.Default.ArrowForward, BluePrimary, "Forward"),
            Triple(Icons.Default.Star, GreenPrimary, "Star"),
            Triple(Icons.Default.MoreHoriz, OrangePrimary, "More"),
        ),
    )

    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        gridItems.forEach { row ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                row.forEach { (icon, color, desc) ->
                    Card(
                        modifier = Modifier.weight(1f).height(80.dp),
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = color),
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                    ) {
                        Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Icon(icon, contentDescription = desc, tint = Color.White, modifier = Modifier.size(32.dp))
                        }
                    }
                }
            }
        }
    }
}

// ==================== 10. BOTTOM NAVIGATION ====================

@Composable
fun BottomNavSection() {
    var selectedItem by remember { mutableIntStateOf(0) }
    val items = listOf(
        Pair("Home", Icons.Default.Home),
        Pair("Discover", Icons.Default.Explore),
        Pair("Cart", Icons.Default.ShoppingCart),
        Pair("Profile", Icons.Default.Person),
    )

    Card(
        shape = RoundedCornerShape(16.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        NavigationBar(containerColor = Color.White) {
            items.forEachIndexed { index, (label, icon) ->
                NavigationBarItem(
                    icon = {
                        if (label == "Cart") {
                            BadgedBox(badge = { Badge(containerColor = RedBadge) { Text("1") } }) {
                                Icon(icon, contentDescription = label)
                            }
                        } else {
                            Icon(icon, contentDescription = label)
                        }
                    },
                    label = { Text(label, fontSize = 11.sp) },
                    selected = selectedItem == index,
                    onClick = { selectedItem = index },
                    colors = NavigationBarItemDefaults.colors(
                        selectedIconColor = BluePrimary,
                        selectedTextColor = BluePrimary,
                        indicatorColor = BlueLight.copy(alpha = 0.3f)
                    )
                )
            }
        }
    }
}
