package com.example.carrompanel

import android.app.Service
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.WindowManager
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast

class FloatingPanelService : Service() {

    private var windowManager: WindowManager? = null
    private var floatingView: View? = null
    private var isRunning = false

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager

        // Main Floating Container
        val rootLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.parseColor("#E60A0A0A")) // Deep dark translucent background
            setPadding(24, 24, 24, 24)
        }

        // Header Title
        val title = TextView(this).apply {
            text = "VOID ON TOP"
            setTextColor(Color.parseColor("#AB47BC")) // Neon Purple
            textSize = 13f
            typeface = android.graphics.Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 16)
        }

        // Status Indicator
        val statusText = TextView(this).apply {
            text = "Status: Idle"
            setTextColor(Color.parseColor("#FF7043")) // Orange/Warning color
            textSize = 11f
            gravity = Gravity.CENTER
            setPadding(0, 0, 0, 16)
        }

        // Toggle Auto-Play Button
        val toggleButton = Button(this).apply {
            text = "Start Auto-Play"
            textSize = 11f
            setBackgroundColor(Color.parseColor("#7B1FA2"))
            setTextColor(Color.WHITE)
            setOnClickListener {
                isRunning = !isRunning
                if (isRunning) {
                    text = "Stop Auto-Play"
                    statusText.text = "Status: Running"
                    statusText.setTextColor(Color.parseColor("#66BB6A")) // Green
                    Toast.makeText(this@FloatingPanelService, "Auto-Play Activated", Toast.LENGTH_SHORT).show()
                    
                    // Trigger test swipe
                    AutoPlayService.instance?.performSwipe(500f, 1600f, 500f, 1000f)
                } else {
                    text = "Start Auto-Play"
                    statusText.text = "Status: Idle"
                    statusText.setTextColor(Color.parseColor("#FF7043"))
                    Toast.makeText(this@FloatingPanelService, "Auto-Play Stopped", Toast.LENGTH_SHORT).show()
                }
            }
        }

        // Close Panel Button
        val closeButton = Button(this).apply {
            text = "Close Panel"
            textSize = 10f
            setBackgroundColor(Color.parseColor("#B71C1C"))
            setTextColor(Color.WHITE)
            setOnClickListener {
                stopSelf()
            }
        }

        rootLayout.addView(title)
        rootLayout.addView(statusText)
        rootLayout.addView(toggleButton)
        rootLayout.addView(closeButton)
        floatingView = rootLayout

        // Window Layout Parameters
        val LAYOUT_FLAG = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            WindowManager.LayoutParams.TYPE_PHONE
        }

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            LAYOUT_FLAG,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = 100
            y = 300
        }

        // Touch listener for dragging the floating panel anywhere on screen
        rootLayout.setOnTouchListener(object : View.OnTouchListener {
            private var initialX = 0
            private var initialY = 0
            private var initialTouchX = 0f
            private var initialTouchY = 0f

            override fun onTouch(v: View, event: MotionEvent): Boolean {
                when (event.action) {
                    MotionEvent.ACTION_DOWN -> {
                        initialX = params.x
                        initialY = params.y
                        initialTouchX = event.rawX
                        initialTouchY = event.rawY
                        return true
                    }
                    MotionEvent.ACTION_MOVE -> {
                        params.x = initialX + (event.rawX - initialTouchX).toInt()
                        params.y = initialY + (event.rawY - initialTouchY).toInt()
                        windowManager?.updateViewLayout(floatingView, params)
                        return true
                    }
                }
                return false
            }
        })

        windowManager?.addView(floatingView, params)
    }

    override fun onDestroy() {
        super.onDestroy()
        if (floatingView != null) {
            windowManager?.removeView(floatingView)
        }
    }
}