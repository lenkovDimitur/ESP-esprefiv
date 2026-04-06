package com.example.uikit

import android.os.Bundle
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.google.android.material.button.MaterialButton
import com.google.android.material.progressindicator.CircularProgressIndicator
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.google.android.material.slider.Slider
import com.google.android.material.switchmaterial.SwitchMaterial

/**
 * Activity demonstrating all UI components from the UI kit.
 * Wire up XML layouts (snippet_*.xml) with interactive behavior.
 */
class UIComponentsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Use any of the snippet layouts, or combine them in a ScrollView
        setContentView(R.layout.activity_ui_components)

        setupButtons()
        setupSegmentedTabs()
        setupProgressIndicators()
        setupBottomNavigation()
        setupToggles()
    }

    // ==================== BUTTONS ====================

    private fun setupButtons() {
        findViewById<MaterialButton>(R.id.btnGetStartedFilled)?.setOnClickListener {
            Toast.makeText(this, "Get Started clicked!", Toast.LENGTH_SHORT).show()
        }

        findViewById<MaterialButton>(R.id.btnGetStartedOutlined)?.setOnClickListener {
            Toast.makeText(this, "Google Sign-In", Toast.LENGTH_SHORT).show()
        }

        findViewById<MaterialButton>(R.id.btnLoginFilled)?.setOnClickListener {
            Toast.makeText(this, "Login clicked", Toast.LENGTH_SHORT).show()
        }

        findViewById<MaterialButton>(R.id.btnContinueCart)?.setOnClickListener {
            Toast.makeText(this, "Continue to checkout", Toast.LENGTH_SHORT).show()
        }

        findViewById<MaterialButton>(R.id.btnClose)?.setOnClickListener {
            finish()
        }
    }

    // ==================== SEGMENTED TABS ====================

    private fun setupSegmentedTabs() {
        val tabs = listOf(
            R.id.tabDaily to "DAILY",
            R.id.tabWeekly to "WEEKLY",
            R.id.tabMonthly to "MONTHLY"
        )

        tabs.forEach { (id, label) ->
            findViewById<TextView>(id)?.setOnClickListener { view ->
                // Reset all tabs
                tabs.forEach { (tabId, _) ->
                    findViewById<TextView>(tabId)?.apply {
                        setBackgroundResource(R.drawable.bg_tab_unselected)
                        setTextColor(getColor(R.color.text_medium))
                    }
                }
                // Activate selected tab
                (view as TextView).apply {
                    setBackgroundResource(R.drawable.bg_tab_selected)
                    setTextColor(getColor(R.color.white))
                }
                Toast.makeText(this, "$label selected", Toast.LENGTH_SHORT).show()
            }
        }
    }

    // ==================== PROGRESS INDICATORS ====================

    private fun setupProgressIndicators() {
        // Animate circular progress to 75%
        findViewById<CircularProgressIndicator>(R.id.circularProgress)?.apply {
            setProgressCompat(75, true)
        }

        // Linear progress bars
        findViewById<LinearProgressIndicator>(R.id.progressGreen)?.apply {
            setProgressCompat(65, true)
        }

        findViewById<LinearProgressIndicator>(R.id.progressBlue)?.apply {
            setProgressCompat(45, true)
        }

        // Slider listener
        findViewById<Slider>(R.id.sliderBlue)?.addOnChangeListener { _, value, _ ->
            findViewById<TextView>(R.id.tvProgressPercent)?.text = "${value.toInt()}%"
            findViewById<CircularProgressIndicator>(R.id.circularProgress)
                ?.setProgressCompat(value.toInt(), true)
        }
    }

    // ==================== BOTTOM NAVIGATION ====================

    private fun setupBottomNavigation() {
        findViewById<BottomNavigationView>(R.id.bottomNavSimple)
            ?.setOnItemSelectedListener { item ->
                when (item.itemId) {
                    R.id.nav_home -> toast("Home")
                    R.id.nav_discover -> toast("Discover")
                    R.id.nav_cart -> toast("Cart")
                    R.id.nav_profile -> toast("Profile")
                }
                true
            }
    }

    // ==================== TOGGLES & SWITCHES ====================

    private fun setupToggles() {
        findViewById<SwitchMaterial>(R.id.toggleSwitch)?.setOnCheckedChangeListener { _, isChecked ->
            toast(if (isChecked) "Toggle ON" else "Toggle OFF")
        }

        findViewById<SwitchMaterial>(R.id.switchExplore)?.setOnCheckedChangeListener { _, isChecked ->
            toast(if (isChecked) "Explore enabled" else "Explore disabled")
        }
    }

    private fun toast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
