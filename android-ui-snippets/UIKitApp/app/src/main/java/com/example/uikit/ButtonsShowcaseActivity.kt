package com.example.uikit

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.button.MaterialButton
import com.google.android.material.floatingactionbutton.FloatingActionButton

/**
 * XML-based Activity rendering all button variants.
 * Uses activity_buttons_showcase.xml layout.
 */
class ButtonsShowcaseActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_buttons_showcase)

        // Filled gradient buttons
        click(R.id.btnGetStartedBlue, "Get Started!")
        click(R.id.btnLoginOrange, "Login")
        click(R.id.btnSignUpPurple, "Sign Up")
        click(R.id.btnContinueGreen, "Continue to Cart")
        click(R.id.btnExplorePurple, "Explore")
        click(R.id.btnExploreGreen, "Explore")
        click(R.id.btnShopNow, "Shop Now")

        // Outlined buttons
        click(R.id.btnGetStartedGoogle, "Google Sign In")
        click(R.id.btnLoginOutlined, "Login")
        click(R.id.btnSignUpOrangeOutlined, "Sign Up")
        click(R.id.btnContinuePlay, "Continue")
        click(R.id.btnContinueArrow, "Continue")

        // Small buttons
        click(R.id.btnGet, "Get")
        click(R.id.btnClose, "Close") { finish() }

        // FABs
        clickFab(R.id.fabAdd, "Add")
        clickFab(R.id.fabSearch, "Search")
        clickFab(R.id.fabPerson, "Profile")
        clickFab(R.id.fabAddGreen, "New Item")
        clickFab(R.id.fabClose, "Dismiss")
    }

    private fun click(id: Int, label: String, action: (() -> Unit)? = null) {
        findViewById<MaterialButton>(id)?.setOnClickListener {
            Toast.makeText(this, label, Toast.LENGTH_SHORT).show()
            action?.invoke()
        }
    }

    private fun clickFab(id: Int, label: String) {
        findViewById<FloatingActionButton>(id)?.setOnClickListener {
            Toast.makeText(this, label, Toast.LENGTH_SHORT).show()
        }
    }
}
