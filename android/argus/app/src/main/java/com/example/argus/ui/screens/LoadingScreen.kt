package com.example.argus.ui.screens

import android.content.Context
import android.os.Build.VERSION.SDK_INT
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.painter.Painter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import coil.ImageLoader
import coil.compose.AsyncImagePainter
import coil.compose.rememberAsyncImagePainter
import coil.decode.GifDecoder
import coil.decode.ImageDecoderDecoder
import coil.request.ImageRequest
import coil.size.Size
import com.example.argus.R

@Composable
fun LoadingScreen(modifier: Modifier = Modifier) {
    Box(modifier = modifier, contentAlignment = Alignment.Center) {
        Image(
            painter = loadingImage(),
            contentDescription = stringResource(R.string.loading),
            modifier = modifier.size(200.dp),
        )
    }
}

@Composable
fun loadingImage(contentScale: ContentScale = ContentScale.Fit) : Painter {
    val context = LocalContext.current
    val imageLoader = ImageLoader.Builder(context)
        .components {
            if (SDK_INT >= 28) {
                add(ImageDecoderDecoder.Factory())
            } else {
                add(GifDecoder.Factory())
            }
        }
        .build()

    return rememberAsyncImagePainter(
        ImageRequest.Builder(context).data(data = R.drawable.loading_img).apply(block = {
            size(Size.ORIGINAL)
        }).build(), imageLoader = imageLoader, contentScale = contentScale
    )
}

@Preview(showBackground = true)
@Composable
fun LoadingPreview() {
    LoadingScreen(Modifier.fillMaxSize())
}