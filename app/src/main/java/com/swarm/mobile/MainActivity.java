package com.swarm.mobile;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.*;
import android.webkit.*;

public class MainActivity extends Activity {

    private LinearLayout root_layout;
    private LinearLayout bottom_glass_bar;
    private EditText edittext_url;
    private ImageView btn_go;
    private ImageView btn_reload;
    private LinearLayout btn_live;
    private TextView txt_live;

    private LinearLayout linear_web;
    private WebView webview1;

    private HorizontalScrollView top_scroll;
    private LinearLayout top_panel;
    private LinearLayout badge_agents;
    private ImageView img_agents;
    private TextView txt_agents;
    private LinearLayout badge_layers;
    private ImageView img_layers;
    private TextView txt_layers;
    private LinearLayout sep1;

    private LinearLayout btn_run;
    private ImageView img_run;
    private TextView txt_run;

    private LinearLayout btn_replay;
    private ImageView img_replay;
    private TextView txt_replay;

    private LinearLayout btn_tour;
    private ImageView img_tour;
    private TextView txt_tour;

    private LinearLayout btn_speed;
    private ImageView img_speed;
    private TextView txt_speed;

    private LinearLayout btn_sound;
    private ImageView img_sound;
    private TextView txt_sound;

    private LinearLayout btn_rotate;
    private ImageView img_rotate;
    private TextView txt_rotate;

    private LinearLayout btn_record;
    private ImageView img_record;
    private TextView txt_record;

    private LinearLayout btn_fullscreen;
    private ImageView img_fullscreen;

