import os
import json
import zipfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

AES_KEY = b"sketchwaresecure"
AES_IV = b"sketchwaresecure"

def encrypt_data(plaintext_str):
    data_bytes = plaintext_str.encode("utf-8")
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data_bytes) + padder.finalize()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(AES_IV))
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()

def build_project():
    work_dir = r"C:\Users\pushp\.gemini\antigravity\scratch\swarm_mobile_build"
    output_swb = r"C:\Users\pushp\.gemini\antigravity\scratch\Swarm_Mobile.swb"

    # 1. Project metadata
    project_meta = {
        "custom_icon": True,
        "sc_ver_code": "1",
        "my_ws_name": "SwarmMobile",
        "color_accent": -10006364,       # M3 Primary: 0xFF6750A4
        "my_app_name": "Swarm Mobile",
        "sc_ver_name": "1.0",
        "sc_id": "603",
        "color_primary": -10006364,
        "color_control_highlight": 536907213,
        "color_control_normal": -10006364,
        "my_sc_reg_dt": "20261109134500",
        "sketchware_ver": 150,
        "my_sc_pkg_name": "com.swarm.mobile",
        "color_primary_dark": -10006364
    }
    project_enc = encrypt_data(json.dumps(project_meta))

    # 2. data/file
    file_content = (
        "@activity\n"
        '{"fileName":"main","fileType":0,"keyboardSetting":0,"options":0,"orientation":0,"theme":-1}\n'
        "@customview\n"
    )
    file_enc = encrypt_data(file_content)

    # 3. data/library
    compat_data = {
        "adUnits": [],
        "configurations": {
            "dynamic_colors": True,
            "material3": True,
            "theme": "DayNight"
        },
        "data": "",
        "libType": 1,
        "reserved1": "",
        "reserved2": "",
        "reserved3": "",
        "testDevices": [],
        "useYn": "Y"
    }
    library_content = (
        "@firebaseDB\n"
        '{"adUnits":[],"data":"","libType":0,"reserved1":"","reserved2":"","reserved3":"","testDevices":[],"useYn":"N"}\n'
        "@compat\n"
        + json.dumps(compat_data) + "\n"
        "@admob\n"
        '{"adUnits":[],"data":"","libType":2,"reserved1":"","reserved2":"","reserved3":"","testDevices":[],"useYn":"N"}\n'
        "@googleMap\n"
        '{"adUnits":[],"data":"","libType":3,"reserved1":"","reserved2":"","reserved3":"","testDevices":[],"useYn":"N"}\n'
    )
    library_enc = encrypt_data(library_content)

    # 4. data/resource (Complete image registration for Sketchware Image Manager)
    all_icons = [
        "ic_agents", "ic_layers", "ic_run", "ic_stop", "ic_replay",
        "ic_tour", "ic_speed", "ic_unmute", "ic_mute", "ic_rotate",
        "ic_record", "ic_fullscreen", "ic_search", "ic_reload",
        "ic_explore", "ic_refresh", "ic_play_arrow", "ic_volume_off",
        "ic_volume_up", "ic_web"
    ]
    img_lines = ['{"resFullName":"' + name + '.png","resName":"' + name + '","resType":1}' for name in all_icons]
    resource_content = "@images\n" + "\n".join(img_lines) + "\n@sounds\n@fonts\n"
    resource_enc = encrypt_data(resource_content)

    # 5. Helper function to create view widget JSON
    def make_widget(id_name, widget_type, parent, convert="LinearLayout", **kwargs):
        w = {
            "adSize": "",
            "adUnitId": "",
            "alpha": 1.0,
            "checked": 0,
            "choiceMode": 0,
            "clickable": kwargs.get("clickable", 1),
            "convert": convert,
            "customView": "",
            "dividerHeight": 1,
            "enabled": 1,
            "firstDayOfWeek": 1,
            "id": id_name,
            "image": {
                "resName": kwargs.get("image_res", "default_image"),
                "rotate": 0,
                "scaleType": kwargs.get("scaleType", "FIT_CENTER")
            },
            "indeterminate": "false",
            "index": kwargs.get("index", 0),
            "inject": kwargs.get("inject", ""),
            "layout": {
                "backgroundColor": kwargs.get("bg_color", 0),
                "borderColor": 0,
                "gravity": kwargs.get("gravity", 0),
                "height": kwargs.get("height", -2),
                "layoutGravity": kwargs.get("layoutGravity", 0),
                "marginBottom": kwargs.get("margin_b", 0),
                "marginLeft": kwargs.get("margin_l", 0),
                "marginRight": kwargs.get("margin_r", 0),
                "marginTop": kwargs.get("margin_t", 0),
                "orientation": kwargs.get("orientation", 0),
                "paddingBottom": kwargs.get("pad_b", 0),
                "paddingLeft": kwargs.get("pad_l", 0),
                "paddingRight": kwargs.get("pad_r", 0),
                "paddingTop": kwargs.get("pad_t", 0),
                "weight": kwargs.get("weight", 0),
                "weightSum": 0,
                "width": kwargs.get("width", -2)
            },
            "max": 100,
            "parent": parent,
            "parentType": 0,
            "preId": id_name,
            "preIndex": kwargs.get("index", 0),
            "preParent": parent,
            "preParentType": 0,
            "progress": 0,
            "progressStyle": "?android:progressBarStyle",
            "scaleX": 1.0,
            "scaleY": 1.0,
            "spinnerMode": 1,
            "text": {
                "hint": kwargs.get("hint", ""),
                "hintColor": kwargs.get("hint_color", -5592406),
                "imeOption": 2, # IME_ACTION_GO
                "inputType": 1, # TYPE_CLASS_TEXT
                "line": 0,
                "singleLine": kwargs.get("singleLine", 0),
                "text": kwargs.get("text", ""),
                "textColor": kwargs.get("text_color", -1),
                "textFont": "default_font",
                "textSize": kwargs.get("textSize", 14),
                "textType": 0
            },
            "translationX": 0.0,
            "translationY": 0.0,
            "type": widget_type
        }
        return w

    # 6. Build True Floating View Hierarchy (FrameLayout Root):
    # - Root: FrameLayout (full screen, bg=-15723748)
    # - Layer 0 (Behind): linear_web with webview1 (MATCH_PARENT, 100% full screen)
    # - Layer 1 (Top Floating): bottom_glass_bar (Search Bar, layoutGravity=TOP 48, top margin 32dp, bg=-14868958)
    # - Layer 2 (Bottom Floating): top_scroll (Controls Bar, layoutGravity=BOTTOM 80, bottom margin 24dp, bg=-14738652)
    # Generous spacing, distinct badge separation, and explicit dark theme colors for 100% Sketchware visual preview!
    widgets = [
        # Root FrameLayout
        make_widget("root_layout", 0, "root", "FrameLayout", width=-1, height=-1, bg_color=-15723748, index=0),

        # Layer 0: Background Container with WebView taking 100% full screen
        make_widget("linear_web", 0, "root_layout", "LinearLayout", orientation=1, width=-1, height=-1, bg_color=-15723748, index=0),
        make_widget("webview1", 7, "linear_web", "WebView", width=-1, height=-1, bg_color=-15723748, index=0),

        # Layer 1: Floating Top Search Bar (layoutGravity=48 [TOP])
        make_widget("bottom_glass_bar", 0, "root_layout", "LinearLayout", orientation=0, width=-1, height=52,
                    layoutGravity=48, margin_t=14, margin_b=0, margin_l=12, margin_r=12,
                    gravity=16, pad_l=10, pad_r=8, pad_t=6, pad_b=6, bg_color=-14868958, index=1),
        
        # Search Bar Children (Left to Right: URL text input -> Search button -> Reload button -> Live button):
        make_widget("edittext_url", 5, "bottom_glass_bar", "EditText", width=0, height=38, weight=1,
                    text="https://aivorygen.netlify.app", hint="Enter web address...", text_color=-1,
                    hint_color=-5592406, textSize=12, singleLine=1, pad_l=12, pad_r=12, margin_r=8,
                    bg_color=-13949389, index=0),
        make_widget("btn_go", 6, "bottom_glass_bar", "ImageView", width=36, height=36, margin_r=4,
                    image_res="ic_search", scaleType="FIT_CENTER", clickable=1, pad_l=6, pad_r=6, pad_t=6, pad_b=6,
                    bg_color=-13817290, index=1),
        make_widget("btn_reload", 6, "bottom_glass_bar", "ImageView", width=36, height=36, margin_r=6,
                    image_res="ic_reload", scaleType="FIT_CENTER", clickable=1, pad_l=6, pad_r=6, pad_t=6, pad_b=6,
                    bg_color=-13817290, index=2),
        make_widget("btn_live", 0, "bottom_glass_bar", "LinearLayout", orientation=0, width=-2, height=36, margin_r=2,
                    pad_l=14, pad_r=14, gravity=17, clickable=1, bg_color=-5036514, index=3),
        make_widget("txt_live", 4, "btn_live", "TextView", width=-2, height=-2, text="Live", text_color=-1, textSize=12, index=0),

        # Layer 2: Floating Bottom Controls Bar (layoutGravity=80 [BOTTOM])
        make_widget("top_scroll", 0, "root_layout", "HorizontalScrollView", width=-1, height=52,
                    layoutGravity=80, margin_t=0, margin_b=18, margin_l=12, margin_r=12,
                    inject='android:scrollbars="none"\nandroid:overScrollMode="never"', bg_color=0, index=2),
        make_widget("top_panel", 0, "top_scroll", "LinearLayout", orientation=0, width=-2, height=48,
                    pad_l=8, pad_r=8, gravity=17, bg_color=0, index=0),

        # Controls Bar Children:
        # Agents Badge
        make_widget("badge_agents", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_l=4, margin_r=8, pad_l=10, pad_r=12, gravity=17, bg_color=-14278088, index=0),
        make_widget("img_agents", 6, "badge_agents", "ImageView", width=18, height=18, image_res="ic_agents", scaleType="FIT_CENTER", index=0),
        make_widget("txt_agents", 4, "badge_agents", "TextView", width=-2, height=-2, margin_l=6, text="0", text_color=-1, textSize=12, index=1),

        # Layers Badge (with clear distinct gap from Agents)
        make_widget("badge_layers", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_l=0, margin_r=8, pad_l=10, pad_r=12, gravity=17, bg_color=-14278088, index=1),
        make_widget("img_layers", 6, "badge_layers", "ImageView", width=18, height=18, image_res="ic_layers", scaleType="FIT_CENTER", index=0),
        make_widget("txt_layers", 4, "badge_layers", "TextView", width=-2, height=-2, margin_l=6, text="0/0", text_color=-1, textSize=12, index=1),

        # Separator line
        make_widget("sep1", 0, "top_panel", "LinearLayout", width=1, height=20, margin_l=4, margin_r=8, bg_color=872415231, index=2),

        # Action Buttons:
        make_widget("btn_run", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_r=6, pad_l=12, pad_r=14, gravity=17, bg_color=-13817290, index=3),
        make_widget("img_run", 6, "btn_run", "ImageView", width=18, height=18, image_res="ic_run", scaleType="FIT_CENTER", index=0),
        make_widget("txt_run", 4, "btn_run", "TextView", width=-2, height=-2, margin_l=6, text="Run", text_color=-1, textSize=12, index=1),

        make_widget("btn_replay", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_r=6, pad_l=12, pad_r=14, gravity=17, bg_color=-13817290, index=4),
        make_widget("img_replay", 6, "btn_replay", "ImageView", width=18, height=18, image_res="ic_replay", scaleType="FIT_CENTER", index=0),
        make_widget("txt_replay", 4, "btn_replay", "TextView", width=-2, height=-2, margin_l=6, text="Replay", text_color=-1, textSize=12, index=1),

        make_widget("btn_tour", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_r=6, pad_l=12, pad_r=14, gravity=17, bg_color=-13817290, index=5),
        make_widget("img_tour", 6, "btn_tour", "ImageView", width=18, height=18, image_res="ic_tour", scaleType="FIT_CENTER", index=0),
        make_widget("txt_tour", 4, "btn_tour", "TextView", width=-2, height=-2, margin_l=6, text="Tour", text_color=-1, textSize=12, index=1),

        make_widget("btn_speed", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_r=6, pad_l=12, pad_r=14, gravity=17, bg_color=-13817290, index=6),
        make_widget("img_speed", 6, "btn_speed", "ImageView", width=18, height=18, image_res="ic_speed", scaleType="FIT_CENTER", index=0),
        make_widget("txt_speed", 4, "btn_speed", "TextView", width=-2, height=-2, margin_l=6, text="1x", text_color=-1, textSize=12, index=1),

        make_widget("btn_sound", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_r=6, pad_l=12, pad_r=14, gravity=17, bg_color=-13817290, index=7),
        make_widget("img_sound", 6, "btn_sound", "ImageView", width=18, height=18, image_res="ic_unmute", scaleType="FIT_CENTER", index=0),
        make_widget("txt_sound", 4, "btn_sound", "TextView", width=-2, height=-2, margin_l=6, text="Sound", text_color=-1, textSize=12, index=1),

        make_widget("btn_rotate", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_r=6, pad_l=12, pad_r=14, gravity=17, bg_color=-13817290, index=8),
        make_widget("img_rotate", 6, "btn_rotate", "ImageView", width=18, height=18, image_res="ic_rotate", scaleType="FIT_CENTER", index=0),
        make_widget("txt_rotate", 4, "btn_rotate", "TextView", width=-2, height=-2, margin_l=6, text="Rotate", text_color=-1, textSize=12, index=1),

        make_widget("btn_record", 0, "top_panel", "LinearLayout", orientation=0, width=-2, height=36,
                    margin_r=6, pad_l=12, pad_r=14, gravity=17, bg_color=-13817290, index=9),
        make_widget("img_record", 6, "btn_record", "ImageView", width=18, height=18, image_res="ic_record", scaleType="FIT_CENTER", index=0),
        make_widget("txt_record", 4, "btn_record", "TextView", width=-2, height=-2, margin_l=6, text="Record", text_color=-1, textSize=12, index=1),

        make_widget("btn_fullscreen", 0, "top_panel", "LinearLayout", orientation=0, width=36, height=36,
                    margin_r=4, pad_l=9, pad_r=9, pad_t=9, pad_b=9, gravity=17, bg_color=-13817290, index=10),
        make_widget("img_fullscreen", 6, "btn_fullscreen", "ImageView", width=18, height=18, image_res="ic_fullscreen", scaleType="FIT_CENTER", index=0)
    ]

    view_content = "@main.xml\n" + "\n".join(json.dumps(w) for w in widgets) + "\n"
    view_enc = encrypt_data(view_content)

    # 7. data/logic
    var_section = (
        "@MainActivity.java_var\n"
        "0:isRunning\n"
        "0:isSound\n"
        "0:isTour\n"
        "0:isLandscape\n"
        "0:isControlsVisible\n"
        "0:isRecording\n"
        "1:speedIndex\n"
        "2:swarmScript\n"
        "2:url\n"
    )

    func_section = "@MainActivity.java_func\n"
    components_section = "@MainActivity.java_components\n"

    events_section = (
        "@MainActivity.java_events\n"
        '{"eventName":"onClick","eventType":1,"targetId":"btn_run","targetType":0}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_replay","targetType":0}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_tour","targetType":0}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_speed","targetType":0}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_sound","targetType":0}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_rotate","targetType":0}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_record","targetType":0}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_fullscreen","targetType":0}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_go","targetType":6}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_reload","targetType":6}\n'
        '{"eventName":"onClick","eventType":1,"targetId":"btn_live","targetType":0}\n\n'
    )

    # onCreate initializeLogic
    on_create_code = """// Request runtime permissions on Android 6.0+ for smooth Audio recording and storage
try {
    if (android.os.Build.VERSION.SDK_INT >= 23) {
        java.util.ArrayList<String> perms = new java.util.ArrayList<String>();
        if (checkSelfPermission(android.Manifest.permission.RECORD_AUDIO) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
            perms.add(android.Manifest.permission.RECORD_AUDIO);
        }
        if (checkSelfPermission(android.Manifest.permission.WRITE_EXTERNAL_STORAGE) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
            perms.add(android.Manifest.permission.WRITE_EXTERNAL_STORAGE);
        }
        if (!perms.isEmpty()) {
            requestPermissions(perms.toArray(new String[0]), 1001);
        }
    }
} catch (Throwable t) {}

// Set dark background on root and webview immediately to prevent white flash
try {
    root_layout.setBackgroundColor(0xFF0F141C);
    webview1.setBackgroundColor(0xFF0F141C);
} catch(Throwable t) {}

// Safe Material 3 Typography & Typeface
try {
    android.graphics.Typeface tf = android.graphics.Typeface.create("sans-serif-medium", android.graphics.Typeface.NORMAL);
    txt_agents.setTypeface(tf);
    txt_layers.setTypeface(tf);
    txt_run.setTypeface(tf);
    txt_replay.setTypeface(tf);
    txt_tour.setTypeface(tf);
    txt_speed.setTypeface(tf);
    txt_sound.setTypeface(tf);
    txt_rotate.setTypeface(tf);
    txt_record.setTypeface(tf);
    txt_live.setTypeface(tf);
    edittext_url.setTypeface(android.graphics.Typeface.create("sans-serif", android.graphics.Typeface.NORMAL));
} catch(Throwable t) {}

// Apply Material 3 Frosted Glass Backgrounds & Rounded Capsule Clipping
try {
    // Bottom Controls Bar: Apply pill background directly to top_scroll and clip all child content to 28dp outline!
    top_scroll.setBackgroundResource(R.drawable.m3_top_bar_bg);
    if (android.os.Build.VERSION.SDK_INT >= 21) {
        top_scroll.setClipToOutline(true);
        top_scroll.setOutlineProvider(android.view.ViewOutlineProvider.BACKGROUND);
    }
    top_panel.setBackgroundColor(android.graphics.Color.TRANSPARENT);

    // Top Search Bar: Apply 28dp pill background and clip to outline
    bottom_glass_bar.setBackgroundResource(R.drawable.m3_glass_bar_bg);
    if (android.os.Build.VERSION.SDK_INT >= 21) {
        bottom_glass_bar.setClipToOutline(true);
        bottom_glass_bar.setOutlineProvider(android.view.ViewOutlineProvider.BACKGROUND);
    }

    badge_agents.setBackgroundResource(R.drawable.m3_badge_bg);
    badge_layers.setBackgroundResource(R.drawable.m3_badge_bg);
    btn_run.setBackgroundResource(R.drawable.m3_btn_item);
    btn_replay.setBackgroundResource(R.drawable.m3_btn_item);
    btn_tour.setBackgroundResource(R.drawable.m3_btn_item);
    btn_speed.setBackgroundResource(R.drawable.m3_btn_item);
    btn_sound.setBackgroundResource(R.drawable.m3_btn_item);
    btn_rotate.setBackgroundResource(R.drawable.m3_btn_item);
    btn_record.setBackgroundResource(R.drawable.m3_btn_item);
    btn_fullscreen.setBackgroundResource(R.drawable.m3_btn_item);
    edittext_url.setBackgroundResource(R.drawable.m3_input_bg);
    btn_go.setBackgroundResource(R.drawable.m3_btn_icon);
    btn_reload.setBackgroundResource(R.drawable.m3_btn_icon);
    btn_live.setBackgroundResource(R.drawable.m3_btn_live);
} catch(Throwable t) {}

// Enforce layout gravity and margins for floating bars at runtime (symmetric 12dp margins, smooth 28dp capsules)
try {
    float density = getResources().getDisplayMetrics().density;
    android.widget.FrameLayout.LayoutParams lpTop = new android.widget.FrameLayout.LayoutParams(
        android.widget.FrameLayout.LayoutParams.MATCH_PARENT,
        (int) (52 * density)
    );
    lpTop.gravity = android.view.Gravity.TOP;
    lpTop.topMargin = (int) (14 * density);
    lpTop.leftMargin = (int) (12 * density);
    lpTop.rightMargin = (int) (12 * density);
    bottom_glass_bar.setLayoutParams(lpTop);

    android.widget.FrameLayout.LayoutParams lpBottom = new android.widget.FrameLayout.LayoutParams(
        android.widget.FrameLayout.LayoutParams.MATCH_PARENT,
        (int) (52 * density)
    );
    lpBottom.gravity = android.view.Gravity.BOTTOM;
    lpBottom.bottomMargin = (int) (18 * density);
    lpBottom.leftMargin = (int) (12 * density);
    lpBottom.rightMargin = (int) (12 * density);
    top_scroll.setLayoutParams(lpBottom);
} catch(Throwable t) {}

// Enforce layout ordering programmatically
try {
    bottom_glass_bar.removeAllViews();
    bottom_glass_bar.addView(edittext_url);
    bottom_glass_bar.addView(btn_go);
    bottom_glass_bar.addView(btn_reload);
    bottom_glass_bar.addView(btn_live);

    top_panel.removeAllViews();
    top_panel.addView(badge_agents);
    top_panel.addView(badge_layers);
    top_panel.addView(sep1);
    top_panel.addView(btn_run);
    top_panel.addView(btn_replay);
    top_panel.addView(btn_tour);
    top_panel.addView(btn_speed);
    top_panel.addView(btn_sound);
    top_panel.addView(btn_rotate);
    top_panel.addView(btn_record);
    top_panel.addView(btn_fullscreen);
} catch(Throwable t) {}

// Subtle pulsing glow animation on live button
try {
    android.animation.ObjectAnimator pulseAnim = android.animation.ObjectAnimator.ofFloat(btn_live, "alpha", 1.0f, 0.45f);
    pulseAnim.setDuration(850);
    pulseAnim.setRepeatCount(android.animation.ValueAnimator.INFINITE);
    pulseAnim.setRepeatMode(android.animation.ValueAnimator.REVERSE);
    pulseAnim.start();
} catch(Throwable t) {}

// Enable Cookies, Third-Party Cookies & Hardware Acceleration for YouTube / Google
try {
    android.webkit.CookieManager cm = android.webkit.CookieManager.getInstance();
    cm.setAcceptCookie(true);
    if (android.os.Build.VERSION.SDK_INT >= 21) {
        cm.setAcceptThirdPartyCookies(webview1, true);
    }
    webview1.setLayerType(android.view.View.LAYER_TYPE_HARDWARE, null);
} catch(Throwable t) {}

// Configure Android WebView for maximum performance & DOM compatibility
try {
    android.webkit.WebSettings ws = webview1.getSettings();
    ws.setJavaScriptEnabled(true);
    ws.setDomStorageEnabled(true);
    ws.setDatabaseEnabled(true);
    ws.setAllowFileAccess(true);
    ws.setAllowContentAccess(true);
    ws.setLoadWithOverviewMode(true);
    ws.setUseWideViewPort(true);
    ws.setBuiltInZoomControls(true);
    ws.setDisplayZoomControls(false);
    ws.setMediaPlaybackRequiresUserGesture(false);
    ws.setJavaScriptCanOpenWindowsAutomatically(true);
    ws.setSupportMultipleWindows(false);
    if (android.os.Build.VERSION.SDK_INT >= 21) {
        ws.setMixedContentMode(android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
    }
    String defaultUa = ws.getUserAgentString();
    if (defaultUa != null && defaultUa.contains("; wv")) {
        ws.setUserAgentString(defaultUa.replace("; wv", ""));
    }
} catch(Throwable t) {}

// Hardware back key handler
try {
    webview1.setOnKeyListener(new android.view.View.OnKeyListener() {
        @Override
        public boolean onKey(android.view.View v, int keyCode, android.view.KeyEvent event) {
            if (event.getAction() == android.view.KeyEvent.ACTION_DOWN && keyCode == android.view.KeyEvent.KEYCODE_BACK) {
                if (customVideoView != null) {
                    root_layout.removeView(customVideoView);
                    customVideoView = null;
                    if (customViewCallback != null) {
                        try { customViewCallback.onCustomViewHidden(); } catch(Throwable t) {}
                        customViewCallback = null;
                    }
                    linear_web.setVisibility(android.view.View.VISIBLE);
                    if (isControlsVisible) {
                        bottom_glass_bar.setVisibility(android.view.View.VISIBLE);
                        top_scroll.setVisibility(android.view.View.VISIBLE);
                    }
                    return true;
                }
                if (isRecording) {
                    btn_record.performClick();
                    return true;
                }
                if (webview1.canGoBack()) {
                    webview1.goBack();
                    return true;
                } else if (!isControlsVisible) {
                    isControlsVisible = true;
                    bottom_glass_bar.setVisibility(android.view.View.VISIBLE);
                    top_scroll.setVisibility(android.view.View.VISIBLE);
                    return true;
                }
            }
            return false;
        }
    });
} catch(Throwable t) {}

// Load swarm.js asset from assets
swarmScript = "";
try {
    java.io.InputStream is = getAssets().open("swarm.js");
    int size = is.available();
    byte[] buffer = new byte[size];
    is.read(buffer);
    is.close();
    swarmScript = new String(buffer, "UTF-8");
} catch(Throwable t) {}

// Setup WebChromeClient with Media/Video Permission Granting for YouTube
try {
    webview1.setWebChromeClient(new android.webkit.WebChromeClient() {
        @Override
        public void onPermissionRequest(final android.webkit.PermissionRequest request) {
            try {
                request.grant(request.getResources());
            } catch(Throwable t) {}
        }

        @Override
        public void onShowCustomView(android.view.View view, android.webkit.WebChromeClient.CustomViewCallback callback) {
            if (customVideoView != null) {
                onHideCustomView();
                return;
            }
            customVideoView = view;
            customViewCallback = callback;
            root_layout.addView(customVideoView, new android.widget.FrameLayout.LayoutParams(
                android.widget.FrameLayout.LayoutParams.MATCH_PARENT,
                android.widget.FrameLayout.LayoutParams.MATCH_PARENT
            ));
            customVideoView.setBackgroundColor(android.graphics.Color.BLACK);
            linear_web.setVisibility(android.view.View.GONE);
            bottom_glass_bar.setVisibility(android.view.View.GONE);
            top_scroll.setVisibility(android.view.View.GONE);
        }

        @Override
        public void onHideCustomView() {
            if (customVideoView == null) return;
            root_layout.removeView(customVideoView);
            customVideoView = null;
            if (customViewCallback != null) {
                try { customViewCallback.onCustomViewHidden(); } catch(Throwable t) {}
                customViewCallback = null;
            }
            linear_web.setVisibility(android.view.View.VISIBLE);
            if (isControlsVisible) {
                bottom_glass_bar.setVisibility(android.view.View.VISIBLE);
                top_scroll.setVisibility(android.view.View.VISIBLE);
            }
        }
    });
    webview1.setWebViewClient(new android.webkit.WebViewClient() {
        @Override
        public boolean shouldOverrideUrlLoading(android.webkit.WebView view, String newUrl) {
            if (newUrl == null) return false;
            if (newUrl.startsWith("http://") || newUrl.startsWith("https://")) {
                // Return false so WebView natively handles HTTP/HTTPS navigation, POST, cookies, and redirects!
                return false;
            }
            // Handle app intents (intent://, vnd.youtube:, market://, etc.)
            if (newUrl.startsWith("intent://")) {
                try {
                    android.content.Intent intent = android.content.Intent.parseUri(newUrl, android.content.Intent.URI_INTENT_SCHEME);
                    if (intent != null) {
                        String fallbackUrl = intent.getStringExtra("browser_fallback_url");
                        if (fallbackUrl != null && !fallbackUrl.isEmpty()) {
                            view.loadUrl(fallbackUrl);
                            return true;
                        }
                        android.net.Uri dataUri = intent.getData();
                        if (dataUri != null) {
                            String scheme = dataUri.getScheme();
                            if ("http".equalsIgnoreCase(scheme) || "https".equalsIgnoreCase(scheme)) {
                                view.loadUrl(dataUri.toString());
                                return true;
                            }
                        }
                        view.getContext().startActivity(intent);
                        return true;
                    }
                } catch (Throwable t) {}
                return true;
            }
            if (newUrl.startsWith("vnd.youtube:")) {
                String vid = newUrl.substring("vnd.youtube:".length());
                view.loadUrl("https://m.youtube.com/watch?v=" + vid);
                return true;
            }
            try {
                android.content.Intent intent = new android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(newUrl));
                view.getContext().startActivity(intent);
                return true;
            } catch (Throwable t) {}
            return true;
        }
        @Override
        public void onPageStarted(android.webkit.WebView view, String startUrl, android.graphics.Bitmap favicon) {
            super.onPageStarted(view, startUrl, favicon);
            if (startUrl != null && !startUrl.isEmpty()) {
                edittext_url.setText(startUrl);
            }
        }
        @Override
        public void onPageFinished(android.webkit.WebView view, String loadedUrl) {
            super.onPageFinished(view, loadedUrl);
            if (loadedUrl != null && !loadedUrl.isEmpty()) {
                edittext_url.setText(loadedUrl);
            }
            if (isRunning && swarmScript != null && !swarmScript.isEmpty()) {
                webview1.evaluateJavascript(
                    "if (typeof window.__swarmRebuild === 'undefined') { " + swarmScript + " } else if (window.__swarmRebuild && !window.__swarmRebuild.app) { window.__swarmRebuild.start(); }",
                    null
                );
            }
        }
        @Override
        public void onReceivedSslError(android.webkit.WebView view, android.webkit.SslErrorHandler handler, android.net.http.SslError error) {
            handler.proceed();
        }
    });
} catch(Throwable t) {}

// Setup SwarmBridge interface
try {
    webview1.addJavascriptInterface(new Object() {
        @android.webkit.JavascriptInterface
        public void onStatus(final int agents, final int built, final int total, final String status) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    txt_agents.setText(String.valueOf(agents));
                    txt_layers.setText(built + "/" + total);
                    if ("Complete".equalsIgnoreCase(status)) {
                        isRunning = false;
                        img_run.setImageResource(R.drawable.ic_run);
                        txt_run.setText("Run");
                        btn_run.setBackgroundResource(R.drawable.m3_btn_item);
                    }
                }
            });
        }
    }, "SwarmBridge");
} catch(Throwable t) {}

// Handle IME Enter / Go on URL field
try {
    edittext_url.setOnEditorActionListener(new android.widget.TextView.OnEditorActionListener() {
        @Override
        public boolean onEditorAction(android.widget.TextView v, int actionId, android.view.KeyEvent event) {
            if (actionId == android.view.inputmethod.EditorInfo.IME_ACTION_GO ||
                actionId == android.view.inputmethod.EditorInfo.IME_ACTION_DONE ||
                (event != null && event.getKeyCode() == android.view.KeyEvent.KEYCODE_ENTER)) {
                btn_go.performClick();
                return true;
            }
            return false;
        }
    });
} catch(Throwable t) {}

// Initialize variables
isTour = false;
isSound = true;
isRunning = false;
isLandscape = false;
isControlsVisible = true;
isRecording = false;
speedIndex = 0;

// Load web address immediately
try {
    url = edittext_url.getText().toString().trim();
    if (url.isEmpty()) url = "https://aivorygen.netlify.app";
    if (url.contains("aivorygen.netlif.app")) url = url.replace("aivorygen.netlif.app", "aivorygen.netlify.app");
    edittext_url.setText(url);
    webview1.loadUrl(url);
} catch(Throwable t) {
    webview1.loadUrl("https://aivorygen.netlify.app");
}
} // Close initializeLogic()

public android.view.View customVideoView = null;
public android.webkit.WebChromeClient.CustomViewCallback customViewCallback = null;

// Hardware-GPU High-Definition Screen Recorder Helper (720p HD, 8 Mbps, 30 FPS, Non-blocking PixelCopy, AudioRecord Muxing)
public static class ScreenRecorderHelper {
    public static android.media.MediaCodec videoCodec;
    public static android.media.MediaCodec audioCodec;
    public static android.media.AudioRecord audioRecord;
    public static android.media.MediaMuxer muxer;
    public static int videoTrackIndex = -1;
    public static int audioTrackIndex = -1;
    public static boolean muxerStarted = false;
    public static final Object muxerLock = new Object();
    public static volatile boolean active = false;

    public static Thread videoDrainThread;
    public static Thread audioRecordThread;
    public static Thread audioDrainThread;
    public static android.os.HandlerThread workerThread;
    public static android.os.Handler workerHandler;
    public static java.io.File outFile;
    public static android.os.Handler mainHandler = new android.os.Handler(android.os.Looper.getMainLooper());
    public static Runnable captureTicker;

    public static int encW = 720;
    public static int encH = 1280;
    public static long startTimeMs = 0;
    public static long lastVideoPtsUs = 0;
    public static long lastAudioPtsUs = 0;

    public static android.graphics.Bitmap gpuBitmap;
    public static int[] argbBuf;
    public static byte[] nv12Buf;

    // Fast In-Place ARGB to NV12 Conversion with Zero Per-Frame Heap Allocations
    public static void convertArgbToNV12(int[] argb, byte[] yuv, int width, int height) {
        int numPixels = width * height;
        int yIndex = 0;
        int uvIndex = numPixels;
        int index = 0;
        for (int j = 0; j < height; j++) {
            boolean isUVRow = ((j & 1) == 0);
            for (int i = 0; i < width; i++) {
                int c = argb[index++];
                int r = (c >> 16) & 0xFF;
                int g = (c >> 8) & 0xFF;
                int b = c & 0xFF;
                int y = ((66 * r + 129 * g + 25 * b + 128) >> 8) + 16;
                yuv[yIndex++] = (byte) (y < 0 ? 0 : (y > 255 ? 255 : y));
                if (isUVRow && (i & 1) == 0) {
                    int u = ((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128;
                    int v = ((112 * r - 94 * g - 18 * b + 128) >> 8) + 128;
                    yuv[uvIndex++] = (byte) (u < 0 ? 0 : (u > 255 ? 255 : u));
                    yuv[uvIndex++] = (byte) (v < 0 ? 0 : (v > 255 ? 255 : v));
                }
            }
        }
    }
}

private void _dummyMethodForSketchware() {
"""

    btn_run_code = """isRunning = !isRunning;
if (isRunning) {
    img_run.setImageResource(R.drawable.ic_stop);
    txt_run.setText("Stop");
    btn_run.setBackgroundResource(R.drawable.m3_btn_item_active);
    webview1.evaluateJavascript(
        "(function() {" +
        "  if (window.__swarmRebuild) {" +
        "    if (!window.__swarmRebuild.app) window.__swarmRebuild.start();" +
        "  } else {" +
        "    window.__swarmAutoStart = true;" +
        "  }" +
        "})();", null);
    webview1.evaluateJavascript(
        "typeof window.__swarmRebuild;",
        new android.webkit.ValueCallback<String>() {
            @Override
            public void onReceiveValue(String val) {
                if (val == null || "undefined".equals(val) || "\\"undefined\\"".equals(val)) {
                    if (swarmScript != null && !swarmScript.isEmpty()) {
                        webview1.evaluateJavascript(swarmScript, null);
                    }
                }
            }
        }
    );
} else {
    img_run.setImageResource(R.drawable.ic_run);
    txt_run.setText("Run");
    btn_run.setBackgroundResource(R.drawable.m3_btn_item);
    webview1.evaluateJavascript("if (window.__swarmRebuild) window.__swarmRebuild.stop(false);", null);
}"""

    # Replay cleanly restarts the swarm build from layer 0, guaranteed to run even if previously stopped
    btn_replay_code = """isRunning = true;
img_run.setImageResource(R.drawable.ic_stop);
txt_run.setText("Stop");
btn_run.setBackgroundResource(R.drawable.m3_btn_item_active);
webview1.evaluateJavascript(
    "(function() {" +
    "  if (window.__swarmRebuild) {" +
    "    window.__swarmRebuild.restart();" +
    "  } else {" +
    "    window.__swarmAutoStart = true;" +
    "  }" +
    "})();", null);
webview1.evaluateJavascript(
    "typeof window.__swarmRebuild;",
    new android.webkit.ValueCallback<String>() {
        @Override
        public void onReceiveValue(String val) {
            if (val == null || "undefined".equals(val) || "\\"undefined\\"".equals(val)) {
                if (swarmScript != null && !swarmScript.isEmpty()) {
                    webview1.evaluateJavascript(swarmScript, null);
                }
            }
        }
    }
);
android.widget.Toast.makeText(MainActivity.this, "Replaying Swarm...", android.widget.Toast.LENGTH_SHORT).show();"""

    # Tour smoothly auto-scrolls the webpage continuously using 60fps rAF + native Android fallback
    btn_tour_code = """isTour = !isTour;
txt_tour.setText(isTour ? "Touring" : "Tour");
btn_tour.setBackgroundResource(isTour ? R.drawable.m3_btn_item_active : R.drawable.m3_btn_item);
if (isTour) {
    webview1.evaluateJavascript(
        "(function() {" +
        "  if (window.__tourRaf) cancelAnimationFrame(window.__tourRaf);" +
        "  window.__tourActive = true;" +
        "  window.__tourDir = 1;" +
        "  window.__tourCooldown = 0;" +
        "  if (window.__swarmRebuild && window.__swarmRebuild.app) {" +
        "    window.__swarmRebuild.app.tour = true;" +
        "    if (window.__swarmRebuild.app.engine && !window.__swarmRebuild.app.engine.started) {" +
        "      window.__swarmRebuild.app.engine.start();" +
        "    }" +
        "  }" +
        "  function tourLoop() {" +
        "    if (!window.__tourActive) return;" +
        "    var doc = document.scrollingElement || document.documentElement || document.body;" +
        "    var maxScroll = (doc ? doc.scrollHeight : 10000) - window.innerHeight;" +
        "    var cur = window.scrollY || (doc ? doc.scrollTop : 0);" +
        "    if (window.__tourCooldown > 0) {" +
        "      window.__tourCooldown--;" +
        "    } else {" +
        "      if (cur >= maxScroll - 35) {" +
        "        window.__tourDir = -1;" +
        "        window.__tourCooldown = 35;" +
        "      } else if (cur <= 10) {" +
        "        window.__tourDir = 1;" +
        "        window.__tourCooldown = 35;" +
        "      }" +
        "    }" +
        "    window.scrollBy(0, 2.5 * window.__tourDir);" +
        "    window.__tourRaf = requestAnimationFrame(tourLoop);" +
        "  }" +
        "  window.__tourRaf = requestAnimationFrame(tourLoop);" +
        "})();", null);
} else {
    webview1.evaluateJavascript(
        "(function() {" +
        "  window.__tourActive = false;" +
        "  if (window.__tourRaf) { cancelAnimationFrame(window.__tourRaf); window.__tourRaf = null; }" +
        "  if (window.__swarmRebuild && window.__swarmRebuild.app) {" +
        "    window.__swarmRebuild.app.tour = false;" +
        "  }" +
        "})();", null);
}"""

    # Speed button cycles 1x, 2x, 3x directly in swarm engine
    btn_speed_code = """int sIdx = ((int) speedIndex + 1) % 3;
speedIndex = sIdx;
int[] speeds = new int[]{1, 2, 3};
String[] labels = new String[]{"1x", "2x", "3x"};
txt_speed.setText(labels[sIdx]);
btn_speed.setBackgroundResource(sIdx == 0 ? R.drawable.m3_btn_item : R.drawable.m3_btn_item_active);
webview1.evaluateJavascript(
    "(function() {" +
    "  if (window.__swarmRebuild && window.__swarmRebuild.app) {" +
    "    var a = window.__swarmRebuild.app;" +
    "    a.speedIx = " + sIdx + ";" +
    "    if (a.engine) a.engine.speed = " + speeds[sIdx] + ";" +
    "  }" +
    "})();", null);"""

    # Sound button toggles Web Audio synthesizer
    btn_sound_code = """isSound = !isSound;
txt_sound.setText(isSound ? "Sound" : "Mute");
img_sound.setImageResource(isSound ? R.drawable.ic_unmute : R.drawable.ic_mute);
btn_sound.setBackgroundResource(isSound ? R.drawable.m3_btn_item : R.drawable.m3_btn_item_active);
webview1.evaluateJavascript(
    "(function() {" +
    "  if (window.__swarmRebuild && window.__swarmRebuild.app && window.__swarmRebuild.app.sfx) {" +
    "    var s = window.__swarmRebuild.app.sfx;" +
    "    s.setOn(" + isSound + ");" +
    "    if (" + isSound + " && s.blocked) s.resume();" +
    "  }" +
    "})();", null);"""

    btn_rotate_code = """isLandscape = !isLandscape;
if (isLandscape) {
    setRequestedOrientation(android.content.pm.ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
    txt_rotate.setText("Port");
    btn_rotate.setBackgroundResource(R.drawable.m3_btn_item_active);
} else {
    setRequestedOrientation(android.content.pm.ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
    txt_rotate.setText("Rotate");
    btn_rotate.setBackgroundResource(R.drawable.m3_btn_item);
}"""

    # Fullscreen toggles floating bars on/off without any ugly cross button
    btn_fullscreen_code = """isControlsVisible = !isControlsVisible;
int vis = isControlsVisible ? android.view.View.VISIBLE : android.view.View.GONE;
bottom_glass_bar.setVisibility(vis);
top_scroll.setVisibility(vis);
if (!isControlsVisible) {
    android.widget.Toast.makeText(MainActivity.this, "Fullscreen: Tap web or press Back to restore", android.widget.Toast.LENGTH_SHORT).show();
}"""

    btn_live_code = """isRunning = false;
img_run.setImageResource(R.drawable.ic_run);
txt_run.setText("Run");
btn_run.setBackgroundResource(R.drawable.m3_btn_item);
webview1.evaluateJavascript("if (window.__swarmRebuild) { window.__swarmRebuild.stop(true); }", null);
String target = edittext_url.getText().toString().trim();
if (target.isEmpty()) target = "https://aivorygen.netlify.app";
else if (!target.startsWith("http://") && !target.startsWith("https://")) target = "https://" + target;
if (target.contains("aivorygen.netlif.app")) target = target.replace("aivorygen.netlif.app", "aivorygen.netlify.app");
edittext_url.setText(target);
url = target;
webview1.loadUrl(url);
android.widget.Toast.makeText(MainActivity.this, "Live page restored", android.widget.Toast.LENGTH_SHORT).show();"""

    btn_go_code = """try {
    android.view.inputmethod.InputMethodManager imm = (android.view.inputmethod.InputMethodManager) getSystemService(android.content.Context.INPUT_METHOD_SERVICE);
    if (imm != null) {
        imm.hideSoftInputFromWindow(edittext_url.getWindowToken(), 0);
    }
} catch (Exception e) {}
edittext_url.clearFocus();
webview1.requestFocus();

String target = edittext_url.getText().toString().trim();
if (target.isEmpty()) {
    target = "https://aivorygen.netlify.app";
} else {
    // Sanitize mobile keyboard comma typos (e.g. youtube,com -> youtube.com)
    if (target.contains(",com")) target = target.replace(",com", ".com");
    if (target.contains(",org")) target = target.replace(",org", ".org");
    if (target.contains(",net")) target = target.replace(",net", ".net");
    if (target.contains(",app")) target = target.replace(",app", ".app");
    if (target.contains(",co")) target = target.replace(",co", ".co");
    if (target.contains(",io")) target = target.replace(",io", ".io");
    if (target.contains("aivorygen.netlif.app")) target = target.replace("aivorygen.netlif.app", "aivorygen.netlify.app");

    if (!target.startsWith("http://") && !target.startsWith("https://")) {
        if (!target.contains(".") || target.contains(" ")) {
            try {
                target = "https://www.google.com/search?q=" + java.net.URLEncoder.encode(target, "UTF-8");
            } catch (Exception e) {
                target = "https://www.google.com/search?q=" + target.replace(" ", "+");
            }
        } else {
            target = "https://" + target;
        }
    }
}
edittext_url.setText(target);
url = target;
webview1.loadUrl(url);"""

    btn_reload_code = """try {
    android.view.inputmethod.InputMethodManager imm = (android.view.inputmethod.InputMethodManager) getSystemService(android.content.Context.INPUT_METHOD_SERVICE);
    if (imm != null) {
        imm.hideSoftInputFromWindow(edittext_url.getWindowToken(), 0);
    }
} catch (Exception e) {}
edittext_url.clearFocus();

String cur = webview1.getUrl();
if (cur != null && !cur.isEmpty() && !"about:blank".equalsIgnoreCase(cur)) {
    webview1.reload();
} else {
    btn_go.performClick();
}
android.widget.Toast.makeText(MainActivity.this, "Reloading...", android.widget.Toast.LENGTH_SHORT).show();"""

    # Crystal-Clear 720p HD, 8 Mbps High-Bitrate, 30 FPS, Non-flickering, Real-Time Speed Recording with Audio
    btn_record_code = """if (!isRecording) {
    int rawW = webview1.getWidth();
    int rawH = webview1.getHeight();
    if (rawW <= 0 || rawH <= 0) {
        rawW = 720;
        rawH = 1280;
    }
    // High-definition 720p standard 16:9 mobile resolution (divisible by 16)
    int outW = 720;
    int outH = ((rawH * 720 / rawW) / 16) * 16;
    if (outH < 720) outH = 720;
    if (outH > 1600) outH = 1600;

    final int encW = outW;
    final int encH = outH;
    final int framerate = 30;

    java.io.File moviesDir = new java.io.File(android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_MOVIES), "SwarmRecordings");
    if (!moviesDir.exists()) {
        boolean ok = moviesDir.mkdirs();
        if (!ok) {
            moviesDir = getExternalFilesDir(android.os.Environment.DIRECTORY_MOVIES);
            if (moviesDir == null) {
                moviesDir = new java.io.File(getFilesDir(), "Recordings");
            }
            moviesDir.mkdirs();
        }
    }
    java.text.SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyyMMdd_HHmmss", java.util.Locale.US);
    final java.io.File outputFile = new java.io.File(moviesDir, "swarm_" + sdf.format(new java.util.Date()) + ".mp4");

    try {
        // High-Quality Video encoder (AVC / H.264 at 8 Mbps for pristine text clarity)
        android.media.MediaFormat vFormat = android.media.MediaFormat.createVideoFormat("video/avc", encW, encH);
        vFormat.setInteger(android.media.MediaFormat.KEY_COLOR_FORMAT, android.media.MediaCodecInfo.CodecCapabilities.COLOR_FormatYUV420SemiPlanar);
        vFormat.setInteger(android.media.MediaFormat.KEY_BIT_RATE, 8000000);
        vFormat.setInteger(android.media.MediaFormat.KEY_FRAME_RATE, framerate);
        vFormat.setInteger(android.media.MediaFormat.KEY_I_FRAME_INTERVAL, 1);

        final android.media.MediaCodec vCodec = android.media.MediaCodec.createEncoderByType("video/avc");
        vCodec.configure(vFormat, null, null, android.media.MediaCodec.CONFIGURE_FLAG_ENCODE);
        vCodec.start();

        // Audio encoder (AAC 44.1kHz Mono, 128 kbps for 100% universal Android hardware mic compatibility)
        final int sampleRate = 44100;
        android.media.MediaFormat aFormat = android.media.MediaFormat.createAudioFormat("audio/mp4a-latm", sampleRate, 1);
        aFormat.setInteger(android.media.MediaFormat.KEY_BIT_RATE, 128000);
        aFormat.setInteger(android.media.MediaFormat.KEY_AAC_PROFILE, android.media.MediaCodecInfo.CodecProfileLevel.AACObjectLC);

        android.media.MediaCodec aCodecCandidate = null;
        try {
            aCodecCandidate = android.media.MediaCodec.createEncoderByType("audio/mp4a-latm");
            aCodecCandidate.configure(aFormat, null, null, android.media.MediaCodec.CONFIGURE_FLAG_ENCODE);
            aCodecCandidate.start();
        } catch(Throwable t) {
            aCodecCandidate = null;
        }
        final android.media.MediaCodec aCodec = aCodecCandidate;

        // Universal Android AudioRecord (Mono, 44.1kHz, 16-bit PCM)
        android.media.AudioRecord aRecord = null;
        if (aCodec != null) {
            try {
                int minBuf = android.media.AudioRecord.getMinBufferSize(sampleRate, android.media.AudioFormat.CHANNEL_IN_MONO, android.media.AudioFormat.ENCODING_PCM_16BIT);
                if (minBuf < 2048) minBuf = 2048;
                aRecord = new android.media.AudioRecord(
                    android.media.MediaRecorder.AudioSource.MIC,
                    sampleRate,
                    android.media.AudioFormat.CHANNEL_IN_MONO,
                    android.media.AudioFormat.ENCODING_PCM_16BIT,
                    minBuf * 2
                );
                if (aRecord.getState() == android.media.AudioRecord.STATE_INITIALIZED) {
                    aRecord.startRecording();
                } else {
                    aRecord.release();
                    aRecord = null;
                }
            } catch(Throwable t) {
                aRecord = null;
            }
        }

        final android.media.MediaMuxer muxer = new android.media.MediaMuxer(outputFile.getAbsolutePath(), android.media.MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);

        ScreenRecorderHelper.videoCodec = vCodec;
        ScreenRecorderHelper.audioCodec = aCodec;
        ScreenRecorderHelper.audioRecord = aRecord;
        ScreenRecorderHelper.muxer = muxer;
        ScreenRecorderHelper.outFile = outputFile;
        ScreenRecorderHelper.videoTrackIndex = -1;
        ScreenRecorderHelper.audioTrackIndex = -1;
        ScreenRecorderHelper.muxerStarted = false;
        ScreenRecorderHelper.active = true;
        ScreenRecorderHelper.encW = encW;
        ScreenRecorderHelper.encH = encH;
        ScreenRecorderHelper.startTimeMs = System.currentTimeMillis();
        ScreenRecorderHelper.lastVideoPtsUs = 0;
        ScreenRecorderHelper.lastAudioPtsUs = 0;

        ScreenRecorderHelper.gpuBitmap = android.graphics.Bitmap.createBitmap(encW, encH, android.graphics.Bitmap.Config.ARGB_8888);
        ScreenRecorderHelper.argbBuf = new int[encW * encH];
        ScreenRecorderHelper.nv12Buf = new byte[encW * encH * 3 / 2];

        ScreenRecorderHelper.workerThread = new android.os.HandlerThread("SwarmPixelCopyWorker");
        ScreenRecorderHelper.workerThread.start();
        ScreenRecorderHelper.workerHandler = new android.os.Handler(ScreenRecorderHelper.workerThread.getLooper());

        final boolean hasAudio = (aRecord != null && aCodec != null);

        // Hide floating bars during recording so only the clean web content is captured
        bottom_glass_bar.setVisibility(android.view.View.INVISIBLE);
        top_scroll.setVisibility(android.view.View.INVISIBLE);

        // Allow tapping anywhere on the webview to stop recording cleanly
        webview1.setOnTouchListener(new android.view.View.OnTouchListener() {
            @Override
            public boolean onTouch(android.view.View v, android.view.MotionEvent event) {
                if (isRecording && event.getAction() == android.view.MotionEvent.ACTION_DOWN) {
                    v.performClick();
                    btn_record.performClick();
                    return true;
                }
                return false;
            }
        });

        // Video Drain Thread
        ScreenRecorderHelper.videoDrainThread = new Thread(new Runnable() {
            @Override
            public void run() {
                android.media.MediaCodec.BufferInfo bInfo = new android.media.MediaCodec.BufferInfo();
                while (ScreenRecorderHelper.active || (bInfo.flags & android.media.MediaCodec.BUFFER_FLAG_END_OF_STREAM) == 0) {
                    try {
                        int outIndex = vCodec.dequeueOutputBuffer(bInfo, 10000);
                        if (outIndex == android.media.MediaCodec.INFO_TRY_AGAIN_LATER) {
                            if (!ScreenRecorderHelper.active) break;
                        } else if (outIndex == android.media.MediaCodec.INFO_OUTPUT_FORMAT_CHANGED) {
                            synchronized (ScreenRecorderHelper.muxerLock) {
                                ScreenRecorderHelper.videoTrackIndex = muxer.addTrack(vCodec.getOutputFormat());
                                if (!hasAudio || ScreenRecorderHelper.audioTrackIndex >= 0) {
                                    if (!ScreenRecorderHelper.muxerStarted) {
                                        muxer.start();
                                        ScreenRecorderHelper.muxerStarted = true;
                                    }
                                }
                            }
                        } else if (outIndex >= 0) {
                            java.nio.ByteBuffer encData = vCodec.getOutputBuffer(outIndex);
                            if ((bInfo.flags & android.media.MediaCodec.BUFFER_FLAG_CODEC_CONFIG) != 0) {
                                bInfo.size = 0;
                            }
                            synchronized (ScreenRecorderHelper.muxerLock) {
                                if (bInfo.size != 0 && ScreenRecorderHelper.muxerStarted && ScreenRecorderHelper.videoTrackIndex >= 0) {
                                    encData.position(bInfo.offset);
                                    encData.limit(bInfo.offset + bInfo.size);
                                    muxer.writeSampleData(ScreenRecorderHelper.videoTrackIndex, encData, bInfo);
                                }
                            }
                            vCodec.releaseOutputBuffer(outIndex, false);
                            if ((bInfo.flags & android.media.MediaCodec.BUFFER_FLAG_END_OF_STREAM) != 0) break;
                        }
                    } catch (Throwable t) { break; }
                }
            }
        });
        ScreenRecorderHelper.videoDrainThread.start();

        // Audio Drain Thread
        if (hasAudio) {
            ScreenRecorderHelper.audioDrainThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    android.media.MediaCodec.BufferInfo bInfo = new android.media.MediaCodec.BufferInfo();
                    while (ScreenRecorderHelper.active || (bInfo.flags & android.media.MediaCodec.BUFFER_FLAG_END_OF_STREAM) == 0) {
                        try {
                            int outIndex = aCodec.dequeueOutputBuffer(bInfo, 10000);
                            if (outIndex == android.media.MediaCodec.INFO_TRY_AGAIN_LATER) {
                                if (!ScreenRecorderHelper.active) break;
                            } else if (outIndex == android.media.MediaCodec.INFO_OUTPUT_FORMAT_CHANGED) {
                                synchronized (ScreenRecorderHelper.muxerLock) {
                                    ScreenRecorderHelper.audioTrackIndex = muxer.addTrack(aCodec.getOutputFormat());
                                    if (ScreenRecorderHelper.videoTrackIndex >= 0) {
                                        if (!ScreenRecorderHelper.muxerStarted) {
                                            muxer.start();
                                            ScreenRecorderHelper.muxerStarted = true;
                                        }
                                    }
                                }
                            } else if (outIndex >= 0) {
                                java.nio.ByteBuffer encData = aCodec.getOutputBuffer(outIndex);
                                if ((bInfo.flags & android.media.MediaCodec.BUFFER_FLAG_CODEC_CONFIG) != 0) {
                                    bInfo.size = 0;
                                }
                                synchronized (ScreenRecorderHelper.muxerLock) {
                                    if (bInfo.size != 0 && ScreenRecorderHelper.muxerStarted && ScreenRecorderHelper.audioTrackIndex >= 0) {
                                        encData.position(bInfo.offset);
                                        encData.limit(bInfo.offset + bInfo.size);
                                        muxer.writeSampleData(ScreenRecorderHelper.audioTrackIndex, encData, bInfo);
                                    }
                                }
                                aCodec.releaseOutputBuffer(outIndex, false);
                                if ((bInfo.flags & android.media.MediaCodec.BUFFER_FLAG_END_OF_STREAM) != 0) break;
                            }
                        } catch (Throwable t) { break; }
                    }
                }
            });
            ScreenRecorderHelper.audioDrainThread.start();

            // Audio Capture Thread
            final android.media.AudioRecord finalRec = aRecord;
            ScreenRecorderHelper.audioRecordThread = new Thread(new Runnable() {
                @Override
                public void run() {
                    byte[] pcmBuf = new byte[2048];
                    while (ScreenRecorderHelper.active) {
                        try {
                            int read = finalRec.read(pcmBuf, 0, pcmBuf.length);
                            if (read > 0) {
                                int inIndex = aCodec.dequeueInputBuffer(5000);
                                if (inIndex >= 0) {
                                    java.nio.ByteBuffer inBuf = aCodec.getInputBuffer(inIndex);
                                    inBuf.clear();
                                    inBuf.put(pcmBuf, 0, read);
                                    long audioPts = (System.currentTimeMillis() - ScreenRecorderHelper.startTimeMs) * 1000L;
                                    if (audioPts <= ScreenRecorderHelper.lastAudioPtsUs) {
                                        audioPts = ScreenRecorderHelper.lastAudioPtsUs + 1000L;
                                    }
                                    ScreenRecorderHelper.lastAudioPtsUs = audioPts;
                                    aCodec.queueInputBuffer(inIndex, 0, read, audioPts, 0);
                                }
                            }
                        } catch(Throwable t) { break; }
                    }
                }
            });
            ScreenRecorderHelper.audioRecordThread.start();
        }

        // Hardware PixelCopy Capture (GPU direct framebuffer copy, zero blinking, zero UI freeze, 720p HD)
        ScreenRecorderHelper.captureTicker = new Runnable() {
            @Override
            public void run() {
                if (!ScreenRecorderHelper.active) return;
                try {
                    if (android.os.Build.VERSION.SDK_INT >= 26) {
                        android.view.PixelCopy.request(
                            getWindow(),
                            ScreenRecorderHelper.gpuBitmap,
                            new android.view.PixelCopy.OnPixelCopyFinishedListener() {
                                @Override
                                public void onPixelCopyFinished(int copyResult) {
                                    if (copyResult == android.view.PixelCopy.SUCCESS && ScreenRecorderHelper.active) {
                                        try {
                                            ScreenRecorderHelper.gpuBitmap.getPixels(ScreenRecorderHelper.argbBuf, 0, encW, 0, 0, encW, encH);
                                            ScreenRecorderHelper.convertArgbToNV12(ScreenRecorderHelper.argbBuf, ScreenRecorderHelper.nv12Buf, encW, encH);
                                            int inIndex = vCodec.dequeueInputBuffer(5000);
                                            if (inIndex >= 0) {
                                                java.nio.ByteBuffer inputBuffer = vCodec.getInputBuffer(inIndex);
                                                inputBuffer.clear();
                                                inputBuffer.put(ScreenRecorderHelper.nv12Buf);
                                                long vidPts = (System.currentTimeMillis() - ScreenRecorderHelper.startTimeMs) * 1000L;
                                                if (vidPts <= ScreenRecorderHelper.lastVideoPtsUs) {
                                                    vidPts = ScreenRecorderHelper.lastVideoPtsUs + 10000L;
                                                }
                                                ScreenRecorderHelper.lastVideoPtsUs = vidPts;
                                                vCodec.queueInputBuffer(inIndex, 0, ScreenRecorderHelper.nv12Buf.length, vidPts, 0);
                                            }
                                        } catch(Throwable t) {}
                                    }
                                }
                            },
                            ScreenRecorderHelper.workerHandler
                        );
                    }
                } catch(Throwable t) {}

                if (ScreenRecorderHelper.active) {
                    ScreenRecorderHelper.mainHandler.postDelayed(this, 1000 / framerate);
                }
            }
        };
        ScreenRecorderHelper.mainHandler.postDelayed(ScreenRecorderHelper.captureTicker, 150);

        isRecording = true;
        txt_record.setText("Stop Rec");
        btn_record.setBackgroundResource(R.drawable.m3_btn_record_active);
        android.widget.Toast.makeText(MainActivity.this, "HD Recording started. Tap screen or press Back to stop.", android.widget.Toast.LENGTH_LONG).show();
    } catch (Exception ex) {
        bottom_glass_bar.setVisibility(android.view.View.VISIBLE);
        top_scroll.setVisibility(android.view.View.VISIBLE);
        android.widget.Toast.makeText(MainActivity.this, "Record start error: " + ex.getMessage(), android.widget.Toast.LENGTH_LONG).show();
    }
} else {
    isRecording = false;
    txt_record.setText("Record");
    btn_record.setBackgroundResource(R.drawable.m3_btn_item);
    ScreenRecorderHelper.active = false;
    if (ScreenRecorderHelper.captureTicker != null) {
        ScreenRecorderHelper.mainHandler.removeCallbacks(ScreenRecorderHelper.captureTicker);
    }

    // Restore floating bars immediately
    bottom_glass_bar.setVisibility(android.view.View.VISIBLE);
    top_scroll.setVisibility(android.view.View.VISIBLE);
    webview1.setOnTouchListener(null);

    new Thread(new Runnable() {
        @Override
        public void run() {
            try {
                if (ScreenRecorderHelper.audioRecord != null) {
                    ScreenRecorderHelper.audioRecord.stop();
                    ScreenRecorderHelper.audioRecord.release();
                    ScreenRecorderHelper.audioRecord = null;
                }
            } catch (Throwable t) {}
            try {
                if (ScreenRecorderHelper.videoCodec != null) {
                    int inIndex = ScreenRecorderHelper.videoCodec.dequeueInputBuffer(10000);
                    if (inIndex >= 0) {
                        ScreenRecorderHelper.videoCodec.queueInputBuffer(inIndex, 0, 0, ScreenRecorderHelper.lastVideoPtsUs + 10000L, android.media.MediaCodec.BUFFER_FLAG_END_OF_STREAM);
                    }
                }
            } catch (Throwable t) {}
            try {
                if (ScreenRecorderHelper.audioCodec != null) {
                    int inIndex = ScreenRecorderHelper.audioCodec.dequeueInputBuffer(10000);
                    if (inIndex >= 0) {
                        ScreenRecorderHelper.audioCodec.queueInputBuffer(inIndex, 0, 0, ScreenRecorderHelper.lastAudioPtsUs + 10000L, android.media.MediaCodec.BUFFER_FLAG_END_OF_STREAM);
                    }
                }
            } catch (Throwable t) {}
            try {
                if (ScreenRecorderHelper.videoDrainThread != null) ScreenRecorderHelper.videoDrainThread.join(2500);
            } catch (Throwable t) {}
            try {
                if (ScreenRecorderHelper.audioDrainThread != null) ScreenRecorderHelper.audioDrainThread.join(2500);
            } catch (Throwable t) {}
            try {
                if (ScreenRecorderHelper.videoCodec != null) {
                    ScreenRecorderHelper.videoCodec.stop();
                    ScreenRecorderHelper.videoCodec.release();
                    ScreenRecorderHelper.videoCodec = null;
                }
            } catch (Throwable t) {}
            try {
                if (ScreenRecorderHelper.audioCodec != null) {
                    ScreenRecorderHelper.audioCodec.stop();
                    ScreenRecorderHelper.audioCodec.release();
                    ScreenRecorderHelper.audioCodec = null;
                }
            } catch (Throwable t) {}
            try {
                synchronized (ScreenRecorderHelper.muxerLock) {
                    if (ScreenRecorderHelper.muxer != null) {
                        if (ScreenRecorderHelper.muxerStarted) ScreenRecorderHelper.muxer.stop();
                        ScreenRecorderHelper.muxer.release();
                        ScreenRecorderHelper.muxer = null;
                    }
                }
            } catch (Throwable t) {}
            try {
                if (ScreenRecorderHelper.workerThread != null) {
                    ScreenRecorderHelper.workerThread.quitSafely();
                    ScreenRecorderHelper.workerThread = null;
                }
            } catch (Throwable t) {}

            final java.io.File savedFile = ScreenRecorderHelper.outFile;
            if (savedFile != null && savedFile.exists() && savedFile.length() > 0) {
                try {
                    android.media.MediaScannerConnection.scanFile(
                        MainActivity.this,
                        new String[]{savedFile.getAbsolutePath()},
                        new String[]{"video/mp4"},
                        null
                    );
                } catch(Throwable t) {}
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        android.widget.Toast.makeText(MainActivity.this, "HD Video saved: " + savedFile.getName(), android.widget.Toast.LENGTH_LONG).show();
                    }
                });
            } else {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        android.widget.Toast.makeText(MainActivity.this, "Recording finished", android.widget.Toast.LENGTH_SHORT).show();
                    }
                });
            }
        }
    }).start();
}"""

    def make_block(code_str):
        return json.dumps({
            "color": -13391105,
            "id": "1",
            "nextBlock": -1,
            "opCode": "addSourceDirectly",
            "parameters": [code_str],
            "spec": "add source directly %s",
            "subStack1": -1,
            "subStack2": -1,
            "type": " ",
            "typeName": ""
        })

    logic_blocks = (
        "@MainActivity.java_onCreate_initializeLogic\n"
        + make_block(on_create_code) + "\n\n"
        "@MainActivity.java_btn_run_onClick\n"
        + make_block(btn_run_code) + "\n\n"
        "@MainActivity.java_btn_replay_onClick\n"
        + make_block(btn_replay_code) + "\n\n"
        "@MainActivity.java_btn_tour_onClick\n"
        + make_block(btn_tour_code) + "\n\n"
        "@MainActivity.java_btn_speed_onClick\n"
        + make_block(btn_speed_code) + "\n\n"
        "@MainActivity.java_btn_sound_onClick\n"
        + make_block(btn_sound_code) + "\n\n"
        "@MainActivity.java_btn_rotate_onClick\n"
        + make_block(btn_rotate_code) + "\n\n"
        "@MainActivity.java_btn_record_onClick\n"
        + make_block(btn_record_code) + "\n\n"
        "@MainActivity.java_btn_fullscreen_onClick\n"
        + make_block(btn_fullscreen_code) + "\n\n"
        "@MainActivity.java_btn_live_onClick\n"
        + make_block(btn_live_code) + "\n\n"
        "@MainActivity.java_btn_go_onClick\n"
        + make_block(btn_go_code) + "\n\n"
        "@MainActivity.java_btn_reload_onClick\n"
        + make_block(btn_reload_code) + "\n\n"
    )

    logic_content = var_section + func_section + components_section + events_section + logic_blocks
    logic_enc = encrypt_data(logic_content)

    # 8. Permissions & ProGuard (PLAIN UTF-8 JSON for FileResConfig compatibility)
    permission_json = json.dumps([
        "android.permission.INTERNET",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.RECORD_AUDIO"
    ])

    proguard_rules = "-keepattributes *Annotation*\n-dontwarn **\n-keep class ** { *; }\n"
    proguard_config = '{"applyMarker":false,"enabled":false}\n'
    stringfog_json = '{"applyMarker":false,"enabled":false}\n'
    gradle_tool_json = '{"applyMarker":false,"enabled":false}\n'
    google_service_json = '{"applyMarker":false,"enabled":false}\n'
    styles_settings_json = '{"actionbar":false,"fab":false,"statusbar":false,"theme":-1}\n'
    custom_blocks_json = '[]\n'

    # 9. Assemble SWB Zip
    if os.path.exists(output_swb):
        os.remove(output_swb)

    with zipfile.ZipFile(output_swb, "w", zipfile.ZIP_DEFLATED) as zout:
        # Core AES encrypted files
        zout.writestr("project", project_enc)
        zout.writestr("data/file", file_enc)
        zout.writestr("data/library", library_enc)
        zout.writestr("data/resource", resource_enc)
        zout.writestr("data/view", view_enc)
        zout.writestr("data/logic", logic_enc)

        # Plain JSON configuration files
        zout.writestr("data/permission", permission_json.encode("utf-8"))
        zout.writestr("data/proguard-rules.pro", proguard_rules.encode("utf-8"))
        zout.writestr("data/proguard", proguard_config.encode("utf-8"))
        zout.writestr("data/stringfog", stringfog_json.encode("utf-8"))
        zout.writestr("data/styles_settings", styles_settings_json.encode("utf-8"))
        zout.writestr("data/gradle_tool", gradle_tool_json.encode("utf-8"))
        zout.writestr("data/google_service", google_service_json.encode("utf-8"))
        zout.writestr("data/custom_blocks", custom_blocks_json.encode("utf-8"))

        # Include all XML drawables strictly under drawable
        drawables_dir = os.path.join(work_dir, "data", "files", "resource", "drawable")
        if os.path.exists(drawables_dir):
            for fname in os.listdir(drawables_dir):
                if fname.endswith(".xml") and "btn_close" not in fname:
                    fpath = os.path.join(drawables_dir, fname)
                    with open(fpath, "rb") as df:
                        zout.writestr(f"data/files/resource/drawable/{fname}", df.read())

        # Include assets (swarm.js)
        assets_dir = os.path.join(work_dir, "data", "files", "assets")
        if os.path.exists(assets_dir):
            for fname in os.listdir(assets_dir):
                fpath = os.path.join(assets_dir, fname)
                with open(fpath, "rb") as af:
                    zout.writestr(f"data/files/assets/{fname}", af.read())

        # Include icons & resource images strictly in resources/images/
        images_dir = os.path.join(work_dir, "resources", "images")
        if os.path.exists(images_dir):
            for fname in os.listdir(images_dir):
                fpath = os.path.join(images_dir, fname)
                if os.path.isfile(fpath) and "ic_close" not in fname:
                    with open(fpath, "rb") as imf:
                        img_bytes = imf.read()
                        zout.writestr(f"resources/images/{fname}", img_bytes)

        # App launcher icon & nomedia markers
        icon_path = os.path.join(work_dir, "resources", "icons", "icon.png")
        if os.path.exists(icon_path):
            with open(icon_path, "rb") as icf:
                zout.writestr("resources/icons/icon.png", icf.read())

        zout.writestr("resources/images/.nomedia", b"")
        zout.writestr("resources/fonts/.nomedia", b"")
        zout.writestr("resources/sounds/.nomedia", b"")

    print(f"Successfully built project to {output_swb} ({os.path.getsize(output_swb)} bytes)")

if __name__ == "__main__":
    build_project()
