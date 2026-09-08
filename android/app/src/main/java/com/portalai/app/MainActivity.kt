package com.portalai.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.VerticalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import kotlinx.coroutines.delay

data class PortalClip(val id: String, val videoUrl: String, val place: String, val country: String, val quality: String)

private val demoClips = listOf(
    PortalClip("1", "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4", "Public Park", "Japan", "480p"),
    PortalClip("2", "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4", "Seaside", "Algeria", "720p"),
    PortalClip("3", "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4", "Side Street", "Canada", "540p")
)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { MaterialTheme { PortalFeed(demoClips) } }
    }
}

@Composable
fun PortalFeed(clips: List<PortalClip>) {
    val pagerState = rememberPagerState(pageCount = { clips.size })
    VerticalPager(state = pagerState, modifier = Modifier.fillMaxSize(), beyondViewportPageCount = 1) { page ->
        PortalVideo(clips[page], isActive = pagerState.currentPage == page) {
            if (page < clips.lastIndex) pagerState.requestScrollToPage(page + 1)
        }
    }
}

@Composable
fun PortalVideo(clip: PortalClip, isActive: Boolean, onFinished: () -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val player = remember(clip.id) {
        ExoPlayer.Builder(context).build().apply {
            setMediaItem(MediaItem.fromUri(clip.videoUrl)); prepare(); repeatMode = Player.REPEAT_MODE_OFF
        }
    }
    DisposableEffect(player) { onDispose { player.release() } }
    LaunchedEffect(isActive) {
        player.playWhenReady = isActive
        if (isActive) { delay(10_000); player.pause(); onFinished() }
    }

    Box(Modifier.fillMaxSize().background(Color.Black)) {
        AndroidView(
            factory = { PlayerView(it).apply { useController = false; this.player = player } },
            modifier = Modifier.fillMaxSize()
        )
        Text(
            "✦ GÉNÉRÉ PAR IA",
            color = Color.White,
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.align(Alignment.TopStart).padding(24.dp).background(Color(0x88000000)).padding(8.dp, 5.dp)
        )
        Column(Modifier.align(Alignment.BottomStart).padding(24.dp)) {
            Text("${clip.place} · ${clip.country}", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
            Text("10 secondes · ${clip.quality} · monde imaginaire", color = Color.White.copy(alpha = .8f))
            Spacer(Modifier.height(22.dp))
            Text("Glisse pour voyager", color = Color.White, fontWeight = FontWeight.SemiBold)
        }
    }
}