    private boolean isRunning;
    private boolean isSound;
    private boolean isTour;
    private boolean isLandscape;
    private boolean isControlsVisible;
    private boolean isRecording;
    private double speedIndex;
    private String swarmScript;
    private String url;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        try {
            getWindow().setFlags(
                android.view.WindowManager.LayoutParams.FLAG_HARDWARE_ACCELERATED,
                android.view.WindowManager.LayoutParams.FLAG_HARDWARE_ACCELERATED
            );
        } catch(Throwable t) {}
        super.onCreate(savedInstanceState);
        initializeLogic();
    }

    private void initializeLogic() {
// Request runtime permissions on Android 6.0+ for smooth Audio recording and storage
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
    final float density = getResources().getDisplayMetrics().density;

    // Bottom Controls Bar: Apply 26dp smooth capsule outline provider & clip to outline
    top_scroll.setBackgroundResource(R.drawable.m3_top_bar_bg);
    if (android.os.Build.VERSION.SDK_INT >= 21) {
        top_scroll.setOutlineProvider(new CapsuleOutlineProvider(26 * density));
        top_scroll.setClipToOutline(true);
    }
    top_scroll.setHorizontalScrollBarEnabled(false);
    top_scroll.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);
    top_scroll.post(new ScrollResetRunnable(top_scroll));
    top_panel.setBackgroundColor(android.graphics.Color.TRANSPARENT);
    top_panel.setPadding((int) (14 * density), 0, (int) (14 * density), 0);

    // Top Search Bar: Apply 26dp smooth capsule outline provider & clip to outline
    bottom_glass_bar.setBackgroundResource(R.drawable.m3_glass_bar_bg);
    if (android.os.Build.VERSION.SDK_INT >= 21) {
        bottom_glass_bar.setOutlineProvider(new CapsuleOutlineProvider(26 * density));
        bottom_glass_bar.setClipToOutline(true);
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

// Enforce layout gravity and margins: Support both LinearLayout and FrameLayout root hierarchies without any overlap!
try {
    final float density = getResources().getDisplayMetrics().density;
    if (root_layout instanceof android.widget.LinearLayout) {
        ((android.widget.LinearLayout) root_layout).setOrientation(android.widget.LinearLayout.VERTICAL);

        android.widget.LinearLayout.LayoutParams lpTop = new android.widget.LinearLayout.LayoutParams(
            android.widget.LinearLayout.LayoutParams.MATCH_PARENT,
            (int) (52 * density)
        );
        lpTop.setMargins((int) (12 * density), (int) (6 * density), (int) (12 * density), (int) (4 * density));
        bottom_glass_bar.setLayoutParams(lpTop);

        android.widget.LinearLayout.LayoutParams lpWeb = new android.widget.LinearLayout.LayoutParams(
            android.widget.LinearLayout.LayoutParams.MATCH_PARENT,
            0,
            1.0f
        );
        lpWeb.setMargins(0, 0, 0, 0);
        linear_web.setLayoutParams(lpWeb);

        android.widget.LinearLayout.LayoutParams lpBottom = new android.widget.LinearLayout.LayoutParams(
            android.widget.LinearLayout.LayoutParams.MATCH_PARENT,
            (int) (52 * density)
        );
        lpBottom.setMargins((int) (12 * density), (int) (4 * density), (int) (12 * density), (int) (10 * density));
        top_scroll.setLayoutParams(lpBottom);
    } else {
        // FrameLayout root fallback: calculate insets cleanly
        android.widget.FrameLayout.LayoutParams lpTop = new android.widget.FrameLayout.LayoutParams(
            android.widget.FrameLayout.LayoutParams.MATCH_PARENT,
            (int) (52 * density)
        );
        lpTop.gravity = android.view.Gravity.TOP;
        lpTop.topMargin = (int) (6 * density);
        lpTop.leftMargin = (int) (12 * density);
        lpTop.rightMargin = (int) (12 * density);
        bottom_glass_bar.setLayoutParams(lpTop);

        android.widget.FrameLayout.LayoutParams lpWeb = new android.widget.FrameLayout.LayoutParams(
            android.widget.FrameLayout.LayoutParams.MATCH_PARENT,
            android.widget.FrameLayout.LayoutParams.MATCH_PARENT
        );
        lpWeb.topMargin = (int) (60 * density);
        lpWeb.bottomMargin = (int) (66 * density);
        linear_web.setLayoutParams(lpWeb);

        android.widget.FrameLayout.LayoutParams lpBottom = new android.widget.FrameLayout.LayoutParams(
            android.widget.FrameLayout.LayoutParams.MATCH_PARENT,
            (int) (52 * density)
        );
        lpBottom.gravity = android.view.Gravity.BOTTOM;
        lpBottom.bottomMargin = (int) (10 * density);
        lpBottom.leftMargin = (int) (12 * density);
        lpBottom.rightMargin = (int) (12 * density);
        top_scroll.setLayoutParams(lpBottom);
    }
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

// Touch listener for smooth scrolling and clean interactions
try {
    webview1.setOnTouchListener(new android.view.View.OnTouchListener() {
        @Override
        public boolean onTouch(android.view.View v, android.view.MotionEvent event) {
            if (isRecording && event.getAction() == android.view.MotionEvent.ACTION_DOWN) {
                v.performClick();
                btn_record.performClick();
                return true;
            }
            if (isTour && (event.getAction() == android.view.MotionEvent.ACTION_DOWN || event.getAction() == android.view.MotionEvent.ACTION_MOVE)) {
                isTour = false;
                txt_tour.setText("Tour");
                btn_tour.setBackgroundResource(R.drawable.m3_btn_item);
                webview1.evaluateJavascript("window.__tourActive = false; if (window.__tourRaf) cancelAnimationFrame(window.__tourRaf);", null);
            }
            return false;
        }
    });
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
    // Standard Chrome Mobile User-Agent without WebView restrictions (no '; wv', no 'Version/4.0')
    ws.setUserAgentString("Mozilla/5.0 (Linux; Android 14; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36");
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
                    _click_fullscreen();
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
            android.view.ViewGroup.LayoutParams lp;
            if (root_layout instanceof android.widget.LinearLayout) {
                lp = new android.widget.LinearLayout.LayoutParams(
                    android.widget.LinearLayout.LayoutParams.MATCH_PARENT,
                    android.widget.LinearLayout.LayoutParams.MATCH_PARENT
                );
            } else {
                lp = new android.widget.FrameLayout.LayoutParams(
                    android.widget.FrameLayout.LayoutParams.MATCH_PARENT,
                    android.widget.FrameLayout.LayoutParams.MATCH_PARENT
                );
            }
            root_layout.addView(customVideoView, lp);
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
                String lower = newUrl.toLowerCase();
                if (lower.equals("https://m.youtube.com/") || lower.equals("https://m.youtube.com") ||
                    lower.equals("https://youtube.com/") || lower.equals("https://youtube.com") ||
                    lower.equals("https://www.youtube.com/") || lower.equals("https://www.youtube.com")) {
                    view.loadUrl("https://m.youtube.com/feed/trending");
                    return true;
                }
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
            if (isTour) {
                isTour = false;
                txt_tour.setText("Tour");
                btn_tour.setBackgroundResource(R.drawable.m3_btn_item);
            }
            view.evaluateJavascript("window.__tourActive = false; if (window.__tourRaf) cancelAnimationFrame(window.__tourRaf);", null);
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
public static class ScrollResetRunnable implements Runnable {
    private final android.widget.HorizontalScrollView scrollView;
    public ScrollResetRunnable(android.widget.HorizontalScrollView sv) {
        this.scrollView = sv;
    }
    @Override
    public void run() {
        try { if (scrollView != null) scrollView.scrollTo(0, 0); } catch(Throwable t) {}
    }
}
public static class CapsuleOutlineProvider extends android.view.ViewOutlineProvider {
    private final float radius;
    public CapsuleOutlineProvider(float radius) {
        this.radius = radius;
    }
    @Override
    public void getOutline(android.view.View view, android.graphics.Outline outline) {
        outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), radius);
    }
}

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

    }

    public void _click_run() {
isRunning = !isRunning;
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
                if (val == null || "undefined".equals(val) || "\"undefined\"".equals(val)) {
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
}
    }

    public void _click_replay() {
isRunning = true;
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
            if (val == null || "undefined".equals(val) || "\"undefined\"".equals(val)) {
                if (swarmScript != null && !swarmScript.isEmpty()) {
                    webview1.evaluateJavascript(swarmScript, null);
                }
            }
        }
    }
);
android.widget.Toast.makeText(MainActivity.this, "Replaying Swarm...", android.widget.Toast.LENGTH_SHORT).show();
    }

    public void _click_tour() {
isTour = !isTour;
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
}
    }

    public void _click_speed() {
int sIdx = ((int) speedIndex + 1) % 3;
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
    "})();", null);
    }

    public void _click_sound() {
isSound = !isSound;
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
    "})();", null);
    }

    public void _click_rotate() {
isLandscape = !isLandscape;
if (isLandscape) {
    setRequestedOrientation(android.content.pm.ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
    txt_rotate.setText("Port");
    btn_rotate.setBackgroundResource(R.drawable.m3_btn_item_active);
} else {
    setRequestedOrientation(android.content.pm.ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
    txt_rotate.setText("Rotate");
    btn_rotate.setBackgroundResource(R.drawable.m3_btn_item);
}
    }

    public void _click_record() {
if (!isRecording) {
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
}
    }

    public void _click_fullscreen() {
        isControlsVisible = !isControlsVisible;
        int vis = isControlsVisible ? android.view.View.VISIBLE : android.view.View.GONE;
        bottom_glass_bar.setVisibility(vis);
        top_scroll.setVisibility(vis);

        if (!(root_layout instanceof android.widget.LinearLayout)) {
            float density = getResources().getDisplayMetrics().density;
            android.view.ViewGroup.LayoutParams lp = linear_web.getLayoutParams();
            if (lp instanceof android.widget.FrameLayout.LayoutParams) {
                android.widget.FrameLayout.LayoutParams lpWeb = (android.widget.FrameLayout.LayoutParams) lp;
                if (isControlsVisible) {
                    lpWeb.topMargin = (int) (60 * density);
                    lpWeb.bottomMargin = (int) (66 * density);
                } else {
                    lpWeb.topMargin = 0;
                    lpWeb.bottomMargin = 0;
                }
                linear_web.setLayoutParams(lpWeb);
            }
        }
        if (!isControlsVisible) {
            android.widget.Toast.makeText(MainActivity.this, "Fullscreen: Tap web or press Back to restore", android.widget.Toast.LENGTH_SHORT).show();
        }
    }

    public void _click_live() {
isRunning = false;
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
android.widget.Toast.makeText(MainActivity.this, "Live page restored", android.widget.Toast.LENGTH_SHORT).show();
    }

    public void _click_go() {
try {
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

    // Direct YouTube root navigation to trending feed so it is always packed with videos!
    String lower = target.toLowerCase();
    if (lower.equals("https://youtube.com") || lower.equals("https://youtube.com/") ||
        lower.equals("https://m.youtube.com") || lower.equals("https://m.youtube.com/") ||
        lower.equals("https://www.youtube.com") || lower.equals("https://www.youtube.com/")) {
        target = "https://m.youtube.com/feed/trending";
    }
}
edittext_url.setText(target);
url = target;
webview1.loadUrl(url);
    }

    public void _click_reload() {
try {
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
android.widget.Toast.makeText(MainActivity.this, "Reloading...", android.widget.Toast.LENGTH_SHORT).show();
    }
}
