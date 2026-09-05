package com.example.carrompanel

import android.content.Intent
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.provider.Settings
import android.view.Gravity
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(50, 100, 50, 50)
            setBackgroundColor(Color.parseColor("#121212"))
        }

        val titleText = TextView(this).apply {
            text = "VoidOnTop Panel"
            textSize = 26f
            setTextColor(Color.parseColor("#9C27B0"))
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 60)
        }

        val btnPermission = Button(this).apply {
            text = "1. Enable Accessibility Service"
            setOnClickListener {
                startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))
            }
        }

        val btnOverlay = Button(this).apply {
            text = "2. Allow Draw Over Other Apps"
            setOnClickListener {
                val intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:$packageName"))
                startActivity(intent)
            }
        }

        val btnToggle = Button(this).apply {
            text = "Launch Floating Panel"
            setOnClickListener {
                if (AutoPlayService.instance != null) {
                    val intent = Intent(this@MainActivity, FloatingPanelService::class.java)
                    startService(intent)
                    Toast.makeText(this@MainActivity, "VoidOnTop Overlay Active", Toast.LENGTH_SHORT).show()
                    finish()
                } else {
                    Toast.makeText(this@MainActivity, "Enable Accessibility Service First!", Toast.LENGTH_LONG).show()
                }
            }
        }

        layout.addView(titleText)
        layout.addView(btnPermission)
        layout.addView(btnOverlay)
        layout.addView(btnToggle)
        
        setContentView(layout)
    }
}